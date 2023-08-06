import os
import numpy as np
from hiphive import ClusterSpace, ForceConstantPotential
from hiphive.self_consistent_phonons import self_consistent_harmonic_model
from hiphive.calculators import ForceConstantCalculator


# parameters
cutoffs = [6.0]
temperatures = [2000, 1000, 300]
size = 6


# scp parameters
n_structures = 30
n_iterations = 50
alpha = 0.2


# read FCP
fcp = ForceConstantPotential.read('fcps/fcp_sixth_order.fcp')
prim = fcp.primitive_structure

# setup scph
cs = ClusterSpace(prim, cutoffs)
supercell = prim.repeat(size)
fcs = fcp.get_force_constants(supercell)
calc = ForceConstantCalculator(fcs)

# run scph
os.makedirs('scph_trajs/', exist_ok=True)
for T in temperatures:
    parameters_traj = self_consistent_harmonic_model(
        supercell, calc, cs, T, alpha, n_iterations, n_structures)
    fcp_scph = ForceConstantPotential(cs, parameters_traj[-1])
    fcp_scph.write('fcps/scph_T{}.fcp'.format(T))
    np.savetxt('scph_trajs/scph_parameters_T{}'.format(T), np.array(parameters_traj))
