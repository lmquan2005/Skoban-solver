from collections import defaultdict
from deadlock import *
from map import *


class State:
    def __init__(self, map: Map):
        self.map = map
        self.boxes = map.boxes
        self.player = map.player
        self.deadlock_detector = DeadlockDetector(self)
    
    def __hash__(self):
        return hash((self.boxes, self.player))
    
    def __repr__(self):
        return f"State(boxes={self.boxes}, player={self.player})"
    
    def update(self, boxes, player):
        self.boxes = boxes
        self.player = player
        self.update_map()
    
    def update_map(self):
        self.map.update(self.boxes, self.player)
    
    def get_available_moves(self):
        available_moves, visited = [], []
        norm_pos = self.player
        stack = [norm_pos]
        
        # Find normalized position by DFS
        while stack:
            pos = stack.pop(0)
            if pos in visited:
                continue
            visited.append(pos)
            
            # Define normalized position as topmost-leftmost position
            if (pos.x < norm_pos.x) or (pos.x == norm_pos.x and pos.y < norm_pos.y):
                norm_pos = pos
            
            for delta in DIRECTION.values():
                new_pos = pos + delta
                if (new_pos in visited) or (new_pos in self.map.walls):
                    continue
                
                if new_pos in self.boxes:
                    new_box_pos = new_pos + delta
                    if new_box_pos not in (self.map.walls | self.boxes) and not self.deadlock_detector.is_deadlock(new_box_pos):
                        available_moves.append((new_pos, delta))
                else:
                    stack.append(new_pos)
        return available_moves, norm_pos, visited
    
    
    def is_finished(self):
        return len(self.map.goals - self.boxes) == 0


class StateSet:
    def __init__(self):
        self.cache = defaultdict(dict)

    def __contains__(self, item):
        boxes, player = item
        if boxes in self.cache:
            state_info = self.cache[boxes]
            for norm_pos in state_info:
                if player in state_info[norm_pos]:
                    return True
        return False

    def update(self, boxes, norm_pos, reachable):
        self.cache[boxes][norm_pos] = reachable

    def look_up(self, item):
        boxes, player = item
        if boxes in self.cache:
            state_info = self.cache[boxes]
            for norm_pos in state_info:
                if player in state_info[norm_pos]:
                    return norm_pos
        return None
    