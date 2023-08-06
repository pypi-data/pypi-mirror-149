import numpy as np
from ase import Atoms
from ase.build import bulk
from hiphive.structure_generation import generate_rattled_structures


def get_bcc_structures(n_structures, a=1, rattle=0.05, size=6):
    atoms_ideal = bulk('Ti', 'bcc', a=a).repeat(size)
    rattled_structures = generate_rattled_structures(
        atoms_ideal, n_structures, rattle)
    structures = []
    for structure in rattled_structures:
        atoms = atoms_ideal.copy()
        displacements = structure.positions - atoms.positions
        forces = np.zeros((len(atoms), 3))
        atoms.new_array('displacements', displacements)
        atoms.new_array('forces', forces)
        structures.append(atoms)
    return structures


def get_hcp_structures(n_structures, a=1, rattle=0.05, size=(3, 3, 6)):
    atoms_ideal = _get_atoms_along_hcp_path(0.0, a, size)
    atoms_hcp = _get_atoms_along_hcp_path(0.2484, a, size)
    rattled_structures = generate_rattled_structures(
        atoms_hcp, n_structures, rattle)
    structures = []
    for structure in rattled_structures:
        atoms = atoms_ideal.copy()
        displacements = structure.positions - atoms.positions
        forces = np.zeros((len(atoms), 3))
        atoms.new_array('displacements', displacements)
        atoms.new_array('forces', forces)
        structures.append(atoms)
    return structures


def get_omega_structures(n_structures, a=1, rattle=0.05, size=(4, 3, 6)):
    atoms_ideal = _get_atoms_along_hcp_path(0.0, a, size)
    atoms_omega = _get_atoms_along_hcp_path(0.48, a, size)
    rattled_structures = generate_rattled_structures(
        atoms_omega, n_structures, rattle)
    structures = []
    for structure in rattled_structures:
        atoms = atoms_ideal.copy()
        displacements = structure.positions - atoms.positions
        forces = np.zeros((len(atoms), 3))
        atoms.new_array('displacements', displacements)
        atoms.new_array('forces', forces)
        structures.append(atoms)
    return structures


def _get_atoms_along_omega_path(dx, a, size):
    """ Returns atoms object displaced along bcc-omega mode """

    x = 1 / np.sqrt(2.0)
    y = x / np.sqrt(3.0)
    z = y / np.sqrt(2.0)

    positions = a * np.array([
                [0, 0,     0],
                [x, 3*y,   0],
                [0, 4*y, 1*z],
                [x, 1*y, 1*z],
                [0, 2*y, 2*z],
                [x, 5*y, 2*z]])

    cell = a * np.diag([2*x, 6*y, 3*z])
    bcc = Atoms(cell=cell, positions=positions, symbols=['Ti']*6, pbc=True)
    bcc.wrap()

    indices1 = [2, 3]
    indices2 = [4, 5]

    atoms = bcc.copy()
    for ind in indices1:
        atoms[ind].position[2] += dx
    for ind in indices2:
        atoms[ind].position[2] -= dx

    atoms = atoms.repeat(size)
    return atoms


def _get_atoms_along_hcp_path(dx, a, size):
    """ Returns atoms object displaced along bcc-hcp mode """

    positions = a * np.array([
                [1,   0,   0],
                [0,   0,   0],
                [0,   1,   0],
                [1,   1,   0],
                [1.5, 0.5, 0.5],
                [0.5, 0.5, 0.5],
                [0.5, 1.5, 0.5],
                [1.5, 1.5, 0.5]])

    cell = a * np.diag([2, 2, 1])
    bcc = Atoms(cell=cell, positions=positions, symbols=['Ti']*8, pbc=True)
    bcc.wrap()

    indices1 = [0, 2, 5, 7]
    indices2 = [1, 3, 4, 6]

    atoms = bcc.copy()
    for ind in indices1:
        atoms[ind].position[0] += dx / np.sqrt(2.0)
        atoms[ind].position[1] -= dx / np.sqrt(2.0)
    for ind in indices2:
        atoms[ind].position[0] -= dx / np.sqrt(2.0)
        atoms[ind].position[1] += dx / np.sqrt(2.0)

    atoms = atoms.repeat(size)
    return atoms
