from collections import defaultdict
def solve_root(f : callable, error : float) -> callable:
    if error <= 0:
        raise AssertionError("Input cannot be negative or 0!")
    def inside(negf, posf):
        inside.iterations = 0
        if f(negf) >= 0 or f(posf) < 0:
            raise AssertionError("Invalid input!")
        while abs(negf - posf) > error:
            midpoint = (negf + posf) / 2
            if f(midpoint) < 0:
                negf = midpoint
            else:
                posf = midpoint
            inside.iterations += 1
        return (posf + negf) / 2
    return inside



def by_diversity(db : {int:{str:int}}) -> [(int,int)]:
    return sorted([(k, len(v)) for k,v in db.items()], key = lambda x: x[1], reverse = True)



def by_size(db : {int:{str:int}}) -> [int]:
    return [i[0] for i in sorted([(k, sum(v.values())) for k,v in db.items()], key = lambda x: x[1], reverse = True)]



def by_party(db : {int:{str:int}}) -> [str]:
    vote_dict = defaultdict(int)
    for i in db.values():
        for k,v in i.items():
            vote_dict[k] += v
    return [k for k,v in sorted(vote_dict.items(), key = lambda x: x[1], reverse = True)]



def registration_by_state(db : {int:{str:int}}, state_zips : {str:{int}}) -> {str:{str:int}}:
    answer = dict()
    for i in state_zips:
        if len(state_zips[i]) > 0:
            answer[i] = dict()
    for i in state_zips:
        for j in state_zips[i]:
            for k,v in db.items():
                if k == j:
                    for x in v:
                        answer[i][x] = 0
#     answer = defaultdict(lambda: defaultdict(int))
    for k,v in state_zips.items():
        for i in v:
            for j in db[i]:
                answer[k][j] += db[i][j]
    return answer
        
            



if __name__ == '__main__':
    # This code is useful for debugging your functions, especially
    #   when they raise exceptions: better than using driver.driver().
    # Feel free to add more tests (including tests showing in the bsc.txt file)
    # Use the driver.driver() code only after you have removed any bugs
    #   uncovered by these test cases.
    
    import math
    
    
    print('\nTesting solve_root')
    def f(x):
        return 3*x**4 + 3*x**3 - 1 
    rooter = solve_root(f, .0001)
    r = rooter(0,1)
    print(f'root 1 is approximately {r} where f({r}) = {f(r)} using {rooter.iterations} iterations')
    r = rooter(-1,-2)
    print(f'root 2 is approximately {r} where f({r}) = {f(r)} using {rooter.iterations} iterations')
    rooter = solve_root(lambda x : 23*math.sqrt(x) - (10*math.log2(x)**2+1000), .001)
    r = rooter(10000,20000)
    print(f'root is approximately {r} where f({r}) = {f(r)} using {rooter.iterations} iterations')


    print('\nTesting by_diversity')
    db1 = {1: {'d': 15, 'i': 15,          'r': 15},
           2: {'d': 12,                   'r':  8},
           3: {'d': 10, 'i': 30, 'l': 20, 'r': 22},
           4: {'d': 30, 'l': 20,          'r': 30},
           5: {'i': 15, 'l': 15,          'r': 15}}
    print(by_diversity(db1))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20                  },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(by_diversity(db2))
    
    
    print('\nTesting by_size')
    db1 = {1: {'d': 15, 'i': 15,          'r': 15},
           2: {'d': 12,                   'r':  8},
           3: {'d': 10, 'i': 30, 'l': 20, 'r': 22},
           4: {'d': 30, 'l': 20,          'r': 30},
           5: {'i': 15, 'l': 15,          'r': 15}}
    print(by_size(db1))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20,                 },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(by_size(db2))


    print('\nTesting by_party')
    db1 = {1: {'d': 15, 'i': 15,          'r': 15},
           2: {'d': 12,                   'r':  8},
           3: {'d': 10, 'i': 30, 'l': 20, 'r': 22},
           4: {'d': 30, 'l': 20,          'r': 30},
           5: {'i': 15, 'l': 15,          'r': 15}}
    print(by_party(db1))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20,                 },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(by_party(db2))
    
    
    print('\nTesting registration_by_state')
    db1 = {1: {'d': 15, 'i': 15, 'r': 15}, 2: {'d': 12, 'r':  8}, 3: {'d': 10, 'i': 30, 'l': 20, 'r': 22}, 4: {'d': 30, 'l': 20, 'r': 30}, 5: {'i': 15, 'l': 15, 'r': 15}}
    print(registration_by_state(db1,{'CA': {1,3}, 'WA': {2,4,5}}))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20,                 },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(registration_by_state(db2,{'CA' : {1000,3000,7000}, 'WA': {2000,4000,5000,8000}, 'OR' : {6000}, 'NV' : {}}))


    
    print('\ndriver testing with batch_self_check:')
    import driver
    driver.default_file_name = "bscq1F19.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()           

