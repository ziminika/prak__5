from collections import defaultdict
import sys

# Description of class Graph:
	# The Graph is a dictionary of dictionaries.
	# The keys are nodes, and the values are dictionaries, 
	# whose keys are the vertices that are associated with 
	# a given node, and whose values are the weight of the edges.
	# Oriented Graph
class Graph:
	# Сreating a Graph object
	def __init__(self):
		self.nodes = defaultdict(defaultdict)

	# Adding a new node to the graph
	def add_node(self, value):
		if value not in self.nodes:
			self.nodes[value] = {}

	# Adding vertices and edges		
	def add_line_and_weight(self, node_start, node_end, weight):
		if node_end not in self.nodes:
			self.add_node(node_end)
		if node_start not in self.nodes:
			self.add_node(node_start)
		self.nodes[node_start][node_end] = weight

	# Output an object of type Graph
	def __str__(self):
		output = ""
		for i in self.nodes:
			output += str(i) + " -> " + str(self.nodes[i]) + '\n'
		return output[0:-1]

	# The function of counting the time of receipt of the signal to all nodes
	def propagation_delay(self, nodeStart):
		if nodeStart not in self.nodes:
			return "Error: nodeStart not in graph"
		Inf = 0
		for i in self.nodes:
			Inf += sum(self.nodes[i].values())
		dist = {}
		is_min_dist = {}
		for i in self.nodes:
			dist[i] = Inf
			is_min_dist[i] = False
		dist[nodeStart] = 0
		node = nodeStart
		is_not_visited = False
		next_node = nodeStart
		while min(is_min_dist.values()) != True:
			min_way = Inf
			is_not_visited = True
			for i in self.nodes[node]:
				is_not_visited = is_not_visited and is_min_dist[i]
				if not is_min_dist[i]:
					if dist[i] >= dist[node] + self.nodes[node][i]:
						dist[i] = dist[node] + self.nodes[node][i]
			is_min_dist[node] = True
			for i in dist:
				if is_min_dist[i] == False and min_way >= dist[i]:
					next_node = i
					min_way = dist[i]
			if is_not_visited == True:
				if min(is_min_dist.values()) != True:
					if min_way == Inf:
						return -1
			node = next_node
		return max(dist.values())

G = Graph()
end = 0
while end == 0:
	str1 = sys.stdin.readline()
	if str1 != "\n":
		node1 = str1[0:-1].split()[0]
		node2 = str1[0:-1].split()[1]
		weight = int(str1[0:-1].split()[2])
		G.add_line_and_weight(node1,node2, weight)
	else:
		end = 1
print("Enter the number of nodes:")
N = int(input())
for i in range(N):
	G.add_node(str(i + 1))
print("Selected nodeStart:")
X = input()
print(G.propagation_delay(X))