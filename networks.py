from costs import euclidean_cost
from defs import PRIMITIVE_TYPES, TERMINAL_TYPES, TERMINAL_MARKER
from util import evolve_type

from collections import defaultdict
import numpy as np
import random

WATTS_STROGATZ_CACHE = {}


def watts_strogatz_sampler(source_index, sink_indices_list, alpha=1, percent=0.1):
    if source_index not in WATTS_STROGATZ_CACHE:
        WATTS_STROGATZ_CACHE[source_index] = np.array([
            1 / np.power(euclidean_cost(source_index, sink_index), alpha)
            for sink_index in sink_indices_list
        ])

    proportions = WATTS_STROGATZ_CACHE[source_index]
    sampled = set(np.random.choice(
        sink_indices_list,
        int(percent * len(sink_indices_list)),
        p=proportions / np.sum(proportions)
    ))
    assert len(sampled) > 0
    return sampled


def erdos_renyi_sampler(source_index, sink_indices_list, percent=0.1):
    assert (percent <= 1) and (percent >= 0)
    num_elems = int(percent * len(sink_indices_list))

    random.shuffle(sink_indices_list)
    sampled = set(sink_indices_list[0:num_elems + 1])
    assert len(sampled) > 0
    return sampled


def complete_sampler(source_index, sink_indices_list):
    return set(sink_indices_list)


# Note: we're making the assumption here that primitive types cannot stay
# primitive, they must evolve. This makes for an easier computation as we
# don't have to worry about self loops.
def build_graph(types_to_indices, sampler_fn, sampler_fn_kwargs):
    edges = defaultdict(set)
    for primitive_type in PRIMITIVE_TYPES:
        primitive_indices = types_to_indices[primitive_type]
        successor_types = evolve_type(primitive_type)
        successor_indices = set()
        for successor_type in successor_types:
            successor_indices = successor_indices.union(types_to_indices[successor_type])
        successor_indices_list = list(successor_indices)
        for primitive_source in primitive_indices:
            successor_sinks = sampler_fn(primitive_source, successor_indices_list, **sampler_fn_kwargs)
            edges[primitive_source] = successor_sinks

    for terminal_type in TERMINAL_TYPES:
        for terminal_source in types_to_indices[terminal_type]:
            edges[terminal_source] = {TERMINAL_MARKER}

    return edges
