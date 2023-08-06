"""
Run molecular dynamics simulations and dump snapshots
"""
from ase.calculators.emt import EMT
from ase.build import bulk

from ase import units
from ase.io.trajectory import Trajectory
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.langevin import Langevin


# parameters
cell_size = 6  # system size
number_of_MD_steps = 500
time_step = 5  # in fs
dump_interval = 50
temperature = 800
traj_file = 'md_trajectory_T{}.traj'

# set up supercell and calculator
atoms = bulk('Ni').repeat(cell_size)
reference_positions = atoms.get_positions()
calc = EMT()

# setup molecular dynamics simulations
atoms.set_calculator(calc)
dyn = Langevin(atoms, time_step * units.fs, temperature * units.kB, 0.02)
traj_writer = Trajectory(traj_file.format(temperature), 'w', atoms)
MaxwellBoltzmannDistribution(atoms, temperature * units.kB)

# run equilibration
dyn.run(number_of_MD_steps)

# run sample
dyn.attach(traj_writer.write, interval=dump_interval)
dyn.run(number_of_MD_steps)
