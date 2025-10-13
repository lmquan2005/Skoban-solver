import os
import time
from state import *


def print_map(map):
    print(f"\033[{32}A", end="")
    for _ in range(32):
        print("\033[2K", end="")
    map.pretty_print()


def breadth_first_search(map):
    state = State(map)
    stack = [(frozenset(state.boxes), state.player, [])]
    state_info_cache = StateSet()

    while stack:
        boxes, player, path = stack.pop(0)
        state.update(boxes, player)
        moves, norm_pos, reachable = state.get_available_moves()
        state_info_cache.update(boxes, norm_pos, reachable)

        for new_pos, d in moves:
            new_boxes = set(boxes)
            new_boxes.remove(new_pos)
            new_boxes.add(new_pos + d)
            new_boxes = frozenset(new_boxes)
            
            state.update(new_boxes, new_pos)
            print_map(state.map)
            
            if (new_boxes, new_pos) in state_info_cache:
                continue
            elif state.is_finished():
                return path + [(new_pos, d)]
            else:
                stack.append((new_boxes, new_pos, path + [(new_pos, d)]))