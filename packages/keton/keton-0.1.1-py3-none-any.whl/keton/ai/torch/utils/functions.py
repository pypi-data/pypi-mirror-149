from typing import Iterable, Tuple

import numpy as np

from torch.utils.data import Dataset, Subset


def fixed_split(dataset: Dataset, val_split, shuffle=True) -> Tuple[Subset, Subset]:
    assert(0 < val_split < 1)
    if shuffle:
        indices = np.random.permutation(len(dataset))
    else:
        indices = np.arange(len(dataset))
    split_idx = int(len(dataset) * val_split)
    return Subset(dataset, indices[split_idx:]), Subset(dataset, indices[:split_idx])


def k_fold_split(dataset: Dataset, k, shuffle=True) -> Iterable[Tuple[Subset, Subset]]:
    assert(k >= 2)
    if shuffle:
        indices = np.random.permutation(len(dataset))
    else:
        indices = np.arange(len(dataset))
    fold_size = (len(dataset) + k - 1) // k
    for i in range(k):
        val_indices = indices[i * fold_size: (i + 1) * fold_size]
        train_indices = np.concatenate(
            (indices[:i * fold_size], indices[(i + 1) * fold_size:]))
        yield Subset(dataset, train_indices), Subset(dataset, val_indices)
