import heapq, collections, re, sys, time, os, random

import csv
import math
import ingest_data
import random

############################################################
# Abstract interfaces for search problems and search algorithms.

# State-based Models for Cellular Differentiation

# 
class CellSearch:
    def __init__(self, data, genes, transition_probabilities, start_state):
        self.data = data
        self.genes = genes
        self.transition_probabilities = transition_probabilities
        self.start_state = start_state

    # Return the start state.
    def startState(self): 
        return self.start_state

    # Return whether |state| is an end state or not.
    def isEnd(self, state):
        return state[1] == 'FATE'

    # Return a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    def succAndCost(self, state):
        gene_profile, cell_type = state
        results = []

        transition_probabilities = self.transition_probabilities[state]
        for next_state, transition_probability in transition_probabilities.iteritems():
            results.append((next_state, next_state, 1/(transition_probability)))
        
        return results