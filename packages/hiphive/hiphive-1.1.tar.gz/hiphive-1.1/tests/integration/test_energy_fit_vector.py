import numpy as np
from ase.build import bulk

from hiphive import ClusterSpace, ForceConstantPotential
from hiphive.force_constant_model import ForceConstantModel
from hiphive.calculators import ForceConstantCalculator


def test_energy_fit_vector():

    # setup
    cutoffs = [5, 3]
    prim = bulk('Ti', 'hcp')
    prim[0].symbol = 'Ta'
    cs = ClusterSpace(prim, cutoffs)

    # supercell with displacements
    size = 3
    supercell_ideal = prim.repeat(size)
    supercell_rattle = prim.repeat(size)
    disp = np.linspace(-1, 1, len(supercell_rattle)*3).reshape(-1, 3)
    supercell_rattle.positions += disp

    # make FCP
    parameters = np.linspace(-5, 10, cs.n_dofs)
    fcp = ForceConstantPotential(cs, parameters)

    # get energy with calculator
    fcs = fcp.get_force_constants(supercell_ideal)
    calc = ForceConstantCalculator(fcs)
    supercell_rattle.calc = calc
    E_calc = supercell_rattle.get_potential_energy()

    # get energy via fit row
    fcm = ForceConstantModel(supercell_ideal, cs)
    A_forces = fcm.get_fit_matrix(disp)
    A_energy = fcm.get_energy_fit_vector(A_forces, disp)
    E_fcm = A_energy.dot(parameters)

    # test
    assert abs(E_fcm) > 1e-4
    assert abs(E_fcm - E_calc) < 1e-8
