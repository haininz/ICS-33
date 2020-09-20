import cProfile
from graph_goody import random_graph, spanning_tree
import pstats

# Put script below to generate data for Problem #2
# In case you fail, the data appears in sample8.pdf in the helper folder
new_graph = random_graph(15000, lambda n : 10*n)
cProfile.run('spanning_tree(new_graph)', 'result')
p = pstats.Stats('result')
p.strip_dirs().sort_stats('ncalls').print_stats(10)
p.strip_dirs().sort_stats('tottime').print_stats(10)