import inspect

class C:
    def __init__(self):
        self.a = 1
        self.b = 2
        
    def add_more_attributes(self): 
        self.c = 3  
         
    def bad_add_more_attributes(self):
        self.private_d = 4 # should raise exception
         
    def bump(self):
        self.a += 1
        self.b += 1
        self.c += 1
        
    def __str__(self):
        return 'a='+str(self.a)+',b='+str(self.b)+',c='+str(self.c)+',d='+str(self.d)

    @staticmethod
    def in_C(calling):
        if calling.function not in C.__dict__:
            return False
        return calling.frame.f_code is C.__dict__[calling.function].__code__
       
    def __setattr__(self,name,value):
        calling = inspect.stack()[1]
        if name.startswith('private_'): #and name not in self.__dict__
                raise NameError('C.__setattr__: cannot explictly use name('+name+') starting with private_')
        elif calling.frame.f_code is C.__dict__['__init__'].__code__:
            self.__dict__['private_'+name] = value
        elif 'private_'+name in self.__dict__:
            if C.in_C(calling):
                self.__dict__['private_'+name] = value
            else:
                raise NameError('C.__setattr__: only C methods can set a private name('+name+')')
        else:
            self.__dict__[name] = value


    def __getattr__(self,name):
        if 'private_'+name in self.__dict__:
            calling = inspect.stack()[1]
            if C.in_C(calling):
                return self.__dict__['private_'+name]
            else:
                raise NameError('C.__getattr__: only C methods can refer to a private name('+name+')')
        raise NameError('C.__getattr__: unknown name('+name+') ')
    
def  f(o):
    return o.a    
        
def  __init__(o):  # Don't confuse this with the __init__ method defined in C
    o.z = 'z'    
        
if __name__ == '__main__':
    # These are all the bsc2.txt tests that don't raise exceptions.
    o = C()
    print(o.__dict__)
    
    o.add_more_attributes()
    o.d = 5
    print(o.__dict__)
    
    o.bump()
    print(o.__dict__)
    
    print(o.c,o.d)
    
    __init__(o)
    print(o.__dict__)
    
    print()
    import driver
    
    driver.default_file_name = 'bscq32F19.txt'
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()

# The driver prints the following information
# {'private_a': 1, 'private_b': 2}
# {'private_a': 1, 'private_b': 2, 'c': 3, 'd': 5}
# {'private_a': 2, 'private_b': 3, 'c': 4, 'd': 5}
# 4 5
# {'private_a': 2, 'private_b': 3, 'c': 4, 'd': 5, 'z': 'z'}
