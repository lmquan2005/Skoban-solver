import heapq
from collections import deque
import time

def is_deadlock(pos, goals, grid):
    """Phát hiện deadlock đơn giản: thùng bị kẹt trong góc tường (2 tường vuông góc)."""
    x, y = pos
    rows, cols = len(grid), len(grid[0])

    # Nếu nằm trên goal thì không kẹt
    if pos in goals:
        return False

    def wall(nx, ny):
        if not (0 <= nx < rows and 0 <= ny < cols):
            return True  # ngoài bản đồ coi như tường
        return grid[nx][ny] == '#'

    up = wall(x - 1, y)
    down = wall(x + 1, y)
    left = wall(x, y - 1)
    right = wall(x, y + 1)

    # Nếu bị kẹt trong góc bởi 2 tường thật
    if (up and left) or (up and right) or (down and left) or (down and right):
        return True

    return False


# Heuristic: tổng khoảng cách Manhattan từ mỗi thùng đến goal gần nhất
def heuristic(player, boxes, goals):
    """
    Heuristic không dùng thư viện: greedy matching giữa box-goal + khoảng cách người chơi.
    """
    boxes = list(boxes)
    goals = list(goals)
    total = 0
    used_goals = set()

    # 1️⃣ Gán mỗi box cho goal gần nhất chưa dùng
    for bx, by in boxes:
        best_d = float('inf')
        best_g = None
        for gx, gy in goals:
            if (gx, gy) in used_goals:
                continue
            d = abs(bx - gx) + abs(by - gy)
            if d < best_d:
                best_d = d
                best_g = (gx, gy)
        if best_g:
            used_goals.add(best_g)
            total += best_d

    # 2️⃣ Thêm chi phí người chơi đến box gần nhất (để hướng dẫn di chuyển hợp lý)
    px, py = player
    if boxes:
        min_player_box = min(abs(px - bx) + abs(py - by) for bx, by in boxes)
    else:
        min_player_box = 0

    # 3️⃣ Trả về tổng heuristic
    return total + 0.5 * min_player_box


def a_star_sokoban(grid, start, boxes, goals):
    rows, cols = len(grid), len(grid[0])
    start_state = (start, tuple(sorted(boxes)))

    pq = []
    heapq.heappush(pq, (heuristic(start, boxes, goals), 0, start_state, ""))  # (f = g+h, g, state, path)

    visited = set()
    moves = [(1,0,'D'),(-1,0,'U'),(0,1,'R'),(0,-1,'L')]

    # 🧮 Thống kê node
    nodes_generated = 1   # trạng thái khởi tạo
    nodes_repeated = 0
    nodes_explored = 0

    while pq:
        f, g, (player, boxes), path = heapq.heappop(pq)

        # Mỗi lần lấy ra khỏi hàng đợi => 1 node được explore
        nodes_explored += 1

        # Kiểm tra đích
        if all(b in goals for b in boxes):
            print(f"✅ Giải thành công sau {nodes_explored} trạng thái duyệt, {nodes_generated} node sinh ra.")
            return path, nodes_generated, nodes_repeated, nodes_explored

        if (player, boxes) in visited:
            nodes_repeated += 1
            continue
        visited.add((player, boxes))

        px, py = player
        for dx, dy, move in moves:
            nx, ny = px + dx, py + dy
            if not (0 <= nx < rows and 0 <= ny < cols):
                continue
            if grid[nx][ny] == '#':
                continue

            new_boxes = set(boxes)
            # Nếu gặp thùng ở ô kế tiếp → thử đẩy
            if (nx, ny) in new_boxes:
                bx, by = nx + dx, ny + dy
                if not (0 <= bx < rows and 0 <= by < cols):
                    continue
                if grid[bx][by] == '#' or (bx, by) in new_boxes:
                    continue
                new_boxes.remove((nx, ny))
                new_boxes.add((bx, by))
                if any(is_deadlock(b, goals, grid) for b in new_boxes):
                    continue

            new_state = ((nx, ny), tuple(sorted(new_boxes)))
            if new_state in visited:
                nodes_repeated += 1
                continue

            new_g = g + 1
            h_val = heuristic((nx, ny), new_boxes, goals)
            heapq.heappush(pq, (new_g + h_val, new_g, new_state, path + move))
            nodes_generated += 1

    print(f"❌ Không tìm được lời giải. Tổng explored: {nodes_explored}, generated: {nodes_generated}")
    return None, nodes_generated, nodes_repeated, nodes_explored


def read_sokoban_map(filename):
    """
    Đọc bản đồ Sokoban từ file .txt với các ký hiệu:
    # = tường, . = sàn, x = box, ? = goal, @ = player,
    - = player trên goal, + = box trên goal.
    Trả về: grid (list[str]), start (tuple), boxes (set), goals (set)
    """
    grid = []
    boxes = set()
    goals = set()
    start = None

    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f]

    max_len = max(len(line) for line in lines)
    for y, line in enumerate(lines):
        # Chuẩn hóa độ dài dòng
        if len(line) < max_len:
            line += " " * (max_len - len(line))
        grid.append(line)

        for x, ch in enumerate(line):
            if ch == '#':
                continue  # tường, bỏ qua
            elif ch in ('.', ' '):
                continue  # sàn, không cần lưu
            elif ch == '@':
                start = (y, x)
            elif ch == '-':
                start = (y, x)
                goals.add((y, x))
            elif ch == 'x':
                boxes.add((y, x))
            elif ch == '+':
                boxes.add((y, x))
                goals.add((y, x))
            elif ch == '?':
                goals.add((y, x))

    return grid, start, boxes, goals
