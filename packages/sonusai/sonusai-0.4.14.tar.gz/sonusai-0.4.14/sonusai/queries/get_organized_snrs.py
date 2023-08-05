from typing import Any
from typing import Callable
from typing import List
from typing import Union

import numpy as np


def _process_snrs(mixdb: dict) -> (int, np.ndarray, np.ndarray):
    snrs_dict = dict()
    for index, augmentation in enumerate(mixdb['target_augmentations']):
        snr = augmentation['snr']
        if snr not in snrs_dict:
            snrs_dict[snr] = list()
        snrs_dict[snr].append(index)
    snrs_list = np.array(list(snrs_dict))
    count = np.zeros(len(snrs_dict), 'int32')
    for sni in range(len(snrs_dict)):
        snr = snrs_list[sni]
        count[sni] = len(snrs_dict[snr])
    ssidx = np.argsort(-count)
    ss = count[ssidx]
    snr_maxcnt = ss[0]
    ord_len = 1
    ii = 1
    while ii < len(snrs_dict) and ss[ii] == snr_maxcnt:
        ord_len += 1
        ii += 1
    return ord_len, snrs_list, ssidx


def get_random_snrs(mixdb: dict, predicate: Callable[[Any], bool] = None) -> list:
    ord_len, snrs_list, ssidx = _process_snrs(mixdb)

    if predicate is None:
        def predicate(x: Any) -> bool:
            return True

    snrs = sorted(list(snrs_list[ssidx[ord_len:]]), reverse=True)

    # Filter on predicate
    snrs = [snr for snr in snrs if predicate(snr)]

    return snrs


def get_ordered_snrs(mixdb: dict, predicate: Callable[[Any], bool] = None) -> list:
    ord_len, snrs_list, ssidx = _process_snrs(mixdb)

    if predicate is None:
        def predicate(x: Any) -> bool:
            return True

    snrs = sorted(list(snrs_list[ssidx[0:ord_len]]), reverse=True)

    # Filter on predicate
    snrs = [snr for snr in snrs if predicate(snr)]

    return snrs


def get_mixids_from_ordered_snr(mixdb: dict,
                                mixid: Union[str, List[int]] = None,
                                predicate: Callable[[Any], bool] = None) -> dict:
    """
    Generate mixids based on an SNR predicate for ordered SNRs
    Return a dictionary where:
        - keys are the SNRs
        - values are lists of the mixids that match the SNR
    """
    from sonusai.queries.queries import get_mixids_from_snr

    snrs = get_ordered_snrs(mixdb)

    if predicate is None:
        def _predicate(x: Any) -> bool:
            return x in snrs
    else:
        def _predicate(x: Any) -> bool:
            return predicate(x) and x in snrs

    return get_mixids_from_snr(mixdb=mixdb, mixid=mixid, predicate=_predicate)


def get_mixids_from_random_snr(mixdb: dict,
                               mixid: Union[str, List[int]] = None,
                               predicate: Callable[[Any], bool] = None) -> dict:
    """
    Generate mixids based on an SNR predicate for random SNRs
    Return a dictionary where:
        - keys are the SNRs
        - values are lists of the mixids that match the SNR
    """
    from sonusai.queries.queries import get_mixids_from_snr

    snrs = get_random_snrs(mixdb)

    if predicate is None:
        def _predicate(x: Any) -> bool:
            return x in snrs
    else:
        def _predicate(x: Any) -> bool:
            return predicate(x) and x in snrs

    return get_mixids_from_snr(mixdb=mixdb, mixid=mixid, predicate=_predicate)
