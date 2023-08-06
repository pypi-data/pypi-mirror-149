from ase.build import bulk
from ase.io import read
from hiphive import ClusterSpace, StructureContainer
from tools import get_bcc_structures, get_hcp_structures, get_omega_structures


# parameters
a0 = 3.32389853
cutoffs = [6.0, 4.0, 4.0]
n_structures = 1


# expansion around the BCC structure
prim = bulk('Ti', 'bcc', a=a0)
cs = ClusterSpace(prim, [6.0, 4.0, 4.0])


# generate rattled structuress
bcc_rattled = get_bcc_structures(n_structures, a=a0, rattle=0.1)
hcp_rattled = get_hcp_structures(n_structures, a=a0, rattle=0.02)
omega_rattled = get_omega_structures(n_structures, a=a0, rattle=0.02)
md_structures = read('Ti_md_structures_T1400.extxyz@:')


# setup StructureContainer
sc = StructureContainer(cs)
user_tag = 'bcc-rattle'
for structure in bcc_rattled:
    sc.add_structure(structure, user_tag=user_tag)

user_tag = 'hcp-rattle'
for structure in hcp_rattled:
    sc.add_structure(structure, user_tag=user_tag)

user_tag = 'omega-rattle'
for structure in omega_rattled:
    sc.add_structure(structure, user_tag=user_tag)

user_tag = 'md-T1400'
for structure in md_structures:
    sc.add_structure(structure, user_tag=user_tag)

# save sc
sc.write('structure_container')
