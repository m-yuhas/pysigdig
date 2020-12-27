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
        if isinstance(value, int):
            self.value = value
            self.sigdigs, self.lsd = Number.get_sigdigs_from_int(self.value)
        elif isinstance(value, str):
            self.value, self.sigdigs, self.lsd = Number.parse_string(value)
        if 'sigdigs' in kwargs:
            self.sigdigs = kwargs['sigdigs']
        if 'lsd' in kwargs:
            self.lsd = kwargs['lsd']
        if 'tolerance' in kwargs:
            self.tolerance = kwargs['tolerance']

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


class SigDigNumber:
    """Dummy"""

    def __init__(self, value: float, significant_digits: int) -> None:
        self.significant_digits = significant_digits
        self.value = round(
            value,
            self.get_most_significant_digit(value) + significant_digits)

    def __str__(self):
        return '{}'.format(self.value)

    def __add__(self, other):
        if isinstance(other, int):
            raise NotImplementedError
        ans_sig_digs = max(
            self.get_most_significant_digit(self.value),
            other.get_most_significant_digit(other.value)) + \
            min(
                abs(self.get_most_significant_digit(self.value) -
                    self.significant_digits),
                abs(other.get_most_significant_digit(other.value) -
                    other.significant_digits))
        return SigDigNumber(
            self.value + other.value, ans_sig_digs)

    def __sub__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, int):
            raise NotImplementedError
        return SigDigNumber(
            self.value * other.value,
            min(self.significant_digits, other.significant_digits))

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

    def __isub__(self, other):
        raise NotImplementedError

    def __iadd__(self, other):
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

    @staticmethod
    def get_most_significant_digit(num):
        """Foo"""
        msd = 0
        if num > 1:
            while num / 10 ** (-1 * msd) >= 1:
                msd -= 1
        else:
            while num / 10 ** (-1 * msd) <= 1:
                msd += 1
        return msd
