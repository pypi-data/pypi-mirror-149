from ase.io import read
from hiphive import StructureContainer, ForceConstantPotential
from trainstation import Optimizer


supercell = read('phono3py_calculation/SPOSCAR')
# Read structure containers and cluster spaces
sc2 = StructureContainer.read('structure_container2')
sc3 = StructureContainer.read('structure_container3')
sc4 = StructureContainer.read('structure_container4')
cs2 = sc2.cluster_space
cs3 = sc3.cluster_space
cs4 = sc4.cluster_space

# Fit models
opt = Optimizer(sc2.get_fit_data())
opt.train()
print(opt)
fcp2 = ForceConstantPotential(cs2, opt.parameters)

opt = Optimizer(sc3.get_fit_data())
opt.train()
print(opt)
fcp3 = ForceConstantPotential(cs3, opt.parameters)

opt = Optimizer(sc4.get_fit_data())
opt.train()
print(opt)
fcp4 = ForceConstantPotential(cs4, opt.parameters)

# Write force constants
# this would look smoother if we had our own hdf5 format for the full fcs!
fcs2 = fcp2.get_force_constants(supercell)
fcs2.write('model2.fcs')

fcs3 = fcp3.get_force_constants(supercell)
fcs3.write('model3.fcs')

fcs4 = fcp4.get_force_constants(supercell)
fcs4.write('model4.fcs')
