from util import evolve_type, get_weighted_euclidean_distance, get_spread_weight_series
import numpy as np

# do caching where necessary

def watts_strogatz_sampler(dataframe, source_index, sink_indices_list, spread_weights, alpha=2, percent=0.2):
    proportions = np.array([
        1/np.power(get_weighted_euclidean_distance(dataframe, source_index, sink_index, spread_weights), alpha) \
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

# primitive cannot stay, must evolve; easier computation in that we don't have to do unions, don't have to worry about self-loops
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
