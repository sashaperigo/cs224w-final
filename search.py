from cell_search import CellSearch
from search_util import UniformCostSearch
import csv
import ingest_data
import collections
import json

cells_file = 'norm.csv'
types_file = 'celltypes.txt'
genes_file = 'genes.txt'

data, genes, transitions = ingest_data.ingest(cells_file, types_file, genes_file)

num_states_explored = collections.defaultdict(int)
total_cost = collections.defaultdict(float)
actions = collections.defaultdict(list)

for cell_type in data:
    if cell_type != '4G' and cell_type != '4GF':
        for starting_state in data[cell_type]:
            cs = CellSearch(data, genes, transitions, starting_state)
            ucs = UniformCostSearch(verbose = 1)
            ucs.solve(cs)
            num_states_explored[starting_state] = ucs.numStatesExplored
            total_cost[starting_state] = ucs.totalCost
            actions[starting_state] = ucs.actions
