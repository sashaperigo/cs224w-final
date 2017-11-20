import pandas as pd


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



# Euclidean distance between two rows
# Still need to multiply this by spread weights to weight different genes differently
# np.sqrt(np.sum((data.iloc[2, 2:] - data.iloc[1, 2:]) ** 2))

# Std dev for each gene
# np.std(data.iloc[:, 2:])

# Weights for each gene
# np.std(data.iloc[:, 2:]) / np.sum(np.std(data.iloc[:, 2:]))


def get_weighted_euclidean(dataframe, index1, index2, spread_weights):
    return np.sqrt(
        np.sum(
            ((dataframe.iloc[index2] - dataframe.iloc[index1]) ** 2) * \
                spread_weights
        )
    )


def get_spread_weight_series(dataframe):
    return np.std(dataframe)/np.sum(np.std(dataframe))
