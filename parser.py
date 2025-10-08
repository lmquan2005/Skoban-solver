from state import SokobanState

class LevelParser:
    WALL = "#"
    BOX = "B"
    GOAL = "O"
    BOX_GOAL = "X"
    PLAYER = "Y"
    
    @classmethod
    def parse(cls, level_string: str) -> SokobanState:
        lines = level_string.strip().split("\n")
        
        player_pos = None
        boxes = []
        goals = []
        walls = []
        
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                pos = (r, c)
                if char == cls.WALL:
                    walls.append(pos)
                elif char == cls.BOX:
                    boxes.append(pos)
                elif char == cls.GOAL:
                    goals.append(pos)
                elif char == cls.BOX_GOAL:
                    goals.append(pos)
                    boxes.append(pos)
                elif char == cls.PLAYER:
                    player_pos = pos
        
        if player_pos is None:
            raise ValueError("No player position found in level")
        
        return SokobanState(
            player_pos, 
            frozenset(boxes), 
            frozenset(goals), 
            frozenset(walls)
        )