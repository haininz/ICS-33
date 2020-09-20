from collections import defaultdict # You can elect to use defaultdicts


def effective_rate(db : {str: {(int,int) : float}}, state : str, income : int ) -> float:
    tax = 0
    for k,v in db[state].items():
        if k[1] == None:
            tax += (income-k[0]) * v
            break
        if income >= k[1]:
            tax += (k[1]-k[0]) * v
        elif k[0] <= income < k[1]:
            tax += (income-k[0]) * v
            break
    return tax/income


def read_db(afile : open) -> {str: {(int,int) : float}}:
    db = defaultdict(dict)
    line_list = [line.rstrip().split(";") for line in afile]
    for i in line_list:
        for j in i[1:]:
            var = j.split(":")
            if var[1] != 'None':
                db[i[0]][(int(var[0]), int(var[1]))] = float(var[2])
            else:
                db[i[0]][(int(var[0]), None)] = float(var[2])
    return db
 

def by_complexity(db : {str: {(int,int) : float}}) -> [(str,int)]:
    answer = []
    for k,v in db.items():
        answer.append((k, len(v)))
    return sorted(answer, key = lambda x: (-x[1], x[0]))
    

def state_summary(db : {str: {(int,int) : float}}) -> {(str,int,(int,int),(int,int))}:
    tax_list = []
    answer = set()
    for k,v in db.items():
        for i in v:
            tax_list.append(i)
        tax_list.sort(key = lambda x: x[0])
        answer.add((k, len(v), tax_list[0]) if len(tax_list) == 1 else (k, len(v), tax_list[0], tax_list[-1]))
        tax_list = []
    return answer
                

def bracket_view(db : {str: {(int,int) : float}}) -> {(int,int): {str : float}}:
    answer = defaultdict(dict)
    tax_set = {j for i in db.values() for j in i}
    for k,v in db.items():
        for m,n in v.items():
            for i in tax_set:
                if m == i:
                    answer[i][k] = n
    return answer 
          

# extra credit
def illegal_tax_tables(db : {str: {(int,int) : float}}) -> {str}:
    answer = set()
#     tax_set = set()
    for i,j in db.items():
        if type(j) != dict:
            answer.add(i)
        else:
            for k in j:
                if len(k) != 2:
                    answer.add(i)
                else:
                    if type(k[0]) != int:
                        answer.add(i)
                    if type(k[1]) != int:
                        if k[1] != None:
                            answer.add(i)
                    if type(k[0]) == type(k[1]) == int:
                        if k[0] < 0 or k[1] < 0:
                            answer.add(i)
#                 tax_set.add(k)
#     tax_list = list(tax_set).sort(key = lambda x: (x[0], x[1]))
#     print(tax_list)
#                         
                            
    return answer



    


         

if __name__ == '__main__':
    import prompt
    from math import isclose
    # checks whether answer is correct, printing appropriate information
    # Note that dict/defaultdict will compare == if they have the same keys and
    #   associated values, regardless of the fact that they print differently
    def check (answer, correct):
        if (answer   == correct) or (type(answer) is float and type(correct) is float and isclose(answer,correct,abs_tol=.00001)):
            print ('    Correct')
        else:
            print ('    INCORRECT')
            print ('      was       =',answer)
            print ('      should be =',correct)
        print()
 
 
 
    if prompt.for_bool('Test effective_rate?', True):  
        db1 = {'CT': {(      0,  12_499): .02,
                      ( 12_500,  49_999): .04, 
                      ( 50_000,    None): .06},

               'IN': {(0, None): .04},

               'LA': {(      0,   9_999): .03,
                      ( 10_000,  12_499): .05,
                      ( 12_500,  49_999): .055,
                      ( 50_000, 299_999): .06,
                      (300_000,    None): .078},
            
                'MA': {(0, None): .055}}
        print('  argument =', db1)
        answer = effective_rate(db1,'CT',40_000)
        print('  answer   =', answer)
        check(answer, 0.0337495)
        
        
        db2 = {'CT': {(      0,  12_499): .02,
                      ( 12_500,  49_999): .04, 
                      ( 50_000,    None): .06},

               'IN': {(0, None): .04},

               'LA': {(      0,   9_999): .03,
                      ( 10_000,  12_499): .05,
                      ( 12_500,  49_999): .055,
                      ( 50_000, 299_999): .06,
                      (300_000,    None): .078},
        
                'CA': {(      0,  49_999): .03,
                       ( 50_000, 299_999): .06,
                       (300_000, 499_999): .062,
                       (500_000, 599_999): .064,
                       (600_000,    None): .078},
        
                'MS': {(      0,   9_999): .02,
                       ( 10_000,  12_499): .04,
                       ( 12_500,  49_999): .05,
                       ( 50_000, 299_999): .06,
                       (300_000, 499_999): .07,
                       (500_000,    None): .09},

                'MA': {(0, None): .055},
        
                'AL': {(0, None): .045}}
        print('  argument =', db2)
        answer = effective_rate(db2,'MS',350_000)
        print('  answer   =', answer)
        check(answer, .05907094285714285)
        
        
 
 
    if prompt.for_bool('Test read_db?', True):        
        print('  argument = db1.txt')
        answer = read_db(open('db1.txt'))
        print('  answer   =', answer)
        check(answer, {
                       'CT': {(      0,  12_499): .02, ( 12_500,  49_999): .04, ( 50_000,    None): .06},
                       'IN': {(0, None): .04},
                       'LA': {(      0,   9_999): .03, ( 10_000,  12_499): .05, ( 12_500,  49_999): .055, ( 50_000, 299_999): .06, (300_000,    None): .078},
                       'MA': {(0, None): .055}
                       })

 
        print('  argument = db2.txt')
        answer = read_db(open('db2.txt'))
        print('  answer   =', answer)
        check(answer, {'CT': {(      0,  12_499): .02,
                              ( 12_500,  49_999): .04, 
                              ( 50_000,    None): .06},

                       'IN': {(0, None): .04},

                       'LA': {(      0,   9_999): .03,
                              ( 10_000,  12_499): .05,
                              ( 12_500,  49_999): .055,
                              ( 50_000, 299_999): .06,
                              (300_000,    None): .078},
                
                        'CA': {(      0,  49_999): .03,
                               ( 50_000, 299_999): .06,
                               (300_000, 499_999): .062,
                               (500_000, 599_999): .064,
                               (600_000,    None): .078},
                
                        'MS': {(      0,   9_999): .02,
                               ( 10_000,  12_499): .04,
                               ( 12_500,  49_999): .05,
                               ( 50_000, 299_999): .06,
                               (300_000, 599_999): .07,
                               (600_000,    None): .09},
        
                        'MA': {(0, None): .055},
                
                        'AL': {(0, None): .045}}
            )

        
        
    if prompt.for_bool('Test by_complexity?', True):  
        db1 = {'CT': {(      0,  12_499): .02,
                      ( 12_500,  49_999): .04, 
                      ( 50_000,    None): .06},

                'IN': {(0, None): .04},

                'LA': {(      0,   9_999): .03,
                       ( 10_000,  12_499): .05,
                       ( 12_500,  49_999): .055,
                       ( 50_000, 299_999): .06,
                       (300_000,    None): .078},
            
                'MA': {(0, None): .055}}
        print('  argument =', db1)
        answer = by_complexity(db1)
        print('  answer   =', answer)
        check(answer, [('LA', 5), ('CT', 3), ('IN', 1), ('MA', 1)])


        db2 = {'CT': {(      0,  12_499): .02,
                      ( 12_500,  49_999): .04, 
                      ( 50_000,    None): .06},

               'IN': {(0, None): .04},

               'LA': {(      0,   9_999): .03,
                      ( 10_000,  12_499): .05,
                      ( 12_500,  49_999): .055,
                      ( 50_000, 299_999): .06,
                      (300_000,    None): .078},
        
                'CA': {(      0,  49_999): .03,
                       ( 50_000, 299_999): .06,
                       (300_000, 499_999): .062,
                       (500_000, 599_999): .064,
                       (600_000,    None): .078},
        
                'MS': {(      0,   9_999): .02,
                       ( 10_000,  12_499): .04,
                       ( 12_500,  49_999): .05,
                       ( 50_000, 299_999): .06,
                       (300_000, 499_999): .07,
                       (500_000,    None): .09},

                'MA': {(0, None): .055},
        
                'AL': {(0, None): .045}}
        print('  argument =', db2)
        answer = by_complexity(db2)
        print('  answer   =', answer)
        check(answer, [('MS', 6), ('CA', 5), ('LA', 5), ('CT', 3), ('AL', 1), ('IN', 1), ('MA', 1)])



 
    if prompt.for_bool('Test state_summary?', True):  
        db1 = {'CT': {(      0,  12_499): .02,
                      ( 12_500,  49_999): .04, 
                      ( 50_000,    None): .06},

                'IN': {(0, None): .04},

                'LA': {(      0,   9_999): .03,
                       ( 10_000,  12_499): .05,
                       ( 12_500,  49_999): .055,
                       ( 50_000, 299_999): .06,
                       (300_000,    None): .078},
            
                'MA': {(0, None): .055}}
        print('  argument =', db1)
        answer = state_summary(db1)
        print('  answer   =', answer)
        check(answer, {('CT', 3, (0, 12499), (50000, None)),
                       ('IN', 1, (0, None)),
                       ('LA', 5, (0, 9999), (300000, None)),
                       ('MA', 1, (0, None))
                      })
 
 
        db2 = {'CT': {(      0,  12_499): .02,
                      ( 12_500,  49_999): .04, 
                      ( 50_000,    None): .06},

               'IN': {(0, None): .04},

               'LA': {(      0,   9_999): .03,
                      ( 10_000,  12_499): .05,
                      ( 12_500,  49_999): .055,
                      ( 50_000, 299_999): .06,
                      (300_000,    None): .078},
        
                'CA': {(      0,  49_999): .03,
                       ( 50_000, 299_999): .06,
                       (300_000, 499_999): .062,
                       (500_000, 599_999): .064,
                       (600_000,    None): .078},
        
                'MS': {(      0,   9_999): .02,
                       ( 10_000,  12_499): .04,
                       ( 12_500,  49_999): .05,
                       ( 50_000, 299_999): .06,
                       (300_000, 499_999): .07,
                       (500_000,    None): .09},

                'MA': {(0, None): .055},
        
                'AL': {(0, None): .045}}
        print('  argument =', db2)
        answer = state_summary(db2)
        print('  answer   =', answer)
        check(answer, {('AL', 1, (0, None)), 
                       ('IN', 1, (0, None)), 
                       ('MS', 6, (0, 9999), (500000, None)), 
                       ('CT', 3, (0, 12499), (50000, None)), 
                       ('CA', 5, (0, 49999), (600000, None)), 
                       ('LA', 5, (0, 9999), (300000, None)), 
                       ('MA', 1, (0, None))}
             )
 
 
 
    if prompt.for_bool('Test bracket_view?', True):  
        db1 = {'CT': {(      0,  12_499): .02,
                      ( 12_500,  49_999): .04, 
                      ( 50_000,    None): .06},

               'IN': {(0, None): .04},

               'LA': {(      0,   9_999): .03,
                      ( 10_000,  12_499): .05,
                      ( 12_500,  49_999): .055,
                      ( 50_000, 299_999): .06,
                      (300_000,    None): .078},
            
                'MA': {(0, None): .055}}
        print('  argument =', db1)
        answer = bracket_view(db1)
        print('  answer   =', answer)
        check(answer, {(0, 12499): {'CT': 0.02}, 
                       (12500, 49999): {'CT': 0.04, 'LA': 0.055}, 
                       (50000, None): {'CT': 0.06}, 
                       (0, None): {'IN': 0.04, 'MA': 0.055}, 
                       (0, 9999): {'LA': 0.03}, 
                       (10000, 12499): {'LA': 0.05}, 
                       (50000, 299999): {'LA': 0.06}, 
                       (300000, None): {'LA': 0.078}})

        
        
        db2 = {'CT': {(      0,  12_499): .02,
                      ( 12_500,  49_999): .04, 
                      ( 50_000,    None): .06},

               'IN': {(0, None): .04},

               'LA': {(      0,   9_999): .03,
                      ( 10_000,  12_499): .05,
                      ( 12_500,  49_999): .055,
                      ( 50_000, 299_999): .06,
                      (300_000,    None): .078},
        
                'CA': {(      0,  49_999): .03,
                       ( 50_000, 299_999): .06,
                       (300_000, 499_999): .062,
                       (500_000, 599_999): .064,
                       (600_000,    None): .078},
        
                'MS': {(      0,   9_999): .02,
                       ( 10_000,  12_499): .04,
                       ( 12_500,  49_999): .05,
                       ( 50_000, 299_999): .06,
                       (300_000, 499_999): .07,
                       (500_000,    None): .09},

                'MA': {(0, None): .055},
        
                'AL': {(0, None): .045}}
        print('  argument =', db2)
        answer = bracket_view(db2)
        print('  answer   =', answer)
        check(answer, {(0, 12499): {'CT': 0.02}, 
                       (12500, 49999): {'CT': 0.04, 'LA': 0.055, 'MS': 0.05}, 
                       (50000, None): {'CT': 0.06}, 
                       (0, None): {'IN': 0.04, 'MA': 0.055, 'AL': 0.045}, 
                       (0, 9999): {'LA': 0.03, 'MS': 0.02}, 
                       (10000, 12499): {'LA': 0.05, 'MS': 0.04}, 
                       (50000, 299999): {'LA': 0.06, 'CA': 0.06, 'MS': 0.06}, 
                       (300000, None): {'LA': 0.078}, (0, 49999): {'CA': 0.03}, 
                       (300000, 499999): {'CA': 0.062, 'MS': 0.07}, 
                       (500000, 599999): {'CA': 0.064}, 
                       (600000, None): {'CA': 0.078}, 
                       (500000, None): {'MS': 0.09}}
             ) 



    if prompt.for_bool('Test illegal_tax_tables?', True):  
        db1 = {'CT': {(      0,  12_499): .02,
                      ( 12_500,  49_999): .04, 
                      ( 50_000,    None): .06},

               'IN': {(0, None): .04},

               'LA': {(      0,   9_999): .03,
                      ( 10_000,  12_499): .05,
                      ( 12_500,  49_999): .055,
                      ( 50_000, 299_999): .06,
                      (300_000,    None): .078},
        
                'CA': {(      0,  49_999): .03,
                       ( 50_000, 299_999): .06,
                       (300_000, 499_999): .062,
                       (500_000, 599_999): .064,
                       (600_000,    None): .078},
        
                'MS': {(      0,   9_999): .02,
                       ( 10_000,  12_499): .04,
                       ( 12_500,  49_999): .05,
                       ( 50_000, 299_999): .06,
                       (300_000, 499_999): .07,
                       (500_000,    None): .09},

                'MA': {(0, None): .055},
        
                'AL': {(0, None): .045}}
        print('  argument =', db1)
        answer = illegal_tax_tables(db1)
        print('  answer   =', answer)
        check(answer, set())
         
        db2 = {'A': set(),

               'B': {(0, 7): .01,
                     (1, 2, 3): .02,
                     (10, None): .04},

               'C': {(0, 7): .01,
                     (8, 'a'): .02,
                     (10, None): .04},

               'D': {(0, 7): .01,
                     ('a', 9): .02,
                     (10, None): .04},

               'E': {(0, 7): .01,
                     (-8, 9): .02,
                     (10, None): .04},

               'F': {(0, 7): .01,
                     (8, -9): .02,
                     (10, None): .04},
               
               'G': {(0, 7): .01,
                     (9, 8): .02,
                     (10, None): .04},
               
               'H': {(0, 8): .01,
                     (9, 9): .02,
                     (10, None): .04},

               'I': {(0, 7): .01,
                     (0, 9): .02,
                     (10, None): .04},

            
               'J': {(0, 7): .01,
                     (8, None): .02,
                     (10, None): .04},

               'K': {(0, 7): .01,
                     (8, None): .02,
                     (9, 10): .04},

            
               'L': {(0, 7): .01,
                     (9, 10): .02,
                     (11, None): .04},

               'M': {(0, 7): .01,
                     (8, 9): .02,
                     (11, None): .04},

               'N': {(0, 7): .01,
                     (8, 9): .01,
                     (10, None): .04},

               'N': {(0, 7): .01,
                     (8, 9): .02,
                     (10, None): .02}}
        print('  argument =', db2)
        answer = illegal_tax_tables(db2)
        print('  answer   =', answer)
        check(answer, {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'J', 'K', 'L', 'M', 'N'})


 
 
