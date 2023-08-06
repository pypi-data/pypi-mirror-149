import os
from ase.io import write
from ase.build import bulk
from hiphive.structure_generation import generate_rattled_structures
from hiphive.utilities import prepare_structures
from tools import get_single_calculator


# Parameters
a0 = 5.4323
dim = 3
rattle_amplitude = 0.02
number_of_structures = 5
potential_file = 'Si.tersoff'
calc = get_single_calculator(potential_file, 'Si', 'tersoff', pair_coeff_tag='Si(B)')
primitive_fname = 'structures/POSCAR'
structures_fname = 'structures/rattled_structures.extxyz'

# Generate rattled structures
atoms_prim = bulk('Si', 'diamond', a=a0)
atoms_ideal = atoms_prim.repeat(dim)

structures = generate_rattled_structures(atoms_ideal, number_of_structures, rattle_amplitude)
structures = prepare_structures(structures, atoms_ideal, calc)

# save structures
if not os.path.isdir(os.path.dirname(structures_fname)):
    os.mkdir(os.path.dirname(structures_fname))
write(primitive_fname, atoms_prim)
write(structures_fname, structures)
