"""
Tests that normal einsum force calculation and numba implementation yields the
same forces
"""

import itertools
import numpy as np

from hiphive.calculators.numba_calc import (cluster_force_contribution_einsum,
                                            cluster_force_contribution_numba)


def test_numba_einsum():
    N = 5
    f = np.zeros(3)
    F_einsum = np.zeros((N, 3))
    F_numba = np.zeros(F_einsum.shape)
    for cluster in itertools.combinations_with_replacement(range(N), r=N):
        f *= 0
        cluster = np.array(cluster)
        positions = np.unique(cluster, return_index=True)[1]
        numbers = len(positions)
        prefactors = np.random.random(numbers)
        fc = np.random.random((3,) * N).flatten()
        fc_tmp = fc.copy()
        disps = np.random.random((N, 3))
        f *= 0
        cluster_force_contribution_einsum(positions, prefactors, numbers,
                                          fc_tmp, fc, N,
                                          disps, cluster, f, F_einsum)
        f *= 0
        fc_tmp = fc.copy()
        cluster_force_contribution_numba(positions, prefactors, numbers,
                                         fc_tmp, fc, N,
                                         disps, cluster, f, F_numba)

    assert np.allclose(F_einsum, F_numba)
