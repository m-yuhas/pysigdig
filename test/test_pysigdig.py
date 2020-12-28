"""Unit test cases for the _pysigdig module."""


import unittest
import pysigdig


class TestConstructor(unittest.TestCase):
    """Test the constructor for Number class."""

    def test_integer(self) -> None:
        """Test constructor when an integer is provided as value."""
        number = pysigdig.Number(1)
        self.assertEqual(number.value, 1)
        self.assertEqual(number.tolerance, None)
        self.assertEqual(number.sigdigs, 1)
        self.assertEqual(number.lsd, 1)

    def test_float(self) -> None:
        """Test constructor when a float is provided as value."""
        number = pysigdig.Number(1.2)
        self.assertAlmostEqual(number.value, 1.2)
        self.assertEqual(number.tolerance, None)
        self.assertEqual(number.sigdigs, float('inf'))
        self.assertEqual(number.lsd, float('-inf'))

    def test_string(self) -> None:
        """Test constructor when a string is provided as value."""
        number = pysigdig.Number('12.30')
        self.assertAlmostEqual(number.value, 12.3)
        self.assertEqual(number.tolerance, None)
        self.assertEqual(number.sigdigs, 4)
        self.assertAlmostEqual(number.lsd, 0.01)


if __name__ == '__main__':
    unittest.main()
