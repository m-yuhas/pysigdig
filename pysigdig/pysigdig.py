"""Module to do arithmetic operations with significant digits."""


from typing import Union
import re


class Number:
    """Class representing a number with information about significant figures
    and tolerance."""

    def __init__(self, value: Union[int, float, str], **kwargs) -> None:
        self.tolerance = None
        self.value = None
        self.lsd = None
        self.sigdigs = None
        if isinstance(value, float):
            self.value = value
            self.sigdigs = float('inf')
            self.lsd = float('-inf')
        elif isinstance(value, int):
            self.value = value
            self.sigdigs, self.lsd = Number.get_sigdigs_from_int(self.value)
        elif isinstance(value, str):
            self.value, self.sigdigs, self.lsd = Number.parse_string(value)
        else:
            raise TypeError(
                'Invalid type {} provided for argument "value"'.format(
                    type(value)))
        if 'sigdigs' in kwargs:
            self.sigdigs = kwargs['sigdigs']
            self.set_lsd_from_sigdigs()
        if 'lsd' in kwargs:
            self.lsd = kwargs['lsd']
            self.set_sigdigs_from_lsd()
        if 'tolerance' in kwargs:
            self.tolerance = kwargs['tolerance']

    def __str__(self):
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError

    def __truediv__(self, other):
        raise NotImplementedError

    def __floordiv__(self, other):
        raise NotImplementedError

    def __mod__(self, other):
        raise NotImplementedError

    def __pow__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        raise NotImplementedError

    def __iadd__(self, other):
        raise NotImplementedError

    def __isub__(self, other):
        raise NotImplementedError

    def __imul__(self, other):
        raise NotImplementedError

    def __idiv__(self, other):
        raise NotImplementedError

    def __ifloordiv__(self, other):
        raise NotImplementedError

    def __imod__(self, other):
        raise NotImplementedError

    def __ipow__(self, other):
        raise NotImplementedError

    def __neg__(self):
        raise NotImplementedError

    def __pos__(self):
        raise NotImplementedError

    def set_lsd_from_sigdigs(self):
        """Determine the least significant digit based on the specified number
        of significant digits and the current value."""
        temp_value = self.value
        if temp_value < 0:
            temp_value = 0 - temp_value
        place = 1
        if temp_value >= 1:
            while temp_value > 0:
                place *= 10
                temp_value -= temp_value % place
            place /= 10
        else:
            place = float(place)
            while temp_value % place == temp_value:
                place /= 10
        self.lsd = float(place) / 10 ** (self.sigdigs - 1)

    def set_sigdigs_from_lsd(self):
        """Determine the number of significant digits based on the specified
        least significant digit and current value."""
        temp_value = self.value
        if temp_value < 0:
            temp_value = 0 - temp_value
        place = float(self.lsd)
        self.sigdigs = 1
        while temp_value / place > 1:
            self.sigdigs += 1
            place *= 10
        self.sigdigs -= 1

    @staticmethod
    def get_sigdigs_from_int(value: int):
        """Get the number of significant digits from an integer"""
        if value < 0:
            value = -value
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
        if re.match(r'\d*\.?\d*', string).group() == '':
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
                place *= 10
                sigdigs += 1
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
        return value, sigdigs, lsd
