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
    true_count = False
    false_count = False
    temp = ll
    value = temp.value
    while temp.next != None:
        if p(value):
            if true_count == False:
                true_front = true_rear = LN(value)
                true_count = True
            else:
                true_front = LN(value)
                true_front.next = true_rear
                true_rear = true_front
        else:
            if false_count == False:
                false_front = false_rear = LN(value)
                false_count = True
            else:
                false_front = LN(value)
                false_front.next = false_rear
                false_rear = false_front
        temp = temp.next
        value = temp.value
    return (true_front, false_front)

# def separate(ll,p):
#     count_t = False
#     count_f = False
#     while ll != None:
#         if p(ll.value):
#             if not count_t:
#                 t1 = t2 = LN(ll.value)
#                 count_t = True
#             else:
#                 t2.next = LN(ll.value)
#                 t2 = t2.next
#         else:
#             if not count_f:
#                 f1 = f2 = LN(ll.value)
#                 count_f = True
#             else:
#                 f2.next = LN(ll.value)
#                 f2 = f2.next
#         ll = ll.next
#     return t1, f1



# Define is_min_heap RECURSIVELY

def is_min_heap(t):
    if not t:
        return True
    elif t.left == t.right == None:
        return True
    elif t.left == None:
        if t.value < t.right.value:
            return is_min_heap(t.right)
        return False
    elif t.right == None:
        if t.value < t.left.value:
            return is_min_heap(t.left)
        return False
    else:
        if t.value < t.left.value and t.value < t.right.value:
            return is_min_heap(t.left) and is_min_heap(t.right)
        return False



# Define bases RECURSIVELY

def bases(c):
    if not c.__bases__:
        return {c}
    answer = {c}
    for i in c.__bases__:
        answer = answer.union(bases(i))
    return answer


# Define the derived popdict class

class popdict(dict):
    def __init__(self,initial_dict=[],**kargs):
        dict.__init__(self, initial_dict, **kargs)
        self.storage = defaultdict(int)
        if initial_dict:
            for i in initial_dict:
                self.storage[i[0]] += 1
        for i in kargs:
            self.storage[i] += 1
        
    def __getitem__(self,key):
        if key in self:
            self.storage[key] += 1
        return dict.__getitem__(self, key)
        
    def __setitem__(self,key,value): 
        dict.__setitem__(self, key, value)
        self.storage[key] += 1
            
    def __delitem__(self,key):
        dict.__delitem__(self, key)
        del self.storage[key]

    def __call__(self,key):
        return self.storage[key] if key in self.storage else 0
    
    def clear(self):
        dict.clear(self)
        dict.clear(self.storage)
        
    def __iter__(self):
        for i in sorted(self.storage, key = lambda x: -self.storage[x]):
            yield i
        



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
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
          
    t = list_to_tree([1,[2,None,None],[3,None,None]]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
    
    t = list_to_tree([2,[1,None,None],[3,None,None]]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
          
    t = list_to_tree([3,[2,None,None],[1,None,None]]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
    
    t = list_to_tree([1,None,[3,None,None]]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
           
    t = list_to_tree([1,[2,None,None],None]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
    
    t = list_to_tree([3,None,[1,None,None]]) 
    print('\nTree is\n',str_tree(t),end='')
    print('is_min_heap =',is_min_heap(t))  
           
    t = list_to_tree([2,[1,None,None],None]) 
    print('\nTree is\n',str_tree(t),end='')
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
    print('\nTree is\n',str_tree(t),end='')
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
    print('\nTree is\n',str_tree(t),end='')
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
    print('\nTree is\n',str_tree(t),end='')
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
    
     
    
# Result from running driver

# Testing separate
# 18->16->14->12->10->8->6->4->2->0->None and 19->17->15->13->11->9->7->5->3->1->None
# 19->17->13->11->7->5->3->2->None and 18->16->15->14->12->10->9->8->6->4->1->0->None
# 10->9->8->7->6->5->4->3->2->1->0->None and 19->18->17->16->15->14->13->12->11->None
# 
# Testing is_min_heap
# 
# Tree is
#  is_min_heap = True
# 
# Tree is
#  ..3
# 1
# ..2
# is_min_heap = True
# 
# Tree is
#  ..3
# 2
# ..1
# is_min_heap = False
# 
# Tree is
#  ..1
# 3
# ..2
# is_min_heap = False
# 
# Tree is
#  ..3
# 1
# is_min_heap = True
# 
# Tree is
#  1
# ..2
# is_min_heap = True
# 
# Tree is
#  ..1
# 3
# is_min_heap = False
# 
# Tree is
#  2
# ..1
# is_min_heap = False
# 
# Tree is
#  ..12
# ........70
# ......30
# ........40
# ....24
# 5
# ..8
# ........82
# ......46
# ........70
# ....16
# ......32
# is_min_heap = True
# 
# Tree is
#  ..12
# ........70
# ......30
# ........40
# ....30
# 5
# ..8
# ........82
# ......32
# ........70
# ....16
# ......32
# is_min_heap = False
# 
# Tree is
#  ..12
# ........70
# ......30
# ........40
# ....30
# 5
# ..8
# ........82
# ......46
# ........70
# ....16
# ......32
# is_min_heap = False
# 
# Testing bases
# {<class '__main__.D'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.G'>, <class 'object'>, <class '__main__.C'>, <class '__main__.F'>}
# {<class '__main__.A'>, <class '__main__.E'>, <class 'object'>, <class '__main__.H'>, <class '__main__.D'>, <class '__main__.G'>, <class '__main__.F'>, <class '__main__.C'>, <class '__main__.B'>}
# 
# Testing popdict
# initial
# {'a': 100, 'b': 200, 'c': 300}
# [('a', 1), ('b', 1), ('c', 1), ('x', 0)]
# 
# after some updates
# {'a': 104, 'b': 200, 'c': 307}
# [('a', 5), ('b', 3), ('c', 7), ('x', 0)]
# 
# iteration order = ['c', 'a', 'b']
# 
# after delete
# {'b': 200, 'c': 307}
# [('a', 0), ('b', 3), ('c', 7), ('x', 0)]
# 
# after clear
# {}
# [('a', 0), ('b', 0), ('c', 0), ('x', 0)]
    
