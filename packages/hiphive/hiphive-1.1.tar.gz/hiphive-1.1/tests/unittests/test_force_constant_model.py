import numpy as np
import tempfile
import unittest
from ase.build import bulk
from hiphive import ClusterSpace
from hiphive.force_constant_model import ForceConstantModel


class TestForceConstantPotential(unittest.TestCase):
    """
    Unittest class for ForceConstantModel.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # setup ClusterSpace
        cutoffs = [5.0]
        prim = bulk('Ti')
        cs = ClusterSpace(prim, cutoffs)
        parameters = np.arange(cs.n_dofs)

        self.prim = prim
        self.supercell = prim.repeat(4)
        self.cs = cs
        self.parameters = parameters

    def setUp(self):
        """ Create a ForceConstantModel. """
        self.fcm = ForceConstantModel(self.supercell, self.cs)
        self.fcm.parameters = self.parameters

    def test_write_and_read(self):
        """
        Test the write and read functionality.
        """

        # test with file object
        with tempfile.TemporaryFile() as file:
            self.fcm.write(file)
            file.seek(0)
            fcm_read = ForceConstantModel.read(file)
            np.testing.assert_almost_equal(self.fcm.parameters,
                                           fcm_read.parameters)
            self.assertEqual(self.fcm.atoms, fcm_read.atoms)

        # test with file name
        with tempfile.NamedTemporaryFile() as file:
            self.fcm.write(file.name)
            fcm_read = ForceConstantModel.read(file.name)
            np.testing.assert_almost_equal(self.fcm.parameters,
                                           fcm_read.parameters)
            self.assertEqual(self.fcm.atoms, fcm_read.atoms)


if __name__ == '__main__':
    unittest.main()
