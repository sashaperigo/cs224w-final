from defs import *
from util import get_normalized_data, get_indices_to_cell_types

import csv

file_labels = ["random_walk_erdos_renyi", "random_walk_watts_strogatz"]


def sum_4g_4gf(indices_to_cell_types):
    terminal_type_dict = {}
    for label in file_labels:
        for cell_type in PRIMITIVE_TYPES:
            sum_4g = 0
            sum_4gf = 0
            for i in range(100):
                file_name = "output_data/%s-%i-%s.csv" % (label, i, cell_type)
                with open(file_name, 'rb') as csv_file:
                    reader = csv.reader(csv_file)
                    next(reader)
                    for row in reader:
                        terminal_type = indices_to_cell_types[int(row[-1])]
                        assert(terminal_type == '4G' or terminal_type == '4GF')
                        if terminal_type == '4G':
                            sum_4g += 1
                        elif terminal_type == '4GF':
                            sum_4gf += 1
            if sum_4g > sum_4gf:
                terminal_type_dict["%s_%s" % (label, cell_type)] = '4G'
            else:
                terminal_type_dict["%s_%s" % (label, cell_type)] = '4GF'
    return terminal_type_dict

data = get_normalized_data(MEASUREMENTS_PATH, TYPES_PATH)
indices_to_cell_types = get_indices_to_cell_types(data)
print sum_4g_4gf(indices_to_cell_types)