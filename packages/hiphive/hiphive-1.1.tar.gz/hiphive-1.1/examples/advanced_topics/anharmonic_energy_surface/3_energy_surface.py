import numpy as np
import matplotlib.pyplot as plt
from ase.io import read
from ase.calculators.emt import EMT
from hiphive import StructureContainer, ForceConstantPotential
from trainstation import Optimizer
from hiphive.calculators import ForceConstantCalculator
from tools import compute_energy_landscape


# parameters
dz_vals = np.linspace(-0.4, 0.4, 21)
atoms_ideal = read('rattled_structures.extxyz')

# read data
sc2 = StructureContainer.read('structure_container2')
sc3 = StructureContainer.read('structure_container3')
cs2 = sc2.cluster_space
cs3 = sc3.cluster_space

# fit models
opt = Optimizer(sc2.get_fit_data(), train_size=1.0)
opt.train()
fcp2 = ForceConstantPotential(cs2, opt.parameters)

opt = Optimizer(sc3.get_fit_data(), train_size=1.0)
opt.train()
fcp3 = ForceConstantPotential(cs3, opt.parameters)

# test models
emt_calc = EMT()
calc_fc2 = ForceConstantCalculator(fcp2.get_force_constants(atoms_ideal))
calc_fc3 = ForceConstantCalculator(fcp3.get_force_constants(atoms_ideal))

pes_emt = compute_energy_landscape(atoms_ideal, emt_calc, dz_vals)
pes_fc2 = compute_energy_landscape(atoms_ideal, calc_fc2, dz_vals)
pes_fc3 = compute_energy_landscape(atoms_ideal, calc_fc3, dz_vals)


# plot pes
fs = 14
lw = 1.5
ms = 8

plt.plot(pes_emt[:, 0], pes_emt[:, 1], '-o', lw=lw, ms=ms, label='EMT')
plt.plot(pes_fc2[:, 0], pes_fc2[:, 1], '-o', lw=lw, ms=ms, label='2nd')
plt.plot(pes_fc3[:, 0], pes_fc3[:, 1], '-o', lw=lw, ms=ms, label='2nd+3rd')
plt.xlim([np.min(dz_vals), np.max(dz_vals)])
plt.ylim(bottom=0.0)

plt.xlabel('Surface layer shift ($\\mathrm{\\AA}$)', fontsize=fs)
plt.ylabel('Potential Energy (eV)', fontsize=fs)

plt.gca().tick_params(labelsize=fs)

plt.legend(loc=9, fontsize=fs)
plt.tight_layout()
plt.savefig('energy_surface.svg')
