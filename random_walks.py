# import numpy as np
# from collections import defaultdict
# from defs import PRIMITIVE_TYPES, EVOLUTIONARY_CHAIN, TERMINAL_MARKER, TERMINAL_TYPES


# def random_walk(cell_types_to_indices, indices_to_cell_types, sampler_fn, n=1):
#     indices_to_actions = defaultdict(list)

#     for primitive_type in PRIMITIVE_TYPES:
#         print "Running random walks from %i cells of type %s..." % (len(cell_types_to_indices[primitive_type]), primitive_type)
#         for index in cell_types_to_indices[primitive_type]:
#             actions = []
#             curr = index
#             cell_type = primitive_type
#             while True:
#                 if cell_type in TERMINAL_TYPES:
#                     break

#                 successor_types = EVOLUTIONARY_CHAIN[cell_type]
#                 # Most cell types just have one successor stage, but HF can
#                 # evolve into either 4G or 4GF.
#                 sink_indices = []
#                 for successor_type in successor_types:
#                     sink_indices += list(cell_types_to_indices[successor_type])

#                 cell_type = successor_types[0]

#                 # This percent should return exactly one node.
#                 percent = float(1) / len(sink_indices)
#                 successor = list(sampler_fn(curr, sink_indices, percent=percent))[0]
#                 actions.append(successor)
#                 curr = successor

#                 # indices_to_actions[index].append(actions)

#     return indices_to_actions
