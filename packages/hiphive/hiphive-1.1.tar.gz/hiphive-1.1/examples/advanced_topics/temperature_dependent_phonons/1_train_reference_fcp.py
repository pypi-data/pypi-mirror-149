import os
from ase.io import read
from hiphive import ClusterSpace, StructureContainer, ForceConstantPotential
from trainstation import Optimizer
from hiphive.cutoffs import Cutoffs


# read training structures
structures = read('training_structures.extxyz@:')

# setup CS and SC
cutoffs = Cutoffs([[6.0, 6.0, 6.0, 4.0, 4.0]])
cs = ClusterSpace(structures[0], cutoffs)
sc = StructureContainer(cs)
for x in structures:
    sc.add_structure(x)
print(sc)

# train
opt = Optimizer(sc.get_fit_data(), fit_method='ridge', alpha=25, train_size=0.9)
opt.train()
print(opt)

# store fcp
fcp = ForceConstantPotential(cs, opt.parameters)
os.makedirs('fcps/', exist_ok=True)
fcp.write('fcps/fcp_sixth_order.fcp')
