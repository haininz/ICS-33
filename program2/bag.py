# Submitter: haininz(Zhou, Haining)
# Partner:   clyu4(Lyu, Chenhan)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
from collections import defaultdict
from goody import type_as_str

class Bag:
    def __init__(self, *alist: list) -> None:
        self.bag = defaultdict(int)
        if alist != ():
            for item in alist[0]:
                self.bag[item] += 1

    def __repr__(self) -> str:
        sub_list = []
        for key, item in self.bag.items():
            for i in range(item):
                sub_list.append(key)
        return 'Bag(' + str(sub_list) + ')'

    def __str__(self) -> str:
        if self.bag == defaultdict(int):
            return 'Bag()'
        sub_list = []
        for key, item in self.bag.items():
            sub_list.append(key + str([item]))
        return 'Bag(' + ", ".join(sub_list) + ')'

    def __len__(self) -> int:
        return sum(self.bag.values())

    def unique(self) -> int:
        return len(self.bag.keys())

    def __contains__(self, test_item) -> bool:
        return True if test_item in self.bag.keys() else False

    def add(self, item: str) ->  None:
        if item not in self.bag.keys():
            self.bag[item] = 1
        else:
            self.bag[item] += 1
    def count(self, item):
        return 0 if item not in self.bag.keys() else self.bag[item]

    def __add__(self, another) -> 'Bag':
        if type(another) != Bag:
            raise TypeError
        sub_list = []
        for key, item in self.bag.items():
            for i in range(item):
                sub_list.append(key)
        for key, item in another.bag.items():
            for i in range(item):
                sub_list.append(key)
        return Bag(sub_list)
    
    def remove(self, item):
        if item in self.bag.keys():
            self.bag[item] -= 1
            if self.bag[item] == 0:
                del self.bag[item]
        else:
            raise ValueError
        
    def __eq__(self, item):
        if type(self) != type(item):
            return False
        else:
            return True if self.bag == item.bag else False
        
    def __ne__(self, item):
        if type(self) != type(item):
            return True
        else:
            return True if self.bag != item.bag else False
        
    def __iter__(self):
        sub_list = []
        for key, item in self.bag.items():
            for i in range(item):
                sub_list.append(key)
        return iter(sub_list)
        


if __name__ == '__main__':
    #Put your own test code here to test Bag before doing bsc tests
    print('Start simple testing')

    import driver
    driver.default_file_name = 'bscp21F19.txt'
#     driver.default_show_exception =True
#     driver.default_show_exception_message =True
#     driver.default_show_traceback =True
    driver.driver()
