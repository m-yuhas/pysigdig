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
        self.assertAlmostEqual(number.value, 1.0002)
        self.assertEqual(number.tolerance, None)
        self.assertEqual(number.sigdigs, 5)
        self.assertAlmostEqual(number.lsd, 1e-4)

    def test_lsd_override(self) -> None:
        """Check that the least significant digit can be overridden with
        optional argument."""
        number = pysigdig.Number(123.456789, sigdigs=90, lsd=0.001)
        self.assertAlmostEqual(number.value, 123.457)
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


class TestAdd(unittest.TestCase):
    """Test case for addition."""

    def test_constant_addition(self) -> None:
        """Adding an instance of number to integer or float is treated as
        addition to a constant with infinite significant digits."""
        number = pysigdig.Number('0.123', tolerance=0.1) + 5.333333333
        self.assertAlmostEqual(number.value, 5.456)
        self.assertEqual(number.tolerance, 0.1)
        self.assertEqual(number.sigdigs, 4)
        self.assertAlmostEqual(number.lsd, 0.001)

    def test_addition_no_tolerance(self) -> None:
        """Add an instance of number to another instance of number, both with
        no tolerance."""
        number = pysigdig.Number('98.87') + pysigdig.Number('78.5')
        self.assertAlmostEqual(number.value, 177.4)
        self.assertEqual(number.tolerance, None)
        self.assertEqual(number.sigdigs, 4)
        self.assertAlmostEqual(number.lsd, 0.1)

    def test_addition_tolerance_on_one_addend(self) -> None:
        """Add an instance of number to another instance of number, one of
        which has a defined tolerance."""
        number = pysigdig.Number('3600', tolerance=10) + pysigdig.Number(0.1)
        self.assertAlmostEqual(number.value, 3600)
        self.assertEqual(number.tolerance, 10)
        self.assertEqual(number.sigdigs, 2)
        self.assertEqual(number.lsd, 100)

    def test_addition_tolerance_on_both_addends(self) -> None:
        """Add an instance of number to another instance of number, both of
        which have a defined tolerance."""
        number = pysigdig.Number(1, tolerance=0.1) + \
            pysigdig.Number(2, tolerance=0.1)
        self.assertEqual(number.value, 3)
        self.assertEqual(number.tolerance, 0.2)
        self.assertEqual(number.sigdigs, 1)
        self.assertEqual(number.lsd, 1)

    def test_addition_invalid_type(self) -> None:
        """Add an instance of number to an invalid type."""
        with self.assertRaises(TypeError):
            print(pysigdig.Number('123') + '123')


class TestSubtract(unittest.TestCase):
    """Test case for subtraction."""

    def test_constant_subtraction(self) -> None:
        """Subtracting a float or int from  an instance of number is treated
        as subtraction of a constant with infinite significant digits."""
        number = pysigdig.Number('0.123', tolerance=0.1) - 5.333333333
        self.assertAlmostEqual(number.value, -5.21)
        self.assertEqual(number.tolerance, 0.1)
        self.assertEqual(number.sigdigs, 4)
        self.assertAlmostEqual(number.lsd, 0.001)

    def test_subtraction_no_tolerance(self) -> None:
        """Subtract an instance of number from another instance of number,
        both with no tolerance."""
        number = pysigdig.Number('98.87') - pysigdig.Number('78.5')
        self.assertAlmostEqual(number.value, 20.4)
        self.assertEqual(number.tolerance, None)
        self.assertEqual(number.sigdigs, 3)
        self.assertAlmostEqual(number.lsd, 0.1)

    def test_subtraction_tolerance_on_one_term(self) -> None:
        """Subtract an instance of number from another instance of number,
        one of which has a defined tolerance."""
        number = pysigdig.Number('3600', tolerance=10) - pysigdig.Number(0.1)
        self.assertAlmostEqual(number.value, 3600)
        self.assertEqual(number.tolerance, 10)
        self.assertEqual(number.sigdigs, 2)
        self.assertEqual(number.lsd, 100)

    def test_subtraction_tolerance_on_both_terms(self) -> None:
        """Subtract an instance of number from another instance of number,
        both of which have a defined tolerance."""
        number = pysigdig.Number(1, tolerance=0.1) - \
            pysigdig.Number(2, tolerance=0.1)
        self.assertEqual(number.value, -1)
        self.assertEqual(number.tolerance, 0.2)
        self.assertEqual(number.sigdigs, 1)
        self.assertEqual(number.lsd, 1)

    def test_subtraction_invalid_type(self) -> None:
        """Subtract an invalid type from an instance of number."""
        with self.assertRaises(TypeError):
            print(pysigdig.Number('123') - '123')


class TestMultiply(unittest.TestCase):
    """Test case for multiplication."""

    def test_constant_multiplication(self) -> None:
        """Multiplying an instance of number by a float or int is treated
        as multiplication of a constant with infinite significant digits."""
        number = pysigdig.Number('0.123', tolerance=0.1) * 5.333333333
        self.assertAlmostEqual(number.value, 0.656)
        self.assertEqual(number.tolerance, 0.5333333333)
        self.assertEqual(number.sigdigs, 3)
        self.assertAlmostEqual(number.lsd, 0.001)

    def test_multiplication_no_tolerance(self) -> None:
        """Multiply an instance of number by another instance of number,
        both with no tolerance."""
        number = pysigdig.Number('98.87') * pysigdig.Number('78.5')
        self.assertAlmostEqual(number.value, 7760)
        self.assertEqual(number.tolerance, None)
        self.assertEqual(number.sigdigs, 3)
        self.assertAlmostEqual(number.lsd, 10)

    def test_multiplication_tolerance_on_one_factor(self) -> None:
        """Multiply an instance of number by another instance of number,
        one of which has a defined tolerance."""
        number = pysigdig.Number('3600', tolerance=10) * pysigdig.Number(0.1)
        self.assertAlmostEqual(number.value, 360)
        self.assertEqual(number.tolerance, 1)
        self.assertEqual(number.sigdigs, 2)
        self.assertEqual(number.lsd, 10)

    def test_multiplication_tolerance_on_both_factors(self) -> None:
        """Multiply an instance of number by another instance of number,
        both of which have a defined tolerance."""
        number = pysigdig.Number(1, tolerance=0.1) * \
            pysigdig.Number(2, tolerance=0.1)
        self.assertEqual(number.value, 2)
        self.assertAlmostEqual(number.tolerance, 0.31)
        self.assertEqual(number.sigdigs, 1)
        self.assertEqual(number.lsd, 1)

    def test_multiplication_invalid_type(self) -> None:
        """Multiply an invalid type by an instance of number."""
        with self.assertRaises(TypeError):
            print(pysigdig.Number('123') * '123')


class TestTrueDivide(unittest.TestCase):
    """Test case for true division."""

    def test_truedivide_by_constant(self) -> None:
        """Dividing an instance of number by a float or int is treated
        as division by a constant with infinite significant digits."""
        number = pysigdig.Number('0.123', tolerance=0.1) / 5.333333333
        self.assertAlmostEqual(number.value, 0.0231)
        self.assertAlmostEqual(number.tolerance, 0.01875)
        self.assertEqual(number.sigdigs, 3)
        self.assertAlmostEqual(number.lsd, 0.0001)

    def test_truedivide_no_tolerance(self) -> None:
        """Divide an instance of number by another instance of number,
        both with no tolerance."""
        number = pysigdig.Number('98.87') / pysigdig.Number('78.5')
        self.assertAlmostEqual(number.value, 1.26)
        self.assertEqual(number.tolerance, None)
        self.assertEqual(number.sigdigs, 3)
        self.assertAlmostEqual(number.lsd, 0.01)

    def test_truedivide_tolerance_on_one_factor(self) -> None:
        """Divide an instance of number by another instance of number,
        one of which has a defined tolerance."""
        number = pysigdig.Number('3600', tolerance=10) / pysigdig.Number(0.1)
        self.assertAlmostEqual(number.value, 36000)
        self.assertEqual(number.tolerance, 100)
        self.assertEqual(number.sigdigs, 2)
        self.assertEqual(number.lsd, 1000)

    def test_truedivide_tolerance_on_both_factors(self) -> None:
        """Divide an instance of number by another instance of number,
        both of which have a defined tolerance."""
        number = pysigdig.Number(1, tolerance=0.1) / \
            pysigdig.Number(2, tolerance=0.1)
        self.assertEqual(number.value, 0.5)
        self.assertAlmostEqual(number.tolerance, 0.078947368)
        self.assertEqual(number.sigdigs, 1)
        self.assertEqual(number.lsd, 0.1)

    def test_truedivide_invalid_type(self) -> None:
        """Dividey an invalid type by an instance of number."""
        with self.assertRaises(TypeError):
            print(pysigdig.Number('123') / '123')


if __name__ == '__main__':
    unittest.main()
