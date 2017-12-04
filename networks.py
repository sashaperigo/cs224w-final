from defs import PRIMITIVE_TYPES, TERMINAL_TYPES, TERMINAL_MARKER
from util import evolve_type, get_weighted_euclidean_distance, get_spread_weight_series

from collections import defaultdict
import numpy as np

# do caching where necessary

def watts_strogatz_sampler(dataframe, source_index, sink_indices_list, spread_weights, alpha=2, percent=0.2):
    proportions = np.array([
        1 / np.power(get_weighted_euclidean_distance(dataframe, source_index, sink_index, spread_weights), alpha) \
            for sink_index in sink_indices
    ])
    sampled = set(np.random.choice(
        sink_indices_list,
        int(percent * len(sink_indices_list)),
        p=proportions/np.sum(proportions)
    ))
    assert len(sampled) > 1
    return sampled


def erdos_renyi_sampler(dataframe, source_index, sink_indices_list, percent=0.2):
    assert (percent <= 1) and (percent >= 0)
    sampled = set(np.random.choice(sink_indices_list, int(percent * len(sink_indices_list))))
    assert len(sampled) > 1
    return sampled


def complete_sampler(dataframe, source_index, sink_indices_list):
    return set(sink_indices_list)


# Note: we're making the assumption here that primitive types cannot stay
# primitive, they must evolve. This makes for an easier computation as we
# don't have to worry about self loops.
def build_graph(dataframe, types_to_indices, sampler_fn, sampler_fn_kwargs):
    edges = defaultdict(set)
    for primitive_type in PRIMITIVE_TYPES:
        primitive_indices = types_to_indices[primitive_type]
        successor_types = evolve_type(primitive_type)
        successor_indices = set()
        for successor_type in successor_types:
            successor_indices = successor_indices.union(types_to_indices[successor_type])
        successor_indices_list = list(successor_indices)
        for primitive_source in primitive_indices:
            successor_sinks = sampler_fn(dataframe, primitive_source, successor_indices_list, **sampler_fn_kwargs)
            edges[primitive_source] = successor_sinks

    for terminal_type in TERMINAL_TYPES:
        for terminal_source in types_to_indices[terminal_type]:
            edges[terminal_source] = {TERMINAL_MARKER}

    return edges
