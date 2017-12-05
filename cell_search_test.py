from cell_search_util import find_shortest_path_from
from defs import TERMINAL_MARKER


# Start at 0, want to go to 10, costs 1 to move down, 2 to move up.
class NumberLineSearchProblem:
    def __init__(self):
        self.edges_dict = {
            0: set([1]),
            1: set([0, 2]),
            2: set([1, 3]),
            3: set([2, 4]),
            4: set([3, 5]),
            5: set([4, 6]),
            6: set([5, 7]),
            7: set([6, 8]),
            8: set([7, 9]),
            9: set([8, 10]),
            10: set([9, TERMINAL_MARKER])
        }
        self.start_index = 0
        self.expected = [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2)]

    def cost_fn(self, index1, index2):
        if index2 < index1:
            return 1
        elif index1 < index2:
            return 2

    def run(self):
        result = find_shortest_path_from(self.start_index, self.edges_dict, self.cost_fn)
        assert(self.expected == result)


print "Running tests..."
problem = NumberLineSearchProblem()
problem.run()
print "All passed!"
