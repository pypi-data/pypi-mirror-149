"""
Test for sum rules being correctly enforced
"""

import numpy as np

from ase.build import bulk
from hiphive import ClusterSpace, ForceConstantPotential


def test_translational_sum_rules():

    cutoffs1 = [4.1, 4.1]
    cutoffs2 = [4.1, 5.3]
    tol = 1e-8

    # setup structures
    structures = {}
    structures['fcc'] = bulk('Al', 'fcc', a=4.05).repeat(4)
    structures['hcp'] = bulk('Ti', 'hcp').repeat(4)
    structures['diamond'] = bulk('Si', 'diamond', a=5.4, cubic=True).repeat(2)
    structures['rocksalt'] = bulk('NaCl', 'rocksalt', a=5.6, cubic=True).repeat(2)

    for structure, atoms in structures.items():

        for cutoffs in [cutoffs1, cutoffs2]:

            # setup FCP hiPhive
            cs = ClusterSpace(atoms, cutoffs, acoustic_sum_rules=True)
            irr_params = np.random.random((cs.n_dofs))
            fcp = ForceConstantPotential(cs, irr_params)
            fcs = fcp.get_force_constants(atoms)
            fc2 = fcs.get_fc_array(order=2)
            fc3 = fcs.get_fc_array(order=3)

            # Second order translational sum rule
            # sum_j Phi_ij = 0 , all i
            for i in range(len(atoms)):
                phi_sum = np.zeros((3, 3))
                for j in range(len(atoms)):
                    phi_sum += fc2[(i, j)]
                assert np.linalg.norm(phi_sum) < tol, \
                    '{}: Second order sum rule Phi_({},j), {}, {}'.format(
                        structure, i, phi_sum, np.linalg.norm(phi_sum))

            # Third order translational sum rule
            # sum_k Phi_ijk = 0 , all i,j
            for i in range(len(atoms)):
                for j in range(len(atoms)):
                    phi_sum = np.zeros((3, 3, 3))
                    for k in range(len(atoms)):
                        phi_sum += fc3[(i, j, k)]
                    assert np.linalg.norm(phi_sum) < tol, \
                        '{}: Third order sum rule Phi_({},{},k), {}, {}'.format(
                            structure, i, j, phi_sum, np.linalg.norm(phi_sum))
