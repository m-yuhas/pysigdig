"""Module to do arithmetic operations with significant digits."""


from typing import Union
import math
import re


class Number:
    """Class representing a number with information about significant figures
    and tolerance."""

    def __init__(self, value: Union[int, float, str], **kwargs) -> None:
        self._tolerance = None
        self._value = None
        self._lsd = None
        self._sigdigs = None
        if isinstance(value, float):
            self._value = value
            self._sigdigs = float('inf')
            self._lsd = float('-inf')
        elif isinstance(value, int):
            self._value = value
            self._sigdigs, self._lsd = Number.get_sigdigs_from_int(value)
        elif isinstance(value, str):
            self._value, self._sigdigs, self._lsd = Number.parse_string(value)
        else:
            raise TypeError(
                'Invalid type {} provided for argument "value"'.format(
                    type(value)))
        if 'sigdigs' in kwargs:
            self._sigdigs = kwargs['sigdigs']
            self.set_lsd_from_sigdigs()
        if 'lsd' in kwargs:
            self._lsd = kwargs['lsd']
            self.set_sigdigs_from_lsd()
        if 'tolerance' in kwargs:
            if isinstance(kwargs['tolerance'], (float, int)):
                self._tolerance = abs(kwargs['tolerance'])
            else:
                self._tolerance = None

    def __int__(self) -> int:
        return int(float(self))

    def __float__(self) -> float:
        if self.lsd == float('-inf'):
            return self._value
        return float(round(self._value, int(-math.log10(self.lsd))))

    def __str__(self) -> str:
        digits = int(-math.log10(self.lsd))
        string = str(float(self))
        if self._lsd >= 1:
            string = string.split('.')[0]
        else:
            string += (digits - len(string.split('.')[1])) * '0'
        if self.tolerance is not None:
            string += ' ± {}'.format(self.tolerance)
        return string

    def __add__(self, other) -> 'Number':
        if isinstance(other, (float, int)):
            new_value = self._value + other
            new_lsd = self.lsd
            new_tolerance = self.tolerance
        elif isinstance(other, Number):
            new_value = self._value + other._value
            new_lsd = max(self.lsd, other.lsd)
            if self.tolerance is None and other.tolerance is None:
                new_tolerance = None
            else:
                new_tolerance = (self.tolerance or 0) + (other.tolerance or 0)
        else:
            raise TypeError(
                'Cannot add type {} to Number.'.format(type(other)))
        return Number(new_value, lsd=new_lsd, tolerance=new_tolerance)

    def __sub__(self, other) -> 'Number':
        if isinstance(other, (float, int)):
            new_value = self._value - other
            new_lsd = self.lsd
            new_tolerance = self.tolerance
        elif isinstance(other, Number):
            new_value = self._value - other._value
            new_lsd = max(self.lsd, other.lsd)
            if self.tolerance is None and other.tolerance is None:
                new_tolerance = None
            else:
                new_tolerance = (self.tolerance or 0) + (other.tolerance or 0)
        else:
            raise TypeError(
                'Cannot subtract type {} from Number.'.format(type(other)))
        return Number(new_value, lsd=new_lsd, tolerance=new_tolerance)

    def __mul__(self, other) -> 'Number':
        if isinstance(other, (float, int)):
            new_value = self._value * other
            new_sigdigs = self.sigdigs
            if self.tolerance is None:
                new_tolerance = None
            else:
                new_tolerance = self.tolerance * other
        elif isinstance(other, Number):
            new_value = self._value * other._value
            new_sigdigs = min(self.sigdigs, other.sigdigs)
            if self.tolerance is None and other.tolerance is None:
                new_tolerance = None
            else:
                new_tolerance = abs((self.tolerance or 0) * other._value) + \
                    abs((other.tolerance or 0) * self._value) + \
                    (self.tolerance or 0) * (other.tolerance or 0)
        else:
            raise TypeError(
                'Cannot multiply Number by type {}.'.format(type(other)))
        return Number(new_value, sigdigs=new_sigdigs, tolerance=new_tolerance)

    def __truediv__(self, other) -> 'Number':
        if isinstance(other, (float, int)):
            new_value = self._value / other
            new_sigdigs = self.sigdigs
            if self.tolerance is None:
                new_tolerance = None
            else:
                new_tolerance = self.tolerance / other
        elif isinstance(other, Number):
            new_value = self._value / other._value
            new_sigdigs = min(self.sigdigs, other.sigdigs)
            if self.tolerance is None and other.tolerance is None:
                new_tolerance = None
            else:
                new_tolerance = max(
                    abs(
                        abs(new_value) -
                        abs(self.max_value / other.min_value)),
                    abs(
                        abs(new_value) -
                        abs(self.min_value / other.max_value)))
        else:
            raise TypeError(
                'Cannot divide Number by type {}.'.format(type(other)))
        return Number(new_value, sigdigs=new_sigdigs, tolerance=new_tolerance)

    def __floordiv__(self, other) -> 'Number':
        if isinstance(other, (float, int)):
            new_value = self._value // other
            new_sigdigs = min(
                self.sigdigs,
                Number.get_sigdigs_from_int(new_value)[0])
            if self.tolerance is None:
                new_tolerance = None
            else:
                new_tolerance = abs(new_value) - abs(self.max_value / other)
        elif isinstance(other, Number):
            new_value = self._value // other._value
            new_sigdigs = min(
                self.sigdigs,
                other.sigdigs,
                Number.get_sigdigs_from_int(new_value)[0])
            if self.tolerance is None and other.tolerance is None:
                new_tolerance = None
            else:
                new_tolerance = max(
                    abs(
                        abs(new_value) -
                        abs(self.max_value / other.min_value)),
                    abs(
                        abs(new_value) -
                        abs(self.min_value / other.max_value)))
        else:
            raise TypeError(
                'Cannot perform floor division on Number by type {}.'.format(
                    type(other)))
        return Number(new_value, sigdigs=new_sigdigs, tolerance=new_tolerance)

    def __mod__(self, other) -> 'Number':
        if isinstance(other, (float, int)):
            new_value = self._value % other
            new_sigdigs = self.sigdigs
            if self.tolerance is None:
                new_tolerance = None
            else:
                new_tolerance = max(
                    abs(abs(new_value) - abs(self.max_value % other)),
                    abs(abs(new_value) - abs(self.min_value % other)))
        elif isinstance(other, Number):
            new_value = self._value % other._value
            new_sigdigs = min(self.sigdigs, other.sigdigs)
            if self.tolerance is None and other.tolerance is None:
                new_tolerance = None
            else:
                new_tolerance = max(
                    abs(
                        abs(new_value) -
                        abs(self.max_value % other.min_value)),
                    abs(
                        abs(new_value) -
                        abs(self.min_value % other.max_value)))
        else:
            raise TypeError(
                'Cannot perform modulo deivision on Number by type {}'.format(
                    type(other)))
        return Number(new_value, sigdigs=new_sigdigs, tolerance=new_tolerance)

    def __pow__(self, other) -> 'Number':
        if isinstance(other, (float, int)):
            new_value = self._value ** other
            new_sigdigs = self.sigdigs
            if self.tolerance is None:
                new_tolerance = None
            else:
                new_tolerance = max(
                    abs(abs(new_value) - abs(self.max_value ** other)),
                    abs(abs(new_value) - abs(self.min_value ** other)))
        else:
            raise TypeError(
                'Only exponentiating by a constant (float or int) is '
                'supported.')
        return Number(new_value, sigdigs=new_sigdigs, tolerance=new_tolerance)

    def __lt__(self, other) -> bool:
        return self.max_value < other.min_value

    def __gt__(self, other) -> bool:
        return self.min_value > other.max_value

    def __le__(self, other) -> bool:
        return self.max_value < other.max_value

    def __ge__(self, other) -> bool:
        return self.min_value > other.min_value

    def __eq__(self, other) -> bool:
        return (
            self.value == other.value and self.sigdigs == other.sigdigs and
            self.tolerance == other.tolerance and self.lsd == other.lsd)

    def __ne__(self, other) -> bool:
        return not self == other

    def __iadd__(self, other) -> 'Number':
        return self + other

    def __isub__(self, other) -> 'Number':
        return self - other

    def __imul__(self, other) -> 'Number':
        return self * other

    def __idiv__(self, other) -> 'Number':
        return self / other

    def __ifloordiv__(self, other) -> 'Number':
        return self // other

    def __imod__(self, other) -> 'Number':
        return self % other

    def __ipow__(self, other) -> 'Number':
        return self ** other

    def __neg__(self) -> 'Number':
        return Number(
            -self.value,
            sigdigs=self.sigdigs,
            tolerance=self.tolerance)

    def __pos__(self) -> 'Number':
        return self

    def set_lsd_from_sigdigs(self):
        """Determine the least significant digit based on the specified number
        of significant digits and the current value."""
        temp_value = self._value
        if temp_value < 0:
            temp_value = 0 - temp_value
        place = 1
        if temp_value >= 1:
            while temp_value > 0:
                place *= 10
                temp_value -= temp_value % place
            place /= 10
        elif temp_value == 0:
            self._lsd = 1
            return
        else:
            place = float(place)
            while temp_value % place == temp_value:
                place /= 10
        self._lsd = float(place) / 10 ** (self.sigdigs - 1)

    def set_sigdigs_from_lsd(self):
        """Determine the number of significant digits based on the specified
        least significant digit and current value."""
        temp_value = self._value
        if temp_value < 0:
            temp_value = 0 - temp_value
        place = float(self.lsd)
        self._sigdigs = 1
        while temp_value / place >= 1:
            self._sigdigs += 1
            place *= 10
        self._sigdigs -= 1

    @property
    def value(self):
        """Foo"""
        return int(self) if isinstance(self._value, int) else float(self)

    @property
    def max_value(self):
        """Foo"""
        return max(
            float(self) + (self.tolerance or 0),
            float(self) - (self.tolerance or 0))

    @property
    def min_value(self):
        """Foo"""
        return min(
            float(self) + (self.tolerance or 0),
            float(self) - (self.tolerance or 0))

    @property
    def sigdigs(self):
        """Get sigdigs"""
        return self._sigdigs

    @property
    def lsd(self):
        """Get least significant digit."""
        return self._lsd

    @property
    def tolerance(self):
        """Get tolerance."""
        return self._tolerance

    @staticmethod
    def get_sigdigs_from_int(value: int):
        """Get the number of significant digits from an integer"""
        if value < 0:
            value = -value
        if value == 0:
            return 1, 1
        place = 1
        lsd = None
        count = 0
        while value > 0:
            remainder = value % (place * 10)
            if remainder != 0 and lsd is None:
                lsd = place
            if lsd is not None:
                count += 1
            value -= remainder
            place *= 10
        return count, lsd

    @staticmethod
    def parse_string(string: str):
        """Parse a string and return it's value, significant digits and least
        significant digit."""
        string = string.strip().lstrip('0')
        if re.match(r'\-?\d*\.?\d*', string).group() == '':
            raise ValueError('String could not be cast to number')
        decimal_index = string.find('.')
        value = 0
        sigdigs = 0
        lsd = None
        if decimal_index == -1:
            place = 1
            for i in range(len(string) - 1, -1, -1):
                value += int(string[i]) * place
                if string[i] != '0' and lsd is None:
                    lsd = place
                if lsd is not None:
                    sigdigs += 1
                place *= 10
        else:
            place = 1
            for i in range(decimal_index - 1, -1, -1):
                value += int(string[i]) * place
                place *= 10
                sigdigs += 1
            place = 1
            for i in range(decimal_index + 1, len(string)):
                place /= 10
                value += int(string[i]) * place
                sigdigs += 1
            lsd = 1 if string[-1] == '.' else place
        return -value if string[0] == '-' else value, sigdigs, lsd
