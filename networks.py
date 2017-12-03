from util import evolve_type

# def watts_strogatz(dataframe, types_to_indices):
#     for cell_type in ["PS", "NP", "HF"]:
#         indices = types_of_indices[cell_type]


def erdos_renyi(dataframe, types_to_indices, percent=20):
    return True


# primitive cannot stay, must evolve
def build_graph(dataframe, types_to_indices, sampler_fn):
    edges = defaultdict(set)
    for primitive_type in PRIMITIVE_TYPES:
        successor_type = evolve_type(primitive_type)
        primitive_indices = types_to_indices[primitive_type]
        successor_indices = types_to_indices[successor_type]
        for primitive_source in primitive_indices:
            successor_sinks = sampler_fn(dataframe, primitive_source, successor_indices)
            for successor_sink in successor_sinks:
                edges[primitive_source].add(successor_sink)
    return edges