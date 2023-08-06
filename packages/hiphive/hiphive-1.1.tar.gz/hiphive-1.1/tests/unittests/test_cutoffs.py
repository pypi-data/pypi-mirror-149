import unittest
import numpy as np

from ase.build import bulk
from hiphive.cutoffs import Cutoffs, estimate_maximum_cutoff, is_cutoff_allowed


class TestCutoffs(unittest.TestCase):
    """
    Unittest class for cutoffs.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cm = [[6.0, 6.0, 6.0, 5.0, 5.0],
                   [0.0, 5.0, 4.0, 3.0, 2.0],
                   [0.0, 0.0, 4.0, 3.0, 0.0]]

    def shortDescription(self):
        """ Prevents unittest from printing docstring in test cases. """
        return None

    def test_estimate_maximum_cutoff(self):
        """
        Test estimate maximum cutoff function
        """

        # precision of estimated maximum cutoff
        tol = 1e-3

        # Simple cubic 3x3x3, theoretical max_cutoff is 2.0
        atoms = bulk('Al', 'sc', a=1.0, cubic=True).repeat(3)
        maximum_cutoff = 2.0

        # Find maximum cutoff
        estimated_maximum_cutoff = estimate_maximum_cutoff(atoms)
        self.assertLess(estimated_maximum_cutoff, maximum_cutoff)
        self.assertLess(abs(maximum_cutoff - estimated_maximum_cutoff), tol)

        # Make sure is_cutoff_allowed works correctly
        allowed_cutoffs = np.linspace(0.0, maximum_cutoff - tol, 15)
        nonallowed_cutoffs = np.linspace(maximum_cutoff + tol, 4 * maximum_cutoff, 15)

        for c in allowed_cutoffs:
            self.assertTrue(is_cutoff_allowed(atoms, c))
        for c in nonallowed_cutoffs:
            self.assertFalse(is_cutoff_allowed(atoms, c))

    def test_str_repr(self):
        """ Test dunder str and dunder repr """
        cutoffs = Cutoffs(self.cm)
        self.assertIsInstance(str(cutoffs), str)
        self.assertIsInstance(repr(cutoffs), str)

    def test_to_filename_tag(self):
        """ Test to_filename_tag function """
        cutoffs = Cutoffs(self.cm)
        tag = cutoffs.to_filename_tag()
        self.assertIsInstance(tag, str)
        self.assertNotIn(' ', tag)


if __name__ == '__main__':
    unittest.main()
