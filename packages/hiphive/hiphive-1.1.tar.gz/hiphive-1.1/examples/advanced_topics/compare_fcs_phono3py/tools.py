"""
Collection of tools for running this tutorial.
"""
import os
from ase.io import read
from ase.calculators.lammpsrun import LAMMPS
from ase.data import atomic_masses, atomic_numbers


def get_single_calculator(potential_file, atom_type, pair_style,
                          pair_coeff_tag=None, mass=None, keep=False):
    """Returns an ase lammps calculator. Only works for monoatomic systems.

    Parameters
    ----------
    potential_file : str
        path to lammps potential file
    atom_type : str
        Atom type (pair coef tag)
    pair_style : str
        pair_style for lammps (must match potential file)
    pair_coeff_tag : str
        If a specific tag is needed rather than just the atom type
    mass : float
        atomic mass
    keep : bool
        keep tmp files or not (False is recommended unless debugging)

    Returns
    --------
    calc (ase-calculator): ASE lammps calculator

    """
    if not os.path.isfile(potential_file):
        raise ValueError('Potential File not found1')

    if mass is None:
        Z = atomic_numbers[atom_type]
        mass = atomic_masses[Z]
    if pair_coeff_tag is None:
        pair_coeff_tag = atom_type

    potential_file = os.path.abspath(potential_file)
    pair_coeff = ['* * ' + potential_file + ' ' + pair_coeff_tag]
    mass = ['1 %.6f' % mass]
    parameters = {'pair_style': pair_style,
                  'pair_coeff': pair_coeff,
                  'mass': mass}
    calc = LAMMPS(parameters=parameters, keep_tmp_files=keep,
                  keep_alive=False, no_data_file=True)
    return calc


def write_vaspruns(out_dir, poscars, calc, translate=False):
    """ For each poscar in poscars writes a vasprun file with forces.
    Calc is used to compute forces for poscars.

    Parameters
    ----------
    out_dir : str
        Output directory
    poscars : list or str
        List of poscars or just single poscar,
        should be named according to phonopy convention i.e. POSCAR-005
    calc : ASE-calculator
        Calculator for computing forces
    """

    # if poscars is single file
    if isinstance(poscars, str):
        poscar_list = [poscars]
    else:
        poscar_list = poscars

    for poscar in poscar_list:
        poscar_number = poscar.split('-')[-1]
        vasprun_name = 'vasprun.xml-%s' % poscar_number
        atoms = read(poscar)
        if translate:
            atoms.translate([0.1, 0.2, 0.3])
            atoms.wrap()
        atoms.set_calculator(calc)
        forces = atoms.get_forces()
        write_vasprun(os.path.join(out_dir, vasprun_name), forces)


def write_vasprun(file_name, forces):
    """ Writes dummy vasprun file with only forces """

    f = open(file_name, 'w')
    f.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
    f.write('<modelling>\n')

    f.write(' <generator>\n')
    f.write('  <i name="version" type="string">4.6.35 </i>\n')
    f.write('</generator>\n')

    f.write(' <calculation>\n')

    f.write('  <varray name="forces" >\n')
    for force in forces:
        f.write('  <v>%16.12f   %16.12f   %16.12f </v>\n'
                % (force[0], force[1], force[2]))
    f.write('  </varray>\n')

    f.write(' </calculation>\n')
    f.write('</modelling>\n')

    f.close()
