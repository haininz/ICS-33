def separate(p : callable, l : [object]) -> ([object],[object]):
    if l == []:
        return [],[] 
    else:
        t_list,f_list = separate(p,l[1:])
        if p(l[0]):
            return [l[0]]+t_list, f_list
        else:
            return t_list, [l[0]] + f_list

# local function version, with no local variables  
# def separate(p,l):
#     def merge(f,r):
#         return (f[0]+r[0],f[1]+r[1])
#     if l == []:
#         return [],[]
#     else:
#         return merge( ([l[0]],[]) if p(l[0]) else ([],[l[0]]) , separate(p,l[1:]) )

def is_sorted(l : [object]):
    if len(l) <= 1:
        return True
    else:
        return l[0] < l[1] and is_sorted(l[1:])


def sort(l : [object]) -> [object]:
    if l == []:
        return []
    else:
        low,high = separate(lambda x : x<=l[0], l[1:])
        return sort(low) + [l[0]] + sort(high)
    
    
# local function version, with no local variables
# def sort(l):
#     def combine(low_high,mid):
#         return sort(low_high[0]) + [mid] + sort(low_high[1])
#     if l == []:
#         return []
#     else:
#         return combine (separate(lambda x : x<=l[0], l[1:]),l[0])


def merge_chars(a : str, b : str) -> str:
    if a == '' or b =='':
        return a+b
#     # could make 3 separate base cases for both or one == ''
#     if a == '' and b == '':
#         return ''
#     elif a == '':
#         return b
#     elif b == '':
#         return a
    else:
        if a[0] <= b[0]:
            return a[0]+merge_chars(a[1:],b)
        else:
            return b[0]+merge_chars(a,b[1:])

 
def nested_count(l : 'any nested list of int', a : int) -> int:
    if l == []:
        return 0
    else:
        return (int(l[0]==a) if type(l[0]) is int else nested_count(l[0],a))  + nested_count(l[1:],a)
#         if type(l[0]) is not list:
#             return int(l[0]==a ) + nested_count(l[1:],a)
#         else:
#             return nested_count(l[0],a) + nested_count(l[1:],a)





if __name__=="__main__":
    import predicate,random,driver
    from goody import irange
    
    print('Testing separate')
    print(separate(predicate.is_positive,[]))
    print(separate(predicate.is_positive,[1, -3, -2, 4, 0, -1, 8]))
    print(separate(predicate.is_prime,[i for i in irange(2,20)]))
    print(separate(lambda x : len(x) <= 3,'to be or not to be that is the question'.split(' ')))
    print(separate(lambda x : x <= 'm','to be or not to be that is the question'.split(' ')))
     
    print('\nTesting is_sorted')
    print(is_sorted([]))
    print(is_sorted([0]))
    print(is_sorted([-5,-4]))
    print(is_sorted([1,2,3,4,5,6,7]))
    print(is_sorted([1,2,3,7,4,5,6]))
    print(is_sorted([1,2,3,4,5,6,5]))
    print(is_sorted([7,6,5,4,3,2,1]))
    
    print('\nTesting sort')
    print(sort([1,2,3,4,5,6,7]))
    print(sort([7,6,5,4,3,2,1]))
    print(sort([4,5,3,1,2,7,6]))
    print(sort([1,7,2,6,3,5,4]))
    l = [i+1 for i in range(30)]
    random.shuffle(l)
    print(l)
    print(sort(l))
    
    print('\nTesting merge_chars')
    print(merge_chars('',''))
    print(merge_chars('','abc'))
    print(merge_chars('abc',''))
    print(merge_chars('ace','bdf'))
    print(merge_chars('abc','xyz'))
    print(merge_chars('abxy','lmzzz'))
    print(merge_chars('acdeghilmnosu','bfjkpqrtvwxyz'))
    print(merge_chars('bcgprvyz','adefhijklmnoqstuwx'))
    print(merge_chars('cdefghijklmnpqrstuvw','aboxyz'))
   
    print('\nTesting nested_count')
    print(nested_count([1,2,4,1,8,1,3,2,1,1],1))
    print(nested_count([[1,2,4,1,8],[1,3,2],1,1],1))
    print(nested_count([[1,2,[4,[1],8],[1,3,2]],[1,1]],1))
    

    driver.default_file_name = "bscq5F19.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
    
