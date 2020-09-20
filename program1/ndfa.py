# Submitter: haininz(Zhou, Haining)
# Partner:   clyu4(Lyu, Chenhan)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
import goody
from collections import defaultdict

def read_ndfa(file : open) -> {str:{str:{str}}}:
    final_dict = defaultdict(dict)
    for line in file:
        process_list = line.rstrip('\n').split(';')
        if len(process_list) == 1:
            final_dict[process_list[0]] = {}
        final_dict[process_list[0]] = {n: set() for n in [k for k in process_list if process_list.index(k) % 2]}
        for n, m in zip([k for k in process_list if process_list.index(k) % 2], [v for v in process_list if process_list.index(v) % 2 == 0][1:]):
            final_dict[process_list[0]][n].add(m)
    return final_dict


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    big_str = ''
    list_small = []
    for i, j in sorted(ndfa.items()):
        big_str += ('  ' + i + ' transitions: ')
        for k, v in sorted(j.items()):
            list_small.append((k, sorted(list(v))))
        big_str += str(list_small)+'\n'
        list_small = []
    return big_str

       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    process_list = [state]
    for num in inputs:
        if len(state) == 0:
            break
        if type(state) == str:
            process_list.append((num, ndfa[state][num]))
            state = set(ndfa[state][num])
        else:
            count = set()
            for substate in state:
                if num not in ndfa[substate]:
                    continue
                count.update(ndfa[substate][num])
            process_list.append((num, count))
            state = count
    return process_list


def interpret(result : [None]) -> str:
    huge_str = f'Start state = {result[0]}\n'
    for i in result[1:-1]:
        huge_str += f'  Input = {i[0]}; new possible states = {sorted(list(i[1]))}\n'
    if result[-1][1] != None:
        huge_str += f'  Input = {result[-1][0]}; new possible states = {sorted(list(result[-1][1]))}\nStop state(s) = {sorted(list(result[-1][1]))}\n'
    else:
        huge_str += f'  Input = {result[-1][0]}; illegal input: simulation terminated\nStop state = None\n'
    return huge_str



if __name__ == '__main__':
    # Write script here
    rule = goody.safe_open("Enter the file name describing this Non-Deterministic Finite Automaton", 'r', 'Illegal file name')
    print("\nThe Description of the file entered for this Non-Deterministic Finite Automaton")
    rule_dict = read_ndfa(rule)
    print(ndfa_as_str(rule_dict))
    sequence = goody.safe_open("Enter the file name describing a sequence of start-states and all their inputs", 'r', 'Illegal file name')
    print()
    for line in sequence:
        print("Start tracing this NDFA in its start-state")
        process_list = process(rule_dict, line.rstrip("\n").split(";")[0], line.rstrip("\n").split(";")[1:])
        print(interpret(process_list))
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
