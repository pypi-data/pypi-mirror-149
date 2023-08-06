import unittest

from hiphive.core.atoms import Atom


class AtomTest(unittest.TestCase):

    def setUp(self):
        self.site = 5
        self.offset = (1, 3, 4)
        self.atom = Atom(self.site, self.offset)

    def test_site(self):
        self.assertEqual(self.site, self.atom.site)

    def test_offset(self):
        self.assertEqual(self.offset, self.atom.offset)


if __name__ == '__main__':
    unittest.main()
