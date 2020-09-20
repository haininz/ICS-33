from performance import Performance
from goody import irange
from graph_goody import random_graph,spanning_tree
# Put script below to generate data for Problem #1
# In case you fail, the data appears in sample8.pdf in the helper folder
def create_random(i):
    global graph
    graph = random_graph(i, lambda n : 10*n)

for i in irange(0,7):
    p = Performance(lambda : spanning_tree(graph), lambda: create_random(2**i * 1000), 5, f'\nSpanning Tree of size {2**i *1000}')
    p.evaluate()
    p.analyze()