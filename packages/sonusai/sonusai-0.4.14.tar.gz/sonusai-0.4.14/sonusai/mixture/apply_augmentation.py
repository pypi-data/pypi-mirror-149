import numpy as np


def apply_augmentation(audio_in: np.ndarray,
                       augmentation: dict,
                       length_common_denominator: int) -> np.ndarray:
    import sox

    from sonusai import SonusAIError
    from sonusai.mixture.constants import BIT_DEPTH
    from sonusai.mixture.constants import CHANNEL_COUNT
    from sonusai.mixture.constants import SAMPLE_RATE

    try:
        # Apply augmentations
        tfm = sox.Transformer()
        tfm.set_input_format(rate=SAMPLE_RATE, bits=BIT_DEPTH, channels=CHANNEL_COUNT)
        tfm.set_output_format(rate=SAMPLE_RATE, bits=BIT_DEPTH, channels=CHANNEL_COUNT)

        # TODO
        #  Always normalize and remove normalize from list of available augmentations
        #  Normalize to globally set level (should this be a global config parameter,
        #  or hard-coded into the script?)
        if 'normalize' in augmentation:
            tfm.norm(db_level=augmentation['normalize'])

        if 'gain' in augmentation:
            tfm.gain(gain_db=augmentation['gain'], normalize=False, limiter=True)

        if 'pitch' in augmentation:
            tfm.pitch(n_semitones=augmentation['pitch'] / 100)

        if 'tempo' in augmentation:
            factor = augmentation['tempo']
            if abs(factor - 1.0) <= 0.1:
                tfm.stretch(factor=factor)
            else:
                tfm.tempo(factor=factor, audio_type='s')

        if 'eq1' in augmentation:
            tfm.equalizer(frequency=augmentation['eq1'][0], width_q=augmentation['eq1'][1],
                          gain_db=augmentation['eq1'][2])

        if 'eq2' in augmentation:
            tfm.equalizer(frequency=augmentation['eq2'][0], width_q=augmentation['eq2'][1],
                          gain_db=augmentation['eq2'][2])

        if 'eq3' in augmentation:
            tfm.equalizer(frequency=augmentation['eq3'][0], width_q=augmentation['eq3'][1],
                          gain_db=augmentation['eq3'][2])

        if 'lpf' in augmentation:
            tfm.lowpass(frequency=augmentation['lpf'])

        # Create output data
        audio_out = tfm.build_array(input_array=audio_in, sample_rate_in=SAMPLE_RATE)

        # make sure length is multiple of length_common_denominator
        audio_len = len(audio_out)
        if audio_len % length_common_denominator:
            pad = length_common_denominator - (audio_len % length_common_denominator)
            audio_out = np.pad(audio_out, pad_width=(0, pad), mode='constant', constant_values=0)

        return audio_out
    except Exception as e:
        raise SonusAIError(f'Error applying {augmentation}: {e}')
