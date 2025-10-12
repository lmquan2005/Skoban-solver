import copy
import queue
import sys
import time

import numpy as np

class Sokoban:
    def __init__(self, matrix):
        self.matrix = matrix
        self.solution = ""
        self.heuristic = 0

    def __lt__(self, other):
        return self.heuristic < other.heuristic

    def isValid(self, char):
        return char in ['#' , #wall
                         ' ', #space
                         '.', #goal
                         '@', #player
                         '$', #box
                         '*', #box on goal
                         '+'] #player on goal
    
    def get_matrix(self):
        return self.matrix

    def get_value(self, x, y):
        return self.matrix[y][x]
    
    def set_value(self, x, y, value):
        if self.isValid(value):
            self.matrix[y][x] = value
        else:
            raise ValueError("Invalid character for Sokoban cell.")
        
    def player_position(self):
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.matrix[y][x] in ['@', '+']:
                    return (x, y)
        raise Exception("Player not found in the matrix.")

    def next_position(self, dx, dy):
        px, py = self.player_position()
        return (px + dx, py + dy)

    def canMove(self, dx, dy):
        return self.get_value(*self.next_position(dx, dy)) in [' ', '.']
    
    def canPush(self, dx, dy):
        next_x, next_y = self.next_position(dx, dy)
        beyond_x, beyond_y = next_x + dx, next_y + dy
        return (self.get_value(next_x, next_y) in ['$', '*'] and
                self.get_value(beyond_x, beyond_y) in [' ', '.'])
    
    def isCompleted(self):
        for row in self.matrix:
            if '$' in row:
                return False
        return True
    
    def movebox (self, dx, dy):
        px, py = self.player_position()
        next_x, next_y = self.next_position(dx, dy)
        beyond_x, beyond_y = next_x + dx, next_y + dy
        
        # Move the box to new position
        if self.get_value(beyond_x, beyond_y) == ' ':
            self.set_value(beyond_x, beyond_y, '$')
        elif self.get_value(beyond_x, beyond_y) == '.':
            self.set_value(beyond_x, beyond_y, '*')
        
        # Update the box's previous position
        if self.get_value(next_x, next_y) == '$':
            self.set_value(next_x, next_y, '@')
        elif self.get_value(next_x, next_y) == '*':
            self.set_value(next_x, next_y, '+')
        
        # Update the player's previous position
        if self.get_value(px, py) == '@':
            self.set_value(px, py, ' ')
        elif self.get_value(px, py) == '+':
            self.set_value(px, py, '.')

    def move(self, dx, dy):
        if self.canPush(dx, dy):
            self.movebox(dx, dy)
        elif not self.canMove(dx, dy):
            return
        else:
            next_x, next_y = self.next_position(dx, dy)
            px, py = self.player_position()
            
            # Move the player to new position
            if self.get_value(next_x, next_y) == ' ':
                self.set_value(next_x, next_y, '@')
            elif self.get_value(next_x, next_y) == '.':
                self.set_value(next_x, next_y, '+')
            
            # Update the player's previous position
            if self.get_value(px, py) == '@':
                self.set_value(px, py, ' ')
            elif self.get_value(px, py) == '+':
                self.set_value(px, py, '.')

def valid_moves(sokoban):
    moves = []
    if sokoban.canMove(0, -1) or sokoban.canPush(0, -1):
        moves.append('U')
    if sokoban.canMove(0, 1) or sokoban.canPush(0, 1):
        moves.append('D')
    if sokoban.canMove(-1, 0) or sokoban.canPush(-1, 0):
        moves.append('L')
    if sokoban.canMove(1, 0) or sokoban.canPush(1, 0):
        moves.append('R')
    return moves

def isDeadlock(sokoban):
    for y in range(1, len(sokoban.matrix) - 1):
        for x in range(1, len(sokoban.matrix[y]) - 1):
            if sokoban.get_value(x, y) == '$':
                if ((sokoban.get_value(x + 1, y) in ['#', '$', '*'] and sokoban.get_value(x, y + 1) in ['#', '$', '*']) or
                    (sokoban.get_value(x - 1, y) in ['#', '$', '*'] and sokoban.get_value(x, y + 1) in ['#', '$', '*']) or
                    (sokoban.get_value(x + 1, y) in ['#', '$', '*'] and sokoban.get_value(x, y - 1) in ['#', '$', '*']) or
                    (sokoban.get_value(x - 1, y) in ['#', '$', '*'] and sokoban.get_value(x, y - 1) in ['#', '$', '*'])):
                    return True
    return False

def btd(sokoban): # Box to dock manhattan distance
    h = 0
    docks = []
    boxes = []
    for y in range(len(sokoban.matrix)):
        for x in range(len(sokoban.matrix[y])):
            if sokoban.get_value(x, y) in ['.', '+', '*']:
                docks.append((x, y))
            if sokoban.get_value(x, y) in ['$', '*']:
                boxes.append((x, y))
    for box in boxes:
        min_dist = float('inf')
        for dock in docks:
            dist = abs(box[0] - dock[0]) + abs(box[1] - dock[1])
            if dist < min_dist:
                min_dist = dist
        h += min_dist
    return h

def ptb(sokoban): # Player to box manhattan distance
    players = sokoban.player_position()
    boxes = []
    for y in range(len(sokoban.matrix)):
        for x in range(len(sokoban.matrix[y])):
            if sokoban.get_value(x, y) in ['$', '*']:
                boxes.append((x, y))
    for box in boxes:
        c = float('inf')
        if (abs(players[0] - box[0]) + abs(players[1] - box[1])) <= c:
            c = abs(players[0] - box[0]) + abs(players[1] - box[1])
    return c

def aStar(sokoban):
    print("=== START A* ===")
    node_visited = 0
    sokoban_state = copy.deepcopy(sokoban)
    sokoban_state.heuristic = btd(sokoban_state) + ptb(sokoban_state)
    stateQueue = queue.PriorityQueue()
    stateQueue.put((sokoban_state.heuristic, sokoban_state))
    visited = set()
    visited.add(tuple(map(tuple, sokoban_state.get_matrix())))
    if isDeadlock(sokoban_state):
        print("Initial state is a deadlock.")
        return None
    while not stateQueue.empty():
        current_heuristic, current_state = stateQueue.get()
        node_visited += 1
        if current_state.isCompleted():
            print(f"Solution found with {len(current_state.solution)} moves: {current_state.solution}")
            print(f"Nodes visited: {node_visited}")
            return current_state.solution
        for move in valid_moves(current_state):
            new_state = copy.deepcopy(current_state)
            if move == 'U':
                new_state.move(0, -1)
            elif move == 'D':
                new_state.move(0, 1)
            elif move == 'L':
                new_state.move(-1, 0)
            elif move == 'R':
                new_state.move(1, 0)
            if tuple(map(tuple, new_state.get_matrix().tolist())) not in visited and not isDeadlock(new_state):
                visited.add(tuple(map(tuple, new_state.get_matrix())))
                new_state.solution += move
                new_state.heuristic = btd(new_state) + ptb(new_state) # + len(new_state.solution)
                stateQueue.put((new_state.heuristic, new_state))
    print("No solution found.")
    return None

def readCommand(argv):
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option('-l', '--level', dest='sokobanLevels',
                      help='level of game to play', default='level1.txt')
    parser.add_option('-m', '--method', dest='agentMethod',
                      help='research method', default='bfs')
    args = dict()
    options, _ = parser.parse_args(argv)
    with open('sokobanLevels/'+options.sokobanLevels,"r") as f: 
        layout = f.readlines()
    args['layout'] = layout
    args['method'] = options.agentMethod
    return args

def transferToGameState(layout):
    """Transfer the layout of initial puzzle"""
    layout = [x.replace('\n','') for x in layout]
    layout = [','.join(layout[i]) for i in range(len(layout))]
    layout = [x.split(',') for x in layout]
    maxColsNum = max([len(x) for x in layout])
    for irow in range(len(layout)):
        for icol in range(len(layout[irow])):
            if layout[irow][icol] == ' ': layout[irow][icol] = ' '   # free space
            elif layout[irow][icol] == '#': layout[irow][icol] = '#' # wall
            elif layout[irow][icol] == '@': layout[irow][icol] = '@' # player
            elif layout[irow][icol] == '$': layout[irow][icol] = '$' # box
            elif layout[irow][icol] == '.': layout[irow][icol] = '.' # goal
            elif layout[irow][icol] == '*': layout[irow][icol] = '*' # box on goal
            elif layout[irow][icol] == '+': layout[irow][icol] = '+' # player on goal
        colsNum = len(layout[irow])
        if colsNum < maxColsNum:
            layout[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 
    return np.array(layout)

if __name__ == '__main__':
    time_start = time.time()
    layout, method = readCommand(sys.argv[1:]).values()
    gameState = Sokoban(transferToGameState(layout))
    if method == 'astar':
        aStar(gameState)
    else:
        raise ValueError('Invalid method.')
    time_end=time.time()
    print('Runtime of %s: %.2f second.' %(method, time_end-time_start))

