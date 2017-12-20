from . import Heuristic
from algo.costs import L2DistanceCost
from algo.problems import MapProblem
from algo.ways.tools import compute_distance

# Use the L2 aerial distance (in meters)
class L2DistanceHeuristic(Heuristic):
    def estimate(self, problem, state):
        target_state = problem.target
        # Return the aerial distance between the state and the target
        return compute_distance(state.coordinates, target_state.coordinates)

