from collections import defaultdict
from Queue import PriorityQueue
from defs import PRIMITIVE_TYPES, TERMINAL_MARKER
from search_util import CellSearchProblem, UniformCostSearch

import numpy as np


# class UniformCostSearch:
#     def __init__(self, start_index, edges_dict, cost_fn):
#         self.start_index = start_index
#         self.edges_dict = edges_dict
#         self.cost_fn = cost_fn
#         self.actions = []

#     def is_end(self, index):
#         return index == TERMINAL_MARKER

#     # Returns a list of the actions the starting cell takes to transition to
#     # the closest terminal cell in the format: [ (index, cost), (index, cost) ]
#     # Each cost represents the cost of a single step, not the total cost up
#     # until that point.
#     def solve(self):
#         print("SOLVING")
#         visited = set()
#         queue = PriorityQueue()
#         queue.put((0, self.start_index))

#         while queue:
#             cost, curr_index = queue.get()

#             if curr_index not in visited:
#                 visited.add(curr_index)
#                 self.actions.append(curr_index)

#                 if self.is_end(curr_index):
#                     print("FOUND END")
#                     # Exclude the first action, as it is the starting state.
#                     self.actions = self.actions[1:]
#                     print(self.actions)
#                     return self.actions

#                 for neighbor in self.edges_dict[curr_index]:
#                     if neighbor not in visited:
#                         total_cost = cost + self.cost_fn(curr_index, neighbor)
#                         queue.put((total_cost, neighbor))


def find_shortest_paths(edges_dict, types_to_indices, cost_fn):
    actions = {primitive_type: defaultdict(list) for primitive_type in PRIMITIVE_TYPES}
    for primitive_type in PRIMITIVE_TYPES:
        # count = 0
        for primitive_start_index in types_to_indices[primitive_type]:
            # if count == 5: break
            actions[primitive_type][primitive_start_index] = find_shortest_path_from(
                primitive_start_index,
                edges_dict,
                cost_fn,
            )
        #    count += 1
    return actions


def find_shortest_path_from(start_index, edges_dict, cost_fn):
    ucs = UniformCostSearch()
    csp = CellSearchProblem(start_index, edges_dict, cost_fn)
    ucs.solve(csp)
    print(ucs.actions)
    return ucs.actions
