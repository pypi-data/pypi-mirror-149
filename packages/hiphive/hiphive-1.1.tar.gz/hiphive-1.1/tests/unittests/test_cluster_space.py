import unittest
import tempfile
import numpy as np
import sys

from ase.build import bulk
from hiphive import ClusterSpace
from hiphive.config import Config
from hiphive.cutoffs import Cutoffs, BaseClusterFilter
from io import StringIO


class TestClusterSpace(unittest.TestCase):
    """
    Unittest class for ClusterSpace.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prim = bulk('Al', 'fcc', a=4.05)
        self.cutoffs = [5.0]

    def shortDescription(self):
        """Prevents unittest from printing docstring in test cases."""
        return None

    def test_init_with_nonpbc(self):
        """ Tests that initializing ClusterSpace with non pbc structure fails. """

        # run with pbc
        ClusterSpace(self.prim, self.cutoffs)

        # all pbc false
        with self.assertRaises(ValueError):
            prim_tmp = self.prim.copy()
            prim_tmp.pbc = False
            ClusterSpace(prim_tmp, self.cutoffs)

        # pbc false in one direction
        with self.assertRaises(ValueError):
            prim_tmp = self.prim.copy()
            prim_tmp.pbc = [1, 0, 1]
            ClusterSpace(prim_tmp, self.cutoffs)

    def test_init_with_short_cutoff(self):
        """ Test that initializing ClusterSpace with a cutoff shorter than NN
        distance does not work if this is the only order. """

        atoms = bulk('Al', 'fcc', a=4.0).repeat(2)
        nn_distance = 2.8284271247461903
        cutoff = nn_distance - 1e-2

        # no third order orbits
        cs = ClusterSpace(atoms, [5.0, cutoff])
        self.assertEqual(cs.get_n_dofs_by_order(order=3), 0)

        # no second order dofs
        cs = ClusterSpace(atoms, [cutoff, 5.0])
        self.assertEqual(cs.get_n_dofs_by_order(order=2), 0)

        # no dofs at all
        with self.assertRaises(ValueError) as cm:
            cs = ClusterSpace(atoms, [cutoff])
        self.assertIn('There are no degrees of freedom', str(cm.exception))

    def test_init_with_with_cluster_filter(self):
        """ Test that initializing ClusterSpace with a primitive cell with
        positions close to edge of cell. """

        class MyFilter(BaseClusterFilter):
            def __call__(self, cluster):
                symbols = [self._atoms.get_chemical_symbols()[i] for i in cluster]
                return symbols.count('Na') != 2

        prim = bulk('NaCl', 'rocksalt', a=4.0)
        cf = MyFilter()
        cs = ClusterSpace(prim, [5.0], cluster_filter=cf)
        for orbit in cs.orbit_data:
            types = tuple(sorted(orbit['prototype_atom_types']))
            self.assertFalse(types == (11, 11))  # no (11, 11) Na-Na
            self.assertIn(types, [(11, 17), (17, 17)])

    def test_init_with_distance_close_to_cutoff(self):
        """ Test that initializing ClusterSpace with a cutoff that is close or
        identical to an interatomic distance raises.
        """

        # set up
        a = 4.0
        tol = 1e-10
        prim = bulk('Al', 'fcc', a=a)

        # Should raise Exeception for these cutoffs
        for cutoff in [a-tol, a, a+tol]:
            with self.assertRaises(Exception):
                ClusterSpace(prim, [cutoff])

        # Should not raise if there exists a larger cutoff
        for cutoff in [a-tol, a, a+tol]:
            ClusterSpace(prim, [5.0, cutoff])

    def test_init_with_cutoffs(self):
        """ Test that initializing ClusterSpace with Cutoffs object works. """
        # with cutoffs object
        cutoffs_obj = Cutoffs(np.array([[5.0, 5.0, 5.0], [4.0, 4.0, 4.0]]))
        ClusterSpace(self.prim, cutoffs_obj)

        # fail with non-list cutoffs
        cutoffs = (5.4, 4.35)
        with self.assertRaises(TypeError):
            ClusterSpace(self.prim, cutoffs)

    def test_init_with_different_settings(self):
        """ Test that initializing ClusterSpace with different settings works. """

        # with sum rules
        ClusterSpace(self.prim, [4.0], sum_rules=True)

        # without sum rules
        ClusterSpace(self.prim, [5.0, 5.0], acoustic_sum_rules=False)

        # with Config object
        conf = Config(acoustic_sum_rules=False)
        ClusterSpace(self.prim, [5.0, 5.0], config=conf)

        # fail with Config object and kwargs
        conf = Config(acoustic_sum_rules=False)
        with self.assertRaises(ValueError):
            ClusterSpace(self.prim, [5.0, 5.0], config=conf, symprec=1e-3)

        # check that ValueErrors are raised with bad kwargs
        with self.assertRaises(ValueError):
            ClusterSpace(self.prim, [5.0], rot=True)
        with self.assertRaises(TypeError):
            ClusterSpace(self.prim, [5.0], acoustic_sum_rules=[1, 2, 3])

    def test_print_tables(self):
        """ Test that print tables works. """
        cs = ClusterSpace(self.prim, [5.0, 5.0])
        with StringIO() as captured_output:
            sys.stdout = captured_output
            cs.print_tables()
            sys.stdout = sys.__stdout__
            self.assertIn('Cutoff Matrix', captured_output.getvalue())
            self.assertIn('Cluster counts', captured_output.getvalue())
            self.assertIn('Orbit counts', captured_output.getvalue())
            self.assertIn('Eigentensor counts', captured_output.getvalue())

    def test_print_orbits(self):
        """ Test that print orbits works. """
        cs = ClusterSpace(self.prim, self.cutoffs)
        with StringIO() as captured_output:
            sys.stdout = captured_output
            cs.print_orbits()
            sys.stdout = sys.__stdout__
            self.assertIn('List of Orbits', captured_output.getvalue())
            self.assertIn('Al Al        |  2.4801  |       (0, 2)',
                          captured_output.getvalue())

    def test_write_and_read(self):
        """ Test the write and read functionality. """
        cs = ClusterSpace(self.prim, self.cutoffs)

        # test with file object
        with tempfile.TemporaryFile() as file:
            cs.write(file)
            file.seek(0)
            cs_read = ClusterSpace.read(file)
            self.assertEqual(str(cs), str(cs_read))

        # test with file name
        with tempfile.NamedTemporaryFile() as file:
            cs.write(file.name)
            cs_read = ClusterSpace.read(file.name)
            self.assertEqual(str(cs), str(cs_read))
            self.assertEqual(str(cs.summary), str(cs_read.summary))

    def test_get_parameter_indices(self):
        """ Test the get_parameter_indices function. """
        cs2 = ClusterSpace(self.prim, [5.0])
        cs3 = ClusterSpace(self.prim, [5.0, 4.0])
        cs4 = ClusterSpace(self.prim, [5.0, 4.0, 4.0])

        inds2 = cs4.get_parameter_indices(order=2)
        inds3 = cs4.get_parameter_indices(order=3)
        inds4 = cs4.get_parameter_indices(order=4)

        # test that indices are increasing with order and correct number
        self.assertLess(max(inds2), min(inds3))
        self.assertLess(max(inds3), min(inds4))
        self.assertEqual(len(inds2+inds3+inds4), cs4.n_dofs)

        # test that correct indices are obtained
        self.assertSequenceEqual(inds2, range(cs2.n_dofs))
        self.assertSequenceEqual(inds2+inds3, range(cs3.n_dofs))
        self.assertSequenceEqual(inds2+inds3+inds4, range(cs4.n_dofs))

    def test_get_n_dofs_by_order(self):
        """ Test the get_n_dofs_by_order function. """
        cs2 = ClusterSpace(self.prim, [5.0])
        cs3 = ClusterSpace(self.prim, [5.0, 4.0])
        cs4 = ClusterSpace(self.prim, [5.0, 4.0, 4.0])

        n_dofs2 = cs2.n_dofs
        n_dofs3 = cs3.n_dofs - n_dofs2
        n_dofs4 = cs4.n_dofs - n_dofs3 - n_dofs2

        self.assertEqual(cs4.get_n_dofs_by_order(order=2), n_dofs2)
        self.assertEqual(cs4.get_n_dofs_by_order(order=3), n_dofs3)
        self.assertEqual(cs4.get_n_dofs_by_order(order=4), n_dofs4)

    def test_str(self):
        """ Test dunder str function. """
        cs = ClusterSpace(self.prim, [4.0, 2.0])
        s = str(cs)
        self.assertIsInstance(s, str)


if __name__ == '__main__':
    unittest.main()
