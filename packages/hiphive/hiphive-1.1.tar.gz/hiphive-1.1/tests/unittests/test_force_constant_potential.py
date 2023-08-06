import numpy as np
import tempfile
import unittest

from itertools import product
from ase.build import bulk
from hiphive import ClusterSpace, ForceConstantPotential, ForceConstants


class TestForceConstantPotential(unittest.TestCase):
    """
    Unittest class for ForceConstantPotential.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # setup ClusterSpace
        cutoffs = [5.0]
        prim = bulk('Ti')
        cs = ClusterSpace(prim, cutoffs)
        parameters = np.arange(cs.n_dofs)

        self.prim = prim
        self.cs = cs
        self.parameters = parameters

    def shortDescription(self):
        """Prevents unittest from printing docstring in test cases."""
        return None

    def setUp(self):
        """ Create a ForceConstantPotential. """
        self.fcp = ForceConstantPotential(self.cs, self.parameters)

    def test_write_and_read(self):
        """ Test the write and read functionality. """

        # test with file name
        with tempfile.NamedTemporaryFile() as file:
            self.fcp.write(file.name)
            fcp_read = ForceConstantPotential.read(file.name)
            self.assertEqual(str(self.fcp), str(fcp_read))
            self.assertEqual(str(self.fcp.cs_summary), str(fcp_read.cs_summary))

        # assert write raise with non-string input
        with tempfile.TemporaryFile() as file:
            with self.assertRaises(ValueError):
                self.fcp.write(file)

        # assert read raise with non-string input
        with tempfile.NamedTemporaryFile() as file:
            self.fcp.write(file.name)
            with self.assertRaises(ValueError):
                fcp_read = ForceConstantPotential.read(file)

    def test_old_write_and_read(self):
        """ Test the old (pickle) write and read functionality. """

        with tempfile.NamedTemporaryFile() as file:
            self.fcp._write_old(file.name)
            fcp_read = ForceConstantPotential.read(file.name)
            self.assertEqual(str(self.fcp), str(fcp_read))

    def test_orbit_data(self):
        """ Test orbit_data property """
        orbit_data = self.fcp.orbit_data
        self.assertEqual(len(orbit_data), len(self.fcp.orbits))
        for orb in orbit_data:
            self.assertIsInstance(orb, dict)

    def test_get_force_constants(self):
        """ Test get_force_constants """

        # test that return type is ForceConstants
        supercell = self.prim.repeat(3)
        fcs = self.fcp.get_force_constants(supercell)
        self.assertIsInstance(fcs, ForceConstants)

        # test basic properties of cs
        for i, j in product(range(len(supercell)), repeat=2):
            fc_ij = fcs[(i, j)]
            fc_ji = fcs[(j, i)]
            np.testing.assert_almost_equal(fc_ij, fc_ji.T)

    def test_str(self):
        """ Test dunder str. """
        self.assertIsInstance(str(self.fcp), str)

    def test_repr(self):
        """ Test dunder repr. """
        self.assertIsInstance(repr(self.fcp), str)

    def test_property_metadata(self):
        """ Test get metadata method. """

        user_metadata = dict(parameters=[1, 2, 3], fit_method='ardr')
        fcp = ForceConstantPotential(self.cs, self.parameters, metadata=user_metadata)
        metadata = fcp.metadata

        # check for user metadata
        self.assertIn('parameters', metadata.keys())
        self.assertIn('fit_method', metadata.keys())

        # check for default metadata
        self.assertIn('date_created', metadata.keys())
        self.assertIn('username', metadata.keys())
        self.assertIn('hostname', metadata.keys())
        self.assertIn('hiphive_version', metadata.keys())


if __name__ == '__main__':
    unittest.main()
