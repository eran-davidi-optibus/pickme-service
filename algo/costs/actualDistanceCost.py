from . import Cost
from algo.ways.tools import compute_distance

class ActualDistanceCost(Cost):
    roads = None
    astar = None

    def __init__(self, roads, astar):
        self.roads = roads
        self.astar = astar

    def compute(self, fromState, toState):
        """

        :rtype:
        """
        from algo.problems import MapProblem

        mapSubProblem = MapProblem(self.roads, fromState.junctionIdx, toState.junctionIdx)
        _, l, _, _ = self.astar.run(mapSubProblem)
        return l
