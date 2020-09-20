from collections import defaultdict

def solve_root(f : callable, error : float) -> callable:
    assert error > 0, 'q1solutions.solve0: error('+str(error)+') not int > 0'
    
    def solveit(negf: float, posf : float) -> float:
        if f(negf) >= 0  and f(posf) < 0:
            negf,posf = posf,negf
        assert f(negf) <  0, 'q1solutions.solve_root.solveit: with negf('+str(negf)+') f(negf) >= 0'
        assert f(posf) >= 0, 'q1solutions.solve_root.solveit: with posf('+str(posf)+') f(posf) <  0'
        solveit.iterations = 0
#         print(f'iteratiion {solveit.iterations}: negf={negf} / posf={posf}')
        while abs(negf-posf) > error:
            solveit.iterations += 1
            mid = (negf+posf)/2
            if f(mid) < 0:
                negf = mid
            else:    
                posf = mid
#             print(f'iteratiion {solveit.iterations}: negf={negf} / posf={posf}')
        return (negf+posf)/2
    
    solveit.iterations = None
    return solveit




# To write small function bodies I used the following abbreviations
# z for a zipcode; p for a party; r for number of registrations.

def by_diversity(db : {int:{str:int}}) -> [(int,int)]:
    zipcodes_parties = []
    for z,pr in db.items():
        zipcodes_parties.append( (z, len(pr.values())) )
    return sorted(zipcodes_parties, key = lambda zps : (-zps[1],zps[0]))
    # or, in 1 line
    return sorted ( ((z,len(pr.values())) for z,pr in db.items()), key = lambda zps : (-zps[1],zps[0]))


def by_size(db : {int:{str:int}}) -> [int]:
    return sorted ( db.keys(), key = lambda z : (-sum(db[z].values()),z))


def by_party(db : {int:{str:int}}) -> [str]:
    parties = set()
    for pr in db.values():
        for p in pr.keys():
            parties.add(p)
            
    party_registration = {}
    for p in parties:
        registration = 0
        for pr in db.values():
            if p in pr:
                registration += pr[p]
        party_registration[p] = registration
    return sorted( party_registration.keys(), key = lambda p : (-party_registration[p],p) )    
    # or, in 1 line
    return sorted ( {p for pr in db.values() for p in pr}, key = lambda p : (-sum((pr.get(p,0) for pr in db.values())),p))


def registration_by_state(db : {int:{str:int}}, state_zips : {str:{int}}) -> {str:{str:int}}:
    # Note each default has argument callable with no arguments: saves lots of ifs
    answer = defaultdict(lambda : defaultdict(int))
    for state, zips in state_zips.items():
        for z in zips:
            for party, registration in (db[z].items() if z in db else []):
                answer[state][party] += registration
    return answer # return defaultdict of defaultdict
    # or return a dict of dict; here s is state
    return {s: {p: z for p,z in pz.items()} for s,pz in answer.items()}
 

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
           7000: {                  'l': 20,                 },
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
    print(registration_by_state(db2,{'CA' : {100,3000,7000}, 'WA': {2000,4000,5000,8000}, 'OR' : {6000}, 'NV' : {}}))


    
    print('\ndriver testing with batch_self_check:')
    import driver
    driver.default_file_name = "bscq1F19.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()           
