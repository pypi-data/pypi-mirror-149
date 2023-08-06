import unittest
import numpy as np

from ase.build import bulk
from hiphive.utilities import get_displacements, get_neighbor_shells, prepare_structure,\
    find_permutation
from ase.calculators.emt import EMT
from ase.calculators.singlepoint import SinglePointCalculator


class TestUtilities(unittest.TestCase):
    """ Unittest class for utility functions. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def shortDescription(self):
        """Prevents unittest from printing docstring in test cases."""
        return None

    def test_get_displacements(self):
        """ Test get_displacements function. """

        for symbol in ['Al', 'Ti', 'Si']:
            atoms_ideal = bulk(symbol).repeat(4)

            atoms = atoms_ideal.copy()
            atoms.rattle(1.0)  # This causes atoms to go outside cell
            ref_disps = atoms.positions - atoms_ideal.positions

            atoms.wrap()
            disps = get_displacements(atoms, atoms_ideal)
            np.testing.assert_almost_equal(ref_disps, disps)

        # raise ValueError if structures dont match
        atoms_ideal = bulk('Al').repeat(4)
        atoms = atoms_ideal.copy()
        atoms.numbers[0] = 27
        with self.assertRaises(ValueError):
            get_displacements(atoms, atoms_ideal)

        atoms = atoms_ideal.copy()
        atoms.cell = atoms.cell * 1.01
        with self.assertRaises(ValueError):
            get_displacements(atoms, atoms_ideal)

    def test_get_shells(self):
        """ Test get_shells function. """

        # FCC
        atoms = bulk('Al', a=1.0)
        expected_fcc_dists = [1/np.sqrt(2), 1.0, np.sqrt(1.5), np.sqrt(2)]
        shells = get_neighbor_shells(atoms, cutoff=1.5)
        self.assertEqual(len(shells), len(expected_fcc_dists))
        for shell, dist in zip(shells, expected_fcc_dists):
            self.assertEqual(shell.types, ('Al', 'Al'))
            self.assertAlmostEqual(shell.distance, dist)
            self.assertIsInstance(str(shell), str)

        # HCP
        atoms = bulk('Al', 'hcp', a=1.0)
        expected_hcp_dists = [1, np.sqrt(2), np.sqrt(8/3)]
        shells = get_neighbor_shells(atoms, cutoff=1.65)
        self.assertEqual(len(shells), len(expected_hcp_dists))
        for shell, dist in zip(shells, expected_hcp_dists):
            self.assertEqual(shell.types, ('Al', 'Al'))
            self.assertAlmostEqual(shell.distance, dist)

        # rocksalt
        atoms = bulk('NaCl', 'rocksalt', a=1.0)
        expected_nacl_shells = [(('Cl', 'Na'), 0.5),
                                (('Cl', 'Cl'), 1/np.sqrt(2)),
                                (('Na', 'Na'), 1/np.sqrt(2)),
                                (('Cl', 'Na'), np.sqrt(3)/2),
                                (('Cl', 'Cl'), 1),
                                (('Na', 'Na'), 1)]
        shells = get_neighbor_shells(atoms, cutoff=1.05)
        self.assertEqual(len(shells), len(expected_nacl_shells))
        for shell, (types, dist) in zip(shells, expected_nacl_shells):
            self.assertEqual(shell.types, types)
            self.assertAlmostEqual(shell.distance, dist)

        # test case where two shells will be within 2*dist_tol
        dist_tol = 1e-5
        atoms = bulk('Al', a=1.0).repeat(3)
        atoms[0].x += 1.5 * dist_tol
        shells = get_neighbor_shells(atoms, cutoff=1.05, dist_tol=dist_tol)

    def test_prepare_structure(self):
        """ Test prepare_structure function. """

        atoms_ideal = bulk('Al').repeat(4)
        N = len(atoms_ideal)

        # with forces as arrays
        atoms = atoms_ideal.copy()
        atoms.rattle(0.1)
        forces_ref = np.random.random((N, 3))
        atoms.new_array('forces', forces_ref)
        atoms = prepare_structure(atoms, atoms_ideal)
        self.assertIn('displacements', atoms.arrays)
        np.testing.assert_almost_equal(atoms.arrays['forces'], forces_ref)
        np.testing.assert_almost_equal(atoms.positions, atoms_ideal.positions)

        # with forces as arrays, but atoms object is permutated
        atoms = atoms_ideal.copy()
        atoms.rattle(0.1)
        forces_ref = np.random.random((N, 3))
        atoms.new_array('forces', forces_ref)

        p = np.arange(0, N, 1)
        np.random.shuffle(p)
        atoms = atoms[p]

        atoms = prepare_structure(atoms, atoms_ideal)
        self.assertIn('displacements', atoms.arrays)
        np.testing.assert_almost_equal(atoms.arrays['forces'], forces_ref)
        np.testing.assert_almost_equal(atoms.positions, atoms_ideal.positions)

        # with SinglePointCalculator
        atoms = atoms_ideal.copy()
        atoms.rattle(0.1)
        forces_ref = np.random.random((N, 3))
        spc = SinglePointCalculator(atoms, forces=forces_ref)
        atoms.calc = spc
        atoms = prepare_structure(atoms, atoms_ideal)
        self.assertIn('displacements', atoms.arrays)
        np.testing.assert_almost_equal(atoms.arrays['forces'], forces_ref)
        np.testing.assert_almost_equal(atoms.positions, atoms_ideal.positions)

        # with calculator
        atoms = atoms_ideal.copy()
        atoms.rattle(0.1)
        calc = EMT()
        atoms = prepare_structure(atoms, atoms_ideal, calc=calc)
        self.assertIn('displacements', atoms.arrays)
        self.assertIn('forces', atoms.arrays)
        np.testing.assert_almost_equal(atoms.positions, atoms_ideal.positions)

        # With both calculator attached and forces as array and they are the same
        atoms = atoms_ideal.copy()
        atoms.rattle(0.1)
        forces_ref = np.random.random((N, 3))
        spc = SinglePointCalculator(atoms, forces=forces_ref)
        atoms.calc = spc
        atoms.set_array('forces', forces_ref)
        atoms = prepare_structure(atoms, atoms_ideal)
        self.assertIn('displacements', atoms.arrays)
        np.testing.assert_almost_equal(atoms.arrays['forces'], forces_ref)
        np.testing.assert_almost_equal(atoms.positions, atoms_ideal.positions)

        # With both calculator provided and forces as array and they are the same
        atoms = atoms_ideal.copy()
        atoms.rattle(0.1)
        atoms.calc = EMT()
        forces_ref = atoms.get_forces()
        atoms.calc = None
        atoms.set_array('forces', forces_ref)
        atoms = prepare_structure(atoms, atoms_ideal, calc=EMT())
        self.assertIn('displacements', atoms.arrays)
        np.testing.assert_almost_equal(atoms.arrays['forces'], forces_ref)
        np.testing.assert_almost_equal(atoms.positions, atoms_ideal.positions)

        # check that error is raised if two calculators are given
        atoms = atoms_ideal.copy()
        atoms.rattle(0.1)
        atoms.calc = EMT()
        atoms.get_forces()
        with self.assertRaises(ValueError):
            prepare_structure(atoms, atoms_ideal, calc=EMT())

        # check that error is raised if calculator attached and forces as array differ
        atoms = atoms_ideal.copy()
        atoms.rattle(0.1)
        forces_ref = np.random.random((N, 3))
        spc = SinglePointCalculator(atoms, forces=forces_ref)
        atoms.calc = spc
        atoms.set_array('forces', forces_ref + 0.1)
        with self.assertRaises(ValueError):
            prepare_structure(atoms, atoms_ideal)

        # check that error is raised if calculator provided and forces as array differ
        atoms = atoms_ideal.copy()
        atoms.rattle(0.1)
        atoms.calc = EMT()
        forces_ref = atoms.get_forces()
        atoms.calc = None
        atoms.set_array('forces', forces_ref + 0.1)
        with self.assertRaises(ValueError):
            prepare_structure(atoms, atoms_ideal, calc=EMT())

        # check that errors are raised if no forces are given
        atoms = atoms_ideal.copy()
        atoms.rattle(0.1)
        with self.assertRaises(ValueError):
            prepare_structure(atoms, atoms_ideal)

    def test_find_permutation(self):
        """ Test find_permutation function. """
        atoms_ideal = bulk('NaCl', 'rocksalt', a=5).repeat(2)

        # find permutation when atoms are wrapped through pbc
        atoms = atoms_ideal.copy()
        atoms.rattle(0.3, seed=42)
        atoms.wrap()
        p = find_permutation(atoms, atoms_ideal)
        self.assertEqual(p, sorted(p))

        # ValueError when two atoms are mapped to the same site
        atoms = atoms_ideal.copy()
        atoms[0].position = atoms[1].position.copy()
        atoms.rattle(0.3, seed=42)
        with self.assertRaises(Exception):
            find_permutation(atoms, atoms_ideal)

        # ValueError when atoms mapped to different species
        atoms = atoms_ideal.copy()
        atoms.wrap()
        atoms[0].position, atoms[1].position = atoms[1].position.copy(), atoms[0].position.copy()
        atoms.rattle(0.3, seed=42)
        with self.assertRaises(Exception):
            find_permutation(atoms, atoms_ideal)


if __name__ == '__main__':
    unittest.main()
