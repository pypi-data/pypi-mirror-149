from typing import Union

import numpy as np


def read_predict_data(filename: str, expected_frames: int) -> Union[None, np.ndarray]:
    """Read predict data from given HDF5 file and return it."""
    import h5py

    from sonusai import logger

    if not filename:
        return None

    logger.info(f'Reading prediction data from {filename}')
    with h5py.File(name=filename, mode='r') as f:
        # prediction data is either [frames, num_classes], or [frames, timesteps, num_classes]
        predict = np.array(f['predict'])

        if predict.ndim == 2:
            frames, num_classes = predict.shape

            if frames != expected_frames:
                logger.warning(f'Ignoring prediction data in {filename} due to frames mismatch')
                return None
        elif predict.ndim == 3:
            frames, timesteps, num_classes = predict.shape

            if frames * timesteps != expected_frames:
                logger.warning(f'Ignoring prediction data in {filename} due to frames mismatch')
                return None

            logger.info(
                f'Reshaping prediction data in {filename} from [{frames}, {timesteps}, {num_classes}] to [{frames * timesteps}, {num_classes}]')
            predict = np.reshape(predict, [frames * timesteps, num_classes], order='F')
        else:
            logger.warning(f'Ignoring prediction data in {filename} due to invalid dimensions')
            return None

        return predict
