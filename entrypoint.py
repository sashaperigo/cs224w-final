from cell_search import find_shortest_paths
from costs import euclidean_cost
from defs import MEASUREMENTS_PATH, TYPES_PATH, OUTPUT_DIR
from networks import build_graph, complete_sampler, erdos_renyi_sampler, watts_strogatz_sampler
from util import get_normalized_data, get_cell_types_to_indices, get_indices_to_cell_types

import pandas as pd


def shortest_paths(cell_types_to_indices, sampler_fn, sampler_fn_kwargs, cost_fn, file_label, n=15):
    for i in range(n):
        graph = build_graph(cell_types_to_indices, sampler_fn, sampler_fn_kwargs)
        actions = find_shortest_paths(graph, cell_types_to_indices, cost_fn)
        for primitive_type, primitive_sources_to_actions in actions.iteritems():
            dataframe = pd.DataFrame.from_dict(
                primitive_sources_to_actions,
                orient='index'
            )
            local_fn = "{}/{}-{}-{}.csv".format(
                OUTPUT_DIR,
                file_label,
                i,
                primitive_type
            )
            dataframe.to_csv(local_fn)


def erdos_renyi(cell_types_to_indices, indices_to_cell_types):
    shortest_paths(
        cell_types_to_indices,
        erdos_renyi_sampler,
        {},
        euclidean_cost,
        'erdos_renyi',
    )


def watts_strogatz(cell_types_to_indices, indices_to_cell_types):
    shortest_paths(
        cell_types_to_indices,
        watts_strogatz_sampler,
        {},
        euclidean_cost,
        'watts_strogatz',
    )


def main():
    data = get_normalized_data(MEASUREMENTS_PATH, TYPES_PATH)
    cell_types_to_indices = get_cell_types_to_indices(data)
    indices_to_cell_types = get_indices_to_cell_types(data)

    erdos_renyi(cell_types_to_indices, indices_to_cell_types)
    watts_strogatz(cell_types_to_indices, indices_to_cell_types)


if __name__ == "__main__":
    main()
