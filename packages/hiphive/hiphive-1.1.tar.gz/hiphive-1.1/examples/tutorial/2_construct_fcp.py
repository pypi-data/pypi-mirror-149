"""
Construct a ForceConstantPotential from training data generated previously.

Runs in approximately 100 seconds on an Intel Core i5-4670K CPU.
"""

from ase.io import read
from hiphive import ClusterSpace, StructureContainer, ForceConstantPotential
from hiphive.utilities import prepare_structures
from trainstation import Optimizer


# read structures containing displacements and forces
prim = read('prim.extxyz')
atoms_ideal = read('supercell_ideal.extxyz')
rattled_structures = read('supercells_rattled.extxyz', index=':')

# set up cluster space
cutoffs = [5.0, 4.0, 4.0]
cs = ClusterSpace(prim, cutoffs)
print(cs)
cs.print_orbits()

# ... and structure container
structures = prepare_structures(rattled_structures, atoms_ideal)
sc = StructureContainer(cs)
for structure in structures:
    sc.add_structure(structure)
print(sc)

# train model
opt = Optimizer(sc.get_fit_data())
opt.train()
print(opt)

# construct force constant potential
fcp = ForceConstantPotential(cs, opt.parameters)
fcp.write('fcc-nickel.fcp')
print(fcp)
