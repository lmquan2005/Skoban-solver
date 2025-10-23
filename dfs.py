import time
import os
import psutil
from queue import Queue
from copy import copy, deepcopy
from datetime import datetime
import math
from sortedcontainers import SortedList
import numpy as np
from scipy.optimize import linear_sum_assignment
import pandas as pd


class Direction:
    def __init__(self, vector, char):
        self.vector = vector
        self.char = char

    def get_char(self):
        return self.char


# Hướng di chuyển: Up, Left, Down, Right (theo chiều kim đồng hồ)
L = Direction((-1, 0), 'L')
R = Direction((1, 0), 'R')
U = Direction((0, -1), 'U')
D = Direction((0, 1), 'D')
directions = [U, L, D, R]


def set_distance():
    distanceToGoal = dict()
    dead_squares = set()
    for goal in goals:
        distanceToGoal[goal] = dict()
        for path in paths:
            distanceToGoal[goal][path] = 1e9
    queue = Queue()
    for goal in goals:
        distanceToGoal[goal][goal] = 0
        queue.put(goal)
        while not queue.empty():
            position = queue.get()
            for direction in directions:
                boxPosition = (position[0] + direction.vector[0], position[1] + direction.vector[1])
                playerPosition = (position[0] + 2 * direction.vector[0], position[1] + 2 * direction.vector[1])
                if boxPosition in paths:
                    if distanceToGoal[goal][boxPosition] == 1e9:
                        if (boxPosition not in walls) and (playerPosition not in walls):
                            distanceToGoal[goal][boxPosition] = distanceToGoal[goal][position] + 1
                            queue.put(boxPosition)
    for path in paths:
        ok = 1
        for goal in goals:
            if distanceToGoal[goal][path] != 1e9:
                ok = 0
                break
        if ok == 1:
            dead_squares.add(path)
    return distanceToGoal, dead_squares


def set_available_moves(player, boxes):
    available_moves = []
    for direction in directions:
        if (player[0] + direction.vector[0], player[1] + direction.vector[1]) not in walls:
            if (player[0] + direction.vector[0], player[1] + direction.vector[1]) in boxes:
                if ((player[0] + 2 * direction.vector[0], player[1] + 2 * direction.vector[1]) not in walls) and \
                        ((player[0] + 2 * direction.vector[0], player[1] + 2 * direction.vector[1]) not in boxes):
                    available_moves.append(direction)
            else:
                available_moves.append(direction)
    return available_moves


def move(player, boxes, direction):
    temp = (player[0] + direction.vector[0], player[1] + direction.vector[1])
    res = True
    boxes = set(boxes)
    if temp in boxes:
        boxes.remove(temp)
        boxes.add((player[0] + 2 * direction.vector[0], player[1] + 2 * direction.vector[1]))

        if (player[0] + 2 * direction.vector[0], player[1] + 2 * direction.vector[1]) in dead_squares:
            res = False
    boxes = tuple(boxes)
    player = temp
    return res, player, boxes


def is_win(goals, boxes):
    return goals.issubset(boxes)


def set_value(filename):
    walls = set()
    goals = set()
    boxes = []
    paths = set()
    player = None
    x = 0
    y = 0
    with open(filename, 'r') as f:
        read_data = f.read()
        lines = read_data.split('\n')
        for line in lines:
            x = 0
            for char in line:
                if char == '#':
                    walls.add((x, y))
                elif char == 'x':
                    boxes.append((x, y))
                    paths.add((x, y))
                elif char == '?':
                    goals.add((x, y))
                    paths.add((x, y))
                elif char == '@':
                    player = (x, y)
                    paths.add((x, y))
                elif char == '-':
                    goals.add((x, y))
                    player = (x, y)
                    paths.add((x, y))
                elif char == '+':
                    goals.add((x, y))
                    boxes.append((x, y))
                    paths.add((x, y))
                elif char == '.':
                    paths.add((x, y))
                x += 1
            y += 1
    return walls, goals, tuple(boxes), paths, player


# =============================== DFS ===============================
map_list = ['MINI COSMOS', 'MICRO COSMOS']
itemMemory = psutil.Process(os.getpid()).memory_info().rss/(1024*1024)
def dfs(curr_player, curr_boxes):
    node_generated = 0
    frontier = [(curr_player, curr_boxes, 0, [])]  
    explored = set()
    explored.add((curr_player, curr_boxes))

    node_generated += 1
    startTime = time.time()

    while frontier:
        now_player, now_boxes, step, actions = frontier.pop()  
        moves = set_available_moves(now_player, now_boxes)
        for m in moves:
            res, new_player, new_boxes = move(now_player, now_boxes, m)
            if res and (new_player, new_boxes) not in explored:
                explored.add((new_player, new_boxes))
                node_generated += 1

                if is_win(goals, new_boxes):
                    end = time.time() - startTime
                    memo_info = abs(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024) - itemMemory)
                    return (node_generated, step + 1, end, memo_info, actions + [m])

                frontier.append((new_player, new_boxes, step + 1, actions + [m]))

    end = time.time() - startTime
    memo_info = abs(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024) - itemMemory)
    return (node_generated, step, end, memo_info, [m.get_char() for m in actions])
# =============================== DFS ===============================
if __name__ == '__main__':
    map_list = ['MINI COSMOS', 'MICRO COSMOS']
    i = -1
    if not os.path.exists("DFS.csv"):
         header_mode = "w+"
    else:
         header_mode = "w"  # Ghi đè file cũ luôn

    with open("DFS.csv", header_mode) as f:
        f.write("Map,Level,Algorithm,Node generated,Step,Time (s),Memory (MB)\n")

    i = 0
    
    print("Loading DFS algorithm results from testcase {}".format(i+1))

    for j in range(i, 80):
        map_name = map_list[int(j/40)]
        level_num = j%40 + 1
        walls, goals, boxes, paths, player = set_value("./Testcases/{}/{}.txt".format(map_list[int(j/40)], j%40+1))
        distanceToGoal, dead_squares = set_distance()
        print(f"\nSolving testcase {j+1} ({map_name} {level_num}): ")
        (node_created, step, times, memo, actions) = dfs(player, boxes)

        f = open("DFS.csv", 'a+')
        f.write("{},{},DFS,{},{},{:0.6f},{:0.6f}\n".format(map_list[int(j/40)], j%40+1, node_created, step, times, memo))
        print("Results testcase {}. Node generated: {}, Step: {}, Time: {:0.6f} s, Memory: {:0.6f} MB\n".format(j+1, node_created, step, times, memo))
        f.close()

        with open("result.txt", "a+") as rf:
             rf.write("=== Testcase {} ({} {}) ===\n".format(j+1, map_list[int(j/40)], j%40+1))
             if step > 0:
                rf.write("Path: {}\n".format("".join([d.get_char() for d in actions])))
             else:
                rf.write("No solution found.\n")

    print("\nSolving DFS algorithm results Completed")