import os
import argparse
from map import *
from methods.bfs import *
from methods.dfs import *

parser = argparse.ArgumentParser(description="Sokoban search")
parser.add_argument("algo", type=str, help="Algorithm used to solve")
parser.add_argument("input", type=str, help="The level filename")
args = parser.parse_args()

algo = {"dfs": depth_first_search, "bfs": breadth_first_search}[args.algo]

map = Map.load(f"levels/{args.input}")
os.system("cls") if os.name == "nt" else os.system("clear")
results = algo(map)
print(results)