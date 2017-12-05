from defs import 
    ENDOTHELIAL_GENES,
    ERYTHROID_GENES,
    TERMINAL_MARKER,
    ERYTHROID,
    ENDOTHELIAL


def predict_label(start_index, list_of_transitions_lists):
    erythroid_vote = 0
    endothelial_vote = 0
    for transitions_list in list_of_transitions_lists:
        final_transition = transitions_list[-1]
        if final_transition[0] == TERMINAL_MARKER:
            final_transition = transitions_list[-2]
        if final_transition[0] == ERYTHROID:
            erythroid_vote += 1
        else:
            endothelial_vote += 1
    if erythroid_vote > endothelial_vote:
        return ERYTHROID
    if erythroid_vote == endothelial_vote: print("WARNING: tie found!")
    return ENDOTHELIAL

# want to generate a "biplot"

# for each predicted fate: want to compute average transitions

# run a statistical test to see if those average transitions are different 