from hiphive import ForceConstantPotential, StructureContainer
from hiphive import enforce_rotational_sum_rules
from trainstation import Optimizer


# fit model
sc = StructureContainer.read('structure_container.sc')
cs = sc.cluster_space
opt = Optimizer(sc.get_fit_data(), train_size=1.0)
opt.train()
print(opt)

# apply sum rules
parameters = opt.parameters
parameters_huang = enforce_rotational_sum_rules(
    cs, parameters, ['Huang'])
parameters_bornhuang = enforce_rotational_sum_rules(
    cs, parameters, ['Born-Huang'])
parameters_rot = enforce_rotational_sum_rules(
    cs, parameters, ['Huang', 'Born-Huang'])

fcp_normal = ForceConstantPotential(cs, parameters)
fcp_huang = ForceConstantPotential(cs, parameters_huang)
fcp_bornhuang = ForceConstantPotential(cs, parameters_bornhuang)
fcp_rot = ForceConstantPotential(cs, parameters_rot)

fcp_normal.write('fcp_normal.fcp')
fcp_huang.write('fcp_huang.fcp')
fcp_bornhuang.write('fcp_bornhuang.fcp')
fcp_rot.write('fcp_rot.fcp')
