from algo.consts import Consts
from algo.heuristics import L2DistanceHeuristic, NullHeuristic, MSTHeuristic, TSPCustomHeuristic
from algo.astar import AStar
from algo.problems import BusProblem
from algo.costs.actualDistanceCost import ActualDistanceCost
import pickle
import time
clock = time.time()
tot_clock = time.time()
roads_file = open('roads.pkl', 'rb')
roads = pickle.load(roads_file)
diff = time.time() - clock
prob = BusProblem.load(Consts.getDataFilePath("TLV_5.in"))

mapAstar = AStar(L2DistanceHeuristic(), shouldCache=True)

# Run A* with the MST heuristic
diff = time.time()-clock
print('start custom huristic after {}'.format(diff))
clock = time.time()
def print_path(path):
    junctions = []
    for j in path:
        junctions.append(j.junctionIdx)
    print(junctions)


tspH = MSTHeuristic(roads, prob.initialState, ActualDistanceCost(roads, mapAstar))
busAstar = AStar(tspH, cost=ActualDistanceCost(roads, mapAstar))
path,gBus,hVal,developed = busAstar.run(prob)
print("A* (MST heuristic):\tg(G)={:.2f}km, h(I)={:.2f}km, developed: {} states".format(gBus/1000, hVal/1000, developed))
diff = time.time() - clock
print('finish the MST heuristic after {}'.format(diff))
print('finish total after: {} sec'.format(time.time()-clock))
print_path(path)