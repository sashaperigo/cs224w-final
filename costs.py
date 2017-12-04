from defs import DISTANCES_FILE, DISTANCES_COLNAME


distances = read_euclidean_distances()


def euclidean_cost(index1, index2):
    index1, index2 = sorted(tuple(index1, index2))
    return distances.ix[index1, index2][DISTANCES_COLNAME]

def read_euclidean_distances(pathname=DISTANCES_FILE):
    distances = pd.read_csv(pathname, index_col=[0, 1], header=None)
    distances.columns = [DISTANCES_COLNAME]
    return distances