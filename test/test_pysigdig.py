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

    def test_invalid(self) -> None:
        """Test constructor when an invalid data type is used as value."""
        with self.assertRaises(TypeError):
            pysigdig.Number([0, 1])

    def test_sigdig_override(self) -> None:
        """Check that number of sigdigs can be overridden with optional arg."""
        number = pysigdig.Number(1.0002003, sigdigs=5)
        self.assertAlmostEqual(number.value, 1.0002003)
        self.assertEqual(number.tolerance, None)
        self.assertEqual(number.sigdigs, 5)
        self.assertAlmostEqual(number.lsd, 1e-4)

    def test_lsd_override(self) -> None:
        """Check that the least significant digit can be overridden with
        optional argument."""
        number = pysigdig.Number(123.456789, lsd=0.001)
        self.assertAlmostEqual(number.value, 123.456789)
        self.assertEqual(number.tolerance, None)
        self.assertEqual(number.sigdigs, 6)
        self.assertAlmostEqual(number.lsd, 0.001)


if __name__ == '__main__':
    unittest.main()
