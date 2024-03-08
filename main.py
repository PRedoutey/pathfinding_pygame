# Patrick Redoutey
# ETGG4803-01
# Lab 5: Graph Traversal and Path Search

import pygame, sys
from pygame.locals import QUIT
import graph

# Switch between Dijkstra and A* by changing 'use_heuristic' on line 88

def graph_init():
	G = graph.Graph()

	G.add_node("Arad", 40, 98, 366)
	G.add_node("Bucharest", 373, 275, 0)
	G.add_node("Craiova", 214, 318, 160)
	G.add_node("Drobeta", 120, 306, 242)
	G.add_node("Eforie", 547, 312, 161)
	G.add_node("Fagaras", 272, 145, 176)
	G.add_node("Giurgiu", 345, 337, 77)
	G.add_node("Hirsova", 516, 252, 151)
	G.add_node("Iasi", 451, 83, 226)
	G.add_node("Lugoj", 119, 221, 244)
	G.add_node("Mehadia", 123, 263, 241)
	G.add_node("Neamt", 378, 50, 234)
	G.add_node("Oradea", 83, 13, 380)
	G.add_node("Pitesti", 287, 233, 100)
	G.add_node("Rimnicu Vilcea", 193, 186, 193)
	G.add_node("Sibiu", 165, 136, 253)
	G.add_node("Timisoara", 43, 187, 329)
	G.add_node("Urziceni", 433, 252, 80)
	G.add_node("Vaslui", 490, 150, 199)
	G.add_node("Zerind", 58, 56, 374)
	
	G.add_edge("Arad", "Timisoara", 118.0)
	G.add_edge("Arad", "Sibiu", 140.0)
	G.add_edge("Arad", "Zerind", 75.0)
	G.add_edge("Bucharest", "Fagaras", 211.0)
	G.add_edge("Bucharest", "Giurgiu", 90.0)
	G.add_edge("Bucharest", "Pitesti", 101.0)
	G.add_edge("Bucharest", "Urziceni", 85.0)
	G.add_edge("Craiova", "Drobeta", 120.0)
	G.add_edge("Craiova", "Pitesti", 138.0)
	G.add_edge("Craiova", "Rimnicu Vilcea", 146.0)
	G.add_edge("Drobeta", "Craiova", 120.0)
	G.add_edge("Drobeta", "Mehadia", 75.0)
	G.add_edge("Eforie", "Hirsova", 86.0)
	G.add_edge("Fagaras", "Bucharest", 211.0)
	G.add_edge("Fagaras", "Sibiu", 99.0)
	G.add_edge("Giurgiu", "Bucharest", 90.0)
	G.add_edge("Hirsova", "Eforie", 86.0)
	G.add_edge("Hirsova", "Urziceni", 98.0)
	G.add_edge("Iasi", "Neamt", 87.0)
	G.add_edge("Iasi", "Vaslui", 92.0)
	G.add_edge("Lugoj", "Mehadia", 70.0)
	G.add_edge("Lugoj", "Timisoara", 111.0)
	G.add_edge("Mehadia", "Drobeta", 75.0)
	G.add_edge("Mehadia", "Lugoj", 70.0)
	G.add_edge("Neamt", "Iasi", 87.0)
	G.add_edge("Oradea", "Sibiu", 151.0)
	G.add_edge("Oradea", "Zerind", 71.0)
	G.add_edge("Pitesti", "Bucharest", 101.0)
	G.add_edge("Pitesti", "Craiova", 138.0)
	G.add_edge("Pitesti", "Rimnicu Vilcea", 97.0)
	G.add_edge("Rimnicu Vilcea", "Craiova", 146.0)
	G.add_edge("Rimnicu Vilcea", "Sibiu", 80.0)
	G.add_edge("Rimnicu Vilcea", "Pitesti", 97.0)
	G.add_edge("Sibiu", "Arad", 140.0)
	G.add_edge("Sibiu", "Fagaras", 99.0)
	G.add_edge("Sibiu", "Oradea", 151.0)
	G.add_edge("Sibiu", "Rimnicu Vilcea", 80.0)
	G.add_edge("Timisoara", "Arad", 118.0)
	G.add_edge("Timisoara", "Lugoj", 111.0)
	G.add_edge("Urziceni", "Bucharest", 85.0)
	G.add_edge("Urziceni", "Hirsova", 98.0)
	G.add_edge("Urziceni", "Vaslui", 142.0)
	G.add_edge("Vaslui", "Iasi", 92.0)
	G.add_edge("Vaslui", "Urziceni", 142.0)
	G.add_edge("Zerind", "Arad", 75.0)
	G.add_edge("Zerind", "Oradea", 71.0)

	return G

pygame.init()

G = graph_init()
# use_heuristic: False -> Dijkstra, True -> A* Search
G.pathfinding_init("Arad", "Bucharest", use_heuristic=True)
ret = 0

fps = 2
clock = pygame.time.Clock()
ds = pygame.display.set_mode((650, 350))
pygame.display.set_caption('Lab 5: Graph Traversal and Path Search')
while True:
	clock.tick(fps)
	for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
	if ret == 0:
		ret = G.pathfinding_next()
	ds.fill((255, 255, 255))
	G.draw(ds)
	pygame.display.update()