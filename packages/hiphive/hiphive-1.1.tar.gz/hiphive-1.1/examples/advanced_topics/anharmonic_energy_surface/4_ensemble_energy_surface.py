import numpy as np
import matplotlib.pyplot as plt
from ase.io import read
from hiphive import StructureContainer
from hiphive.force_constant_model import ForceConstantModel
from trainstation import EnsembleOptimizer
from hiphive.calculators import ForceConstantCalculator
from tools import compute_energy_landscape


# parameters
ensemble_size = 20
dz_vals = np.linspace(-0.4, 0.4, 21)
atoms_ideal = read('rattled_structures.extxyz')


# read data
sc = StructureContainer.read('structure_container3')
cs = sc.cluster_space

# training
eopt = EnsembleOptimizer(sc.get_fit_data(), train_size=0.5, ensemble_size=ensemble_size)
eopt.train()

# average model
fcm = ForceConstantModel(atoms_ideal, cs)
fcm.parameters = eopt.parameters
calc_ave = ForceConstantCalculator(fcm.get_force_constants())
pes_ave = compute_energy_landscape(atoms_ideal, calc_ave, dz_vals)

# ensemble models
ensemble_pes = []
for parameters in eopt.parameters_splits:
    fcm.parameters = parameters
    calc = ForceConstantCalculator(fcm.get_force_constants())
    pes = compute_energy_landscape(atoms_ideal, calc, dz_vals)
    ensemble_pes.append(pes)

# plot pes
fs = 14
lw = 2.2
alpha = 0.7

for pes in ensemble_pes:
    plt.plot(pes[:, 0], pes[:, 1], '-', lw=lw, alpha=alpha)
plt.plot(pes_ave[:, 0], pes_ave[:, 1], 'k', lw=lw+1, label='Average model')

plt.xlim([np.min(dz_vals), np.max(dz_vals)])
plt.ylim(bottom=0.0)
plt.xlabel('Surface layer shift ($\\mathrm{\\AA}$)', fontsize=fs)
plt.ylabel('Potential Energy (eV)', fontsize=fs)
plt.gca().tick_params(labelsize=fs)

plt.legend(loc=9, fontsize=fs)
plt.tight_layout()
plt.savefig('ensemble_energy_surface.svg')
