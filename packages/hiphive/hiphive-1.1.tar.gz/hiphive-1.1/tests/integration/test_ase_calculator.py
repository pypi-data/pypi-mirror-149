"""
Tests force and energy calculation of simple system
"""

import numpy as np

from ase import Atoms
from hiphive import ForceConstants
from hiphive.calculators import ForceConstantCalculator


def test_ase_calculator():
    tol = 1e-8

    # setup
    atoms = Atoms(symbols=['Ta']*2, positions=[[10, 10, 9], [10, 10, 11]],
                  cell=20*np.eye(3), pbc=True)

    np.random.seed(42)
    disps = np.random.uniform(0.0, 0.2, (2, 3))

    fc2_00 = np.random.uniform(0.0, 5.0, (3, 3))
    fc2_01 = np.random.uniform(0.0, 5.0, (3, 3))
    fc2_11 = np.random.uniform(0.0, 5.0, (3, 3))
    fc_dict = {(0, 0): fc2_00, (0, 1): fc2_01, (1, 1): fc2_11}
    fcs = ForceConstants.from_sparse_dict(fc_dict, supercell=atoms)

    # manual calc
    f0 = - (np.dot(fc2_00, disps[0]) + np.dot(fc2_01, disps[1]))
    f1 = - (np.dot(fc2_11, disps[1]) + np.dot(fc2_01.T, disps[0]))

    forces_ref = np.vstack((f0, f1))
    E_ref = - 0.5 * (np.dot(f0, disps[0]) + np.dot(f1, disps[1]))

    # ForceConstantCalculator
    calc = ForceConstantCalculator(fcs)
    atoms.positions += disps
    atoms.calc = calc
    forces_ase = atoms.get_forces()
    E_ase = atoms.get_potential_energy()

    assert np.linalg.norm(forces_ase - forces_ref) < tol, 'Forces not equal'
    assert np.linalg.norm(E_ase - E_ref) < tol, 'Energy not equal'
