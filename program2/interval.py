# Submitter: haininz(Zhou, Haining)
# Partner:   clyu4(Lyu, Chenhan)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
from goody import type_as_str
from math import sqrt

class Interval:
    def __init__(self, minimum, maximum):
        self.min = minimum
        self.max = maximum

    def min_max(num1, num2=None):
        assert (type(num1) is int) or (type(num1) is float), "The input for minimum must be an int or a float!"
        assert (type(num2) is int) or (type(
            num2) is float) or num2 == None, "If you want to put in a maximum, then it must be an int or a float!"
        if num2 != None:
            assert num1 <= num2, "The minimum cannot be bigger than the maximum!"
        else:
            num2 = num1
        return Interval(num1, num2)

    def mid_err(num1, num2=0):
        assert (type(num1) is int) or (type(num1) is float), "The input for the first number must be an int or a float!"
        assert (type(num2) is int) or (type(
            num2) is float) or num2 == 0, "If you want to put in a second number, then it must be an int or a float!"
        assert num2 >= 0, "The second input must be a positive number!"
        return Interval(num1 - num2, num1 + num2)

    def __repr__(self):
        return "Interval(" + str(self.min) + "," + str(self.max) + ")"

    def __str__(self):
        mid = (self.min + self.max) / 2
        error = mid - self.min
        return str(mid) + "(+/-" + str(abs(error)) + ")"

    def best(self):
        return (self.min + self.max) / 2

    def error(self):
        mid = self.best()
        return mid - self.min

    def relative_error(self):
        mid = self.best()
        error = self.error()
        return abs(error / mid) * 100

    def __bool__(self):
        return self.min != self.max

    def __pos__(self):
        return Interval(self.min, self.max)

    def __neg__(self):
        return Interval(-self.min, -self.max)

    def __add__(self, right):
        if self._got_type(right):
            if type(right) == Interval:
                return Interval(self.min + right.min, self.max + right.max)
            elif type(right) in [int, float]:
                return Interval(self.min + right, self.max + right)
        else:
            return NotImplemented

    def __radd__(self, left):
        if self._got_type(left):
            if type(left) == Interval:
                return Interval(self.min + left.min, self.max + left.max)
            elif type(left) in [int, float]:
                return Interval(self.min + left, self.max + left)
        else:
            return NotImplemented

    def __sub__(self, right):
        if self._got_type(right):
            if type(right) == Interval:
                return Interval(self.min - right.max, self.max - right.min)
            elif type(right) in [int, float]:
                return Interval(self.min - right, self.max - right)
        else:
            return NotImplemented

    def __rsub__(self, left):
        if self._got_type(left):
            if type(left) == Interval:
                return Interval(left.min - self.max, left.max - self.min)
            elif type(left) in [int, float]:
                return Interval(left - self.max, left - self.min)
        else:
            return NotImplemented

    def __mul__(self, right):
        if self._got_type(right):
            if type(right) == Interval:
                return Interval(
                    min(self.min * right.min, self.min * right.max, self.max * right.min, self.max * right.max),
                    max(self.min * right.min, self.min * right.max, self.max * right.min, self.max * right.max))
            else:
                return Interval(self.min * right, self.max * right)
        else:
            return NotImplemented

    def __rmul__(self, left):
        if self._got_type(left):
            if type(left) == Interval:
                return Interval(min(self.min * left.min, self.min * left.max, self.max * left.min, self.max * left.max),
                                max(self.min * left.min, self.min * left.max, self.max * left.min, self.max * left.max))
            else:
                return Interval(self.min * left, self.max * left)
        else:
            return NotImplemented

    def __truediv__(self, right):
        if self._got_type(right):
            if type(right) == Interval:
                if right.min <= 0 and right.max >= 0:
                    raise ZeroDivisionError
                return Interval(
                    min(self.min / right.min, self.min / right.max, self.max / right.min, self.max / right.max),
                    max(self.min / right.min, self.min / right.max, self.max / right.min, self.max / right.max))
            else:
                if right == 0:
                    raise ZeroDivisionError
                return Interval(min(self.min / right, self.max / right), max(self.min / right, self.max / right))
        else:
            return NotImplemented

    def __rtruediv__(self, left):
        if self._got_type(left):
            if self.min <= 0 and self.max >= 0:
                raise ZeroDivisionError
            elif type(left) == Interval:
                return Interval(min(left.min / self.min, left.max / self.min, left.min / self.max, left.max / self.max),
                                max(left.min / self.min, left.max / self.min, left.min / self.max, left.max / self.max))
            else:
                return Interval(min(left / self.min, left / self.max), max(left / self.min, left / self.max))
        else:
            return NotImplemented

    def __pow__(self, right):
        if not type(right) is int:
            return NotImplemented
        else:
            return Interval(min(self.min ** right, self.max ** right), max(self.min ** right, self.max ** right))

    def __eq__(self, right):
        if type(right) is Interval:
            return self.min == right.min and self.max == right.max
        elif type(right) is int or type(right) is float:
            return self.min == right and self.max == right
        else:
            return NotImplemented

    def __nq__(self, right):
        if type(right) is Interval:
            return self.min != right.min or self.max != right.max
        elif type(right) is int or type(right) is float:
            return self.min != right and self.max != right
        else:
            return NotImplemented

    def __lt__(self, right):
        if 'compare_mode' not in Interval.__dict__.keys():
            raise AssertionError('No compare mode.')
        else:
            if Interval.__dict__['compare_mode'] not in ['liberal', 'conservative']:
                raise AssertionError('Invaild comapare mode.')
            else:
                if self.compare_mode == "conservative":
                    if type(right) is Interval:
                        return self.max < right.min
                    elif type(right) in [int, float]:
                        return self.max < right
                    else:
                        raise TypeError(f'unorderable types: {type_as_str(self)}()<{type_as_str(right)}()')
                        # return NotImplemented
                elif self.compare_mode == "liberal":
                    if type(right) is Interval:
                        return self.best() < right.best()
                    elif type(right) in [int, float]:
                        return self.best() < right
                    else:
                        raise TypeError(f'unorderable types: {type_as_str(self)()}<{type_as_str(right)}()')

    def __le__(self, right):
        if 'compare_mode' not in Interval.__dict__.keys():
            raise AssertionError('No compare mode.')
        else:
            if Interval.__dict__['compare_mode'] not in ['liberal', 'conservative']:
                raise AssertionError('Invaild comapare mode.')
            else:
                if Interval.compare_mode == "conservative":
                    if type(right) is Interval:
                        return self.max <= right.min
                    elif type(right) in [int, float]:
                        return self.max <= right
                    else:
                        raise TypeError(f'unorderable types: {type_as_str(self)}() <= {type_as_str(right)}()')
                elif Interval.compare_mode == "liberal":
                    if type(right) is Interval:
                        return self.best() <= right.best()
                    elif type(right) in [int, float]:
                        return self.best() <= right
                    else:
                        raise TypeError(f'unorderable types: {type_as_str(self)}() <= {type_as_str(right)}()')

    def __gt__(self, right):
        if 'compare_mode' not in Interval.__dict__.keys():
            raise AssertionError('No compare mode.')
        else:
            if Interval.__dict__['compare_mode'] not in ['liberal', 'conservative']:
                raise AssertionError('Invaild comapare mode.')
            else:
                if Interval.compare_mode == "conservative":
                    if type(right) is Interval:
                        return self.min > right.max
                    elif type(right) in [int, float]:
                        return self.min > right
                    else:
                        raise TypeError(f'unorderable types: {type_as_str(self)}() > {type_as_str(right)}()')
                elif Interval.compare_mode == "liberal":
                    if type(right) is Interval:
                        return self.best() > right.best()
                    elif type(right) in [int, float]:
                        return self.best() > right
                    else:
                        raise TypeError(f'unorderable types: {type_as_str(self)}() > {type_as_str(right)}()')

    def __ge__(self, right):
        if 'compare_mode' not in Interval.__dict__.keys():
            raise AssertionError('No compare mode.')
        else:
            if Interval.__dict__['compare_mode'] not in ['liberal', 'conservative']:
                raise AssertionError('Invaild comapare mode.')
            else:
                if Interval.compare_mode == "conservative":
                    if type(right) is Interval:
                        return self.min >= right.max
                    elif type(right) in [int, float]:
                        return self.min >= right
                    else:
                        raise TypeError(f'unorderable types: {type_as_str(self)}() >= {type_as_str(right)}()')
                elif Interval.compare_mode == "liberal":
                    if type(right) is Interval:
                        return self.best() >= right.best()
                    elif type(right) in [int, float]:
                        return self.best() >= right
                    else:
                        raise TypeError(f'unorderable types: {type_as_str(self)}() >= {type_as_str(right)}()')

    def __abs__(self):
        return Interval(0.0, abs(self.max)) if self.min < 0 and self.max > 0 else Interval(
            min(abs(self.min), abs(self.max)), max(abs(self.min), abs(self.max)))

    def sqrt(self):
        return Interval(min(sqrt(self.min), sqrt(self.max)), max(sqrt(self.min), sqrt(self.max)))

    def __setattr__(self, name, value):
        assert name not in self.__dict__, "You cannot change any class instances!"
        assert name in ["max", "min"], "You cannot define new class instances other than max and min!"
        self.__dict__[name] = value

    def _got_type(self, item):
        if type(item) not in [int, float, Interval]:
            return False
        return True

if __name__ == '__main__':
    g = Interval.mid_err(9.8,.05)
    print(repr(g))
    g = Interval.min_max(9.75,9.85)
    print(repr(g))
    d = Interval.mid_err(100,1)
    t = (d/(2*g)).sqrt()
    print(t,repr(t),t.relative_error())

    import driver

    driver.default_file_name = 'bscp22F19.txt'
    #     driver.default_show_exception=True
    #     driver.default_show_exception_message=True
    #     driver.default_show_traceback=True
    driver.driver()
