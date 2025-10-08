from parser import LevelParser
from solvers import BFSSolver, DFSSolver

def print_result(algorithm_name: str, result):
    """Print search result in a formatted way"""
    print(f"\n{'='*60}")
    print(f"Algorithm: {algorithm_name}")
    print(f"{'='*60}")
    
    if result.success:
        print(f"✓ Solution found!")
        print(f"  Solution length: {result.solution_length} moves")
        print(f"  Nodes explored: {result.nodes_explored}")
        print(f"  Moves: {result.solution}")
    else:
        print(f"✗ No solution found")
        print(f"  Nodes explored: {result.nodes_explored}")

def main():
    # Example level
    level = """\
    #####
    #   #
    #B  #
  ###   ###
  #       #
### # ### #     ######
#   # ### #######  ..#
# B  B              X#
##### #### #&####   .#
    #      ###  ######
    ########\
    """
    
    print("Sokoban AI Solver")
    print("="*60)
    
    # Parse the level
    print("Parsing level...")
    initial_state = LevelParser.parse(level)
    print(f"  Player position: {initial_state.player_pos}")
    print(f"  Number of boxes: {len(initial_state.box_positions)}")
    print(f"  Number of goals: {len(initial_state.goals)}")
    
    # Solve with BFS
    result = BFSSolver.solve(initial_state)
    print_result("Breadth-First Search (BFS)", result)
    
    # Solve with DFS
    result = DFSSolver.solve(initial_state, max_depth=500)
    print_result("Depth-First Search (DFS)", result)

if __name__ == "__main__":
    main()