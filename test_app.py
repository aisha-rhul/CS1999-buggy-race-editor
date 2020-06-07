import unittest

import app


class TestNumerics(unittest.TestCase):
    def test_validate_integer(self):
        self.assertEqual(app.validate_integer(5, 3), True)
        self.assertEqual(app.validate_integer(4, 4), True)
        self.assertEqual(app.validate_integer(3, 4), False)


if __name__ == '__main__':
    unittest.main()
