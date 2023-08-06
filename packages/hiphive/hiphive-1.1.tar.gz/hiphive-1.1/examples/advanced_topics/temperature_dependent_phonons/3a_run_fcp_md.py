"""
This script carries a series of molecular dynamics simulations at different
temperatures and stores snapshots to file.
"""

import os
import numpy as np
from ase.io import write, read
from ase.io.trajectory import Trajectory

from hiphive import ForceConstantPotential
from hiphive.calculators import ForceConstantCalculator

from ase import units
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.langevin import Langevin
from ase.md import MDLogger


if not os.path.exists('md_runs'):
    os.makedirs('md_runs')


# parameters
size = 6
temperatures = [2000, 1000, 300]
number_of_equilibration_steps = 3000
number_of_production_steps = 3000
time_step = 1.0
dump_interval = 100

# read FCP
fcp = ForceConstantPotential.read('fcps/fcp_sixth_order.fcp')
prim = fcp.primitive_structure

# setup calculator
atoms_ideal = prim.repeat(size)
fcs = fcp.get_force_constants(atoms_ideal)
calc = ForceConstantCalculator(fcs)

for temperature in temperatures:

    print('Temperature: {}'.format(temperature))

    # set up molecular dynamics simulation
    atoms = atoms_ideal.copy()
    atoms.set_calculator(calc)
    dyn = Langevin(atoms, time_step * units.fs, temperature * units.kB, 0.02)

    # equilibration run
    rs = np.random.RandomState(2020)
    MaxwellBoltzmannDistribution(atoms, temperature * units.kB, rng=rs)
    dyn.run(number_of_equilibration_steps)

    # production run
    log_file = 'md_runs/T{:}.log'.format(temperature)
    traj_file = 'md_runs/T{:}.traj'.format(temperature)
    logger = MDLogger(dyn, atoms, log_file,
                      header=True, stress=False,
                      peratom=True, mode='w')
    traj_writer = Trajectory(traj_file, 'w', atoms)
    dyn.attach(logger, interval=dump_interval)
    dyn.attach(traj_writer.write, interval=dump_interval)
    dyn.run(number_of_production_steps)

    # prepare snapshots for later use
    frames = []
    for atoms in read(traj_file, ':'):
        forces = atoms.get_forces()
        displacements = atoms.positions - atoms_ideal.get_positions()
        atoms.positions = atoms_ideal.get_positions()
        atoms.new_array('displacements', displacements)
        atoms.new_array('forces', forces)
        frames.append(atoms.copy())
    print(' Number of snapshots: {}'.format(len(frames)))
    write('md_runs/snapshots_T{:}.xyz'.format(temperature), frames, format='extxyz')
