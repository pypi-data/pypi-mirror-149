from hiphive.structure_generation import generate_rattled_structures
from ase.build import fcc110
from ase.io import write
from ase.calculators.emt import EMT
from ase.optimize import BFGS
from hiphive.utilities import prepare_structures

# parameters
number_of_structures = 5
rattle_std = 0.05
surface_size = (3, 4, 8)
structures_fname = 'rattled_structures.extxyz'

# setup atoms and calculator
atoms_ideal = fcc110('Cu', size=surface_size)
calc = EMT()

atoms_ideal.center(vacuum=20, axis=2)
atoms_ideal.pbc = True

# relax structure
atoms_ideal.set_calculator(calc)
dyn = BFGS(atoms_ideal)
converged = dyn.run(fmax=0.0001, steps=1000)


# generate rattled structures
structures = generate_rattled_structures(atoms_ideal, number_of_structures, rattle_std)
structures = prepare_structures(structures, atoms_ideal, calc)

# save structures
write(structures_fname, structures)
