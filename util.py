import numpy as np
import pandas as pd
from collections import defaultdict
import random

EVOLUTIONARY_CHAIN = {
    'PS': ['PS', 'NP'],
    'NP': ['NP', 'HF'],
    'HF': ['4G', '4GF']
}

PRIMITIVE_TYPES = [
    'PS', 'NP', 'HF'
]


def get_normalized_data(measurements_path, types_path):
    measurements = get_data(measurements_path)
    types = get_data(types_path)
    return pd.concat([types, measurements], axis=1)


def get_data(path):
    return pd.read_csv(path)

# def evaluate_network_model():
#   # Create network model
#   # Run search problem for all 3000+ cells to find terminal states
#   # Compare terminal states to "gold list" from paper
#   # Evaluate model


def get_weighted_euclidean(dataframe, index1, index2, spread_weights):
    return np.sqrt(
        np.sum(
            ((dataframe.iloc[index2] - dataframe.iloc[index1]) ** 2) *
            spread_weights
        )
    )


def get_spread_weight_series(dataframe):
    return np.std(dataframe) / np.sum(np.std(dataframe))


def cell_types_to_indices(dataframe):
    types = ["HF", "PS", "NP", "4G", "4GF"]
    types_to_indices = {}
    for cell_type in types:
        types_to_indices[cell_type] = set(
            dataframe.loc[dataframe['Type'] == cell_type].index.tolist())
    return types_to_indices


# def watts_strogatz(dataframe, types_to_indices):
#     for cell_type in ["PS", "NP", "HF"]:
#         indices = types_of_indices[cell_type]


def erdos_renyi(dataframe, types_to_indices, percent=20):
    return True


def evolve_type(cell_type):
    return EVOLUTIONARY_CHAIN[cell_type]


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


data = get_normalized_data("norm.csv", "celltypes.txt")
types_to_indices = cell_types_to_indices(data)
