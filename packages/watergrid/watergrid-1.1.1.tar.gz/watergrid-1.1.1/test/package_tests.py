import unittest

import watergrid


class PackageTestCase(unittest.TestCase):
    def test_version(self):
        self.assertNotEqual(watergrid.__version__, "")


if __name__ == "__main__":
    unittest.main()
