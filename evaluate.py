from defs import *
from util import get_normalized_data, get_indices_to_cell_types, get_spread_weight_series

from collections import defaultdict
import csv
import numpy as np
import os
import pandas as pd

file_labels = [
    "random_walk_erdos_renyi",
    "random_walk_watts_strogatz",
    "watts_strogatz_shortest_paths",
    "erdos_renyi_shortest_paths",
    "random_walk_watts_strogatz_a2"
]


# Returns a dictionary within a dictionary of the following format:
# {
#   file_label : {
#       primitive_cell_index : [ [actions], [actions] ]
#   }
# }
def load_output_data():
    print "Reading in input data..."
    output_data = {}
    for label in file_labels:
        indices_to_actions = defaultdict(list)
        for cell_type in PRIMITIVE_TYPES:
            for fname in os.listdir("output_data/%s" % label):
                if fname.startswith("."):
                    continue
                file_name = "output_data/%s/%s" % (label, fname)
                with open(file_name, 'rb') as csv_file:
                    reader = csv.reader(csv_file)
                    next(reader)

                    for row in reader:
                        if row[-1] == TERMINAL_MARKER:
                            row = row[:len(row) - 1]
                        actions = [int(action) for action in row]
                        indices_to_actions[int(row[0])].append(actions)
        output_data[label] = indices_to_actions
    return output_data


# Returns a dictionary mapping each terminal cell type to the set of indices
# that transitioned into that terminal type in the majority of trials for a
# given paradigm and model type.
#
# Params:
# - output_data: dict, of the form described above
# - indices_to_cell_types: dict
# - file_label: string, label used to label output files
#               (i.e. "random_walk_watts_strogatz", "random_walk_erdos_renyi")
def get_terminal_types_to_indices(output_data, indices_to_cell_types, file_label):
    indices_to_terminal_types = defaultdict(int)

    indices_to_actions = output_data[file_label]
    for primitive_index, actions_list in indices_to_actions.iteritems():
        for actions in actions_list:
            terminal_type = indices_to_cell_types[actions[-1]]
            assert(terminal_type == '4G' or terminal_type == '4GF')

            # On first pass, add 1 to our dictionary value for each 4G
            # cell we encounter, and subtract one for each 4GF cell.
            if terminal_type == '4G':
                indices_to_terminal_types[primitive_index] += 1
            else:
                indices_to_terminal_types[primitive_index] -= 1

    # Condition over whether or not the sum is greater than 0 to determine
    # whether a primitive cell transitioned into a 4G or 4GF cell in more
    # trials.
    terminal_type_to_indices = defaultdict(set)
    for index, terminal_type_sum in indices_to_terminal_types.iteritems():
        if terminal_type_sum > 0:
            terminal_type_to_indices["4G"].add(index)
        else:
            terminal_type_to_indices["4GF"].add(index)
    return terminal_type_to_indices


def instantiate_avg_transitions():
    genes = pd.read_csv(GENES_PATH, header=None)
    columns = ['PS-NP', 'NP-HF', 'HF-4G/4GF']
    return pd.DataFrame(0, index=genes[0].tolist(), columns=columns, dtype=np.float64)


def avg_gene_transitions(cells_df, output_data, indices_to_cell_types):
    spread_weights = get_spread_weight_series(cells_df)

    for label in file_labels:
        print "Calculating average transitions for %s..." % label
        terminal_types_to_indices = get_terminal_types_to_indices(output_data, indices_to_cell_types, label)

        for terminal_type in TERMINAL_TYPES:
            avg_transitions_df = instantiate_avg_transitions()
            ps_np_count = 0
            np_hf_count = 0
            hf_terminal_count = 0

            for primitive_index in terminal_types_to_indices[terminal_type]:
                list_of_actions = output_data[label][primitive_index]

                for actions in list_of_actions:
                    for i in range(1, len(actions)):
                        delta = cells.iloc[int(actions[i])] - cells.iloc[int(actions[i - 1])]
                        if i == 1:
                            curr_avg = avg_transitions_df['PS-NP']
                            avg_transitions_df['PS-NP'] = (curr_avg * ps_np_count + delta) / (ps_np_count + 1)
                            ps_np_count += 1
                        elif i == 2:
                            curr_avg = avg_transitions_df['NP-HF']
                            avg_transitions_df['NP-HF'] = (curr_avg * np_hf_count + delta) / (np_hf_count + 1)
                            np_hf_count += 1
                        elif i == 3:
                            curr_avg = avg_transitions_df['HF-4G/4GF']
                            avg_transitions_df['HF-4G/4GF'] = (curr_avg * hf_terminal_count + delta) / (hf_terminal_count + 1)
                            hf_terminal_count += 1
                for column_header in avg_transitions_df:
                    avg_transitions_df[column_header] = avg_transitions_df[column_header] * spread_weights
            avg_transitions_df.to_csv("output_data/average_transitions/%s-%s" % (label, terminal_type))


def calculate_percents(output_data, indices_to_cell_types):
    for label in file_labels:
        print "Calculating percentage of 4G and 4GF cells for %s..." % label
        df = pd.DataFrame(index=PRIMITIVE_TYPES, columns=TERMINAL_TYPES)

        primitive_to_terminal_types = {
            "PS": (0, 0),
            "NP": (0, 0),
            "HF": (0, 0)
        }
        for index, list_of_actions in output_data[label].iteritems():
            primitive_type = indices_to_cell_types[index]
            for actions in list_of_actions:
                terminal_type = indices_to_cell_types[actions[-1]]
                counts = primitive_to_terminal_types[primitive_type]
                if terminal_type == '4G':
                    primitive_to_terminal_types[primitive_type] = (counts[0], counts[1] + 1)
                else:
                    primitive_to_terminal_types[primitive_type] = (counts[0] + 1, counts[1])

        column_4g = []
        column_4gf = []
        for primitive_type, counts in primitive_to_terminal_types.iteritems():
            percent_4g = counts[0] / float(counts[0] + counts[1])
            percent_4gf = counts[1] / float(counts[0] + counts[1])
            column_4g.append(percent_4g)
            column_4gf.append(percent_4gf)
        df["4G"] = column_4g
        df["4GF"] = column_4gf

        df.to_csv("output_data/percents/%s.csv" % label)


def find_terminal_types(output_data, indices_to_cell_types):
    for label in file_labels:
        print "Finding terminal types for all cells in %s..." % label
        with open("output_data/terminal_types/%s.csv" % label, "wb") as csv_file:
            writer = csv.writer(csv_file)
            for index, list_of_actions in output_data[label].iteritems():
                count = 0
                for actions in list_of_actions:
                    terminal_type = indices_to_cell_types[actions[-1]]
                    assert(terminal_type == "4G" or terminal_type == "4GF")
                    if terminal_type == "4G":
                        count += 1
                    else:
                        count -= 1
                if count > 0:
                    writer.writerow([index, "4G"])
                else:
                    writer.writerow([index, "4GF"])


data = get_normalized_data(MEASUREMENTS_PATH, TYPES_PATH)
genes = pd.read_csv(GENES_PATH, header=None)
genes_list = genes.iloc[:, 0].tolist()
cells = data[genes_list]

indices_to_cell_types = get_indices_to_cell_types(data)

output_data = load_output_data()
avg_gene_transitions(cells, output_data, indices_to_cell_types)
# calculate_percents(output_data, indices_to_cell_types)
# find_terminal_types(output_data, indices_to_cell_types)
