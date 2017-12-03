from util import evolve_type
import numpy as np

# do caching where necessary

def watts_strogatz_sampler(dataframe, source_index, sink_indices_list, alpha=2):
    pass

def erdos_renyi_sampler(dataframe, source_index, sink_indices_list, percent=0.2):
    assert (percent <= 1) and (percent >= 0)
    return set(np.random.choice(sink_indices_list, int(percent * len(sink_indices_list))))

# primitive cannot stay, must evolve
def build_graph(dataframe, types_to_indices, sampler_fn, sampler_fn_kwargs):
    edges = defaultdict(set)
    for primitive_type in PRIMITIVE_TYPES:
        successor_type = evolve_type(primitive_type)
        primitive_indices = types_to_indices[primitive_type]
        successor_indices_list = list(types_to_indices[successor_type])
        for primitive_source in primitive_indices:
            successor_sinks = sampler_fn(dataframe, primitive_source, successor_indices_list, **sampler_fn_kwargs)
            edges[primitive_source] = successor_sinks

    return edges
