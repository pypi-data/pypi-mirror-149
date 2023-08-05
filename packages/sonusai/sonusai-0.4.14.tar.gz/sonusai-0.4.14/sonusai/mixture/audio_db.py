import numpy as np


def build_noise_audio_db(mixdb: dict, show_progress: bool = False) -> list:
    from tqdm import tqdm

    from sonusai.mixture.apply_augmentation import apply_augmentation
    from sonusai.mixture.read_audio import read_audio

    db = list()
    for file_index in tqdm(sorted(list(set([sub['noise_file_index'] for sub in mixdb['mixtures']]))),
                           desc='Read noise audio', disable=not show_progress):
        audio_in = read_audio(name=mixdb['noises'][file_index]['name'])
        for augmentation_index in sorted(list(set([sub['noise_augmentation_index'] for sub in mixdb['mixtures']]))):
            db.append({
                'file':         file_index,
                'augmentation': augmentation_index,
                'audio':        apply_augmentation(audio_in=audio_in,
                                                   augmentation=mixdb['noise_augmentations'][augmentation_index],
                                                   length_common_denominator=1)
            })
    return db


def get_noise_audio_from_db(db: list, file_index: int, augmentation_index: int) -> np.ndarray:
    from sonusai import SonusAIError

    for record in db:
        if record['file'] == file_index and record['augmentation'] == augmentation_index:
            return record['audio']

    raise SonusAIError(f'Could not find file_index {file_index} and augmentation_index '
                       f'{augmentation_index} in noise database')


_audio_db_global = dict()


def build_target_audio_db(mixdb: dict, show_progress: bool = False) -> list:
    from tqdm import tqdm

    from sonusai.utils import p_map

    _audio_db_global['mixdb'] = mixdb
    indices = sorted(list(set([sub['target_file_index'] for sub in mixdb['mixtures']])))
    progress = tqdm(total=len(indices), desc='Read target audio', disable=not show_progress)
    db = p_map(_read_target_audio, indices, progress=progress)
    return db


def _read_target_audio(file_index: int) -> dict:
    from sonusai.mixture.read_audio import read_audio

    return {
        'file':  file_index,
        'audio': read_audio(name=_audio_db_global['mixdb']['targets'][file_index]['name'])
    }


def get_target_audio_from_db(db: list, file_index: int) -> np.ndarray:
    from sonusai import SonusAIError

    for record in db:
        if record['file'] == file_index:
            return record['audio']

    raise SonusAIError(f'Could not find file_index {file_index} in target database')


def check_audio_files_exist(mixdb: dict) -> None:
    from os.path import exists
    from os.path import expandvars

    from sonusai import SonusAIError

    for file_index in sorted(list(set(sub['noise_file_index'] for sub in mixdb['mixtures']))):
        file_name = expandvars(mixdb['noises'][file_index]['name'])
        if not exists(file_name):
            raise SonusAIError(f'Could not find {file_name}')

    for file_index in sorted(list(set(sub['target_file_index'] for sub in mixdb['mixtures']))):
        file_name = expandvars(mixdb['targets'][file_index]['name'])
        if not exists(file_name):
            raise SonusAIError(f'Could not find {file_name}')
