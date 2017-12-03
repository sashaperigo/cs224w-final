
# def watts_strogatz(dataframe, types_to_indices):
#     for cell_type in ["PS", "NP", "HF"]:
#         indices = types_of_indices[cell_type]


def erdos_renyi(dataframe, types_to_indices, percent=20):
    return True


def build_graph(dataframe, types_of_indices, sampler_fn):
    edges = defaultdict(set)
    for cell_type in PRIMITIVE_TYPES:
        indices = types_to_indices[cell_type]
        for src in indices:

            for dst in indices:
                # No self edges!
                if src == dst:
                    continue
                if sampler_fn(dataframe, src, dst):
                    # Conditional depending on what type of graph we're doing
                    edges[src].add(dst)