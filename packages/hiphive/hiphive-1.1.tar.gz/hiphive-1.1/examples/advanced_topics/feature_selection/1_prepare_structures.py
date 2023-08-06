from ase.io import write
from ase.cluster import Icosahedron
from ase.optimize import BFGS
from ase.calculators.emt import EMT
from hiphive.structure_generation import generate_rattled_structures
from hiphive.utilities import prepare_structures


# parameters
structures_fname = 'rattled_structures.extxyz'
number_of_structures = 10
particle_size = 3
a0 = 4.05
rattle_std = 0.02

# setup
atoms_ideal = Icosahedron('Al', particle_size, a0)
calc = EMT()
atoms_ideal.set_calculator(calc)

# center atoms and add pbc
atoms_ideal.center(vacuum=20)
atoms_ideal.pbc = True

# relax particle
dyn = BFGS(atoms_ideal)
converged = dyn.run(fmax=0.0001, steps=1000)

# generate structures
structures = generate_rattled_structures(atoms_ideal, number_of_structures, rattle_std)
structures = prepare_structures(structures, atoms_ideal, calc)

# save structures
write(structures_fname, structures)
