from map import DIRECTION

class DeadlockDetector:
    def __init__(self, state):
        self.state = state
        self.reachable_pulls = self.get_reachable_pulls()

    
    def is_deadlock(self, box_pos):
        return (
            self.is_simple_deadlock(box_pos) or
            self.is_freeze_deadlock()
        )

    def get_reachable_pulls(self):
        stack = list(self.state.map.goals)
        visited = set()

        while stack:
            pos = stack.pop(0)
            visited.add(pos)

            for delta in DIRECTION.values():
                new_pos = pos + delta
                if any([
                        new_pos in visited,
                        new_pos in self.state.map.walls,
                        new_pos + delta in self.state.map.walls
                ]):
                    continue
                
                stack.append(new_pos)
        
        return visited


    def is_simple_deadlock(self, pos):
        return pos not in self.reachable_pulls


    def detect_frozen_boxes(self):
        walls = set(self.state.map.walls)
        goals = set(self.state.map.goals)
        boxes = set(self.state.map.boxes)
        frozen = set()
        
        def is_blocked(box):
            return (box in walls) or (box in frozen)
        
        for box in boxes:
            if box in goals:
                continue
            if ((box + DIRECTION["up"] in walls or box + DIRECTION["down"] in walls) and
                (box + DIRECTION["left"] in walls or box + DIRECTION["right"] in walls)):
                frozen.add(box)
        
        changed = True
        while changed:
            changed = False
            for box in boxes:
                if box in goals or box in frozen:
                    continue
                
                up = box + DIRECTION["up"]
                down = box + DIRECTION["down"]
                left = box + DIRECTION["left"]
                right = box + DIRECTION["right"]
                
                x_blocked = is_blocked(up) and is_blocked(down)
                y_blocked = is_blocked(left) and is_blocked(right)
                if x_blocked and y_blocked:
                    frozen.add(box)
                    changed = True
        return frozen


    def is_freeze_deadlock(self):
        frozen = self.detect_frozen_boxes()
        goals = set(self.state.map.goals)
        return any(fz not in goals for fz in frozen)