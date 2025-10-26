import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import os


dfs = pd.read_csv("dfs.csv",na_values=["???","??? "])
Astar =pd.read_csv("A_star.csv",na_values=["???","??? "])


def drawChart(factor,map):
	stepDFS = []
	stepAstar = []
	if (map == "MINI COSMOS"):
		stepDFS = dfs[factor][0:40]
		stepAstar = Astar[factor][0:40]
	else:
		stepDFS = dfs[factor][40:len(dfs)]
		stepAstar = Astar[factor][40:len(Astar)]
		
	barWidth = 0.25
	fig = plt.subplots(figsize =(12, 8))

	index = []
	for i in range(0,len(stepDFS)):
			index.append(i+1)
	
	# Set position of bar on X axis
	br1 = np.arange(len(stepDFS))
	br2 = [x + barWidth for x in br1]
	
	# Make the plot
	plt.bar(br1, stepDFS, color ='r', width = barWidth,
			edgecolor ='grey', label ='DFS')
	plt.bar(br2, stepAstar, color ='g', width = barWidth,
			edgecolor ='grey', label ='A_star')
	
	# Adding Xticks
	ylab = ""
	if (factor == "Step"):
		ylab = "Step"
	elif (factor == "Time (s)"):
		ylab = "sec"
	elif (factor == "Node generated"):
		ylab = "Node"
	else:
		ylab = "MB"

	plt.xlabel('TC', fontweight ='bold', fontsize = 15)
	plt.ylabel(ylab, fontweight ='bold', fontsize = 15)

	plt.xticks([barWidth/2 + r for r in range(len(stepDFS))],index)
	if (factor == "Memory (MB)"):
		plt.title("The amount of memory used in " + map +  " Testcases")
	elif (factor == "Time (s)"):
		plt.title("The amount of time elapsed in " + map + " Testcases")
	elif (factor == "Node generated"):
		plt.title("The amount of node generated in " + map + " Testcases")
	else:
		plt.title("The number of " + factor + " taken in " + map + " Testcases")
	plt.legend()
	
	save = ""
	if (factor == "Memory (MB)"):
		save = "memory"
	elif (factor == "Step"):
		save = "step"
	elif (factor == "Node generated"):
		save = "nodeGenerated"
	else:
		save = "time"
	plt.savefig("./Charts/" + save + "_" + map + ".png")	
	# plt.close(fig)

os.makedirs("./Charts", exist_ok=True)

drawChart("Step","MINI COSMOS")
drawChart("Step","MICRO COSMOS")
drawChart("Time (s)", "MINI COSMOS")
drawChart("Time (s)", "MICRO COSMOS")
drawChart("Memory (MB)","MINI COSMOS")
drawChart("Memory (MB)","MICRO COSMOS")
drawChart("Node generated","MINI COSMOS")
drawChart("Node generated","MICRO COSMOS")