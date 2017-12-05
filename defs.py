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

DISTANCES_FILE = 'euclidean_distances.csv'

DISTANCES_COLNAME = 'distance'

MEASUREMENTS_PATH = 'input_data/norm.csv'

TYPES_PATH = 'input_data/celltypes.txt'

ENDOTHELIAL_GENES = [
    'Cdh5', 'Erg', 'HoxB4', 'Sox7', 'Sox17',
]

ERYTHROID_GENES = [
    'Gata1', 'Gfi1b', 'Hbbbh1', 'Ikaros', 'Myb', 'Nfe2',
]

ENDOTHELIAL = '4G'

ERYTHROID = '4GF'
