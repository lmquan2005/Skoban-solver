from typing import FrozenSet, Tuple, Set, Dict
from collections import deque

class DeadlockDetector:
        
    @staticmethod
    def is_simple_deadlock(box_pos: Tuple[int, int],
                          goals: FrozenSet[Tuple[int, int]],
                          walls: FrozenSet[Tuple[int, int]]) -> bool:
        # If box is on a goal, it's not a deadlock
        if box_pos in goals:
            return False
        
        r, c = box_pos
        
        # Check adjacent cells
        up_wall = (r-1, c) in walls
        down_wall = (r+1, c) in walls
        left_wall = (r, c-1) in walls
        right_wall = (r, c+1) in walls
        
        # Corner deadlock: box stuck in corner
        if (up_wall or down_wall) and (left_wall or right_wall):
            return True
        
        # Additional check: box against wall with no goal on that wall
        if up_wall or down_wall:
            # Check if there's any goal in this column
            has_goal_in_column = any(g[1] == c for g in goals)
            if not has_goal_in_column:
                return True
        
        if left_wall or right_wall:
            # Check if there's any goal in this row
            has_goal_in_row = any(g[0] == r for g in goals)
            if not has_goal_in_row:
                return True
        
        return False
    
    @staticmethod
    def is_freeze_deadlock(box_positions: FrozenSet[Tuple[int, int]],
                          goals: FrozenSet[Tuple[int, int]],
                          walls: FrozenSet[Tuple[int, int]]) -> bool:
        boxes = set(box_positions)
        
        for box in boxes:
            if box in goals:
                continue
            
            # Check if box is frozen (cannot be pushed in any direction)
            if DeadlockDetector._is_box_frozen(box, boxes, walls, goals):
                return True
        
        return False
    
    @staticmethod
    def _is_box_frozen(box: Tuple[int, int], 
                      boxes: Set[Tuple[int, int]],
                      walls: FrozenSet[Tuple[int, int]],
                      goals: FrozenSet[Tuple[int, int]]) -> bool:
        if box in goals:
            return False
        
        r, c = box
        
        # Check horizontal freeze
        left_blocked = (r, c-1) in walls or (r, c-1) in boxes
        right_blocked = (r, c+1) in walls or (r, c+1) in boxes
        horizontal_frozen = left_blocked and right_blocked
        
        # Check vertical freeze
        up_blocked = (r-1, c) in walls or (r-1, c) in boxes
        down_blocked = (r+1, c) in walls or (r+1, c) in boxes
        vertical_frozen = up_blocked and down_blocked
        
        # Box is frozen if it's blocked both horizontally and vertically
        return horizontal_frozen or vertical_frozen
    
    @staticmethod
    def is_line_deadlock(box_positions: FrozenSet[Tuple[int, int]],
                        goals: FrozenSet[Tuple[int, int]],
                        walls: FrozenSet[Tuple[int, int]]) -> bool:
        boxes = set(box_positions)
        
        # Check horizontal lines
        for box in boxes:
            if box in goals:
                continue
            
            r, c = box
            
            # Check if against top or bottom wall
            if (r-1, c) in walls or (r+1, c) in walls:
                # Find all boxes in this row
                line_boxes = [b for b in boxes if b[0] == r]
                line_goals = [g for g in goals if g[0] == r]
                
                # Check if boxes form a continuous line with no goals
                if len(line_boxes) >= 2 and len(line_goals) == 0:
                    if DeadlockDetector._is_continuous_line(line_boxes, horizontal=True):
                        return True
            
            # Check if against left or right wall
            if (r, c-1) in walls or (r, c+1) in walls:
                # Find all boxes in this column
                line_boxes = [b for b in boxes if b[1] == c]
                line_goals = [g for g in goals if g[1] == c]
                
                # Check if boxes form a continuous line with no goals
                if len(line_boxes) >= 2 and len(line_goals) == 0:
                    if DeadlockDetector._is_continuous_line(line_boxes, horizontal=False):
                        return True
        
        return False
    
    @staticmethod
    def _is_continuous_line(positions: list, horizontal: bool) -> bool:
        if len(positions) < 2:
            return False
        
        if horizontal:
            # Sort by column
            positions = sorted(positions, key=lambda p: p[1])
            # Check continuity
            for i in range(len(positions) - 1):
                if positions[i+1][1] - positions[i][1] > 1:
                    return False
        else:
            # Sort by row
            positions = sorted(positions, key=lambda p: p[0])
            # Check continuity
            for i in range(len(positions) - 1):
                if positions[i+1][0] - positions[i][0] > 1:
                    return False
        
        return True
    
    @staticmethod
    def is_bipartite_deadlock(box_positions: FrozenSet[Tuple[int, int]],
                             goals: FrozenSet[Tuple[int, int]],
                             walls: FrozenSet[Tuple[int, int]]) -> bool:
        boxes = list(box_positions)
        goals_list = list(goals)
        
        if len(boxes) > len(goals_list):
            return True  # More boxes than goals = deadlock
        
        # Build reachability graph: which boxes can reach which goals
        reachable = DeadlockDetector._build_reachability_graph(
            boxes, goals_list, walls, box_positions
        )
        
        # Use maximum matching to check if all boxes can reach distinct goals
        max_matching = DeadlockDetector._max_bipartite_matching(
            len(boxes), len(goals_list), reachable
        )
        
        # If matching size < number of boxes, it's a deadlock
        return max_matching < len(boxes)
    
    @staticmethod
    def _build_reachability_graph(boxes: list, goals: list,
                                  walls: FrozenSet[Tuple[int, int]],
                                  all_boxes: FrozenSet[Tuple[int, int]]) -> Dict:
        reachable = {i: [] for i in range(len(boxes))}
        
        for i, box in enumerate(boxes):
            for j, goal in enumerate(goals):
                # Simple check: is there a clear path considering walls only?
                if DeadlockDetector._has_path_ignoring_boxes(box, goal, walls):
                    reachable[i].append(j)
        
        return reachable
    
    @staticmethod
    def _has_path_ignoring_boxes(start: Tuple[int, int], 
                                 end: Tuple[int, int],
                                 walls: FrozenSet[Tuple[int, int]]) -> bool:
        if start == end:
            return True
        
        queue = deque([start])
        visited = {start}
        
        while queue:
            r, c = queue.popleft()
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_pos = (r + dr, c + dc)
                
                if new_pos == end:
                    return True
                
                if (new_pos not in walls and 
                    new_pos not in visited):
                    visited.add(new_pos)
                    queue.append(new_pos)
        
        return False
    
    @staticmethod
    def _max_bipartite_matching(n_boxes: int, n_goals: int, 
                               reachable: Dict) -> int:
        match = [-1] * n_goals
        
        def dfs(box: int, visited: Set[int]) -> bool:
            for goal in reachable[box]:
                if goal in visited:
                    continue
                visited.add(goal)
                
                if match[goal] == -1 or dfs(match[goal], visited):
                    match[goal] = box
                    return True
            return False
        
        matching = 0
        for box in range(n_boxes):
            visited = set()
            if dfs(box, visited):
                matching += 1
        
        return matching
    
    @staticmethod
    def detect_all_deadlocks(box_positions: FrozenSet[Tuple[int, int]],
                           goals: FrozenSet[Tuple[int, int]],
                           walls: FrozenSet[Tuple[int, int]],
                           last_pushed_box: Tuple[int, int] = None) -> bool:
        # Quick check: if last box was pushed, check only that box first
        if last_pushed_box and last_pushed_box not in goals:
            if DeadlockDetector.is_simple_deadlock(last_pushed_box, goals, walls):
                return True
        
        # Check all boxes for simple deadlocks
        for box in box_positions:
            if DeadlockDetector.is_simple_deadlock(box, goals, walls):
                return True
        
        # Check freeze deadlocks
        if DeadlockDetector.is_freeze_deadlock(box_positions, goals, walls):
            return True
        
        # Check line deadlocks
        if DeadlockDetector.is_line_deadlock(box_positions, goals, walls):
            return True
        
        # Expensive check: bipartite matching (use sparingly)
        # Only run this for small numbers of boxes
        if len(box_positions) <= 6:
            if DeadlockDetector.is_bipartite_deadlock(box_positions, goals, walls):
                return True
        
        return False