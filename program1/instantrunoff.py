# Submitter: haininz(Zhou, Haining)
# Partner:   clyu4(Lyu, Chenhan)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
import goody
from collections import defaultdict
from builtins import set

def read_voter_preferences(file : open):
    vote_name = defaultdict(list)
    for line in file:
        vote_name[line.rstrip('\n').split(';')[0]].extend(line.rstrip('\n').split(';')[1:])
    return vote_name


def dict_as_str(d : {None:None}, key : callable=None, reverse : bool=False) -> str:
    big_str = ''
    for i in sorted(d, key = key, reverse = reverse):
        big_str += "  " + i + " -> " + str(d[i]) + "\n"
    return big_str


def evaluate_ballot(vp : {str:[str]}, cie : {str}) -> {str:int}:
    vote_num = dict()
    for i in list(vp.values())[0]:
        if i in cie:
            vote_num[i] = 0
    count = 0
    while count < len(list(vp.values())):
        for j in list(vp.values())[count]:
            if j in cie:
                vote_num[j] += 1
                break
        count += 1
    return vote_num

def remaining_candidates(vd : {str:int}) -> {str}:
    candidate_set = set()
    for k,v in vd.items():
        if v != min(list(vd.values())):
            candidate_set.add(k)
    return candidate_set


def run_election(vp_file : open) -> {str}:
    ballot_count = 1
    vd = read_voter_preferences(vp_file)
    print("Preferences: voter -> [candidates in order]")
    print(dict_as_str(vd))
    rc = {i for i in list(vd.values())[0]}
    while len(rc) != 1:
        if len(list(vd.values())[0]) <= ballot_count:
            break
        votes = evaluate_ballot(vd, rc)
        print(f'Vote count on ballot #{ballot_count}: candidates (sorted alphabetically) using only candidates in set {rc}')
        for i, j in sorted(votes.items()):
            print(f'{i} -> {j}')
        print(f'Vote count on ballot #{ballot_count}: candidates (sorted numerically) using only candidates in set {rc}')
        for i, j in sorted(votes.items(), key = (lambda x: x[1]), reverse = True):
            print(f'{i} -> {j}')
        rc =  remaining_candidates(votes)
        ballot_count += 1
    print(f'Election winner is {set(list(rc)[0])}' if len(rc) == 1 else 'Not any unique winner: all remaining candidates on the ballot tie')
    return rc if len(rc) == 1 else set()
    
        
if __name__ == '__main__':
    # Write script here
    vote = goody.safe_open("Enter the file name describing all the voter preferences", 'r', 'Illegal file name')
    run_election(vote)
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
