"""
Prepare training structures for FCC-Ni using an EMT calculator and a
Monte Carlo rattle approach for generating displacements.

Runs in approximately 10 seconds on an Intel Core i5-4670K CPU.
"""

from ase.io import write
from ase.build import bulk
from ase.calculators.emt import EMT
from hiphive.structure_generation import generate_mc_rattled_structures


# parameters
n_structures = 5
cell_size = 4
rattle_std = 0.03
minimum_distance = 2.3

# setup
prim = bulk('Ni', cubic=True)
atoms_ideal = prim.repeat(cell_size)

# generate structures
structures = generate_mc_rattled_structures(atoms_ideal, n_structures, rattle_std, minimum_distance)

for atoms in structures:
    atoms.calc = EMT()
    atoms.get_forces()

# save structures
write('prim.extxyz', prim)
write('supercell_ideal.extxyz', atoms_ideal)
write('supercells_rattled.extxyz', structures)
