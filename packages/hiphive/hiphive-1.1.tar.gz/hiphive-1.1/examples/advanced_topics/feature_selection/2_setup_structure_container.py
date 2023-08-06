from ase.io import read
from hiphive import ClusterSpace, StructureContainer


structures = read('rattled_structures.extxyz@:')
cutoffs = [8]

cs = ClusterSpace(structures[0], cutoffs)
sc = StructureContainer(cs)
for structure in structures:
    sc.add_structure(structure)

sc.write('structure_container')
