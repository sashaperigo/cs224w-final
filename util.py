import numpy as np
import pandas as pd
from collections import defaultdict
import random
from defs import CELL_TYPES, PRIMITIVE_TYPES, EVOLUTIONARY_CHAIN

# ----DATA UTIL----

def get_normalized_data(measurements_path, types_path):
    measurements = get_data(measurements_path)
    types = get_data(types_path)
    return pd.concat([types, measurements], axis=1)


def get_data(path):
    return pd.read_csv(path)


def get_cell_types_to_indices(dataframe):
    types_to_indices = {}
    for cell_type in CELL_TYPES:
        types_to_indices[cell_type] = set(
            dataframe.loc[dataframe['Type'] == cell_type].index.tolist()
        )
    return types_to_indices


# ----GENE UTIL----

def get_weighted_euclidean_distance(dataframe, index1, index2, spread_weights):
    return np.sqrt(
        np.sum(
            ((dataframe.iloc[index2] - dataframe.iloc[index1]) ** 2) *
            spread_weights
        )
    )


def get_spread_weight_series(dataframe):
    return np.std(dataframe) / np.sum(np.std(dataframe))


def evolve_type(cell_type):
    return EVOLUTIONARY_CHAIN[cell_type]

