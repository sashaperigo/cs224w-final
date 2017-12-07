from collections import defaultdict
from defs import PRIMITIVE_TYPES, EVOLUTIONARY_CHAIN, TERMINAL_MARKER


def random_walk(cell_types_to_indices, indices_to_cell_types, sampler_fn):
    indices_to_actions = defaultdict(list)

    for cell_type in PRIMITIVE_TYPES:
        for index in cell_types_to_indices[cell_type]:
            actions = []
            curr = index
            while curr != TERMINAL_MARKER:
                successor_types = EVOLUTIONARY_CHAIN[indices_to_cell_types[curr]]
                # Most cell types just have one successor stage, but HF can
                # evolve into either 4G or 4GF.
                for successor_type in successor_types:
                    sink_indices = cell_types_to_indices[successor_type]
                    # This percent should return exactly one node.
                    percent = float(1) / len(sink_indices)
                    successor = sampler_fn(curr, sink_indices, percent=percent)
                    actions.append(successor)
            indices_to_actions[index] = actions
