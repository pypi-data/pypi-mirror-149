import numpy as np
import tempfile
import unittest

from hiphive.core.orbits import Orbit, OrientationFamily


class TestStructureOrbit(unittest.TestCase):
    """
    Unittest class for Orbit.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # generate dummy OrientationFamilies
        self.orientation_families = []
        for i in range(10):
            of = OrientationFamily(i)
            of.cluster_indices = [2*i, 2*i+1]
            of.permutation_indices = [3*i, 4*i]
            self.orientation_families.append(of)

        # generate random matrices as third order eigentensors
        self.eigentensors = []
        for _ in range(5):
            self.eigentensors.append(np.random.randint(0, 10, (3, 3, 3)))

        # generate eigensymmetry indices
        self.eigensymmetries = []
        for _ in range(3):
            self.eigensymmetries.append(tuple(np.random.randint(0, 48, (2,))))

        self.order, self.radius, self.max_dist = 3, 2.25, 3.8

    def setUp(self):
        """ Create an Orbit. """
        orbit = Orbit()
        orbit.orientation_families = self.orientation_families
        orbit.eigensymmetries = self.eigensymmetries
        orbit.eigentensors = self.eigentensors
        orbit.order = self.order
        orbit.radius = self.radius
        orbit.maximum_distance = self.max_dist
        self.orbit = orbit

    def test_write_and_read(self):
        """
        Test the write and read functionality.
        """

        # write
        temp_file = tempfile.TemporaryFile()
        self.orbit.write(temp_file)

        # read
        temp_file.seek(0)
        orbit_read = Orbit.read(temp_file)

        # check eigentensors
        for et1, et2 in zip(self.orbit.eigentensors, orbit_read.eigentensors):
            np.testing.assert_almost_equal(et1, et2)

        # check eigensymmetries
        for es1, es2 in zip(self.orbit.eigensymmetries,
                            orbit_read.eigensymmetries):
            self.assertSequenceEqual(es1, es2)

        # check attributes
        self.assertEqual(self.orbit.order, orbit_read.order)
        self.assertEqual(self.orbit.radius, orbit_read.radius)
        self.assertEqual(self.orbit.maximum_distance,
                         orbit_read.maximum_distance)

        # check orientation families
        for of1, of2 in zip(self.orbit.orientation_families,
                            orbit_read.orientation_families):
            self.assertEqual(of1.symmetry_index, of2.symmetry_index)
            self.assertSequenceEqual(of1.cluster_indices, of2.cluster_indices)
            self.assertSequenceEqual(of1.permutation_indices,
                                     of2.permutation_indices)


if __name__ == '__main__':
    unittest.main()
