from collections import defaultdict
from collections import deque
import sys

# Description of class Graph:
	# The Graph is a dictionary of lists.
	# The keys are nodes, and the values are lists, 
	# consisting of nodes that have a path fron a given node.
	# Oriented Graph
class Graph:
	# Сreating a Graph object
	def __init__(self):
		self.nodes = defaultdict(list)

	# Adding a new node to the graph
	def add_node(self, value):
		if value not in self.nodes:
			self.nodes[value] = []

	# Adding vertices and line	
	def add_line(self, node_start, node_end):
		if node_end not in self.nodes:
			self.add_node(node_end)
		if node_start not in self.nodes:
			self.add_node(node_start)
		self.nodes[node_start].append(node_end)

	# Output an object of type Graph
	def __str__(self):
		output = ""
		for i in self.nodes:
			output += str(i) + " -> " + str(self.nodes[i]) + '\n'
		return output[0:-1]
	
	# Implementation of dfs algorithm
	def dfs(self, node):
		if node not in self.nodes:
			print("Error: node not in graph")
			return
		visited = [] # list of visited nodes 
		self.dfs_rec(node, visited) # recursive algorithm
		not_visited = list(set(self.nodes) - set(visited)) # if there are unvisited nodes
		while not_visited:
			self.dfs_rec(not_visited[0], visited)
			not_visited = list(set(self.nodes) - set(visited))

	# Recursive algorithm (need for dfs function)
	def dfs_rec(self, node, visited):
		if node not in visited:
			visited.append(node)
			print(node)
		for i in self.nodes[node]:
			if i not in visited:
				self.dfs_rec(i, visited)

	# Implementation of bfs algorithm			
	def bfs(self, node):
		if node not in self.nodes:
			print("Error: node not in graph")
			return
		visited = [] # list of visited nodes 
		q = deque() # the deque of nodes (used as a queue)
		q.append(node)
		while q:
			node = q.popleft()
			if node not in visited:
				visited.append(node)
				for i in self.nodes[node]:
					q.append(i)
				print(node)

G = Graph()
end = 0
while end == 0:
	str1 = sys.stdin.readline()
	if str1 != "\n":
		node1 = str1[0:-1].split()[0]
		node2 = str1[0:-1].split()[1]
		G.add_line(node1,node2)
	else:
		end = 1
print("Selected node:")
node = input()
print("Choose a method:\n1 - BFS\n2 - DFS")
method = int(input())
if method != 1:
	if method != 2:
		print("Error: incorrect method")
		pass
	else:
		G.dfs(node)
else:
	G.bfs(node)