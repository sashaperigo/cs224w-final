from cell_search_problem import CellSearchProblem
from defs import PRIMITIVE_TYPES

def find_shortest_paths(edges_dict, types_to_indices, cost_fn):
    actions = {}
    for primitive_type in PRIMITIVE_TYPES:
        for primitive_start_index in types_to_indices[primitive_type]:
            actions[primitive_start_index] = find_shortest_path_from(
                primitive_start_index,
                edges_dict,
                cost_fn,
            )
    return actions

def find_shortest_path_from(start_index, edges_dict, cost_fn):
    cs = CellSearchProblem(start_index, edges_dict, cost_fn)
    ucs = UniformCostSearch(verbose = 1)
    ucs.solve(cs)
    print(ucs.actions)
    return ucs.actions