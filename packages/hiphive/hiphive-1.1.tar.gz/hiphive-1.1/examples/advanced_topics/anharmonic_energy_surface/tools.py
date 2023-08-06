import numpy as np


def compute_energy_landscape(atoms, calc, dz_vals, tol=1e-3):
    """ Compute energy landscape for shifting the top surface layer """

    # compute reference energy
    atoms.set_calculator(calc)
    E0 = atoms.get_potential_energy()

    # find surface atom
    z = atoms.positions[:, 2]
    atom_indices = np.where(z + tol > np.max(z))

    # run displacement path
    data = []
    for dz in dz_vals:
        atoms_tmp = atoms.copy()
        atoms_tmp.set_calculator(calc)
        atoms_tmp.positions[atom_indices, 2] += dz
        data.append([dz, atoms_tmp.get_potential_energy() - E0])
    return np.array(data)
