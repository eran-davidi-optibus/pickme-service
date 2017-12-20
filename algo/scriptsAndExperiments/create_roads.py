import pickle

from algo.consts import Consts
from algo.ways.graph import load_map_from_csv

file = open('roads.pkl', 'wb')
roads = load_map_from_csv(Consts.getDataFilePath("israel.csv"))
pickle.dump(roads, file)
