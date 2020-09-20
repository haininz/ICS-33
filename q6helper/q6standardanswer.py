from functools import reduce         # can use for bases
from collections import defaultdict  # can use for popdict


# List Node class and helper functions (to set up problem)

class LN:
    def __init__(self,value,next=None):
        self.value = value
        self.next  = next

def list_to_ll(l):
    if l == []:
        return None
    front = rear = LN(l[0])
    for v in l[1:]:
        rear.next = LN(v)
        rear = rear.next
    return front

def str_ll(ll):
    answer = ''
    while ll != None:
        answer += str(ll.value)+'->'
        ll = ll.next
    return answer + 'None'



# Tree Node class and helper functions (to set up problem)

class TN:
    def __init__(self,value,left=None,right=None):
        self.value = value
        self.left  = left
        self.right = right

def list_to_tree(alist):
    if alist == None:
        return None
    else:
        return TN(alist[0],list_to_tree(alist[1]),list_to_tree(alist[2])) 
    
def str_tree(atree,indent_char ='.',indent_delta=2):
    def str_tree_1(indent,atree):
        if atree == None:
            return ''
        else:
            answer = ''
            answer += str_tree_1(indent+indent_delta,atree.right)
            answer += indent*indent_char+str(atree.value)+'\n'
            answer += str_tree_1(indent+indent_delta,atree.left)
            return answer
    return str_tree_1(0,atree) 


# Define separate ITERATIVELY

def separate(ll,p):
    t, f = None, None
    while ll != None:
        if p(ll.value):
            t = LN(ll.value,t)
        else:
            f = LN(ll.value,f)
        ll = ll.next
    return (t,f)



# Define is_min_heap RECURSIVELY

def is_min_heap(t):
    if t == None:
        return True
    else:
        return (t.left  == None or t.value < t.left.value)  and\
               (t.right == None or t.value < t.right.value) and\
               is_min_heap(t.left) and is_min_heap(t.right)



# Define bases RECURSIVELY

def bases(c):
    if c is object:  # or, if c.__bases__ == []:
        return {object}
    else:
        return {c}.union( *(bases(x) for x in c.__bases__) )
#         return {c} | reduce( (lambda x,y : x|y), (bases(x) for x in c.__bases__))

# def bases(c):
#     if c.__bases__ == []:
#         return {c:0}
#     else:
#         anc = [{c:-1}] + [bases(c) for c in c.__bases__]
#         return {c: 1+min(one[c] for one in anc if c in one) for cd in anc for c in cd}



# Define the derived popdict base

class popdict(dict):
    def __init__(self,initial_dict=[],**kargs):
        dict.__init__(self,initial_dict,**kargs)
        self._popularity = defaultdict(int)
        for k in dict.__iter__(self):
            self._popularity[k] = 1
        
    def __getitem__(self,key):
        answer = dict.__getitem__(self,key)
        self._popularity[key] += 1
        return answer

    def __setitem__(self,key,value):
        dict.__setitem__(self,key,value)
        self._popularity[key] += 1
        
    def __delitem__(self,key):
        del self._popularity[key]
        dict.__delitem__(self,key)
        
    def __call__(self,key):
        return self._popularity.get(key,0)

    def clear(self):
        dict.clear(self)
        self._popularity.clear()
            
    def __iter__(self):
        for k in sorted(self._popularity, key = lambda x : -self._popularity[x]):
            yield k
            

# Testing Script

if __name__ == '__main__':
    print('Testing separate')
    ll = list_to_ll([i for i in range(20)])
    even,odd = separate(ll,lambda x : x%2 == 0) 
    print(str_ll(even)+' and '+str_ll(odd))
    
    import predicate
    prime,composite = separate(ll,predicate.is_prime) 
    print(str_ll(prime)+' and '+str_ll(composite))
    
    small,big = separate(ll,lambda x : x <= 10) 
    print(str_ll(small)+' and '+str_ll(big))
    
    print('\nTesting is_min_heap')
    t = None
    print('\nTree is\n'+str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
          
    t = list_to_tree([1,[2,None,None],[3,None,None]]) 
    print('\nTree is\n'+str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
    
    t = list_to_tree([2,[1,None,None],[3,None,None]]) 
    print('\nTree is\n'+str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
          
    t = list_to_tree([3,[2,None,None],[1,None,None]]) 
    print('\nTree is\n'+str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
    
    t = list_to_tree([1,None,[3,None,None]]) 
    print('\nTree is\n'+str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
           
    t = list_to_tree([1,[2,None,None],None]) 
    print('\nTree is\n'+str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
    
    t = list_to_tree([3,None,[1,None,None]]) 
    print('\nTree is\n'+str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
           
    t = list_to_tree([2,[1,None,None],None]) 
    print('\nTree is\n'+str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
    
    t = list_to_tree(
            [5,
              [8,
                [16,
                   [32,None,None],
                   [46,
                      [70,None,None],
                      [82,None,None]
                   ]
                ],
                None],
              [12,
                 [24,
                    None,
                    [30,
                       [40,None,None],
                       [70,None,None]
                    ]
                 ],
                 None
              ]
            ])
    print('\nTree is\n'+str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
  
    t = list_to_tree(
            [5,
              [8,
                [16,
                   [32,None,None],
                   [32,
                      [70,None,None],
                      [82,None,None]
                   ]
                ],
                None],
              [12,
                 [30,
                    None,
                    [30,
                       [40,None,None],
                       [70,None,None]
                    ]
                 ],
                 None
              ]
            ])
    print('\nTree is\n'+str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  

    t = list_to_tree(
            [5,
              [8,
                [16,
                   [32,None,None],
                   [46,
                      [70,None,None],
                      [82,None,None]
                   ]
                ],
                None],
              [12,
                 [30,
                    None,
                    [30,
                       [40,None,None],
                       [70,None,None]
                    ]
                 ],
                 None
              ]
            ])
    print('\nTree is\n'+str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
      
    
    
    print('\nTesting bases')
    
    class F:pass
    class C:pass
    class G:pass
    class B(F):pass
    class D(G):pass
    class A(B,C,D):pass
    print(bases(A))
    
    class A          : pass    
    class B          : pass
    class C(A)       : pass    
    class D(A,B)     : pass
    class E(A)       : pass
    class F(C,D)     : pass    
    class G(B)       : pass
    class H(E,F,G)   : pass
    print(bases(H))
          
  

    print('\nTesting popdict')
    d = popdict([('a',100)],b=200,c=300)
    print('initial')
    print(d)
    print([(k,d(k)) for k in 'abcx'])
    
    d['a']
    d['b']
    d['b']
    d['a'] = 103
    d['a'] += 1  # accesses d['a'] 2 times: to get value and store value
    d['c'] += 5  # accesses d['c'] 2 times: to get value and store value
    d['c'] += 1  # accesses d['c'] 2 times: to get value and store value
    d['c'] += 1  # accesses d['c'] 2 times: to get value and store value
    try:
        d['x'] # should raise exception: 
        print('Did not raise exception')
    except:
        pass
    
    print('\nafter some updates')
    print(d)
    print([(k,d(k)) for k in 'abcx'])
    
    print('\niteration order =',[k for k in d])
    
    del d['a']
    
    print('\nafter delete')
    print(d)
    print([(k,d(k)) for k in 'abcx'])

    d.clear()
    
    print('\nafter clear')
    print(d)
    print([(k,d(k)) for k in 'abcx'])


    import driver
    driver.default_file_name = "bscq6F19.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
    
     
    
