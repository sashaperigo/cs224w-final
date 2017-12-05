from cell_search import find_shortest_paths
from costs import euclidean_cost
from defs import MEASUREMENTS_PATH, TYPES_PATH
from networks import build_graph, complete_sampler
from util import get_normalized_data, get_cell_types_to_indices


data = get_normalized_data(MEASUREMENTS_PATH, TYPES_PATH)
cell_types_to_indices = get_cell_types_to_indices(data)
example = build_graph(cell_types_to_indices, complete_sampler, {})


find_shortest_paths(example, cell_types_to_indices, euclidean_cost)
