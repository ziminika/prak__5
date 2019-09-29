from collections import defaultdict
import sys

# Description of class Graph:
	# The Graph is a dictionary of dictionaries.
	# The keys are nodes, and the values are dictionaries, 
	# whose keys are the vertices that are associated with 
	# a given node, and whose values are the weight of the edges.
	# Non-oriented Graph
class Graph:
	# Сreating a Graph object
	def __init__(self):
		self.nodes = defaultdict(defaultdict)

	# Adding a new node to the graph
	def add_node(self, value):
		if value not in self.nodes:
			self.nodes[value] = {}

	# Adding vertices and edges		
	def add_edge_and_weight(self, nodeStart, nodeEnd, weight):
		if nodeEnd not in self.nodes:
			self.add_node(nodeEnd)
		if nodeStart not in self.nodes:
			self.add_node(nodeStart)
		self.nodes[nodeStart][nodeEnd] = weight
		self.nodes[nodeEnd][nodeStart] = weight

	# Output an object of type Graph
	def __str__(self):
		output = ""
		for i in self.nodes:
			output += str(i) + " -> " + str(self.nodes[i]) + '\n'
		return output[0:-1]

	# Function to find the shortest path between nodes 
	# nodeStart and nodeEnd. Dijkstra's algorithm is used.
	def short_way(self, nodeStart, nodeEnd):
		if nodeStart not in self.nodes:
			return "Error: nodeStart not in graph"
		if nodeEnd not in self.nodes:
			return "Error: nodeEnd not in graph"
		Inf = 0
		for i in self.nodes:
			Inf += sum(self.nodes[i].values())
		dist = {} # storing distances between the nodeStart and other
		is_min_dist = {} # bool type storage. "True" corresponds to the shortest distance already found
		path = {} # storing the path from nodeStart
		for i in self.nodes:
			dist[i] = Inf
			is_min_dist[i] = False
		dist[nodeStart] = 0
		path[nodeStart] = []
		node = nodeStart
		while is_min_dist[nodeEnd] != True:
			is_not_visited = True
			min_way = Inf
			for i in self.nodes[node]:
				is_not_visited = is_not_visited and is_min_dist[i]
				if not is_min_dist[i]:
					if dist[i] >= dist[node] + self.nodes[node][i]:
						dist[i] = dist[node] + self.nodes[node][i]
						path[i] = path[node].copy()
						path[i].append(node)
			is_min_dist[node] = True
			for i in dist:
				if is_min_dist[i] == False and min_way >= dist[i]:
					next_node = i
					min_way = dist[i]
			if is_not_visited == True and is_min_dist[nodeEnd] != True and node == nodeStart:
				return "Path doesn't exist"
			node = next_node
		path[nodeEnd].append(nodeEnd)
		return path[nodeEnd]

G = Graph()
end = 0
while end == 0:
	str1 = sys.stdin.readline()
	if str1 != "\n":
		node1 = str1[0:-1].split()[0]
		node2 = str1[0:-1].split()[1]
		weight = int(str1[0:-1].split()[2])
		G.add_edge_and_weight(node1,node2, weight)
	else:
		end = 1
print("Selected nodeStart:")
nodeStart = input()
print("Selected nodeEnd:")
nodeEnd = input()
print(G.short_way(nodeStart, nodeEnd))