from collections import deque
from typing import Optional, Tuple
from state import SokobanState

class SearchResult:
    """Container for search results"""
    def __init__(self, solution: Optional[str], nodes_explored: int, 
                 solution_length: int = 0):
        self.solution = solution
        self.nodes_explored = nodes_explored
        self.solution_length = solution_length
        self.success = solution is not None

class BFSSolver:
    """Breadth-First Search solver"""
    
    @staticmethod
    def solve(initial_state: SokobanState) -> SearchResult:
        """Solve using BFS - guarantees shortest solution"""
        queue = deque([initial_state])
        visited = {initial_state}
        nodes_explored = 0
        
        while queue:
            state = queue.popleft()
            nodes_explored += 1
            
            if state.is_goal():
                return SearchResult(state.moves, nodes_explored, len(state.moves))
            
            for successor in state.get_successors():
                if successor not in visited:
                    visited.add(successor)
                    queue.append(successor)
        
        return SearchResult(None, nodes_explored)

class DFSSolver:
    """Depth-First Search solver with depth limit"""
    
    @staticmethod
    def solve(initial_state: SokobanState, max_depth: int = 100) -> SearchResult:
        """Solve using DFS with depth limit"""
        stack = [(initial_state, 0)]
        visited = {initial_state}
        nodes_explored = 0
        
        while stack:
            state, depth = stack.pop()
            nodes_explored += 1
            
            if state.is_goal():
                return SearchResult(state.moves, nodes_explored, len(state.moves))
            
            if depth < max_depth:
                for successor in state.get_successors():
                    if successor not in visited:
                        visited.add(successor)
                        stack.append((successor, depth + 1))
        
        return SearchResult(None, nodes_explored)