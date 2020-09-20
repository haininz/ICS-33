# Submitter: haininz(Zhou, Haining)
# Partner:   clyu4(Lyu, Chenhan)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
import re, traceback, keyword

def pnamedtuple(type_name, field_names, mutable= False, defaults = {}):
    def show_listing(s):
        for line_number, line_text in enumerate( s.split('\n'),1 ):
            print(f' {line_number: >3} {line_text.rstrip()}')

    # put your code here
    # bind class_definition (used below) to the string constructed for the class
    ### Testing the validity of input type_name, field_names:
    if type(type_name) is not str:
        raise SyntaxError("Illegal type_name")
    def unique(iterable):
        iterated = set()
        for i in iterable:
            if i not in iterated:
                iterated.add(i)
                yield i
                
#    Check the validity of the input type_name and field_names
    pattern = re.compile(r'^[a-zA-Z][\w]*$')
    field_list = []
    if pattern.match(type_name) == None:
        raise SyntaxError('Illegal name1.')
    if type(field_names) == str:
        field_names = re.split(r'[ ,]+', field_names)
    if type(field_names) == list:
        for names in unique(field_names):            
            if pattern.match(names) == None or keyword.iskeyword(names):
                raise SyntaxError('Illegal name3.')
            field_list.append(names)
    else:
        raise SyntaxError('Unsupported type.')
    if defaults:
        for i in defaults:
            if i not in field_names:
                raise SyntaxError("The name in default must appear in field_names")
    for i in field_list:
        if type(i) is not str:
            raise SyntaxError("Elements inside the field_names must be str")
        
#    Collect parts
#    1. __init__
    init_str = ''
    for i in field_list:
        init_str += (f"        self.{i} = {defaults[i]}\n" if i in defaults else f"        self.{i} = {i}\n")
#    2. __repr__
    repr_str = ''
    for i in field_list:
        repr_str += i + "={" + f"self.{i}" + "},"
#    3. get_x()
    get_str = '\n'
    for i in field_list:
        get_str += f"    def get_{i}(self):\n        return self.{i}\n\n"
#    Create the giant string
    class_definition = '''\
class {name}:
    _fields = {field_list}
    _mutable = {mutable}
    def __init__(self, {args}):
{init_str}
    
    def __repr__(self):
        return f'{name}({repr_str})'
{get_str}
    def __getitem__(self, index):
        if type(index) is int:
            try:
                return eval('self.get_' + {name}._fields[index] + '()')
            except:
                raise IndexError('Point.__getitem__: index is illegal.')
        elif type(index) is str:
            if index not in {name}._fields:
                raise IndexError('Point.__getitem__: index is illegal.')
            return eval('self.get_' + index + '()')
        else:
            raise IndexError('Point.__getitem__: index is illegal.')
            
    def __eq__(self, right):
        if type(right) is not {name}:
            return False
        for i in {name}._fields:
            if self.__getitem__(i) != right.__getitem__(i):
                return False
        return True
        
    def _asdict(self):
        item_dict = dict()
        for i in {name}._fields:
            item_dict[i] = self.__getitem__(i)
        return item_dict
    
    def _make(iterable):
        return {name}(*iterable)
        
    def _replace(self, **kargs):
        for j in kargs:
            if j not in {name}._fields:
                raise TypeError('Required name is not in fields')
        value_list = []
        for i in {name}._fields:
            value_list.append(kargs[i] if i in kargs else self.__dict__[i])
        if self._mutable == False:
            return {name}._make(value_list)
        elif self._mutable == True:
            for j in kargs:
                self.__dict__[j] = kargs[j]
                               
    def __setattr__(self, key, value):
        if key not in self.__dict__ or {name}._mutable:
            self.__dict__[key] = value
        else:
            raise AttributeError('{name} are not supposed to change.')
        
    '''.format(field_list = field_list, mutable = mutable, name = type_name, args = ", ".join(field_list), init_str = init_str, 
               repr_str = repr_str[:-1], get_str = get_str[:-1])
    

    # When debugging, uncomment following line to show source code for the class
    # show_listing(class_definition)
    
    # Execute this class_definition, a str, in a local name space; then bind the
    #   the source_code attribute to class_definition; after try/except return the
    #   class object created; if there is a syntax error, list the class and
    #   also show the error
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )    
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):        
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test pnamedtuple below in script with Point = pnamedtuple('Point','x,y')

    #driver tests
    import driver
    driver.default_file_name = 'bscp3F19.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
