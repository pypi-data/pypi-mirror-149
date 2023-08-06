from ase.io import read
from hiphive import StructureContainer
from hiphive import ClusterSpace


# setup
rattled_structures = read('rattled_structures.extxyz@:')

# Second order model
cs = ClusterSpace(rattled_structures[0], [5.1])
sc = StructureContainer(cs)
for structure in rattled_structures:
    sc.add_structure(structure)
sc.write('structure_container2')


# Third order model
cs = ClusterSpace(rattled_structures[0], [5.1, 3.0])
sc = StructureContainer(cs)
for structure in rattled_structures:
    sc.add_structure(structure)
sc.write('structure_container3')
