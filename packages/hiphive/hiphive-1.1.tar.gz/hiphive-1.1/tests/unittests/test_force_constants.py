import unittest
import tempfile
import numpy as np
import sys

from io import StringIO
from itertools import product, combinations_with_replacement
from ase.build import bulk
from hiphive import ClusterSpace, ForceConstantPotential, ForceConstants
from hiphive.force_constants import SortedForceConstants, RawForceConstants
from hiphive.force_constants import symbolize_force_constant,\
    array_to_dense_dict, check_label_symmetries, dense_dict_to_sparse_dict


def generate_random_force_constant(cluster, symmetric):
    """ Helper function for generating random force constant tensors. """
    shape = (3, ) * len(cluster)
    if symmetric:
        from hiphive.core.eigentensors import init_ets_from_label_symmetry
        fc = np.zeros(shape)
        for et in init_ets_from_label_symmetry(cluster):
            fc += et * np.random.random()
    else:
        fc = np.random.random((shape))
    return fc


class TestSortedForceConstants(unittest.TestCase):
    """
    Unittest class for SortedForceConstants.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # supercell
        self.supercell = bulk('Al', 'fcc', a=4.0).repeat((2, 2, 1))
        self.n_atoms = len(self.supercell)

        # setup dummy fc_dict
        self.pairs = list(combinations_with_replacement(range(self.n_atoms), r=2))
        self.triplets = list(combinations_with_replacement(range(self.n_atoms), r=3))
        fc_dict = dict()
        for cluster in self.pairs + self.triplets:
            fc_dict[cluster] = generate_random_force_constant(cluster, True)
        self.fc_dict = fc_dict

    def setUp(self):
        self.fcs = SortedForceConstants(self.fc_dict, self.supercell)

    def shortDescription(self):
        """ Prevents unittest from printing docstring in test cases. """
        return None

    def test_init(self):
        """ Test initializing SortedForceConstants. """

        # initialze with sorted fc_dict
        fcs = SortedForceConstants(self.fc_dict, self.supercell)
        self.assertIsInstance(fcs, ForceConstants)
        self.assertIsInstance(fcs, SortedForceConstants)

        # initialize with unsorted fc_dict
        fc_dict = self.fc_dict.copy()
        fc_dict[(1, 0)] = np.random.random((3, 3))
        with self.assertRaises(ValueError):
            SortedForceConstants(fc_dict, self.supercell)

        # initialize with cluster larger than number of atoms in supercell
        fc_dict = self.fc_dict.copy()
        fc_dict[0, self.n_atoms] = np.random.random((3, 3))
        with self.assertRaises(ValueError):
            SortedForceConstants(fc_dict, self.supercell)

        # initialize with negative cluster
        fc_dict = self.fc_dict.copy()
        fc_dict[-1, 0] = np.random.random((3, 3))
        with self.assertRaises(ValueError):
            SortedForceConstants(fc_dict, self.supercell)

        # without PBC
        fc_dict = self.fc_dict.copy()
        fc_dict[-1, 0] = np.random.random((3, 3))
        supercell = self.supercell.copy()
        supercell.pbc = [True, False, True]
        with self.assertRaises(ValueError):
            SortedForceConstants(fc_dict, supercell)

    def test_getitem(self):
        """ Test dunder getitem. """

        # pairs
        for pair in self.pairs:

            # check sorted pair
            fc_target = self.fc_dict[pair]
            np.testing.assert_almost_equal(self.fcs[pair], fc_target)

            # check transposed pair
            pair2 = tuple(reversed(pair))
            np.testing.assert_almost_equal(self.fcs[pair2], fc_target.T)

        # triplets
        for triplet in self.triplets:

            # check sorted triplet
            fc_target = self.fc_dict[triplet]
            np.testing.assert_almost_equal(self.fcs[triplet], fc_target)

            # TODO: check transposed triplet

    def test_orders_property(self):
        """ Test orders property. """
        self.assertEqual(self.fcs.orders, [2, 3])

    def test_read_write(self):
        """ Test read and write """
        fcs_file = tempfile.NamedTemporaryFile()
        self.fcs.write(fcs_file.name)

        fcs_read = SortedForceConstants.read(fcs_file.name)
        self.assertTrue(self.fcs == fcs_read)


class TestRawForceConstants(unittest.TestCase):
    """
    Unittest class for RawForceConstants.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # supercell
        self.supercell = bulk('Al', 'fcc', a=4.0).repeat((2, 2, 1))
        self.n_atoms = len(self.supercell)

        # setup dummy fc_dict
        self.pairs = list(product(range(self.n_atoms), repeat=2))
        self.triplets = list(product(range(self.n_atoms), repeat=3))
        fc_dict = dict()
        for pair in self.pairs:
            fc_dict[pair] = np.random.random((3, 3))
        for triplet in self.triplets:
            fc_dict[triplet] = np.random.random((3, 3, 3))

        self.fc_dict = fc_dict

    def setUp(self):
        self.fcs = RawForceConstants(self.fc_dict, self.supercell)

    def shortDescription(self):
        """ Prevents unittest from printing docstring in test cases. """
        return None

    def test_init(self):
        """ Test initializing RawForceConstants. """

        # initialze with fc_dict
        fcs = RawForceConstants(self.fc_dict, self.supercell)
        self.assertIsInstance(fcs, ForceConstants)
        self.assertIsInstance(fcs, RawForceConstants)

    def test_getitem(self):
        """ Test dunder getitem. """

        for cluster in self.pairs + self.triplets:
            fc_target = self.fc_dict[cluster]
            np.testing.assert_almost_equal(self.fcs[cluster], fc_target)

        self.fcs._fc_dict.pop((0, 0))
        np.testing.assert_almost_equal(self.fcs[(0, 0)], np.zeros((3, 3)))

    def test_orders_property(self):
        """ Test orders property. """
        self.assertEqual(self.fcs.orders, [2, 3])

    def test_read_write(self):
        """ Test read and write """
        fcs_file = tempfile.NamedTemporaryFile()
        self.fcs.write(fcs_file.name)

        fcs_read = ForceConstants.read(fcs_file.name)
        self.assertTrue(self.fcs == fcs_read)


class TestForceConstants(unittest.TestCase):
    """
    Unittest class for ForceConstants.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prim = bulk('Al', 'fcc')
        self.supercell = self.prim.repeat(4)
        self.n_atoms = len(self.supercell)

        cs2 = ClusterSpace(self.prim, [5.0])
        cs3 = ClusterSpace(self.prim, [5.0, 4.0])
        self.fcp2 = ForceConstantPotential(cs2, np.random.random(cs2.n_dofs))
        self.fcp3 = ForceConstantPotential(cs3, np.random.random(cs3.n_dofs))
        self.fcs2 = self.fcp2.get_force_constants(self.supercell)
        self.fcs3 = self.fcp3.get_force_constants(self.supercell)

    def shortDescription(self):
        """ Prevents unittest from printing docstring in test cases."""
        return None

    def test_get_fc_array(self):
        """ Test get_fc_array """

        # assert ValueError for unavaible orders
        not_available = set(range(10)) - set(self.fcs3.orders)
        for order in not_available:
            with self.assertRaises(ValueError):
                self.fcs3.get_fc_array(order=order)

        # check shape is ok for available orders
        for order in self.fcs3.orders:
            fc_array = self.fcs3.get_fc_array(order=order)
            target_shape = (self.n_atoms,) * order + (3,) * order
            self.assertSequenceEqual(fc_array.shape, target_shape)

        # different formats
        fc2 = self.fcs2.get_fc_array(order=2, format='phonopy')
        self.assertEqual(fc2.shape, (self.n_atoms, self.n_atoms, 3, 3))

        fc2 = self.fcs2.get_fc_array(order=2, format='ase')
        self.assertEqual(fc2.shape, (3 * self.n_atoms, 3 * self.n_atoms))

        with self.assertRaises(ValueError):
            self.fcs2.get_fc_array(order=3, format='ase')

        with self.assertRaises(ValueError):
            self.fcs2.get_fc_array(order=2, format='qwerty')

    def test_gc_fc_dict(self):
        """ Test get_fc_dict """

        # assert ValueError for unavaible orders
        not_available = set(range(10)) - set(self.fcs3.orders)
        for order in not_available:
            with self.assertRaises(ValueError):
                self.fcs3.get_fc_dict(order=order)

        # check that all returned force constants are of correct order
        for order in self.fcs3.orders:
            fc_dict = self.fcs3.get_fc_dict(order=order)
            for cluster in fc_dict.keys():
                self.assertEqual(len(cluster), order)

    def test_from_arrays(self):
        """ Test initalization via arrays. """

        supercell = self.prim.repeat(3)
        n_atoms = len(supercell)

        # raise if no arrays available
        with self.assertRaises(ValueError):
            ForceConstants.from_arrays(supercell)

        # raise if bad shape
        fc2_array = np.random.random((n_atoms, n_atoms+1, 3, 3))
        fc3_array = np.random.random((n_atoms, n_atoms, n_atoms, 3, 4, 3))
        with self.assertRaises(ValueError):
            ForceConstants.from_arrays(supercell, fc2_array=fc2_array)
        with self.assertRaises(ValueError):
            ForceConstants.from_arrays(supercell, fc3_array=fc3_array)

        # Unsorted arrays
        fc2_array = np.random.random((n_atoms, n_atoms, 3, 3))
        fc3_array = np.random.random((n_atoms, n_atoms, n_atoms, 3, 3, 3))

        fcs = ForceConstants.from_arrays(supercell, fc2_array, fc3_array)
        self.assertEqual(fcs.orders, [2, 3])

        pairs = [(0, 1), (5, 5), (2, 3), (4, 11)]
        triplets = [(0, 0, 0), (1, 2, 3), (11, 1, 18)]
        for pair in pairs:
            np.testing.assert_almost_equal(fc2_array[pair], fcs[pair])
        for triplet in triplets:
            np.testing.assert_almost_equal(fc3_array[triplet], fcs[triplet])

        fcs = ForceConstants.from_arrays(supercell, fc2_array)
        self.assertEqual(fcs.orders, [2])
        for pair in pairs:
            np.testing.assert_almost_equal(fc2_array[pair], fcs[pair])

        fcs = ForceConstants.from_arrays(supercell, fc3_array=fc3_array)
        self.assertEqual(fcs.orders, [3])
        for triplet in triplets:
            np.testing.assert_almost_equal(fc3_array[triplet], fcs[triplet])

        # Sorted arrays
        # TODO : Added sorted fc3_array
        fc2_array = np.zeros((self.n_atoms, self.n_atoms, 3, 3))
        for pair in combinations_with_replacement(range(self.n_atoms), r=2):
            pair2 = tuple(reversed(pair))
            fc2_pair = generate_random_force_constant(pair, True)
            fc2_array[pair] = fc2_pair
            fc2_array[pair2] = fc2_pair.T

        fcs = ForceConstants.from_arrays(self.supercell, fc2_array)
        self.assertEqual(fcs.orders, [2])
        self.assertIsInstance(fcs, SortedForceConstants)

    def test_len(self):
        """ Test dunder len """
        self.assertEqual(len(self.fcs2._fc_dict), len(self.fcs2))
        self.assertEqual(len(self.fcs3._fc_dict), len(self.fcs3))

    def test_add(self):
        """ Test dunder add """

        # setup third order fcs without any second order terms
        fc3_dict = self.fcs3.get_fc_dict(order=3)
        fcs3 = ForceConstants.from_sparse_dict(fc3_dict, self.supercell)

        # adding
        fcs2 = self.fcs2
        fcs23 = fcs2 + fcs3
        self.assertEqual(len(fcs23), len(fcs2)+len(fcs3))
        self.assertEqual(fcs23.orders, fcs2.orders+fcs3.orders)

        # check that force constants agree
        for pair in fcs2.clusters:
            np.testing.assert_almost_equal(fcs2[pair], fcs23[pair])
        for triplet in fcs3.clusters:
            np.testing.assert_almost_equal(fcs3[triplet], fcs23[triplet])

        # test for ValueError when two fcs are not compatible
        with self.assertRaises(ValueError):
            fcs2 + fc3_dict

        # overlapping orders
        with self.assertRaises(ValueError):
            fcs2 + fcs2

        # incompatible supercells
        fcs2._supercell.positions[0] += 0.1
        with self.assertRaises(ValueError):
            fcs2 + fcs3

    def test_print_force_constant(self):
        """ Test print_force_constant """
        with StringIO() as captured_output:
            sys.stdout = captured_output
            self.fcs2.print_force_constant(self.fcs2.clusters[0])
            self.fcs2.print_force_constant(self.fcs2.clusters[-1])
            self.fcs3.print_force_constant(self.fcs3.clusters[0])
            self.fcs3.print_force_constant(self.fcs3.clusters[-1])
            sys.stdout = sys.__stdout__

    def test_eq(self):
        """ Test dunder eq """

        # True for identical fcs
        fcs3_other = self.fcp3.get_force_constants(self.supercell)
        self.assertTrue(self.fcs3 == fcs3_other)

        # different orders
        self.assertFalse(self.fcs2 == self.fcs3)

        # small change in force constants
        fcs3_other._fc_dict[(0, 0)][0, 0] += 0.001
        self.assertFalse(self.fcs3 == fcs3_other)
        fcs3_other._fc_dict[(0, 0)][0, 0] -= 0.001
        self.assertTrue(self.fcs3 == fcs3_other)

        # different supercell
        supercell_large = self.prim.repeat((5, 4, 4))
        fcs2_other = self.fcp2.get_force_constants(supercell_large)
        self.assertFalse(self.fcs2 == fcs2_other)

        fcs2_other = self.fcp2.get_force_constants(self.fcs2.supercell)
        fcs2_other._supercell.positions[2] += 0.1
        self.assertFalse(self.fcs2 == fcs2_other)

        fcs2_other = self.fcp2.get_force_constants(self.fcs2.supercell)
        fcs2_other._supercell.cell[1, 1] += 0.01
        self.assertFalse(self.fcs2 == fcs2_other)

        fcs2_other = self.fcp2.get_force_constants(self.fcs2.supercell)
        fcs2_other._supercell.numbers[0] = 27
        self.assertFalse(self.fcs2 == fcs2_other)

    def test_str_repr(self):
        """ Test dunder str and dunder repr """
        retval = str(self.fcs3)
        self.assertIsInstance(retval, str)
        retval = repr(self.fcs3)
        self.assertIsInstance(retval, str)

    def test_compute_gamma_frequencies(self):
        """ Test compute_gamma_frequencies function. """
        freqs = self.fcs3.compute_gamma_frequencies()
        self.assertEqual(len(freqs), 3 * self.n_atoms)

    def test_assert_acoustic_sum_rules(self):
        """ Test assert_acoustic_sum_rules. """

        # check that assert sum rules passes
        self.fcs2.assert_acoustic_sum_rules()
        self.fcs3.assert_acoustic_sum_rules()

        # setup fc2 which violates sum rules
        fc2_dict = self.fcs3.get_fc_dict()
        fc2_dict[(0, 0)] += 0.01
        fcs = ForceConstants.from_sparse_dict(fc2_dict, self.supercell)

        # check assertion error is raised
        with self.assertRaises(AssertionError):
            fcs.assert_acoustic_sum_rules()

        # but not for third order
        fcs.assert_acoustic_sum_rules(order=3)

        # or for order 2 with large tol
        fcs.assert_acoustic_sum_rules(order=2, tol=0.1)

        # ValueError when order not available
        with self.assertRaises(ValueError):
            fcs.assert_acoustic_sum_rules(order=4)

    def test_read_write_phonopy(self):
        """ Test read and write phonopy/phono3py """

        supercell = self.fcs3.supercell
        fc2_file = tempfile.NamedTemporaryFile()
        fc3_file = tempfile.NamedTemporaryFile()

        self.fcs3.write_to_phonopy(fc2_file.name, format='hdf5')
        self.fcs3.write_to_phono3py(fc3_file.name)

        fc2 = ForceConstants.read_phonopy(supercell, fc2_file.name, format='hdf5')
        fc3 = ForceConstants.read_phono3py(supercell, fc3_file.name)
        fcs_read = fc2 + fc3

        # check supercell
        self.assertEqual(self.fcs3.supercell, fcs_read.supercell)
        self.assertEqual(len(self.fcs3), len(fcs_read))
        for c in self.fcs3.clusters:
            np.testing.assert_almost_equal(self.fcs3[c], fcs_read[c])

    def test_read_write_shengBTE(self):
        """ Test read and write shengBTE """

        supercell = self.fcs3.supercell
        fc3_file = tempfile.NamedTemporaryFile()

        self.fcs3.write_to_shengBTE(fc3_file.name, self.prim)
        fcs_read = ForceConstants.read_shengBTE(
            supercell, fc3_file.name, self.prim)

        # check supercell
        self.assertEqual(self.fcs3.supercell, fcs_read.supercell)
        self.assertEqual(len(self.fcs3.get_fc_dict(order=3)), len(fcs_read))
        for c in self.fcs3.get_fc_dict(order=3).keys():
            np.testing.assert_almost_equal(self.fcs3[c], fcs_read[c])


class TestForceConstantsHelpers(unittest.TestCase):
    """
    Unittest class for force constant helper functions
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.supercell = bulk('Al', 'fcc').repeat(4)
        self.n_atoms = len(self.supercell)

        cs2 = ClusterSpace(self.supercell, [5.0])
        fcp2 = ForceConstantPotential(cs2, np.random.random(cs2.n_dofs))
        self.fcs2 = fcp2.get_force_constants(self.supercell)

    def shortDescription(self):
        """ Prevents unittest from printing docstring in test cases."""
        return None

    def test_array_to_dense_dict(self):
        """ Test array_to_dense_dict """
        n = 10
        fc_array = np.random.random((n, n, n, 3, 3, 3))
        fc_dict = array_to_dense_dict(fc_array)

        for triplet in product(range(n), repeat=3):
            np.testing.assert_almost_equal(fc_array[triplet], fc_dict[triplet])

    def test_check_label_symmetries(self):
        """ Test check_label_symmetries """

        # setup dense fc dict with label symmetries
        clusters = [(0, 1), (2, 5), (3, 4), (3, 5)]
        fc_dense = dict()
        for cluster in clusters:
            fc = np.random.random((3, 3))
            fc_dense[cluster] = fc
            fc_dense[tuple(reversed(cluster))] = fc.T.copy()

        # label symmetry is ok
        self.assertEqual(check_label_symmetries(fc_dense), True)

        # destroy label symmetry
        fc_dense[(1, 0)][0, 1] += 0.001
        self.assertEqual(check_label_symmetries(fc_dense), False)

    def test_dense_dict_to_sparse_dict(self):
        """ Test dense_dict_to_sparse_dict """

        # setup dense fc dict with label symmetries
        clusters = [(0, 1), (2, 5), (3, 4), (3, 5)]
        fc_dense = dict()
        for cluster in clusters:
            fc = np.random.random((3, 3))
            fc_dense[cluster] = fc
            fc_dense[tuple(reversed(cluster))] = fc.T.copy()

        # check that sparse dict have all the correct information
        fc_sparse = dense_dict_to_sparse_dict(fc_dense)
        self.assertEqual(len(fc_sparse), len(clusters))
        for c in clusters:
            np.testing.assert_almost_equal(fc_sparse[c], fc_dense[c])

    def test_symbolize_force_constants(self):
        """ Test symbolize_force_constant function. """

        # test with diagonal second order fc
        fc2 = np.array([[2.2, 0, 0], [0, 2.2, 0], [0, 0, 2.2]])
        fc2_sym = symbolize_force_constant(fc2)
        for i in range(3):
            # diagonal elements
            self.assertEqual('a', fc2_sym[i][i])
            for j in set(range(3))-set([i]):
                # off diagonal elements
                self.assertEqual(0, fc2_sym[i][j])

        # test with negative value
        fc2 = np.array([[1, 2, 3], [0, 0, 0], [-1, -2, -3]])
        fc2_sym = symbolize_force_constant(fc2)
        for i in range(3):
            self.assertEqual('-' + fc2_sym[0][i], fc2_sym[2][i])
            self.assertEqual(0, fc2_sym[1][i])


if __name__ == '__main__':
    unittest.main()
