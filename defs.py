EVOLUTIONARY_CHAIN = {
    'PS': ['NP'],
    'NP': ['HF'],
    'HF': ['4G', '4GF'],
}

CELL_TYPES = [
    'PS', 'NP', 'HF', '4G', '4GF',
]

PRIMITIVE_TYPES = [
    'PS', 'NP', 'HF',
]

TERMINAL_TYPES = [
    '4G', '4GF',
]

TERMINAL_MARKER = 'TERMINAL_MARKER'

DISTANCES_FILE = 'input_data/euclidean_distances.csv'

DISTANCES_COLNAME = 'distance'

MEASUREMENTS_PATH = 'input_data/norm.csv'

TYPES_PATH = 'input_data/celltypes.txt'

GENES_PATH = 'input_data/genes.txt'

OUTPUT_DIR = 'output_data'

NUM_TRIALS = 100
