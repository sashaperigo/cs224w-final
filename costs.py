import pandas as pd

from defs import DISTANCES_FILE, DISTANCES_COLNAME, TERMINAL_MARKER


def euclidean_cost(index1, index2):
    if (index1 == TERMINAL_MARKER) or (index2 == TERMINAL_MARKER): return 0
    index1, index2 = sorted((index1, index2))
    return distances.ix[index1, index2][DISTANCES_COLNAME]


def read_euclidean_distances(pathname=DISTANCES_FILE):
    distances = pd.read_csv(pathname, index_col=[0, 1], header=None)
    distances.columns = [DISTANCES_COLNAME]
    return distances


distances = read_euclidean_distances()
