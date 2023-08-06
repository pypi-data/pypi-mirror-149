"""
Run molecular dynamics simulations using the fourth order
hiPhive force constant potential and the ASE MD module.

Runs in approximately 500 seconds on an Intel Core i5-4670K CPU.
"""

import os
import numpy as np
from ase.build import bulk
from hiphive import ForceConstantPotential
from hiphive.calculators import ForceConstantCalculator

from ase import units
from ase.io.trajectory import Trajectory
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.langevin import Langevin
from ase.md import MDLogger


# parameters
cell_size = 6  # system size
number_of_MD_steps = 1000
time_step = 5  # in fs
dump_interval = 20
temperatures = [600, 1200]
log_file = 'md_runs/logs_T{}'
traj_file = 'md_runs/trajs_T{}.traj'
if not os.path.isdir(os.path.dirname(log_file)):
    os.mkdir(os.path.dirname(log_file))

# set up supercell
atoms = bulk('Ni').repeat(cell_size)
reference_positions = atoms.get_positions()

# get force constant calculator
fcp = ForceConstantPotential.read('fcc-nickel.fcp')
fcs = fcp.get_force_constants(atoms)
calc = ForceConstantCalculator(fcs)

# run molecular dynamics simulations
atoms.set_calculator(calc)
for temperature in temperatures:
    dyn = Langevin(atoms, time_step * units.fs, temperature * units.kB, 0.02)
    logger = MDLogger(dyn, atoms, log_file.format(temperature),
                      header=True, stress=False, peratom=True, mode='w')
    traj_writer = Trajectory(traj_file.format(temperature), 'w', atoms)
    dyn.attach(logger, interval=dump_interval)
    dyn.attach(traj_writer.write, interval=dump_interval)

    # run MD
    MaxwellBoltzmannDistribution(atoms, temperature * units.kB)
    dyn.run(number_of_MD_steps)

# compute mean-square displacement from MD trajectories
for temperature in temperatures:
    traj_reader = Trajectory(traj_file.format(temperature), 'r')
    msd = []
    for atoms in [a for a in traj_reader][10:]:
        displacements = atoms.positions - reference_positions
        msd.append(np.mean(np.sum(displacements**2, axis=1)))
    print('T = {:4d}    MSD = {:.5f} A**2'.format(temperature, np.mean(msd)))
