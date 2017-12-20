from algo.consts import Consts
from algo.heuristics import L2DistanceHeuristic, NullHeuristic, MSTHeuristic, TSPCustomHeuristic
from algo.astar import AStar
from algo.problems import BusProblem
from algo.costs.actualDistanceCost import ActualDistanceCost
import pickle
import time




def run_astar(fname):
    roads_file = open('roads.pkl', 'rb')
    roads = pickle.load(roads_file)
    prob = BusProblem.load(fname)
    mapAstar = AStar(L2DistanceHeuristic(), shouldCache=True)
    tspH = MSTHeuristic(roads, prob.initialState, ActualDistanceCost(roads, mapAstar))
    busAstar = AStar(tspH, cost=ActualDistanceCost(roads, mapAstar))
    path,gBus,hVal,developed = busAstar.run(prob)
    return path
