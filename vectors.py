import math
from numbers import Number


class VectorError(Exception):
    pass


class Vector(object):

    def __init__(self, *values, convert=None):
        if convert:
            self.values = list(map(convert, list(values)))
        else:
            if all(isinstance(e, Number) for e in values):
                self.values = values
            else:
                raise TypeError(
                    'All components of Vector must be of type <Number>')

    def _checktype(self, other):
        if type(self) == type(other):
            return True
        else:
            raise TypeError('Expected Vector, got ' + type(other).__name__)
            return False

    def __drepr__(self):
        return 'Vector(' + str(self.values)[1:-1] + ')'

    def __srepr__(self):
        return 'Vector(' + ",".join([str(f) for f in self.values]) + ')'
    __repr__ = __drepr__

    def __add__(self, other):
        if self._checktype(other):
            return Vector(*(a + b for a, b in self.combine(other)))

    def __sub__(self, other):
        if self._checktype(other):
            return Vector(*(a - b for a, b in self.combine(other)))

    def __len__(self):
        return len(self.values)

    def combine(self, other):
        if len(self.values) != len(other.values):
            raise VectorError('Vector Dimensions are unequal')
        else:
            return zip(self.values, other.values)

    def __neg__(self):
        return Vector(*(-a for a in self.values))

    def __pos__(self):
        return self

    def __abs__(self):
        return sum((a ** 2 for a in self.values)) ** 0.5

    def __abs_sq__(self):
        return sum((a ** 2 for a in self.values))

    def __mul__(self, other):
        if isinstance(other, Number):
            return Vector(*(a * other for a in self.values))
        elif type(other) == type(self):
            raise VectorError('Type of multiplication unspecified')
        else:
            raise TypeError(
                'Cannot multiply Vector and ' + type(other).__name__)
        # return sum( (a*b for a,b in self.combine(other)))
    __rmul__ = __mul__

    def dot(self, other):
        if self._checktype(other):
            return sum((a * b for a, b in self.combine(other)))

    def cross(self, other):
        if self._checktype(other):
            _a = self.values
            _b = other.values
            if len(_a) != len(_b):
                raise VectorError('Vector Dimensions are unequal')
                return False
            if not (2 <= len(_a) <= 3):
                raise VectorError(
                    'Cross product can only be calculated for 2d and 3d Vectors.')
                return False
            if len(_a) == 2:
                _a.append(0)
                _b.append(0)

            return Vector(_a[1] * _b[2] - _a[2] * _b[1], _a[2] * _b[0] - _a[0] * _b[2], _a[0] * _b[1] - _a[1] * _b[0])

    def angle(self, other):
        if self._checktype(other):
            return math.acos((self.dot(other)) / (abs(self) * abs(other)))

    def __contains__(self, other):
        return other in self.values

    def __sum__(self):
        return sum(self.values)

    def __bool__(self):
        return sum(self.values) > 0

    def __iter__(self):
        for e in self.values:
            yield e

    def __getitem__(self, i):
        return self.values[i]

    def __setitem__(self, i, val):
        if isinstance(val, Number):
            self.values[i] = val
        else:
            raise TypeError('Vector components must be of type <Number>')

    def proj(self, b):
        if self._checktype(b):
            return b * ((self.dot(b)) / (b.__abs_sq__()))

    def normalize(self):
        return self * (1.0 / abs(self))

    def convert(self, conv):
        self.values = list(map(conv, self.values))

    def use_simplified_repr(use):
        if use:
            Vector.__repr__ = Vector.__srepr__
        else:
            Vector.__repr__ = Vector.__drepr__
