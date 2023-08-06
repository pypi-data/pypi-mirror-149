"""
Tests building CS, FCP, SC for a few different crystal structures.
"""

import numpy as np

from ase.build import bulk
from hiphive import ClusterSpace, StructureContainer, ForceConstantPotential


def generate_supercell(prim, repeat=(4, 4, 5)):
    """ Generates supercell given a primitive object """
    supercell = prim.repeat(repeat)

    displacements = np.random.random((supercell.positions.shape))
    forces = np.random.random((supercell.positions.shape))
    supercell.new_array('displacements', displacements)
    supercell.new_array('forces', forces)

    # rotate supercell
    supercell.rotate(63.142, v=(1, 2, 3), rotate_cell=True)
    return supercell


def test_CS_FCP_SC_with_crystal_structures():
    a0 = 3.0
    cutoffs = [3.5]

    # structure lists
    monoatomic_structures = ['sc', 'bcc', 'fcc', 'hcp', 'diamond']
    binary_structures = ['rocksalt', 'zincblende', 'cesiumchloride', 'wurtzite']

    # generate structures
    crystal_structures = {}
    for crystal in monoatomic_structures:
        prim = bulk('Ta', crystal, a=a0)
        supercell = generate_supercell(prim)
        crystal_structures[crystal] = (prim, supercell)

    for crystal in binary_structures:
        prim = bulk('NaCl', crystal, a=a0)
        supercell = generate_supercell(prim)
        crystal_structures[crystal] = (prim, supercell)

    # test all structures
    for crystal, (prim, supercell) in crystal_structures.items():
        try:
            cs = ClusterSpace(prim, cutoffs)
        except Exception as e:
            msg = 'Failed to build ClusterSpace for {}'.format(crystal)
            msg += '\n{}'.format(e)
            assert False, msg

        try:
            sc = StructureContainer(cs)
            sc.add_structure(supercell)
        except Exception as e:
            msg = 'Failed to build StructureContainer for {}'.format(crystal)
            msg += '\n{}'.format(e)
            assert False, msg

        parameters = np.random.random(cs.n_dofs)
        try:
            ForceConstantPotential(cs, parameters)
        except Exception as e:
            msg = 'Failed to build ForceConstantPotential for {}'.format(crystal)
            msg += '\n{}'.format(e)
            assert False, msg
