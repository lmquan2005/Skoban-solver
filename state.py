from typing import FrozenSet, Tuple, List
from deadlock import DeadlockDetector


class SokobanState:
    
    def __init__(
        self, player_pos: Tuple[int, int], 
        box_positions: FrozenSet[Tuple[int, int]],
        goals: FrozenSet[Tuple[int, int]],
        walls: FrozenSet[Tuple[int, int]],
        moves: str = ""
    ):    
        self.player_pos = player_pos
        self.box_positions = frozenset(box_positions)
        self.goals = goals
        self.walls = walls
        self.moves = moves
        
    def __hash__(self):
        return hash((self.player_pos, self.box_positions))
    
    def __eq__(self, other):
        return (self.player_pos == other.player_pos and 
                self.box_positions == other.box_positions)
    
    def is_goal(self) -> bool:
        return self.box_positions == self.goals
    
    def get_successors(self) -> List['SokobanState']:
        successors = []
        directions = [
            (-1, 0, 'u', 'U'),  # up
            (1, 0, 'd', 'D'),   # down
            (0, -1, 'l', 'L'),  # left
            (0, 1, 'r', 'R')    # right
        ]
        
        for dr, dc, move, push_move in directions:
            new_r = self.player_pos[0] + dr
            new_c = self.player_pos[1] + dc
            new_pos = (new_r, new_c)
            
            # Check if new position is a wall
            if new_pos in self.walls:
                continue
            
            # Check if there's a box at new position
            if new_pos in self.box_positions:
                # Try to push the box
                box_new_r = new_r + dr
                box_new_c = new_c + dc
                box_new_pos = (box_new_r, box_new_c)
                
                # Check if box can be pushed
                if (box_new_pos not in self.walls and 
                    box_new_pos not in self.box_positions):
                    
                    new_boxes = set(self.box_positions)
                    new_boxes.remove(new_pos)
                    new_boxes.add(box_new_pos)
                    
                    # Comprehensive deadlock detection
                    if not DeadlockDetector.detect_all_deadlocks(
                        frozenset(new_boxes), self.goals, self.walls, box_new_pos):
                        successors.append(SokobanState(
                            new_pos, frozenset(new_boxes), 
                            self.goals, self.walls, 
                            self.moves + push_move))
            else:
                # Simple move without pushing
                successors.append(SokobanState(
                    new_pos, self.box_positions, 
                    self.goals, self.walls, 
                    self.moves + move))
        
        return successors