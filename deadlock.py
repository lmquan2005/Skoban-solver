from map import DIRECTION

class DeadlockDetector:
    def __init__(self, state):
        self.state = state
        self.reachable_pulls = self.get_reachable_pulls()
    

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
    
    def is_freeze_deadlock(self, box_pos):
        return self.is_axis_freeze("x", box_pos) and self.is_axis_freeze("y", box_pos)
    
    def is_axis_freeze(self, axis, box_pos, prev_box=None):
        walls, boxes = self.state.map.walls, self.state.boxes
        up_pos = box_pos + (DIRECTION["up"] if axis == "x" else DIRECTION["left"])
        down_pos = box_pos + (DIRECTION["down"] if axis == "x" else DIRECTION["right"])
        
        if up_pos in walls or down_pos in walls:
            return True
        if self.is_simple_deadlock(up_pos) and self.is_simple_deadlock(down_pos):
            return True
        
        if prev_box is not None:
            if up_pos == prev_box and down_pos in boxes and self.is_axis_freeze(axis, down_pos, box_pos):
                return True
            if down_pos == prev_box and up_pos in boxes and self.is_axis_freeze(axis, up_pos, box_pos):
                return True
        else:
            if up_pos in boxes and self.is_axis_freeze(axis, up_pos, box_pos):
                return True
            if down_pos in boxes and self.is_axis_freeze(axis, down_pos, box_pos):
                return True
        
        return False
        

    def is_deadlock(self, box_pos):
        return (
            self.is_simple_deadlock(box_pos)
            # or self.is_freeze_deadlock(box_pos)
        )