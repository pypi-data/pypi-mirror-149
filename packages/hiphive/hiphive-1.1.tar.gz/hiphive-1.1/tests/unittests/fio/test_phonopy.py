import numpy as np
import tempfile
import unittest

from ase.build import bulk
from hiphive import ClusterSpace
from hiphive.force_constant_model import ForceConstantModel
from hiphive.input_output.phonopy import read_phonopy_fc2, write_phonopy_fc2, \
                                         read_phonopy_fc3, write_phonopy_fc3, \
                                         _filename_to_format


class TestPhonopyIO(unittest.TestCase):
    """
    Unittest class for phonopy IO functionality..
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set up a dummy force constants
        prim = bulk('Ti')
        supercell = prim.repeat((4, 4, 2))
        cs = ClusterSpace(prim, [4.0, 4.0])
        parameters = np.random.normal(0.0, 1.0, (cs.n_dofs, ))
        fcm = ForceConstantModel(supercell, cs)
        fcm.parameters = parameters
        self.fcs = fcm.get_force_constants()
        self.fc2 = self.fcs.get_fc_array(order=2)
        self.fc3 = self.fcs.get_fc_array(order=3)

    def shortDescription(self):
        """ Prevents unittest from printing docstring in test cases."""
        return None

    def test_fc2(self):
        """ Test write/read for fc2. """

        for fc_input in [self.fcs, self.fc2]:
            # test read and write with text format
            temp_file = tempfile.NamedTemporaryFile()
            write_phonopy_fc2(temp_file.name, fc_input, format='text')
            fc2_read = read_phonopy_fc2(temp_file.name, format='text')
            np.testing.assert_almost_equal(fc2_read, self.fc2)

            # test read and write with hdf5 format
            temp_file = tempfile.NamedTemporaryFile()
            write_phonopy_fc2(temp_file.name, fc_input, format='hdf5')
            fc2_read = read_phonopy_fc2(temp_file.name, format='hdf5')
            np.testing.assert_almost_equal(fc2_read, self.fc2)

        # test that format=None correctly guesses the format
        temp_file = tempfile.NamedTemporaryFile(suffix='.hdf5')
        write_phonopy_fc2(temp_file.name, self.fc2)
        fc2_read = read_phonopy_fc2(temp_file.name)
        np.testing.assert_almost_equal(fc2_read, self.fc2)

        # test that erronoues format raises
        with self.assertRaises(ValueError):
            write_phonopy_fc2(temp_file.name, self.fc2, format='vasp')
        with self.assertRaises(ValueError):
            read_phonopy_fc2(temp_file.name, format='vasp')

        # test that np.array with erronoues shape raises
        with self.assertRaises(ValueError):
            write_phonopy_fc2(temp_file.name, self.fc3, format='text')

        # test that erronoues input raises error
        for fc_input in [self.fc2.tolist(), self.fcs.get_fc_dict()]:
            with self.assertRaises(TypeError):
                write_phonopy_fc2(temp_file.name, fc_input, format='text')

    def test_fc3(self):
        """ Test write/read for fc3. """

        # test read and write
        for fc_input in [self.fcs, self.fc3]:
            temp_file = tempfile.NamedTemporaryFile()
            write_phonopy_fc3(temp_file.name, fc_input)
            fc3_read = read_phonopy_fc3(temp_file.name)
            np.testing.assert_almost_equal(fc3_read, self.fc3)

        # test that np.array with erronoues shape raises
        with self.assertRaises(ValueError):
            write_phonopy_fc3(temp_file.name, self.fc2)

        # test that erronoues input type (list and dict) raises
        for fc_input in [self.fc2.tolist(), self.fcs.get_fc_dict()]:
            with self.assertRaises(TypeError):
                write_phonopy_fc3(temp_file.name, fc_input)

    def test_filename_to_format(self):
        """ Test filename_to_format functionality. """

        # identify text format
        self.assertEqual(_filename_to_format('FORCE_CONSTANTS'), 'text')

        # identify hdf5 format
        self.assertEqual(_filename_to_format('fc2.hdf5'), 'hdf5')
        self.assertEqual(_filename_to_format('qwerty1337.hdf5'), 'hdf5')
        self.assertEqual(_filename_to_format('asd/bsd/csd.hdf5'), 'hdf5')

        # files which can not be identified
        fnames = ['asd', 'fc2', 'fc3.pickle']
        for fname in fnames:
            with self.assertRaises(ValueError):
                _filename_to_format(fname)


if __name__ == '__main__':
    unittest.main()
