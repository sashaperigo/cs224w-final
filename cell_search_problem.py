from defs import TERMINAL_MARKER

############################################################
# Abstract interfaces for search problems and search algorithms.

# State-based Models for Cellular Differentiation
class CellSearchProblem:
    def __init__(self, start_index, edges_dict, cost_fn):
        self.start_index = start_index
        self.edges_dict = edges_dict
        self.cost_fn = cost_fn

    # Return the start state.
    def startState(self): 
        return self.start_index

    # Return whether |state| is an end state or not.
    def isEnd(self, state):
        return state == TERMINAL_MARKER

    # Return a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    # For us, action and newState are the same --> we just use the cell/node/state dataframe index.
    # Cost is the weighted Euclidean distance between the current cell and the successor. 
    def succAndCost(self, state):
        results = []
        for successor_state in self.edges_dict[state]:
            cost = self.cost_fn(state, successor_state)
            results.append((successor_state, successor_state, cost))
        
        return results
