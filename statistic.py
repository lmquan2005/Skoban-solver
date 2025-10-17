import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Đọc dữ liệu
BFS = pd.read_csv("BFS.csv", na_values=["???", "??? "])
DFS = pd.read_csv("DFS.csv", na_values=["???", "??? "])
Astar = pd.read_csv("A_star.csv", na_values=["???", "??? "])


def drawChart(factor, map):
    # Lấy dữ liệu đúng map
    if map == "MINI COSMOS":
        stepBFS = BFS[factor][0:40].reset_index(drop=True)
        stepDFS = DFS[factor][0:40].reset_index(drop=True)
        stepAstar = Astar[factor][0:40].reset_index(drop=True)
    else:
        stepBFS = BFS[factor][40:].reset_index(drop=True)
        stepDFS = DFS[factor][40:].reset_index(drop=True)
        stepAstar = Astar[factor][40:].reset_index(drop=True)

    # Đặt chiều rộng cột
    barWidth = 0.25
    fig = plt.subplots(figsize=(12, 8))

    index = np.arange(len(stepBFS))

    # Các vị trí của cột
    br1 = index
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    # Tạo biểu đồ
    plt.bar(br1, stepBFS, color='r', width=barWidth,
            edgecolor='grey', label='BFS')
    plt.bar(br2, stepDFS, color='b', width=barWidth,
            edgecolor='grey', label='DFS')
    plt.bar(br3, stepAstar, color='g', width=barWidth,
            edgecolor='grey', label='A*')

    # Nhãn trục Y
    if factor == "Step":
        ylab = "Step"
    elif factor == "Time (s)":
        ylab = "Seconds"
    elif factor == "Node generated":
        ylab = "Nodes"
    else:
        ylab = "Memory (MB)"

    # Cài đặt trục và tiêu đề
    plt.xlabel('Testcase', fontweight='bold', fontsize=15)
    plt.ylabel(ylab, fontweight='bold', fontsize=15)
    plt.xticks([r + barWidth for r in range(len(stepBFS))],
               [i + 1 for i in range(len(stepBFS))])

    # Tiêu đề biểu đồ
    title_map = "in " + map + " Testcases"
    if factor == "Memory (MB)":
        plt.title("Memory usage " + title_map)
    elif factor == "Time (s)":
        plt.title("Execution time " + title_map)
    elif factor == "Node generated":
        plt.title("Generated nodes " + title_map)
    else:
        plt.title("Solution steps " + title_map)

    plt.legend()

    # Lưu biểu đồ
    save_name = factor.lower().replace(" ", "_").replace("(", "").replace(")", "")
    plt.savefig(f"./Charts/{save_name}_{map}.png")
    plt.close()


# --- Vẽ biểu đồ cho tất cả yếu tố ---
drawChart("Step", "MINI COSMOS")
drawChart("Step", "MICRO COSMOS")
drawChart("Time (s)", "MINI COSMOS")
drawChart("Time (s)", "MICRO COSMOS")
drawChart("Memory (MB)", "MINI COSMOS")
drawChart("Memory (MB)", "MICRO COSMOS")
drawChart("Node generated", "MINI COSMOS")
drawChart("Node generated", "MICRO COSMOS")

print(f"Loaded {len(BFS)} BFS records, {len(DFS)} DFS records, {len(Astar)} A* records.")
print("Last BFS Map:", BFS["Map"].iloc[-1])
