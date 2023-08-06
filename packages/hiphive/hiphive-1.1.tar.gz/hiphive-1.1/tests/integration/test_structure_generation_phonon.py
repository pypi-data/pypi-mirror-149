"""
Test that phonon rattle works well using a force constant matrix (fc2)
constructed from an EMT calculator
"""

import numpy as np

from ase.build import bulk
from ase.calculators.emt import EMT
from ase.units import (kB, _hbar, J, s)
from hiphive import ClusterSpace, StructureContainer, ForceConstantPotential
from hiphive.calculators import ForceConstantCalculator
from trainstation import Optimizer
from hiphive.utilities import get_displacements
from hiphive.structure_generation import generate_phonon_rattled_structures
from hiphive.structure_generation.phonon import _PhononRattler


def check_structure_displacements(atoms_ideal, atoms, max_disp, cell_tol):
    assert np.all(atoms_ideal.numbers == atoms.numbers)
    assert np.linalg.norm(atoms_ideal.cell - atoms.cell) < cell_tol
    disps = get_displacements(atoms, atoms_ideal)

    disps = np.linalg.norm(disps, axis=1)
    assert np.max(disps) < max_disp


def test_phonon_rattle():
    # setup
    n_structs = 100
    T = 1000
    max_disp = 1.0
    cell_tol = 1e-8
    atoms_ideal = bulk('Ni').repeat(5)
    calc = EMT()

    # compute fc2
    cs = ClusterSpace(atoms_ideal, [6.0])
    atoms_rattle = atoms_ideal.copy()
    atoms_rattle.rattle(0.01)
    atoms_rattle.calc = calc
    disps = get_displacements(atoms_rattle, atoms_ideal)
    forces = atoms_rattle.get_forces()
    atoms_rattle.positions = atoms_ideal.get_positions()
    atoms_rattle.new_array('displacements', disps)
    atoms_rattle.new_array('forces', forces)
    sc = StructureContainer(cs)
    sc.add_structure(atoms_rattle)
    opt = Optimizer(sc.get_fit_data())
    opt.train()
    fcp = ForceConstantPotential(cs, opt.parameters)
    fcs = fcp.get_force_constants(atoms_ideal)

    # test init with different shapes of fc2
    np.random.seed(abs(hash('hiphive')) // 2**32)
    fc2 = fcs.get_fc_array(order=2, format='ase')
    structures = generate_phonon_rattled_structures(atoms_ideal, fc2, n_structs, T)

    np.random.seed(abs(hash('hiphive')) // 2**32)
    fc2 = fcs.get_fc_array(order=2)
    structures2 = generate_phonon_rattled_structures(atoms_ideal, fc2, n_structs, T)

    for s1, s2 in zip(structures, structures2):
        assert np.allclose(s1.positions, s2.positions)

    # check rattle structures
    structures = generate_phonon_rattled_structures(atoms_ideal, fc2, n_structs, T)
    for atoms in structures:
        check_structure_displacements(atoms_ideal, atoms, max_disp, cell_tol)

    fc_calc = ForceConstantCalculator(fcs)
    atoms = atoms_ideal.copy()
    atoms.calc = fc_calc
    potential_energies = []
    for rattled_atoms in structures:
        atoms.positions = rattled_atoms.positions
        potential_energies.append(atoms.get_potential_energy())

    assert np.isclose(np.mean(potential_energies), len(atoms) * 3 / 2 * kB * T, 1.0)

    # Bose-Einstein rattle
    structures = generate_phonon_rattled_structures(
        atoms_ideal, fc2, n_structs, T, QM_statistics=True)
    for atoms in structures:
        check_structure_displacements(atoms_ideal, atoms, max_disp, cell_tol)

    fc_calc = ForceConstantCalculator(fcs)
    atoms = atoms_ideal.copy()
    atoms.calc = fc_calc
    potential_energies = []
    for rattled_atoms in structures:
        atoms.positions = rattled_atoms.positions
        potential_energies.append(atoms.get_potential_energy())

    pr = _PhononRattler(atoms_ideal.get_masses(), fc2)
    w_s = pr.w2_s[3:]
    hbar = _hbar * J * s
    n_BE = 1 / (np.exp(hbar * w_s / (kB * T)) - 1)
    ET = (hbar * w_s * n_BE)
    E0 = hbar * w_s * 0.5
    assert np.isclose(np.mean(potential_energies), 0.5 * (ET + E0).sum(), 1.0)
