import numpy as np


def truth_reduction(x: np.ndarray, func: str) -> np.ndarray:
    from sonusai import SonusAIError

    if func == 'max':
        return np.max(x, axis=0)

    if func == 'mean':
        return np.mean(x, axis=0)

    raise SonusAIError(f'Invalid truth reduction function: {func}')
