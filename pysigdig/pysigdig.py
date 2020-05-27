"""Module to do arithmetic operations with significant digits."""

class Number:

    def __init__(self,
                 value: float,
                 significant_digits: int,
                 tolerance: float = None,
                 tolerance_sig_dgs: int = None) -> None:
        self.signficant_digits = significant_digits
        self.tolerance_sig_digs = tolerance_sig_dgs
        self.value = round(
            value,
            self.get_most_signficant_digit(value) - significant_digits)
        self.tolerance = round(
            value, 
            self.get_most_signficant_digit(tolerance) - tolerance_sig_dgs)

    def __str__(self):
        return "{} ± {}".format(self.value, self.tolerance)

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
    
    def __neg__(self, other):
        raise NotImplementedError
    
    def __pos__(self, other):
        raise NotImplementedError

    def get_most_signficant_digit(self, n):
        msd = 0
        if n > 1:
            while n / 10 ** msd <= 1:
                msd += 1
        else:
            while n / 10 ** msd >= 1:
                msd -= 1
        return msd
        