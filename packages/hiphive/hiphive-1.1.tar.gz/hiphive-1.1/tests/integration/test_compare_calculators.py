"""
Tests that the ForceConstantCalculator and ForceConstantModel yield the same
forces.
"""

import numpy as np

from ase.build import bulk
from hiphive import ClusterSpace
from hiphive.calculators import ForceConstantCalculator
from hiphive.force_constant_model import ForceConstantModel


def test_compare_force_calculators():
    # Setup prim, atoms and fcp, fcm
    prim = bulk('Si')
    atoms = bulk('Si', cubic=True).repeat(2)
    cs = ClusterSpace(prim, [4.0, 4.0])
    fcm = ForceConstantModel(atoms, cs)

    # setup fcm calc
    params = np.random.random(len(fcm.parameters))
    fcm.parameters = params

    # setup ase calc
    fcs = fcm.get_force_constants()
    ase_calc = ForceConstantCalculator(fcs)

    # generate displacements
    displacements = np.random.normal(0.0, 0.1, atoms.positions.shape)
    atoms_tmp = atoms.copy()
    atoms_tmp.positions += displacements
    atoms_tmp.calc = ase_calc

    # calc forces
    forces_fcm_calc = fcm.get_forces(displacements)
    forces_ase_calc = atoms_tmp.get_forces()

    diff = np.linalg.norm(forces_fcm_calc - forces_ase_calc)
    assert diff < 1e-10, 'Forces from FCM/ASE calc did not match: {}'.format(diff)
