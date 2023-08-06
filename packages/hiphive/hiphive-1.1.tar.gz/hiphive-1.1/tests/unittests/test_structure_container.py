import numpy as np
import tempfile
import unittest

from ase.build import bulk
from ase.calculators.singlepoint import SinglePointCalculator
from ase.calculators.emt import EMT
from hiphive import ClusterSpace, StructureContainer
from hiphive.force_constant_model import ForceConstantModel
from hiphive.structure_container import FitStructure, are_configurations_equal


class TestStructureContainer(unittest.TestCase):
    """
    Unittest class for StructureContainer.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # setup ClusterSpace
        cutoffs = [5.0]
        prim = bulk('Al', 'fcc', a=4.05)
        self.cs = ClusterSpace(prim, cutoffs)

        # setup supercells
        supercell = prim.repeat(4)
        self.rand_fit_matrix = np.random.random(
            (len(supercell)*3, self.cs.n_dofs))
        calc = EMT()
        rattled_structures = []
        for i in range(7):
            atoms = supercell.copy()
            atoms.calc = calc
            atoms.rattle(0.05, seed=i)
            forces = atoms.get_forces()
            displacements = atoms.positions - supercell.positions
            atoms.positions = supercell.get_positions()
            atoms.calc = None
            atoms.new_array('displacements', displacements)
            atoms.new_array('forces', forces)
            rattled_structures.append(atoms)
        self.rattled_structures = rattled_structures

    def setUp(self):
        """ Create an empty StructureContainer. """
        self.sc = StructureContainer(self.cs)

    def test_init(self):
        """
        Test initializing StructureContainer.
        """
        # empty
        sc = StructureContainer(self.cs)
        self.assertIsInstance(sc, StructureContainer)

        # with FitStructures
        M = self.rand_fit_matrix
        fs_list = [FitStructure(atoms, M) for atoms in self.rattled_structures]
        sc = StructureContainer(self.cs, fs_list)
        self.assertIsInstance(sc, StructureContainer)

    def test_len(self):
        """
        Test dunder len.
        """
        for structure in self.rattled_structures:
            self.sc.add_structure(structure)
            self.assertEqual(len(self.sc), len(self.sc._structure_list))

    def test_getitem(self):
        """
        Test dunder getitem.
        """
        for i, structure in enumerate(self.rattled_structures):
            self.sc.add_structure(structure)
        for i, structure in enumerate(self.rattled_structures):
            fs = self.sc[i]
            self.assertEqual(fs.atoms, structure)

    def test_data_shape(self):
        """
        Test data_shape property.
        """
        structure = self.rattled_structures[0]
        self.assertIsNone(self.sc.data_shape)
        self.sc.add_structure(structure)
        target_shape = (3 * len(structure), self.cs.n_dofs)
        self.assertEqual(self.sc.data_shape, target_shape)

    def test_cluster_space(self):
        """
        Test cluster_space property.
        """
        self.assertEqual(str(self.sc.cluster_space), str(self.cs))

    def test_write_and_read(self):
        """
        Test the write and read functionality.
        """

        # save and read empty structure container
        temp_file = tempfile.TemporaryFile()
        self.sc.write(temp_file)
        temp_file.seek(0)
        sc_read = StructureContainer.read(temp_file)
        self.assertEqual(str(self.sc._cs), str(sc_read._cs))
        self.assertIsNone(sc_read._previous_fcm)
        temp_file.close()

        # save with structures
        temp_file = tempfile.TemporaryFile()
        for i, structure in enumerate(self.rattled_structures):
            self.sc.add_structure(structure)
        self.sc.write(temp_file)

        # read with fit matrices
        temp_file.seek(0)
        sc_read = StructureContainer.read(temp_file)
        self.assertIsInstance(sc_read._previous_fcm, ForceConstantModel)

        # check
        self.assertEqual(str(sc_read), str(self.sc))
        M, f = self.sc.get_fit_data()
        M_read, f_read = sc_read.get_fit_data()
        np.testing.assert_almost_equal(M, M_read)
        np.testing.assert_almost_equal(f, f_read)

        # read without structures
        temp_file.seek(0)
        sc_read = StructureContainer.read(temp_file, read_structures=False)
        temp_file.close()
        self.assertEqual(str(self.sc._cs), str(sc_read._cs))
        self.assertIsNone(sc_read.data_shape)

    def test_add_structure(self):
        """
        Test add_structure functionality.
        """

        # ignore if no displacements
        structure = self.rattled_structures[0].copy()
        structure.set_array('displacements', None)
        with self.assertRaises(ValueError) as cm:
            self.sc.add_structure(structure)
        self.assertIn('Atoms must have displacements array', str(cm.exception))

        # ignore if no forces
        structure = self.rattled_structures[0].copy()
        structure.set_array('forces', None)
        with self.assertRaises(ValueError) as cm:
            self.sc.add_structure(structure)
        self.assertIn('Atoms must have forces', str(cm.exception))

        # Adding with SinglePointCalculator
        structure = self.rattled_structures[0].copy()
        forces = structure.get_array('forces')
        structure.set_array('forces', None)  # delete forces array
        calc = SinglePointCalculator(structure, forces=forces)
        structure.calc = calc
        self.sc.add_structure(structure)
        self.assertEqual(len(self.sc._structure_list), 1)

        # ignore duplicates
        structure = self.rattled_structures[0].copy()
        with self.assertRaises(ValueError) as cm:
            self.sc.add_structure(structure)
        self.assertIn('Atoms is identical to structure', str(cm.exception))

        # add structures with different E_pot (meta data)
        self.sc.delete_all_structures()
        for i, structure in enumerate(self.rattled_structures):
            self.sc.add_structure(structure, E_pot=i)
        self.assertEqual([fs.E_pot for fs in self.sc].count(0), 1)

    def test_delete_all_structures(self):
        """
        Test delete_all_structures functionality.
        """
        # add structures
        for structure in self.rattled_structures:
            self.sc.add_structure(structure)
        self.assertEqual(len(self.sc), len(self.rattled_structures))

        # remove structures
        self.sc.delete_all_structures()
        self.assertEqual(len(self.sc), 0)

    def test_get_fit_data(self):
        """
        Test get fit data.
        """

        # get fit data from empty StructureContainer
        self.assertIsNone(self.sc.get_fit_data())

        # add structures
        for structure in self.rattled_structures:
            self.sc.add_structure(structure)

        # get partial fit data
        partial_indices = [0, 3]
        target_n_rows = 3 * len(structure) * len(partial_indices)
        M_partial, f_partial = self.sc.get_fit_data(partial_indices)
        self.assertEqual(M_partial.shape[0], target_n_rows)
        self.assertEqual(f_partial.shape[0], target_n_rows)

        # get all fit data (default behaviour)
        target_n_rows = 3 * len(structure) * len(self.rattled_structures)
        M_full, f_full = self.sc.get_fit_data()
        self.assertEqual(M_full.shape[0], target_n_rows)
        self.assertEqual(f_full.shape[0], target_n_rows)

    def test_str(self):
        """
        Test dunder str.
        """
        self.assertIsInstance(str(self.sc), str)

    def test_repr(self):
        """
        Test dunder repr.
        """
        self.assertIsInstance(repr(self.sc), str)

    def test_are_configurations_equal(self):
        """
        Test the helper function are_configurations_equal
        """

        # set up atoms objects
        atoms1 = bulk('Al', 'fcc', a=4.05).repeat((3, 2, 1))
        atoms1.new_array('forces', np.random.random((len(atoms1), 3)))
        atoms2 = atoms1.copy()

        # check that they are equal
        self.assertTrue(are_configurations_equal(atoms1, atoms2))

        # False when pbc is changed
        atoms2_copy = atoms2.copy()
        atoms2_copy.pbc = [False, True, True]
        self.assertFalse(are_configurations_equal(atoms1, atoms2_copy))

        # False when cell is changed
        atoms2_copy = atoms2.copy()
        atoms2_copy.cell[1][2] += 0.1
        self.assertFalse(are_configurations_equal(atoms1, atoms2_copy))

        # False when different number of arrays
        atoms2_copy = atoms2.copy()
        atoms2_copy.new_array('arr', np.random.random((len(atoms2_copy), 3)))
        self.assertFalse(are_configurations_equal(atoms1, atoms2_copy))

        # False when different named arrays
        atoms2_copy = atoms2.copy()
        atoms2_copy.set_array('forces', None)  # delete array
        atoms2_copy.new_array('arr', np.random.random((len(atoms2_copy), 3)))
        self.assertFalse(are_configurations_equal(atoms1, atoms2_copy))


class TestFitStructure(unittest.TestCase):
    """
    Unittest class for FitStructure.

    FitStructure will implicitly be tested from the StructureContainer tests.
    """

    def setUp(self):
        self.atoms = bulk('Al', 'fcc', a=4.05).repeat((3, 2, 1))
        self.atoms.set_array('displacements', np.random.random((len(self.atoms), 3)))
        self.atoms.set_array('forces', np.random.random((len(self.atoms), 3)))
        self.fit_matrix = np.random.random((len(self.atoms)*3, 50))
        self.meta_data = dict(tag='123')
        self.fs = FitStructure(self.atoms, self.fit_matrix, **self.meta_data)

    def test_str(self):
        """
        Test dunder str.
        """
        self.assertIsInstance(str(self.fs), str)

    def test_repr(self):
        """
        Test dunder repr.
        """
        self.assertIsInstance(repr(self.fs), str)

    def test_getattr(self):
        """
        Test custom getattr function.
        """
        meta_data = dict(E_pot=2.123, dft_code='vasp', c=[0.5, 0.5])
        fs = FitStructure(self.atoms, self.fit_matrix, **meta_data)

        # test the function call
        for key, val in meta_data.items():
            self.assertEqual(fs.__getattr__(key), val)

        # test accessing meta_data as an attribute
        self.assertEqual(fs.E_pot, meta_data['E_pot'])
        self.assertEqual(fs.dft_code, meta_data['dft_code'])
        self.assertEqual(fs.c, meta_data['c'])

        # test regular attribute call
        fs._atoms
        with self.assertRaises(AttributeError):
            fs.hello_world


if __name__ == '__main__':
    unittest.main()
