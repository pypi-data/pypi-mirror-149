"""
Generate displaced structures using
* Standard rattle, gaussian displacements
* Monte Carlo rattle, gaussian displacements w penatly for short atomic dists
* Phonon rattle, construct a rough guess of fc2 and populate phonon modes with
  thermal energy corresponding to a temperature

The hyper parameters for the different methods are chosen such that the
magnitude of the displacements will be roughly the same

This script may take a few minutes to run.
"""

from ase.build import bulk
from ase.io import write
from ase.calculators.emt import EMT
from hiphive import ClusterSpace, StructureContainer, ForceConstantPotential
from trainstation import Optimizer
from hiphive.utilities import prepare_structures
from hiphive.structure_generation import (generate_rattled_structures,
                                          generate_mc_rattled_structures,
                                          generate_phonon_rattled_structures)


# parameters
alat = 3.52         # lattice parameter
size = 6            # supercell size
n_structures = 25      # number of configurations to generate

# rattle parameters
T = 800
rattle_std = 0.12
min_distance = 0.67 * alat

# reference structure
prim = bulk('Ni', a=alat)
calc = EMT()

supercell = prim.repeat(size)
reference_positions = supercell.get_positions()
write('reference_structure.xyz', supercell)

# standard rattle
print('standard rattle')
structures_rattle = generate_rattled_structures(
    supercell, n_structures, rattle_std)
write('structures_rattle.extxyz', structures_rattle)

# Monte Carlo rattle
print('Monte Carlo rattle')
structures_mc_rattle = generate_mc_rattled_structures(
    supercell, n_structures, 0.25*rattle_std, min_distance, n_iter=20)
write('structures_mc_rattle.extxyz', structures_mc_rattle)


# Phonon rattle

# initial model
cs = ClusterSpace(supercell, [5.0])
sc = StructureContainer(cs)
rattled_structures = generate_rattled_structures(supercell, 1, 0.05)
rattled_structures = prepare_structures(rattled_structures, supercell, calc)

for structure in rattled_structures:
    sc.add_structure(structure)
opt = Optimizer(sc.get_fit_data(), train_size=1.0)
opt.train()
fcp = ForceConstantPotential(cs, opt.parameters)

# generate phonon rattled structures
fc2 = fcp.get_force_constants(supercell).get_fc_array(order=2, format='ase')
structures_phonon_rattle = generate_phonon_rattled_structures(
    supercell, fc2, n_structures, T)
write('structures_phonon_rattle_T{}.extxyz'.format(T), structures_phonon_rattle)  # noqa
