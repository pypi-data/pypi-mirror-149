import numpy as np
from ase import Atoms
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms


THz2meV = 4.13567


def get_band(q_start, q_stop, N):
    """ Return path between q_start and q_stop """
    return np.array([q_start + (q_stop-q_start)*i/(N-1) for i in range(N)])


def get_bcc_bands(N=100):
    N2G = get_band(np.array([0, 0, 0.5]), np.array([0, 0, 0]), N)
    G2H = get_band(np.array([0, 0, 0]), np.array([0.5, -0.5, 0.5]), N)
    H2P2G = get_band(np.array([0.5, 0.5, 0.5]), np.array([0, 0, 0]), N)
    bands = [N2G, G2H, H2P2G]
    return bands


def get_dispersion(fcp, dim):
    # setup phonopy and get FCs

    prim = fcp.primitive_structure
    atoms_phonopy = PhonopyAtoms(symbols=prim.get_chemical_symbols(),
                                 scaled_positions=prim.get_scaled_positions(),
                                 cell=prim.cell)
    phonopy = Phonopy(atoms_phonopy, supercell_matrix=dim*np.eye(3),
                      primitive_matrix=None)
    supercell = phonopy.get_supercell()
    supercell = Atoms(cell=supercell.cell, numbers=supercell.numbers, pbc=True,
                      scaled_positions=supercell.get_scaled_positions())

    fcs = fcp.get_force_constants(supercell)
    phonopy.set_force_constants(fcs.get_fc_array(order=2))

    # get phonon dispersion
    bands = get_bcc_bands()
    phonopy.set_band_structure(bands)
    qvecs, qnorms, freqs, _ = phonopy.get_band_structure()
    freqs = [f * THz2meV for f in freqs]
    return qnorms, freqs
