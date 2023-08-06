from ase.io import read
from hiphive import ClusterSpace, StructureContainer, ForceConstantPotential
from trainstation import Optimizer


temperatures = [2000, 1000, 300]
cutoffs = [6.0]

for T in temperatures:
    structures = read('md_runs/snapshots_T{:}.xyz'.format(T), index=':')

    cs = ClusterSpace(structures[0], cutoffs)
    sc = StructureContainer(cs)
    for s in structures:
        sc.add_structure(s)

    opt = Optimizer(sc.get_fit_data(), train_size=1.0)
    opt.train()
    print(opt)
    fcp = ForceConstantPotential(cs, opt.parameters)
    fcp.write('fcps/ehm_T{}.fcp'.format(T))
