class Table:
    def __init__(self,name,fields,checks):
        assert type(name) is str, "name must be a string"
        assert type(fields) is list and len(set(fields)) == len(fields), "invalid input of fields"
        assert type(checks) is list, "invalid input type of checks"
        for f in checks:
            assert callable(f), "the list element of checks must be callable"
        assert len(fields) == len(checks), "the length of fields must match the length of checks"
        self.name = name
        self.fields = fields
        self.checks = checks
        self.records = []
                

    # If the attributes name, fields, and records are set correctly, __str__ returns
    #   a string that will print nicely (see the specifications).
    def __str__(self):
        def just(v,l):
            return (str(v).rjust(l) if type(v) is int else str(v).ljust(l))
        
        lengths = [len(field) for field in self.fields]
        for i in range(len(lengths)):
            lengths[i] = max([lengths[i]]+[len(str(r[i])) for r in self.records])
    
        return 'Table: ' + self.name + ' (with '+str(len(self.checks))+' checks)\n'+\
               ' | '.join([str(self.fields[i]).ljust(lengths[i]) for i in range(len(self.fields))])+'\n'+\
               '-+-'.join([lengths[i]*'-' for i in range(len(lengths))]) + '\n' +\
               '\n'.join([' | '.join([just(r[i],lengths[i]) for i in range(len(self.fields))]) for r in self.records])


    # If the attributes name, fields, and records are set correctly, raw returns
    #   a string that will print in a different way, showing each attribute.
    def raw(self):
        return\
             'self.name    = '+str(self.name)+'\n'+\
             'self.fields  = '+str(self.fields)+'\n'+\
             'self.checks  = '+str(self.checks)+'\n'+\
             'self.records = '+str(self.records)
             
    
    def add_record(self,*record):
        assert len(record) == len(self.fields)
        for k,v in zip(self.checks, record):
            assert k(v)
        self.records.append(list(record))


        
    def __call__(self,field):
        assert field in self.fields
        return self.fields.index(field)
    
      

    def __getitem__(self,i):
        if type(i) not in [int, tuple]:
            raise IndexError
        if type(i) is int:
            assert 0 <= i < len(self.records)
            return self.records[i]
        elif type(i) is tuple:
            assert len(i) == 2
            return self.records[i[0]][self.fields.index(i[1])]
                
        
        
        
    def select_records(self,name,predicate):
        newObj = Table(name, self.fields, self.checks)
        for i in self.records:
            if predicate(i):
                newObj.records.append(i)
        return newObj
    
    
    def project(self,*fields):
        temp = []
        for i in fields:
            assert i in self.fields and i not in temp
            temp.append(i)
        self.checks = [v for k,v in zip(self.fields, self.checks) if k in fields]
        new_records = [[] for _ in range(len(self.records))]
        for i,j in zip(new_records, self.records):
            for k,v in zip(self.fields, j):
                if k in fields:
                    i.append(v)
        self.records = new_records
        self.fields = list(fields)       

 

    def __iter__(self):
        giant_list = []
        temp = []
        count = 0
        for i in self.records:
            for k,v in zip(self.fields, i):
                temp.append((count, k, v))
            giant_list.append(temp)
            temp = []
            count += 1
        for i in giant_list:
            for j in sorted(i, key = lambda x: x[1]):
                yield j

                
              
                
       
    ################################################## 
    #
    # Extra credit worth 1 point: don't attempt unless you have written all
    #   the previous methods correctly

    def sort_records(self, field, key = (lambda v : v), reverse = False):
        self.records.sort(key = lambda x: key(x[self.fields.index(field)]), reverse = reverse)
    
    
    def __add__(self,right):
        if set.intersection(set(self.fields), set(right.fields)):
            new_name = self.name + "+" + right.name
            new_fields = self.fields
            new_checks = self.checks
            new_records = self.records
            for i in range(len(right.fields)):
                if right.fields[i] not in self.fields:
                    new_fields.append(right.fields[i])
                    new_checks.append(right.checks[i])
                    for k,v in zip(new_records, right.records):
                        k.append(v[i])
            new_object = Table(new_name, new_fields, new_checks)
            new_object.records = sorted(new_records, key = lambda x: x[0])
            return new_object





if __name__ == '__main__':
    # Write any other code here to test Table before doing bsc test; for example

    # Here are simple tests not raising exceptions (illustrated in the problem statement)
    # Comment out any tests you no longer want to perform
    # The driver is run at the bottom of this script
    import prompt
    print('For simple test __init__ and beyond to work, __init__ must work correctly')
    print('  for cases when it does not need to throw exceptions.')
    print('Also, calling __iter__ will raise an exception if it is implemented')
    print('   by just pass')
    if prompt.for_bool('\nDo you want to perform simple tests before bsc tests',False):
        # Table (__init__)
        print('\n\n-->Testing Table (__init__), simply')
        employee = Table('Employee', ['Name', 'EmpId', 'DeptName'], [lambda v: type(v) is str, lambda v: type(v) is int and 1000<=v<=9999, lambda v: v in ['Finance','Sales']])
        print(employee)
        print(employee.raw())
         
         
        # add_record
        print('\n\n-->Testing add_record simply')
        employee = Table('Employee', ['Name', 'EmpId', 'DeptName'], [lambda v: type(v) is str, lambda v: type(v) is int and 1000<=v<=9999, lambda v: v in ['Finance','Sales']])
        employee.add_record('Bob',2241,'Sales')
        employee.add_record('Cathy',3401,'Finance')
        employee.add_record('Alice',3415,'Finance')
        employee.add_record('David',2202,'Sales')
        print(employee)
        print(employee.raw())
         
     
        # __call__
        print('\n\n-->Testing __call__ simply')
        employee = Table('Employee', ['Name', 'EmpId', 'DeptName'], [lambda v: type(v) is str, lambda v: type(v) is int and 1000<=v<=9999, lambda v: v in ['Finance','Sales']])
        for i in ['Name', 'EmpId', 'DeptName']:
            print(i,'is in self.fields at index',employee(i))
             
         
        # __getitem__
        print('\n\n-->Testing __getitem__ simply')
        employee = Table('Employee', ['Name', 'EmpId', 'DeptName'], [lambda v: type(v) is str, lambda v: type(v) is int and 1000<=v<=9999, lambda v: v in ['Finance','Sales']])
        employee.records = [['Bob', 2241, 'Sales'], ['Cathy', 3401, 'Finance'], ['Alice', 3415, 'Finance'], ['David', 2202, 'Sales']]
        print(employee[0])
        print(employee[2])
        print(employee[0,'Name'])
        print(employee[0,'EmpId'])
        print(employee[0,'DeptName'])
         
        
        # select_records
        print('\n\n-->Testing select_records simply')
        employee = Table('Employee', ['Name', 'EmpId', 'DeptName'], [lambda v: type(v) is str, lambda v: type(v) is int and 1000<=v<=9999, lambda v: v in ['Finance','Sales']])
        employee.records = [['Bob', 2241, 'Sales'], ['Cathy', 3401, 'Finance'], ['Alice', 3415, 'Finance'], ['David', 2202, 'Sales']]
        sales = employee.select_records('Sales',lambda r : r[employee('DeptName')] == 'Sales')   
        print(sales)
         
         
        #  project
        print('\n\n-->Testing project simply')
        employee = Table('Employee', ['Name', 'EmpId', 'DeptName'], [lambda v: type(v) is str, lambda v: type(v) is int and 1000<=v<=9999, lambda v: v in ['Finance','Sales']])
        employee.records = [['Bob', 2241, 'Sales'], ['Cathy', 3401, 'Finance'], ['Alice', 3415, 'Finance'], ['David', 2202, 'Sales']]
        employee.project('Name','DeptName')
        print(employee)
        print(employee.raw())
         
         
        #  __iter__
        print('\n\n-->Testing __iter__ simply')
        employee = Table('Employee', ['Name', 'EmpId', 'DeptName'], [lambda v: type(v) is str, lambda v: type(v) is int and 1000<=v<=9999, lambda v: v in ['Finance','Sales']])
        employee.records = [['Bob', 2241, 'Sales'], ['Cathy', 3401, 'Finance'], ['Alice', 3415, 'Finance'], ['David', 2202, 'Sales']]
        for i in employee:
            print(i)
         
         
        #  sort_records +
        if prompt.for_bool('\nDo you want to perform extra credit tests',False):
            print('\n\n-->Testing sort_records simply: 1 point extra credit')
            employee = Table('Employee', ['Name', 'EmpId', 'DeptName'], [lambda v: type(v) is str, lambda v: type(v) is int and 1000<=v<=9999, lambda v: v in ['Finance','Sales']])
            employee.records = [['Bob', 2241, 'Sales'], ['Cathy', 3401, 'Finance'], ['Alice', 3415, 'Finance'], ['David', 2202, 'Sales']]
            employee.sort_records('EmpId', lambda ei : ei% 10)
            print(employee)
             
            print('\n\n-->Testing + simply: 1 point extra credit')
            employee = Table('Employee', ['Name', 'EmpId', 'DeptName'], [lambda v: type(v) is str, lambda v: type(v) is int and 1000<=v<=9999, lambda v: v in ['Finance','Sales']])
            employee.records = [['Bob', 2241, 'Sales'], ['Cathy', 3401, 'Finance'], ['Alice', 3415, 'Finance'], ['David', 2202, 'Sales']]
            department = Table('Department', ['Manager', 'DeptName'], [lambda v: type(v) is str, lambda v: v in ['Finance', 'Sales', 'Production']])
            department.records = [['George', 'Finance'], ['Harriet', 'Sales'], ['Charles', 'Production']]
            print(employee+department)
 
         
         
 
 
    print('\n\n')
    import driver
    driver.default_file_name = 'bscile2S19.txt'
    #Uncomment the following lines to see MORE details on exceptions
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
    driver.driver()
