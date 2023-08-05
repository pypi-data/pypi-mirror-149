"""sonusai genmixdb

usage: genmixdb [-hv] CONFIG...

options:
   -h, --help
   -v, --verbose    Be verbose.

Create mixture database data for training and evaluation.

genmixdb creates a database of training and evaluation feature and truth data generation information. It allows
the choice of audio neural-network feature types that are supported by the Aaware real-time front-end and truth
data that is synchronized frame-by-frame with the feature data.

Here are some examples:

#### Adding target data
Suppose you have an audio file which is an example, or target, of what you want to
recognize or detect. Of course, for training a NN you also need truth data for that
file (also called labels). If you don't already have it, genmixdb can create truth using
energy-based sound detection on each frame of the feature data. You can also select
different feature types. Here's an example:

genmixdb target_gfr32ts2.yml

where target_gfr32ts2.yml contains:
---
targets:
  - data/target.wav

feature: gfr32ts2

target_augmentations:
  -
    normalize: -3.5
...

The mixture database is written to a JSON file that inherits the base name of the config file.

#### Target data mix with noise and augmentation

genmixdb mix_gfr32ts2.yml

where mix_gfr32ts2.yml contains:
---
targets:
  - data/target.wav

noises:
  - data/noise.wav

target_count: 5

feature: gfr32ts2

output: data/my_mix.h5

target_augmentations:
  -
    normalize: -3.5
    pitch: [-3, 0, 3]
    tempo: [0.8, 1, 1.2]
    snr: 20

noise_augmentations:
  -
    normalize: -3.5
...

In this example a time-domain mixture is created and feature data is calculated as
specified by 'feature: gfr32ts2'. Various feature types are available which vary in
spectral and temporal resolution (4 ms or higher), and other feature algorithm
parameters. The total feature size, dimension, and #frames for mixture is reported
in the log file (the log file name is derived from the output file base name; in this
case it would be mix_gfr32ts2.log).

Truth (labels) can be automatically created per feature output frame based on sound
energy detection. By default, these are appended to the feature data in a single HDF5
output file. By default, truth/label generation is turned on with default algorithm
and threshold levels (see truth section) and a single class, i.e., detecting a single
type of sound. The truth format is a single float per class representing the
probability of activity/presence, and multi-class truth/labels are possible by
specifying the number of classes and either a scalar index or a vector of indices in
which to put the truth result. For example, 'num_class: 3' and  'truth_index: 2' adds
a 1x3 vector to the feature data with truth put in index 2 (others would be 0) for
data/target.wav being an audio clip from sound type of class 2.

The mixture is created with potential data augmentation functions in the following way:
1. apply noise augmentation rule
2. apply target augmentation rule
3. adjust noise gain for specific SNR
4. add augmented noise to augmented target

The mixture length is the target length by default, and the noise signal is repeated
if it is shorter, or trimmed if longer. If 'target_count: <count>' is specified, then
the target audio is concatenated <count> times for each augmentation rule.
(See the Augmentation section for details on augmentation rules.)

#### Target and noise using path lists

Target and noise audio is specified as a list containing text files, audio files, and
file globs. Text files are processed with items on each line where each item can be a
text file, an audio file, or a file glob. Each item will be searched for audio files
which can be WAV, MP3, FLAC, AIFF, or OGG format with any sample rate, bit depth, or
channel count. All audio files will be converted to 16 kHz, 16-bit, single channel
format before processing. For example,

genmixdb dog-bark.yml

where dog-bark.yml contains:
---
targets:
  - slib/dog-outside/*.wav
  - slib/dog-inside/*.wav

will find all .wav files in the specified directories and process them as targets.

"""
import json
import re
import time
from copy import deepcopy
from glob import glob
from numbers import Number
from os import listdir
from os.path import dirname
from os.path import isabs
from os.path import isdir
from os.path import join
from os.path import splitext
from random import seed
from random import uniform

import numpy as np
import sox
import yaml
from docopt import docopt
from pyaaware import FeatureGenerator
from tqdm import tqdm

import sonusai
from sonusai import SonusAIError
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.mixture import apply_augmentation
from sonusai.mixture import estimate_audio_length
from sonusai.mixture import generate_truth
from sonusai.mixture import get_class_weights_threshold
from sonusai.mixture import get_config_from_file
from sonusai.mixture import get_next_noise
from sonusai.mixture import get_total_class_count
from sonusai.mixture import load_config
from sonusai.mixture import read_audio
from sonusai.mixture import update_truth_settings
from sonusai.utils import expandvars
from sonusai.utils import human_readable_size
from sonusai.utils import p_map
from sonusai.utils import seconds_to_hms
from sonusai.utils import trim_docstring

genmixdb_global = dict()


def genmixdb(file: str = None,
             config: dict = None,
             logging: bool = True,
             show_progress: bool = False) -> dict:
    if (file is None and config is None) or (file is not None and config is not None):
        raise SonusAIError(f'Must specify either file name or config.')

    if file is not None:
        config = get_config_from_file(file)

    seed(config['seed'])

    if logging:
        logger.debug(f'Seed: {config["seed"]}')
        logger.debug('Configuration:')
        logger.debug(yaml.dump(config))

    if logging:
        logger.info('Collecting targets')
    targets = get_input_files(records=config['targets'], truth_settings=config['truth_settings'])
    if len(targets) == 0:
        raise SonusAIError('Canceled due to no targets')

    if logging:
        logger.debug('List of targets:')
        logger.debug(yaml.dump([sub['name'] for sub in targets], default_flow_style=False))

    if logging:
        logger.info('Collecting noises')
    noises = get_input_files(records=config['noises'])
    if len(noises) == 0:
        if logging:
            logger.warning(f'Did not find any noises; using default noise: {sonusai.mixture.DEFAULT_NOISE}')
        noises = get_input_files(records=[sonusai.mixture.DEFAULT_NOISE])
    if logging:
        logger.debug('List of noises:')
        logger.debug(yaml.dump([sub['name'] for sub in noises], default_flow_style=False))

    if logging:
        logger.info('Collecting target augmentations')
    target_augmentations = get_augmentations(rules=config['target_augmentations'], target=True)
    expanded_target_augmentations = ''
    for augmentation in target_augmentations:
        expanded_target_augmentations += f'- {augmentation}\n'
    if logging:
        logger.debug('Expanded list of target augmentations:')
        logger.debug(expanded_target_augmentations)

    if logging:
        logger.info('Collecting noise augmentations')
    noise_augmentations = get_augmentations(config['noise_augmentations'], target=False)
    expanded_noise_augmentations = ''
    for augmentation in noise_augmentations:
        expanded_noise_augmentations += f'- {augmentation}\n'
    if logging:
        logger.debug('Expanded list of noise augmentations:')
        logger.debug(expanded_noise_augmentations)

    noise_sets = len(noises) * len(noise_augmentations)
    target_sets = len(targets) * len(target_augmentations)
    total_mixtures = noise_sets * target_sets
    if logging:
        logger.info('')
        logger.info(f'Found {total_mixtures} mixtures to process')

    class_weights_threshold = get_class_weights_threshold(config)

    if config['truth_mode'] not in ['normal', 'mutex']:
        raise SonusAIError(f'invalid truth_mode: {config["truth_mode"]}')

    truth_mutex = config['truth_mode'] == 'mutex'
    if truth_mutex:
        max_class = config['num_classes'] - 1
    else:
        max_class = config['num_classes']

    fg = FeatureGenerator(feature_mode=config['feature'],
                          frame_size=config['frame_size'],
                          num_classes=config['num_classes'],
                          truth_mutex=truth_mutex)

    num_bands = fg.num_bands
    stride = fg.stride
    step = fg.step
    decimation = fg.decimation

    transform_frame_ms = float(config['frame_size']) / float(sonusai.mixture.SAMPLE_RATE / 1000)
    feature_ms = transform_frame_ms * decimation * stride
    feature_step_ms = transform_frame_ms * decimation * step
    feature_samples = config['frame_size'] * decimation * stride
    feature_step_samples = config['frame_size'] * decimation * step

    total_duration = 0
    for duration in [sub['duration'] for sub in targets]:
        for augmentation in target_augmentations:
            length = int(duration * sonusai.mixture.SAMPLE_RATE)
            if 'tempo' in augmentation:
                length /= augmentation['tempo']
            if length % feature_step_samples:
                length += feature_step_samples - int(length % feature_step_samples)
            total_duration += float(length) / sonusai.mixture.SAMPLE_RATE
    total_duration *= noise_sets

    total_samples = total_duration * sonusai.mixture.SAMPLE_RATE

    mixture_bytes = total_samples * sonusai.mixture.BIT_DEPTH / 8
    truth_t_bytes = total_samples * config['num_classes'] * sonusai.mixture.FLOAT_BYTES
    feature_bytes = total_samples / feature_step_samples * stride * num_bands * sonusai.mixture.FLOAT_BYTES
    truth_f_bytes = total_samples / feature_step_samples * config['num_classes'] * sonusai.mixture.FLOAT_BYTES

    if logging:
        logger.info('')
        logger.info(f'Estimated duration:   {seconds_to_hms(seconds=total_duration)}')
        logger.info('Estimated sizes:')
        logger.info(f' mixture:             {human_readable_size(mixture_bytes, 1)}')
        logger.info(f' truth_t:             {human_readable_size(truth_t_bytes, 1)}')
        logger.info(f' feature:             {human_readable_size(feature_bytes, 1)}')
        logger.info(f' truth_f:             {human_readable_size(truth_f_bytes, 1)}')
        logger.info(f'Feature shape:        {stride} x {num_bands} ({stride * num_bands} total params)')
        logger.info(f'Feature samples:      {feature_samples} samples ({feature_ms} ms)')
        logger.info(f'Feature step samples: {feature_step_samples} samples ({feature_step_ms} ms)')

    mixdb = {
        'class_count':              list(),
        'class_labels':             config['class_labels'],
        'class_weights_threshold':  list(class_weights_threshold),
        'feature':                  config['feature'],
        'feature_samples':          feature_samples,
        'feature_step_samples':     feature_step_samples,
        'frame_size':               config['frame_size'],
        'mixtures':                 list(),
        'noise_augmentations':      noise_augmentations,
        'noises':                   noises,
        'num_classes':              config['num_classes'],
        'target_augmentations':     target_augmentations,
        'targets':                  targets,
        'truth_mutex':              truth_mutex,
        'truth_reduction_function': config['truth_reduction_function'],
    }

    # Read in all audio data beforehand to avoid reading it multiple times in the loop
    if logging:
        logger.debug('Reading noise audio')
    raw_noise_audio = list()
    for noise in noises:
        raw_noise_audio.append(read_audio(name=noise['name']))

    if logging:
        logger.debug('Reading target audio')
    raw_target_audio = list()
    for target in targets:
        raw_target_audio.append(read_audio(name=target['name']))

    # First pass to get indices and offsets
    mixtures = [[] for _ in range(noise_sets)]
    n_id = 0
    for noise_index, noise in enumerate(noises):
        for noise_augmentation_index, noise_augmentation in enumerate(noise_augmentations):
            mixtures[n_id] = [[] for _ in range(target_sets)]
            t_id = 0
            noise_offset = 0
            noise_length = estimate_audio_length(audio_in=raw_noise_audio[noise_index],
                                                 augmentation=noise_augmentation,
                                                 length_common_denominator=1)
            for target_index, target in enumerate(targets):
                for target_augmentation_index, target_augmentation in enumerate(target_augmentations):
                    if not isinstance(target['truth_settings'], list):
                        target['truth_settings'] = [target['truth_settings']]

                    update_truth_settings(target['truth_settings'], config['truth_settings'])

                    for truth_setting in target['truth_settings']:
                        if not isinstance(truth_setting['index'], list):
                            truth_setting['index'] = [truth_setting['index']]

                        if any(idx > max_class for idx in truth_setting['index']):
                            raise SonusAIError('invalid truth index')

                    mixtures[n_id][t_id] = {'target_file_index':         target_index,
                                            'noise_file_index':          noise_index,
                                            'noise_offset':              noise_offset,
                                            'target_augmentation_index': target_augmentation_index,
                                            'noise_augmentation_index':  noise_augmentation_index}
                    t_id += 1

                    target_length = estimate_audio_length(audio_in=raw_target_audio[target_index],
                                                          augmentation=target_augmentation,
                                                          length_common_denominator=feature_step_samples)
                    noise_offset = int((noise_offset + target_length) % noise_length)

            n_id += 1

    genmixdb_global['mixdb'] = mixdb
    genmixdb_global['config'] = config
    genmixdb_global['target_augmentations'] = target_augmentations
    genmixdb_global['raw_target_audio'] = raw_target_audio
    genmixdb_global['feature_step_samples'] = feature_step_samples

    progress = tqdm(total=total_mixtures, desc='genmixdb', disable=not show_progress)

    # Second pass to fill in the details
    for n_id in range(len(mixtures)):
        genmixdb_global['augmented_noise_audio'] = apply_augmentation(
            audio_in=raw_noise_audio[mixtures[n_id][0]['noise_file_index']],
            augmentation=noise_augmentations[mixtures[n_id][0]['noise_augmentation_index']],
            length_common_denominator=1)
        mixtures[n_id] = p_map(_process_mixture, mixtures[n_id], progress=progress)

    progress.close()

    # Flatten mixtures
    mixdb['mixtures'] = [item for sublist in mixtures for item in sublist]
    mixdb['class_count'] = get_total_class_count(mixdb)

    total_samples = sum([sub['samples'] for sub in mixdb['mixtures']])
    total_duration = total_samples / sonusai.mixture.SAMPLE_RATE
    mixture_bytes = total_samples * sonusai.mixture.BIT_DEPTH / 8
    truth_t_bytes = total_samples * config['num_classes'] * 4
    feature_bytes = total_samples / feature_step_samples * stride * num_bands * 4
    truth_f_bytes = total_samples / feature_step_samples * config['num_classes'] * 4
    if logging:
        logger.info('')
        logger.info(f'Actual duration: {seconds_to_hms(seconds=total_duration)}')
        logger.info('Actual sizes:')
        logger.info(f' mixture:        {human_readable_size(mixture_bytes, 1)}')
        logger.info(f' truth_t:        {human_readable_size(truth_t_bytes, 1)}')
        logger.info(f' feature:        {human_readable_size(feature_bytes, 1)}')
        logger.info(f' truth_f:        {human_readable_size(truth_f_bytes, 1)}')

    return mixdb


def get_input_files(records, truth_settings=None):
    if truth_settings is None:
        truth_settings = list()

    files = list()
    for record in records:
        append_input_files(files, record, truth_settings)
    return files


def append_input_files(files: list, in_record, truth_settings: list, tokens=None):
    if tokens is None:
        tokens = dict()
    in_name = in_record

    if isinstance(in_record, dict):
        if 'target_name' in in_record:
            in_name = in_record['target_name']
        else:
            raise SonusAIError('Target list contained record without target_name')

        if 'truth_settings' in in_record:
            truth_settings = in_record['truth_settings']

    in_name, new_tokens = expandvars(in_name)
    tokens.update(new_tokens)
    names = glob(in_name)
    if not names:
        raise SonusAIError(f'Could not find {in_name}. Make sure path exists')
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                append_input_files(files, child, truth_settings, tokens)
        else:
            try:
                if ext == '.txt':
                    with open(file=name, mode='r') as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition('#')[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = expandvars(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                append_input_files(files, child, truth_settings, tokens)
                elif ext == '.yml':
                    try:
                        yml_config = load_config(name)

                        if 'targets' in yml_config:
                            for record in yml_config['targets']:
                                append_input_files(files, record, truth_settings, tokens)
                    except Exception as e:
                        raise SonusAIError(f'Error processing {name}: {e}')
                else:
                    sox.file_info.validate_input_file(name)
                    duration = sox.file_info.duration(name)
                    for key, value in tokens.items():
                        name = name.replace(value, f'${key}')
                    entry = {
                        'name':     name,
                        'duration': duration,
                    }
                    if len(truth_settings) > 0:
                        entry['truth_settings'] = truth_settings
                        for truth_setting in entry['truth_settings']:
                            if 'function' in truth_setting and truth_setting['function'] == 'file':
                                truth_setting['config']['file'] = splitext(name)[0] + '.h5'
                    files.append(entry)
            except SonusAIError:
                raise
            except Exception as e:
                raise SonusAIError(f'Error processing {name}: {e}')


def get_augmentations(rules: list, target: bool) -> list:
    augmentations = list()
    for rule in rules:
        expand_augmentations(augmentations, rule, target)

    augmentations = rand_augmentations(augmentations)
    return augmentations


def expand_augmentations(augmentations: list, rule: dict, target: bool):
    # replace old 'eq' rule with new 'eq1' rule to allow both for backward compatibility
    rule = {'eq1' if key == 'eq' else key: value for key, value in rule.items()}

    for key in rule:
        if key not in sonusai.mixture.VALID_AUGMENTATIONS:
            raise SonusAIError(f'Invalid augmentation: {key}')

        if key in ['eq1', 'eq2', 'eq3']:
            # eq must be a list of length 3 or a list of length 3 lists
            valid = True
            multiple = False
            if isinstance(rule[key], list):
                if any(isinstance(el, list) for el in rule[key]):
                    multiple = True
                    for value in rule[key]:
                        if not isinstance(value, list) or len(value) != 3:
                            valid = False
                else:
                    if len(rule[key]) != 3:
                        valid = False
            else:
                valid = False

            if not valid:
                raise SonusAIError(f'Invalid augmentation value for {key}: {rule[key]}')

            if multiple:
                for value in rule[key]:
                    expanded_rule = deepcopy(rule)
                    expanded_rule[key] = deepcopy(value)
                    expand_augmentations(augmentations, expanded_rule, target)
                return

        elif key == 'count':
            pass

        else:
            if isinstance(rule[key], list):
                for value in rule[key]:
                    if isinstance(value, list):
                        raise SonusAIError(f'Invalid augmentation value for {key}: {rule[key]}')
                    expanded_rule = deepcopy(rule)
                    expanded_rule[key] = deepcopy(value)
                    expand_augmentations(augmentations, expanded_rule, target)
                return
            elif not isinstance(rule[key], Number):
                if not rule[key].startswith('rand'):
                    raise SonusAIError(f'Invalid augmentation value for {key}: {rule[key]}')

    # Set default snr for target if needed
    if target and 'snr' not in rule:
        rule['snr'] = sonusai.mixture.DEFAULT_SNR

    # Remove snr rule from noise if needed
    if not target and 'snr' in rule:
        del rule['snr']

    augmentations.append(rule)


def rand_repl(m):
    return f'{uniform(float(m.group(1)), float(m.group(4))):.2f}'


def rand_augmentations(in_rules):
    out_rules = list()
    for rule in in_rules:
        # do any keys contain rand?
        has_rand = False
        for key in rule:
            if 'rand' in str(rule[key]):
                has_rand = True
                break

        if has_rand:
            count = 1
            if rule['count'] is not None:
                count = rule['count']
                del rule['count']
            for i in range(count):
                new_rule = deepcopy(rule)
                for key in new_rule:
                    new_rule[key] = eval(re.sub(sonusai.mixture.RAND_PATTERN, rand_repl, str(new_rule[key])))

                    # convert eq values from strings to numbers
                    if key in ['eq1', 'eq2', 'eq3']:
                        for n in range(3):
                            if isinstance(new_rule[key][n], str):
                                new_rule[key][n] = eval(new_rule[key][n])
                out_rules.append(new_rule)
        else:
            out_rules.append(rule)
    return out_rules


def get_output_from_config(config: dict, config_name: str) -> str:
    try:
        config_base = splitext(config_name)[0]
        name = str(splitext(config['output'])[0])
        name = name.replace('${config}', config_base)
        return name
    except Exception as e:
        raise SonusAIError(f'Error getting genmixdb base name: {e}')


def _process_mixture(mixture: dict) -> dict:
    target_index = mixture['target_file_index']
    noise_offset = mixture['noise_offset']
    target_augmentation_index = mixture['target_augmentation_index']

    target_augmentation = genmixdb_global['target_augmentations'][target_augmentation_index]

    augmented_target_audio = apply_augmentation(audio_in=genmixdb_global['raw_target_audio'][target_index],
                                                augmentation=target_augmentation,
                                                length_common_denominator=genmixdb_global['feature_step_samples'])

    noise_segment, _ = get_next_noise(offset_in=noise_offset,
                                      length=len(augmented_target_audio),
                                      audio_in=genmixdb_global['augmented_noise_audio'])

    # target_gain is the sum of 'gain', noise overflow adjustment, and mixture
    # overflow adjustment. It is used to return the target audio to its normalized
    # level when calculating truth (unless target gain is set to zero, in which
    # case the truth will be all zeros).
    if 'gain' in target_augmentation:
        target_gain = 10 ** (target_augmentation['gain'] / 20)
    else:
        target_gain = 1

    if 'snr' in target_augmentation:
        if target_augmentation['snr'] < -96:
            # Special case for zeroing out target data
            mixture['target_snr_gain'] = 0
            mixture['noise_snr_gain'] = 1
            target_gain = 0
        else:
            target_energy = np.mean(np.square(np.single(augmented_target_audio)))
            noise_energy = np.mean(np.square(np.single(noise_segment)))
            noise_gain = np.sqrt(target_energy / noise_energy) / 10 ** (
                    target_augmentation['snr'] / 20)

            # Check for noise_gain > 1 to avoid clipping
            if noise_gain > 1:
                mixture['target_snr_gain'] = 1 / noise_gain
                mixture['noise_snr_gain'] = 1
                target_gain = target_gain / noise_gain
            else:
                mixture['target_snr_gain'] = 1
                mixture['noise_snr_gain'] = noise_gain

    # Check for clipping in mixture
    gain_adjusted_target_audio = np.single(augmented_target_audio) * mixture['target_snr_gain']
    gain_adjusted_noise_audio = np.single(noise_segment) * mixture['noise_snr_gain']
    mixture_audio = gain_adjusted_target_audio + gain_adjusted_noise_audio

    if any(abs(mixture_audio) >= 32768):
        # Clipping occurred; lower gains to bring audio within int16 bounds
        gain_adjustment = 32760 / max(abs(mixture_audio))
        mixture['target_snr_gain'] *= gain_adjustment
        mixture['noise_snr_gain'] *= gain_adjustment
        target_gain *= gain_adjustment

    mixture['samples'] = len(augmented_target_audio)
    mixture['target_gain'] = target_gain

    gain_adjusted_target_audio = np.int16(np.single(augmented_target_audio) * mixture['target_snr_gain'])
    gain_adjusted_noise_audio = np.int16(np.single(noise_segment) * mixture['noise_snr_gain'])
    generate_truth(mixdb=genmixdb_global['mixdb'],
                   record=mixture,
                   target=gain_adjusted_target_audio,
                   noise=gain_adjusted_noise_audio)

    return mixture


def main():
    try:
        args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

        verbose = args['--verbose']

        for config_file in args['CONFIG']:
            start_time = time.monotonic()
            logger.info(f'Creating mixture database for {config_file}')
            config = get_config_from_file(config_file)
            output = get_output_from_config(config, config_file)

            log_name = output + '.log'
            create_file_handler(log_name)
            update_console_handler(verbose)
            initial_log_messages('genmixdb')

            mixdb = genmixdb(config=config, show_progress=True)

            json_name = output + '.json'
            with open(file=json_name, mode='w') as file:
                json.dump(mixdb, file, indent=2)
                logger.info(f'Wrote mixture database for {config_file} to {json_name}')

            end_time = time.monotonic()
            logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')

    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)


if __name__ == '__main__':
    main()
