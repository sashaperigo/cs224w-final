from itertools import combinations
import pandas as pd
from util import get_normalized_data, get_spread_weight_series, get_weighted_euclidean_distance

# get_weighted_euclidean_distance(dataframe, source_index, sink_index, spread_weights)

cells = get_normalized_data("input_data/norm.csv", "input_data/celltypes.txt")
spread_weights = get_spread_weight_series(cells)

genes = pd.read_csv("input_data/genes.txt", header=None)
genes_list = genes.iloc[:, 0].tolist()

cells_view = cells[genes_list]

indices = list(combinations(range(len(cells_view)), 2))
distances = []
for index in indices:
    distance = get_weighted_euclidean_distance(cells_view, index[0], index[1], spread_weights)
    distances.append(distance)

series_index = pd.MultiIndex.from_tuples(indices, names=['first', 'second'])
series = pd.Series(distances, index=series_index)

series.to_csv("input_data/euclidean_distances.csv")
