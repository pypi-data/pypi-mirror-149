from ase.io import read
from hiphive import ClusterSpace, StructureContainer

# parameters
cutoffs = [8.0]
structures = read('MoS2_rattled_structures.extxyz@:')

# build clusterspace and structurecontainer
cs = ClusterSpace(structures[0], cutoffs)
sc = StructureContainer(cs)
for structure in structures:
    sc.add_structure(structure)
sc.write('structure_container.sc')
