from . import GreedySolver
import numpy as np

class GreedyBestFirstSolver(GreedySolver):
    def __init__(self, roads, astar, scorer):
        super().__init__(roads, astar, scorer)

    # Find the next state to develop
    def _getNextState(self, problem, currState):
        successors = list(problem.expand(currState))
        # TODO : Return the next state

        def func(state):
            return self._scorer.compute(currState, state)
        # Pick the closest vertex
        bestIdx = successors.index(min(successors, key=func))

        if bestIdx is None:
            return None

        return successors[bestIdx]
