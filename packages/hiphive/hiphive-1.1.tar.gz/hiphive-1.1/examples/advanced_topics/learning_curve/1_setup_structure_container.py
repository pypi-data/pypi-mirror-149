"""
Create and save a StructureContainer to file
"""
from ase.build import bulk
from ase.calculators.emt import EMT
from hiphive import ClusterSpace, StructureContainer
from hiphive.structure_generation import generate_mc_rattled_structures
from hiphive.utilities import prepare_structures


# parameters
cutoffs = [6.5, 5.0, 4.0]
cell_size = 5
number_of_structures = 3
rattle_std = 0.03
minimum_distance = 2.3

# setup
atoms_ideal = bulk('Ni').repeat(cell_size)
calc = EMT()

# generate structures
structures = generate_mc_rattled_structures(
    atoms_ideal, number_of_structures, rattle_std, minimum_distance)
structures = prepare_structures(structures, atoms_ideal, calc)

# set up cluster space and structure container
cs = ClusterSpace(structures[0], cutoffs)
sc = StructureContainer(cs)
for structure in structures:
    sc.add_structure(structure)
sc.write('structure_container.sc')
