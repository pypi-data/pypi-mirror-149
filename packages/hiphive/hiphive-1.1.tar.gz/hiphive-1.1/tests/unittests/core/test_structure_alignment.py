import unittest
from ase.build import bulk
from hiphive.core.structure_alignment import _assert_structures_match


class TestStructureAlignment(unittest.TestCase):
    """ Unittest class for utility functions. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def shortDescription(self):
        """Prevents unittest from printing docstring in test cases."""
        return None

    def test_assert_structures_match(self):
        """ Multiple tests for relate_structures function """

        atoms = bulk('Al').repeat(3)

        # different num atoms
        atoms2 = atoms.copy()
        atoms2.append(atoms2[0])
        with self.assertRaises(ValueError):
            _assert_structures_match(atoms, atoms2)

        # different symbols
        atoms2 = atoms.copy()
        atoms2.numbers[0:4] = 27
        with self.assertRaises(ValueError):
            _assert_structures_match(atoms, atoms2)

        # different symbols
        atoms2 = atoms.copy()
        atoms2.set_cell(atoms2.cell * 1.01)
        with self.assertRaises(ValueError):
            _assert_structures_match(atoms, atoms2)


if __name__ == '__main__':
    unittest.main()
