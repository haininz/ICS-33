import re
from goody import irange
from collections import defaultdict


# Before running the driver on the bsc.txt file, ensure you have put a regular
#   expression pattern in the files repattern1a.txt, repattern1b.txt, and
#   repattern2a.txt. The patterns must be all on the first line

def pages (page_spec : str, unique :  bool) -> [int]: #result in ascending order
    answer = []
    pattern = r"^([1-9][0-9]*)(?:(?:(:|-)([1-9][0-9]*)(?:(?:\/)([1-9][0-9]*))?))?$"
    seperate = page_spec.split(",")
    for i in seperate:
        m = re.match(pattern, i).groups()
        assert m != None, 'No match'
        if m[1] == None:
            answer.append(int(m[0]))
        else:
            if m[1] == "-":
                assert int(m[2]) >= int(m[0]), f"pages: in page specification {m[0]}-{m[2]}, {m[2]} > {m[0]}"
                if m[3] != None:
                    answer += [k for k in irange(int(m[0]), int(m[2]), int(m[3]))]
                else:
                    answer += [k for k in irange(int(m[0]), int(m[2]))]
            elif m[1] == ":":
                if m[3] != None:
                    answer += [k for k in irange(int(m[0]), int(m[0]) + int(m[2]) - 1, int(m[3]))]
                else:
                    answer += [k for k in irange(int(m[0]), int(m[0]) + int(m[2]) - 1)]
    if unique == True:
        answer = list(set(answer))
    return sorted(answer)

def expand_re(pat_dict:{str:str}):
    for k,v in pat_dict.items():
        keys_list = re.split('#', v)
        stored_val = v
        for i in keys_list:
            if i in pat_dict:
                pattern = re.compile("#" + i + "#")
                stored_val = re.sub(pattern, '(?:' + pat_dict[i] + ')', stored_val)
        pat_dict[k] = stored_val


if __name__ == '__main__':
    
    p1a = open('repattern1a.txt').read().rstrip() # Read pattern on first line
    print('Testing the pattern p1a: ',p1a)
    for text in open('bm1.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p1a,text)
        print(' ','Matched' if m != None else "Not matched")
        
    p1b = open('repattern1b.txt').read().rstrip() # Read pattern on first line
    print('\nTesting the pattern p1b: ',p1b)
    for text in open('bm1.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p1b,text)
        print('  ','Matched with groups ='+ str(m.groups()) if m != None else 'Not matched' )
        
        
    p2 = open('repattern2a.txt').read().rstrip() # Read pattern on first line
    print('\nTesting the pattern p2: ',p2)
    for text in open('bm2a.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p2,text)
        print('  ','Matched with groups ='+ str(m.groups()) if m != None else 'Not matched' )
        
    print('\nTesting pages function')
    for text in open('bm2b.txt'):
        text = text.rstrip().split(';')
        text,unique = text[0], text[1]=='True'
        try:
            p = pages(text,unique)
            print('  ','pages('+text+','+str(unique)+') = ',p)
        except:
            print('  ','pages('+text+','+str(unique)+') = raised exception')
        
    
    print('\nTesting expand_re')
    pd = dict(digit = r'[0-9]', integer = r'[+-]?#digit##digit#*')
    print('  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary
    # {'digit': '[0-9]', 'integer': '[+-]?(?:[0-9])(?:[0-9])*'}
    
    pd = dict(integer       = r'[+-]?[0-9]+',
              integer_range = r'#integer#(..#integer#)?',
              integer_list  = r'#integer_range#(?,#integer_range#)*',
              integer_set   = r'{#integer_list#?}')
    print('\n  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary 
    # {'integer': '[+-]?[0-9]+',
    #  'integer_range': '(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?',
    #  'integer_list': '(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?)(?,(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?))*',
    #  'integer_set': '{(?:(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?)(?,(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?))*)?}'
    # }
    
    pd = dict(a='correct',b='#a#',c='#b#',d='#c#',e='#d#',f='#e#',g='#f#')
    print('\n  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary 
    # {'a': 'correct',
    #  'b': '(?:correct)',
    #  'c': '(?:(?:correct))',
    #  'd': '(?:(?:(?:correct)))',
    #  'e': '(?:(?:(?:(?:correct))))',
    #  'f': '(?:(?:(?:(?:(?:correct)))))',
    #  'g': '(?:(?:(?:(?:(?:(?:correct))))))'
    # }
    
    print()
    print()
    import driver
    driver.default_file_name = "bscq2F19.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()