"""
Test of ForceConstants and the various ways of accessing FCs
"""

import numpy as np
from ase.build import bulk
from numpy.linalg import norm
from hiphive import ForceConstants
from hiphive.force_constants import array_to_dense_dict


def test_force_constants_basic():
    TOL = 1e-8

    supercell = bulk('Al').repeat((2, 2, 1))
    fc2 = np.random.random((3, 3))
    fc3 = np.random.random((3, 3, 3))
    fc4 = np.random.random((3, 3, 3, 3))

    fc_dict = dict()
    fc_dict[(0, 1)] = fc2
    fc_dict[(0, 1, 2)] = fc3
    fc_dict[(0, 1, 2, 3)] = fc4

    fcs = ForceConstants.from_sparse_dict(fc_dict, supercell)

    # check get_item
    assert norm(fcs[(0, 1)] - fc2) < TOL
    assert norm(fcs[(0, 1, 2)] - fc3) < TOL
    assert norm(fcs[(0, 1, 2, 3)] - fc4) < TOL

    assert norm(fcs[(1, 0)] - fc2.transpose([1, 0])) < TOL
    assert norm(fcs[(2, 1, 0)] - fc3.transpose([2, 1, 0])) < TOL
    assert norm(fcs[(3, 2, 1, 0)] - fc4.transpose([3, 2, 1, 0])) < TOL

    # get fc_dict
    fc_dict_new = fcs.get_fc_dict()

    for cluster, fc in fc_dict.items():
        assert norm(fc_dict_new[cluster] - fc) < TOL

    # get fc_array
    fc_array2 = fcs.get_fc_array(order=2)
    fc_array3 = fcs.get_fc_array(order=3)
    fc_array4 = fcs.get_fc_array(order=4)

    assert norm(fc_array2[(0, 1)] - fc_dict[(0, 1)]) < TOL
    assert norm(fc_array3[(0, 1, 2)] - fc_dict[(0, 1, 2)]) < TOL
    assert norm(fc_array4[(0, 1, 2, 3)] - fc_dict[(0, 1, 2, 3)]) < TOL

    # Attempt to initialize ForceConstants from numpy array from phonopy
    N = 54
    supercell = bulk('Al').repeat((N, 1, 1))

    # setup fc2 which is symmetric in atomic indicies
    fc2_phonopy_dummy = np.zeros((N, N, 3, 3))
    for i in range(N):
        for j in range(i, N):
            M = np.random.random((3, 3))
            fc2_phonopy_dummy[(i, j)] = M
            fc2_phonopy_dummy[(j, i)] = M.T

    fc_dict = array_to_dense_dict(fc2_phonopy_dummy)
    fcs = ForceConstants.from_dense_dict(fc_dict, supercell)
    assert np.linalg.norm(fcs.get_fc_array(order=2) - fc2_phonopy_dummy) < TOL
