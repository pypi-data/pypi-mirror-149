"""
Test the rattle structure generation algorithms
"""

import numpy as np

from ase.build import bulk
from hiphive.utilities import get_displacements
from hiphive.structure_generation import (generate_rattled_structures,
                                          generate_mc_rattled_structures)


tol = 1e-8


def check_structure_displacements(atoms_ideal, atoms, max_disp):
    assert np.all(atoms_ideal.numbers == atoms.numbers)
    assert np.linalg.norm(atoms_ideal.cell - atoms.cell) < tol
    disps = get_displacements(atoms, atoms_ideal)

    disps = np.linalg.norm(disps, axis=1)
    assert np.max(disps) < max_disp


def test_rattle():
    atoms_ideal = bulk('Si', 'diamond', a=5.5).repeat(5)

    rattle_std = 0.1
    max_disp = 0.5

    atoms_list1 = generate_rattled_structures(atoms_ideal, 2, rattle_std)
    atoms_list2 = generate_mc_rattled_structures(atoms_ideal, 2, rattle_std/4, 1.8)

    # check rattle structures
    for atoms in atoms_list1:
        check_structure_displacements(atoms_ideal, atoms, max_disp)

    # check mc rattle structures
    for atoms in atoms_list2:
        check_structure_displacements(atoms_ideal, atoms, max_disp)
