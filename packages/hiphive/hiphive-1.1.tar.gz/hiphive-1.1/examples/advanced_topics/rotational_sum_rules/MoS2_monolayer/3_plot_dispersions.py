import numpy as np
import matplotlib.pyplot as plt
from ase import Atoms
from hiphive import ForceConstantPotential
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms


def get_band(q_start, q_stop, N=500):
    return np.array([q_start + (q_stop-q_start)*i/(N-1) for i in range(N)])


def compute_dispersion(prim, fcp):
    dim_matrix = np.diag([6, 6, 1])

    # setup phonopy
    atoms_phonopy = PhonopyAtoms(symbols=prim.get_chemical_symbols(),
                                 scaled_positions=prim.get_scaled_positions(),
                                 cell=prim.cell)
    phonopy = Phonopy(atoms_phonopy, supercell_matrix=dim_matrix,
                      primitive_matrix=None)

    # set force constants
    supercell = phonopy.get_supercell()
    supercell = Atoms(cell=supercell.cell, numbers=supercell.numbers, pbc=True,
                      scaled_positions=supercell.get_scaled_positions())
    fcs = fcp.get_force_constants(supercell)
    phonopy.set_force_constants(fcs.get_fc_array(order=2))

    # get dispersion
    band1 = get_band(np.array([0, 0, 0]), np.array([0.5, 0, 0]))
    bands = [band1]

    # get phonon dispersion
    phonopy.set_band_structure(bands)
    qvecs, qnorms, freqs, _ = phonopy.get_band_structure()
    return qnorms[0], freqs[0]


# compute dispersions
fcp_normal = ForceConstantPotential.read('fcp_normal.fcp')
fcp_rot = ForceConstantPotential.read('fcp_rot.fcp')
fcp_huang = ForceConstantPotential.read('fcp_huang.fcp')
fcp_bornhuang = ForceConstantPotential.read('fcp_bornhuang.fcp')

prim = fcp_normal.primitive_structure

qvec_normal, freqs_normal = compute_dispersion(prim, fcp_normal)
qvec_rot, freqs_rot = compute_dispersion(prim, fcp_rot)
qvec_huang, freqs_huang = compute_dispersion(prim, fcp_huang)
qvec_bornhuang, freqs_bornhuang = compute_dispersion(prim, fcp_bornhuang)


# plot
lw = 3.0
fs = 14
fig = plt.figure(figsize=(7.0, 4.8))
ax1 = fig.add_subplot(1, 1, 1)

ax1.plot(qvec_normal, freqs_normal, '-', lw=lw, color='tab:blue')
ax1.plot(np.nan, np.nan, '-', lw=lw, color='tab:blue', label='T')


ax1.plot(qvec_huang, freqs_huang, '--', lw=lw, color='tab:red')
ax1.plot(np.nan, np.nan, '--', lw=lw, color='tab:red', label='T + H')

ax1.plot(qvec_bornhuang, freqs_bornhuang, '--', lw=lw, color='tab:green')
ax1.plot(np.nan, np.nan, '--', lw=lw, color='tab:green', label='T + BH')

ax1.plot(qvec_rot, freqs_rot, '--', lw=lw, color='tab:orange')
ax1.plot(np.nan, np.nan, '--', lw=lw, color='tab:orange', label='T + H + BH')

ax1.set_xlabel('Wave vector', fontsize=fs)
ax1.set_ylabel('Frequency (THz)', fontsize=fs)
ax1.tick_params(labelsize=fs)
ax1.legend(fontsize=fs)

# zoom on gamma point
ax1.set_xlim([0.0, 0.07])
ax1.set_ylim([-0.5, 3.0])

fig.tight_layout()
fig.savefig('MoS2_phonon_dispersion.svg')
