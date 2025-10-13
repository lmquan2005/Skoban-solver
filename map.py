"""
Convention on directions and coordinates:
————————————————→ y-axis
|
|
|
|
↓ x-axis

x and y start at 1 instead of 0.
"""

class Position:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"Position(x={self.x}, y={self.y})"
    
    def to_tuple(self):
        return (self.x, self.y)
    
    @staticmethod
    def from_tuple(tup) -> "Position":
        return Position(tup[0], tup[1])

    def dist(self, other: "Position" = None):
        if not other:
            return abs(self.x) + abs(self.y)
        return (self - other).dist()


DIRECTION = {
    "up": Position(-1, 0),
    "down": Position(1, 0),
    "left": Position(0, -1),
    "right": Position(0, 1),
}

WALL = "\033[38;5;244m█\033[0m"
BOX = "\033[38;5;172m■\033[0m"
BOX_ON_GOAL = "\033[38;5;82m■\033[0m"
GOAL = "\033[38;5;196m●\033[0m"
PLAYER = "\033[38;5;21m☺\033[0m"
PLAYER_ON_GOAL = "\033[38;5;196m☺\033[0m"
FLOOR = " "

TXT_WALL = frozenset(["#", "W"])
TXT_BOX = frozenset(["B"])
TXT_GOAL = frozenset([".", "G"])
TXT_BOX_ON_GOAL = frozenset(["X"])
TXT_PLAYER = frozenset(["&", "P", "@"])
TXT_PLAYER_ON_GOAL = frozenset(["Y"])
TXT_FLOOR = frozenset([" ", "_", "-"])

DEFAULT_WALL = "#"
DEFAULT_BOX = "B"
DEFAULT_BOX_ON_GOAL = "X"
DEFAULT_GOAL = "."
DEFAULT_PLAYER = "&"
DEFAULT_PLAYER_ON_GOAL = "Y"
DEFAULT_FLOOR = " "

class Map:
    def __init__(self, walls: list[Position], goals: list[Position], boxes: list[Position] = [], player: Position = None):
        self.walls = frozenset(walls)
        self.goals = frozenset(goals)
        self.boxes = set(boxes)
        self.player = player
    
    def __repr__(self):
        return f"Map(walls={self.walls}, goals={self.goals})"
    
    def __hash__(self):
        return hash((self.walls, self.goals))
    
    def update(self, boxes: set[Position], player: Position = None):
        if player:
            self.player = player
        self.boxes = boxes
    
    def get_boxes(self) -> set[Position]:
        return self.boxes
    
    def get_player(self) -> Position:
        return self.player
    
    @staticmethod
    def from_string(map_str: str) -> "Map":
        walls, goals, boxes, player = [], [], [], None
        for x, line in enumerate(map_str.splitlines()):
            for y, char in enumerate(line):
                pos = Position(x, y)
                if char in TXT_WALL:
                    walls.append(pos)
                elif char in TXT_GOAL:
                    goals.append(pos)
                elif char in TXT_BOX:
                    boxes.append(pos)
                elif char in TXT_BOX_ON_GOAL:
                    boxes.append(pos)
                    goals.append(pos)
                elif char in TXT_PLAYER:
                    player = pos
                elif char in TXT_PLAYER_ON_GOAL:
                    player = pos
                    goals.append(pos)
                elif char in TXT_FLOOR:
                    continue
                else:
                    raise ValueError(f"Unrecognized symbol: '{char}'")
        return Map(walls, goals, boxes, player)

    def to_string(self) -> str:
        all_x = [pos.x for pos in (self.walls | self.goals)]
        all_y = [pos.y for pos in (self.walls | self.goals)]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        rows = []
        for x in range(min_x, max_x + 1):
            row = []
            for y in range(min_y, max_y + 1):
                pos = Position(x, y)
                is_wall = pos in self.walls
                is_goal = pos in self.goals
                is_box = pos in self.boxes
                is_player = pos == self.player
                
                if is_goal and is_box:
                    row.append(DEFAULT_BOX_ON_GOAL)
                elif is_goal and is_player:
                    row.append(DEFAULT_PLAYER_ON_GOAL)
                elif is_box:
                    row.append(DEFAULT_BOX)
                elif is_goal:
                    row.append(DEFAULT_GOAL)
                elif is_player:
                    row.append(DEFAULT_PLAYER)
                elif is_wall:
                    row.append(DEFAULT_WALL)
                else:
                    row.append(DEFAULT_FLOOR)
                    
            rows.append("".join(row))
        return "\n".join(rows)

    @staticmethod
    def load(file_path: str) -> "Map":
        with open(file_path, "r", encoding="utf8") as file:
            content = file.read()
        return Map.from_string(content)
    
    @staticmethod
    def save(obj, file_path: str):
        with open(file_path, "w", encoding="utf8") as file:
            file.write(obj.to_string())
    
    def pretty(self) -> str:
        all_x = [pos.x for pos in (self.walls | self.goals)]
        all_y = [pos.y for pos in (self.walls | self.goals)]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        rows = []
        for x in range(min_x, max_x + 1):
            row = []
            for y in range(min_y, max_y + 1):
                pos = Position(x, y)
                is_wall = pos in self.walls
                is_goal = pos in self.goals
                is_box = pos in self.boxes
                is_player = pos == self.player
                
                if is_goal and is_box:
                    row.append(BOX_ON_GOAL)
                elif is_goal and is_player:
                    row.append(PLAYER_ON_GOAL)
                elif is_box:
                    row.append(BOX)
                elif is_goal:
                    row.append(GOAL)
                elif is_player:
                    row.append(PLAYER)
                elif is_wall:
                    row.append(WALL)
                else:
                    row.append(FLOOR)
                    
            rows.append("".join(row))
        return "\n".join(rows)

    def pretty_print(self):
        print(self.pretty())

test_map = Map.load("levels/level2.txt")