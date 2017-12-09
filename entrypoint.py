from cell_search import find_shortest_paths
from costs import euclidean_cost
from defs import *
from networks import build_graph, complete_sampler, erdos_renyi_sampler, watts_strogatz_sampler
from util import get_normalized_data, get_cell_types_to_indices, get_indices_to_cell_types

from collections import defaultdict
from multiprocessing import Pool, TimeoutError
import pandas as pd

N_PROCESSES = 4


def random_walks_multiple(cell_types_to_indices, sampler_fn, file_label, n=100):
    pool = Pool(N_PROCESSES)
    pool.map(
        random_walks_wrapper,
        [(cell_types_to_indices, sampler_fn, file_label, i) for i in range(n)]
    )


def random_walks_wrapper(args):
    random_walks(*args)


def random_walks(cell_types_to_indices, sampler_fn, file_label, index):
    for primitive_type in PRIMITIVE_TYPES:
        indices_to_actions = run_random_walk(cell_types_to_indices, primitive_type, sampler_fn)
        dataframe = pd.DataFrame.from_dict(
            indices_to_actions,
            orient='index'
        )
        local_fn = "{}/{}-{}-{}.csv".format(
            OUTPUT_DIR,
            file_label,
            index,
            primitive_type
        )
        dataframe.to_csv(local_fn)


def run_random_walk(cell_types_to_indices, primitive_type, sampler_fn):
    indices_to_actions = defaultdict(list)

    for index in cell_types_to_indices[primitive_type]:
        curr = index
        cell_type = primitive_type
        while True:
            if cell_type in TERMINAL_TYPES:
                break

            successor_types = EVOLUTIONARY_CHAIN[cell_type]
            # Most cell types just have one successor stage, but HF can
            # evolve into either 4G or 4GF.
            sink_indices = []
            for successor_type in successor_types:
                sink_indices += list(cell_types_to_indices[successor_type])

            cell_type = successor_types[0]

            # This percent should return exactly one node.
            percent = float(1) / len(sink_indices)
            successor_set = sampler_fn(curr, sink_indices, percent=percent)
            successor = list(successor_set)[0]
            indices_to_actions[index].append(successor)
            curr = successor

    return indices_to_actions


def shortest_paths_multiple(cell_types_to_indices, sampler_fn, sampler_fn_kwargs, cost_fn, file_label, n=15):
    pool = Pool(N_PROCESSES)
    pool.map(
        shortest_paths_wrapper,
        [(cell_types_to_indices, sampler_fn, sampler_fn_kwargs, cost_fn, file_label, i) for i in range(n)]
    )


def shortest_paths_wrapper(args):
    shortest_paths(*args)


def shortest_paths(cell_types_to_indices, sampler_fn, sampler_fn_kwargs, cost_fn, file_label, index):
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
            index,
            primitive_type
        )
        dataframe.to_csv(local_fn)


def erdos_renyi(cell_types_to_indices):
    shortest_paths_multiple(
        cell_types_to_indices,
        erdos_renyi_sampler,
        {},
        euclidean_cost,
        'erdos_renyi_shortest_paths',
    )


def watts_strogatz(cell_types_to_indices):
    shortest_paths_multiple(
        cell_types_to_indices,
        watts_strogatz_sampler,
        {},
        euclidean_cost,
        'watts_strogatz_shortest_paths',
    )


def main():
    data = get_normalized_data(MEASUREMENTS_PATH, TYPES_PATH)
    cell_types_to_indices = get_cell_types_to_indices(data)

    # erdos_renyi(cell_types_to_indices)
    # watts_strogatz(cell_types_to_indices)
    # random_walks(cell_types_to_indices, erdos_renyi_sampler, "random_walk_erdos_renyi")
    random_walks_multiple(cell_types_to_indices, watts_strogatz_sampler, "random_walk_watts_strogatz")


if __name__ == "__main__":
    main()
