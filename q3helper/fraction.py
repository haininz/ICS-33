from goody import irange
from goody import type_as_str

import math

class Fraction:
    # Call as Fraction._gcd(...); no self parameter
    # Helper method computes the Greatest Common Divisor of x and y
    @staticmethod
    def _gcd(x : int, y : int) -> int:
        assert x >= 0 and y >= 0, 'Fraction._gcd: x('+str(x)+') and y('+str(y)+') must be >= 0'
        while y != 0:
            x, y = y, x % y
        return x

    # Returns a string that is the decimal representation of a Fraction, with
    #   decimal_places digitst appearing after the decimal points.
    # For example: if x = Fraction(23,8), then x(5) returns '2.75000'
    def __call__(self, decimal_places):
        answer = ''
        num = self.num
        denom = self.denom
    
        # handle negative values
        if num < 0:
            num, answer = -num, '-'
    
        # handle integer part
        if num >= denom:
            answer += str(num//denom)
            num     = num - num//denom*denom
            
        # handle decimal part
        answer += '.'+str(num*10**decimal_places//denom)
        return answer
    
    @staticmethod
    # Call as Fraction._validate_arithmetic(..); with no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), lt (left type) and rt (right type)
    # An example call (from my __add__ method), which checks whether the type of
    #   right is a Fraction or int is...
    # Fraction._validate_arithmetic(right, {Fraction,int},'+','Fraction',type_as_str(right))
    def _validate_arithmetic(v, t : set, op : str, lt : str, rt : str):
        if type(v) not in t:
            raise TypeError('unsupported operand type(s) for '+op+
                            ': \''+lt+'\' and \''+rt+'\'')        

    @staticmethod
    # Call as Fraction._validate_relational(..); with no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), and rt (right type)
    def _validate_relational(v, t : set, op : str, rt : str):
        if type(v) not in t:
            raise TypeError('unorderable types: '+
                            'Fraction() '+op+' '+rt+'()')        


    def __init__(self,num=0,denom=1):
        assert denom != 0 and type(num) is int and type(denom) is int, "Invalid input!"
        if denom < 0:
            denom *= -1
            num *= -1
        common_factor = Fraction._gcd(abs(num), abs(denom))
        self.num = int(num//common_factor)
        self.denom = int(denom//common_factor)

    def __repr__(self):
        return f'Fraction({self.num},{self.denom})'
    
    def __str__(self):
        return f'{self.num}/{self.denom}'
   
    def __bool__(self):
        return (False if self.num == 0 else True) 

    def __getitem__(self,i):
        if i not in [0, 1] and "numerator".find(i) != 0 and "denominator".find(i) != 0:
            raise TypeError
        else:
            return self.num if i == 0 or "numerator".find(str(i)) == 0 else self.denom    
 
    def __pos__(self):
        return Fraction(self.num, self.denom)
    
    def __neg__(self):
        return Fraction(self.num * -1, self.denom)
    
    def __abs__(self):
        return Fraction(abs(self.num), self.denom)
    
    def __add__(self,right):
        Fraction._validate_arithmetic(right, {Fraction,int},'+','Fraction',type_as_str(right))
        if type_as_str(right) == "int":
            return Fraction(self.num + self.denom * right, self.denom)
        elif type_as_str(right) == "fraction.Fraction":
            return Fraction(self.num * right.denom + right.num * self.denom, self.denom * right.denom)
        
        
    def __radd__(self,left):
        Fraction._validate_arithmetic(left, {Fraction,int},'+', type_as_str(left), 'Fraction')
        if type_as_str(left) == "int":
            return Fraction(self.num + self.denom * left, self.denom)
        elif type_as_str(left) == "fraction.Fraction":
            return Fraction(self.num * left.denom + left.num * self.denom, self.denom * left.denom)
        

    def __sub__(self,right):
        Fraction._validate_arithmetic(right, {Fraction,int},'-','Fraction',type_as_str(right))
        if type_as_str(right) == "int":
            return Fraction(self.num - self.denom * right, self.denom)
        elif type_as_str(right) == "fraction.Fraction":
            return Fraction(self.num * right.denom - right.num * self.denom, self.denom * right.denom)
        
     
    def __rsub__(self,left):
        Fraction._validate_arithmetic(left, {Fraction,int},'-', type_as_str(left), 'Fraction')
        if type_as_str(left) == "int":
            return Fraction(self.denom * left - self.num, self.denom)
        elif type_as_str(left) == "fraction.Fraction":
            return Fraction(left.num * self.denom - self.num * left.denom, self.denom * left.denom)
        
     
    def __mul__(self,right):
        Fraction._validate_arithmetic(right, {Fraction,int},'*','Fraction',type_as_str(right))
        if type_as_str(right) == "int":
            return Fraction(self.num * right, self.denom)
        elif type_as_str(right) == "fraction.Fraction":
            return Fraction(self.num * right.num, self.denom * right.denom)
        

    def __rmul__(self,left):
        Fraction._validate_arithmetic(left, {Fraction,int},'*', type_as_str(left), 'Fraction')
        if type_as_str(left) == "int":
            return Fraction(self.num * left, self.denom)
        elif type_as_str(left) == "fraction.Fraction":
            return Fraction(self.num * left.num, self.denom * left.denom)
        
        
    def __truediv__(self,right):
        Fraction._validate_arithmetic(right, {Fraction,int},'/','Fraction',type_as_str(right))
        if type_as_str(right) == "int":
            if right == 0:
                raise ZeroDivisionError
            return Fraction(self.num, self.denom * right)
        elif type_as_str(right) == "fraction.Fraction":
            return Fraction(self.num * right.denom, self.denom * right.num)


    def __rtruediv__(self,left):
        Fraction._validate_arithmetic(left, {Fraction,int},'/', type_as_str(left), 'Fraction')
        if type_as_str(left) == "int":
            if left == 0:
                raise ZeroDivisionError
            return Fraction(self.denom * left, self.num)
        elif type_as_str(left) == "fraction.Fraction":
            return Fraction(self.denom * left.num, self.num * left.denom)


    def __pow__(self,right):
        Fraction._validate_arithmetic(right, {int},'**','Fraction',type_as_str(right))
        if right > 0:
            return Fraction(int(math.pow(self.num, right)), int(math.pow(self.denom, right)))
        elif right < 0:
            return Fraction(int(math.pow(self.denom, abs(right))), int(math.pow(self.num, abs(right))))
        else:
            return 1
        

    def __eq__(self,right):
        Fraction._validate_relational(right, {Fraction, int},'==', type_as_str(right))
        if type_as_str(right) == "int":
            return self.num == self.denom * right
        elif type_as_str(right) == "fraction.Fraction":
            return self.num * right.denom == right.num * self.denom

    def __lt__(self,right):
        Fraction._validate_relational(right, {Fraction, int},'<', type_as_str(right))
        if type_as_str(right) == "int":
            return self.num < self.denom * right
        elif type_as_str(right) == "fraction.Fraction":
            return self.num * right.denom < right.num * self.denom

    
    def __gt__(self,right):
        Fraction._validate_relational(right, {Fraction, int},'>', type_as_str(right))
        if type_as_str(right) == "int":
            return self.num > self.denom * right
        elif type_as_str(right) == "fraction.Fraction":
            return self.num * right.denom > right.num * self.denom
        
        
    # Uncomment this method when you are ready to write/test it
    # If this is pass, then no attributes will be set!
    def __setattr__(self,name,value):
        if name in self.__dict__:
            raise NameError
        else:
            self.__dict__[name] = value
 


##############################


# Newton: pi = 6*arcsin(1/2); see the arcsin series at http://mathforum.org/library/drmath/view/54137.html
# Check your results at http://www.geom.uiuc.edu/~huberty/math5337/groupe/digits.html
#   also see http://www.numberworld.org/misc_runs/pi-5t/details.html
def compute_pi(n):
    def prod(r):
        answer = 1
        for i in r:
            answer *= i
        return answer
    
    answer = Fraction(1,2)
    x      = Fraction(1,2)
    for i in irange(1,n):
        big    = 2*i+1
        answer += Fraction(prod(range(1,big,2)),prod(range(2,big,2)))*x**big/big       
    return 6*answer





if __name__ == '__main__':
    # Put in simple tests for Fraction before allowing driver to run
 
    print()
    import driver
    
    driver.default_file_name = 'bscq31F19.txt'
#     driver.default_show_traceback= True
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
    driver.driver()
