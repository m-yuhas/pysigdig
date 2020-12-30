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
        number = pysigdig.Number(123.456789, sigdigs=90, lsd=0.001)
        self.assertAlmostEqual(number.value, 123.456789)
        self.assertEqual(number.tolerance, None)
        self.assertEqual(number.sigdigs, 6)
        self.assertAlmostEqual(number.lsd, 0.001)

    def test_tolerance(self) -> None:
        """Check that a tolerance can be added when calling the
        constructor."""
        number = pysigdig.Number(84000, tolerance=10)
        self.assertAlmostEqual(number.value, 84000)
        self.assertEqual(number.tolerance, 10)
        self.assertEqual(number.sigdigs, 2)
        self.assertEqual(number.lsd, 1000)


class TestIntegerCast(unittest.TestCase):
    """Test case for cast to integer."""

    def test_cast_to_int(self) -> None:
        """Test a cast to integer."""
        number = pysigdig.Number('3600')
        self.assertEqual(int(number), 3600)


class TestFloatCast(unittest.TestCase):
    """Test case for cast to float."""

    def test_cast_to_float(self) -> None:
        """Test a cast to float."""
        number = pysigdig.Number('45.6900')
        self.assertAlmostEqual(float(number), 45.69)


class TestStringCast(unittest.TestCase):
    """Test case for cast to string."""

    def test_trailing_zeros(self) -> None:
        """Test string cast on number with significant trailing zeros."""
        number = pysigdig.Number('1234.567890')
        self.assertEqual(str(number), '1234.567890')

    def test_no_trailing_zeros(self) -> None:
        """Test string cast on number with no trailing zeros."""
        number = pysigdig.Number('1234.56789')
        self.assertEqual(str(number), '1234.56789')

    def test_no_fractional_part(self) -> None:
        """Test string cast on number with no fractional part."""
        number = pysigdig.Number('64000')
        self.assertEqual(str(number), '64000')

    def test_with_tolerance(self) -> None:
        """Test string cast on number with tolerance."""
        number = pysigdig.Number('1.23450000', tolerance=0.01)
        self.assertEqual(str(number), '1.23450000 ± 0.01')


if __name__ == '__main__':
    unittest.main()
