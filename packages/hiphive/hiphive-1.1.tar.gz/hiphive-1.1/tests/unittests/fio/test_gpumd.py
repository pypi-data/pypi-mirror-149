import numpy as np
import tempfile
import unittest

from ase.build import bulk
from hiphive import ClusterSpace
from hiphive.force_constant_model import ForceConstantModel
from hiphive.input_output.gpumd import write_fcp_txt, write_r0, _get_lookup_data_naive, \
    _get_lookup_data_smart


class TestGPUMDIO(unittest.TestCase):
    """
    Unittest class for GPUMD IO functionality..
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set up a dummy force constants
        prim = bulk('Ti')
        self.supercell = prim.repeat((4, 4, 2))
        cs = ClusterSpace(prim, [4.0, 4.0, 4.0], acoustic_sum_rules=False)
        parameters = np.exp(-np.arange(0, cs.n_dofs))
        fcm = ForceConstantModel(self.supercell, cs)
        fcm.parameters = parameters
        self.fcs = fcm.get_force_constants()

    def shortDescription(self):
        """ Prevents unittest from printing docstring in test cases."""
        return None

    def test_write_fcs_gpumd(self):
        """ Tests write_fcs_gpumd function. """

        # check if writing function works without failure
        for order in self.fcs.orders:
            f1 = tempfile.NamedTemporaryFile()
            f2 = tempfile.NamedTemporaryFile()
            self.fcs.write_to_GPUMD(f1.name, f2.name, order=order)

    def test_write_fcp_txt(self):
        """ Tests that write_fcp_txt runs without failure. """
        temp_file = tempfile.NamedTemporaryFile()
        write_fcp_txt(temp_file.name, 'path/to/fcs/', n_types=2, max_order=4)

    def test_write_r0(self):
        """ Tests that write_r0 runs without failure. """
        temp_file = tempfile.NamedTemporaryFile()
        write_r0(temp_file.name, self.supercell)

    def test_get_lookup_data(self):
        """ Tests get_lookup_data function. """
        tol = 1e-4

        for order in self.fcs.orders:
            clusters = [c for c in self.fcs._fc_dict.keys() if len(c) == order]
            c1, f1 = _get_lookup_data_naive(self.fcs, order, tol)
            c2, f2 = _get_lookup_data_smart(self.fcs, order, tol)

            # compare methods
            self.assertEqual(len(c1), len(c2))
            self.assertEqual(len(f1), len(f2))

            # compare with reference
            for cluster_lookup, fc_lookup in zip([c1, c2], [f1, f2]):
                for c in clusters:
                    fc_ref = self.fcs[c]
                    if c not in cluster_lookup:
                        self.assertLess(np.linalg.norm(fc_ref), tol)
                    else:
                        fc = fc_lookup[cluster_lookup[c]]
                        self.assertLess(np.linalg.norm(fc - fc_ref), tol)


if __name__ == '__main__':
    unittest.main()
