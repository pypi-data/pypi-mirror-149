import subprocess
import glob
import os
import shutil
from ase.io import write, read
from tools import get_single_calculator, write_vaspruns

# Parameters
dim = 3
potential_file = 'Si.tersoff'
calc = get_single_calculator(potential_file, 'Si', 'tersoff',
                             pair_coeff_tag='Si(B)')

# Phono3py calculation
work_dir = 'phono3py_calculation/'
if not os.path.exists(work_dir):
    os.makedirs(work_dir)
os.chdir(work_dir)

# read and write POSCAR
atoms_prim = read('../structures/POSCAR')
write('POSCAR', atoms_prim, format='vasp')

# Generate displaced supercells
subprocess.call('phono3py -d --dim=\"%d %d %d\"' % (dim, dim, dim), shell=True)
if not os.path.exists('poscars'):
    os.makedirs('poscars')
else:
    shutil.rmtree('poscars')
    os.makedirs('poscars')
subprocess.call('mv POSCAR-* poscars', shell=True)

# Compute forces and write vasprun-xxx.xml
poscars = glob.glob('poscars/POSCAR-*')
if not os.path.exists('vaspruns'):
    os.makedirs('vaspruns')
else:
    shutil.rmtree('vaspruns')
    os.makedirs('vaspruns')

write_vaspruns('vaspruns/', poscars, calc, translate=True)
subprocess.call('phono3py --cf3 vaspruns/vasprun.xml*', shell=True)

# Write fc2 and fc3
subprocess.call('phono3py --dim=\"%d %d %d\" --sym_fc3r --sym_fc2'
                % (dim, dim, dim), shell=True)
os.chdir('..')
