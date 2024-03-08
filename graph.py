import pygame
import math

NODE_UNVISITED = 0
NODE_CURRENT = 1
NODE_VISITED = 2
NODE_PATH = 3


class Node:

    def __init__(self, name, x, y, h=None):
        self.name = name
        self.x = x
        self.y = y
        # variables for dijkstra / A*
        self.h = h  # heuristic
        self.state = None
        self.dist = None
        self.prev = None
        self.just_checked = False  # used for visuals
        self.just_changed = False  # used for visuals

    def draw(self, ds, font, use_heuristic=False):
        if self.state == NODE_UNVISITED:
            box_color = (200, 200, 200)
            if self.just_checked:
                outline_color = (255, 0, 0)
                self.just_checked = False
                if self.just_changed:
                    text_color = (255, 0, 0)
                    self.just_changed = False
                else:
                    text_color = (0, 0, 0)
            else:
                outline_color = (0, 0, 0)
                text_color = (0, 0, 0)
        elif self.state == NODE_CURRENT:
            outline_color = (0, 0, 255)
            box_color = (200, 200, 200)
            text_color = (0, 0, 0)
        elif self.state == NODE_VISITED:
            outline_color = (0, 0, 255)
            box_color = (0, 0, 255)
            text_color = (0, 0, 255)
        elif self.state == NODE_PATH:
            outline_color = (0, 255, 0)
            box_color = (0, 255, 0)
            text_color = (0, 255, 0)
        pygame.draw.rect(ds, outline_color, (self.x - 5, self.y - 5, 10, 10))
        pygame.draw.rect(ds, box_color, (self.x - 3, self.y - 3, 6, 6))
        if use_heuristic:
            text = f"{self.name} ({self.h})"
        else:
            text = self.name
        name_text = font.render(text, True, text_color)
        name_rect = name_text.get_rect()
        name_rect.x = self.x + 6
        name_rect.center = name_rect.center[0], self.y
        ds.blit(name_text, name_rect)
        dist_text = font.render(str(self.dist), True, text_color)
        dist_rect = dist_text.get_rect()
        dist_rect.center = (name_rect.center[0], name_rect.center[1] - 12)
        ds.blit(dist_text, dist_rect)


class Graph:

    def __init__(self):
        self.data = {}  # graph data
        self.nodes = {}  # node data
        # available fonts: ['dejavuserif', 'dejavusansmono', 'dejavusans']
        self.font = pygame.font.SysFont("dejavusans", 10)
        # variables for dijkstra / A*
        self.use_heuristic = None  # False for Dijkstra, True for A*
        self.start = None
        self.end = None
        self.cur_node_name = None
        self.cur_neighbors = None
        self.find_next_node = None  # will be function

    def add_node(self, name, x, y, h=None):
        if name not in self.data:
            self.data[name] = {}  # neighbors
            self.nodes[name] = Node(name, x, y, h)  # node

    def add_edge(self, start, end, edge):
        if start not in self.data or end not in self.data:
            raise IndexError("Invalid key")
        self.data[start][end] = edge

    def get_edge(self, start, end):
        if start not in self.data or end not in self.data:
            raise IndexError("Invalid key")
        return self.data[start][end]

    def get_num_nodes(self):
        return len(self.data)

    def find_next_node_dijkstra(self):
        # Initialize lowest distance - it will determine next node
        lowest_dist = math.inf
        # Set current node as the node with the lowest temporary value
        for node in self.nodes.values():
            if node.state == NODE_UNVISITED and node.dist < lowest_dist:
                lowest_dist = node.dist
                self.cur_node_name = node.name
        return lowest_dist

    def find_next_node_a_star(self):
        # Initialize lowest distance - it will determine next node
        lowest_dist = math.inf
        # Set current node as the node with the lowest temporary value
        for node in self.nodes.values():
            if node.state == NODE_UNVISITED and node.dist + node.h < lowest_dist:
                lowest_dist = node.dist + node.h
                self.cur_node_name = node.name
        return lowest_dist

    def pathfinding_init(self, start, end, use_heuristic=False):
        """
        Params:\n
          start: name of starting city (str)\n
          end: name of destination city (str)\n
          use_heuristic: False for Dijkstra, True for A* Search
        """
        if start not in self.data or end not in self.data:
            raise IndexError("Invalid key")
        self.start = start
        self.end = end
        self.use_heuristic = use_heuristic
        if self.use_heuristic:
            self.find_next_node = self.find_next_node_a_star
        else:
            self.find_next_node = self.find_next_node_dijkstra
        # Initialize node data
        for node in self.nodes.values():
            node.state = NODE_UNVISITED
            node.dist = math.inf
            node.prev = start
        # Set starting node
        self.cur_node_name = start
        self.nodes[self.cur_node_name].state = NODE_CURRENT
        self.nodes[self.cur_node_name].dist = 0
        # Initialize neighbor list
        self.cur_neighbors = []
        for neighbor in self.data[self.cur_node_name].keys():
            if self.nodes[neighbor].state == NODE_UNVISITED:
                self.cur_neighbors.append(neighbor)
    
    def pathfinding_next(self):
        """
		Returns:\n
		-1 if no path exists\n
		 0 if still processing\n
		 1 if path has been found
		"""
        cur_node = self.nodes[self.cur_node_name]
        # If there are any neighbors, process one
        if len(self.cur_neighbors) != 0:
            cur_neighbor = self.cur_neighbors[0]
            dist = self.get_edge(self.cur_node_name, cur_neighbor)
            neighbor_node = self.nodes[cur_neighbor]
            # Update temporary value of node if current node provides a shorter path
            if neighbor_node.dist > cur_node.dist + dist:
                neighbor_node.dist = cur_node.dist + dist
                neighbor_node.just_changed = True
                # Record node that caused update - used for determining actual path
                neighbor_node.prev = self.cur_node_name
            neighbor_node.just_checked = True
            self.cur_neighbors.pop(0)
        # Otherwise, choose next node to visit
        else:
            # Set current node as visited
            cur_node.state = NODE_VISITED
            # If current node is end node, stop - solution has been found
            if self.cur_node_name == self.end:
                # End in success
                self.find_path()
                return 1
            # Set current node and return lowest temporary value
            lowest_dist = self.find_next_node()
            if lowest_dist == math.inf:
                # End in failure
                return -1
            cur_node = self.nodes[self.cur_node_name]
            cur_node.state = NODE_CURRENT
            # If current node is end node, stop - solution has been found
            # This is an optimization of Dijkstra's algorithm
            # if self.cur_node_name == self.end:
            #     # End in success
            #     self.find_path()
            #     return 1
            # Initialize neighbor list
            for neighbor in self.data[self.cur_node_name].keys():
                if self.nodes[neighbor].state == NODE_UNVISITED:
                    self.cur_neighbors.append(neighbor)
        return 0

    def find_path(self):
        path = []
        self.nodes[self.cur_node_name].state = NODE_PATH
        path.append(self.cur_node_name)
        while self.cur_node_name != self.start:
            self.cur_node_name = self.nodes[self.cur_node_name].prev
            self.nodes[self.cur_node_name].state = NODE_PATH
            path.insert(0, self.cur_node_name)
        total_dist = self.nodes[self.end].dist
        path_string = self.start
        for node in path[1:]:
            path_string += " -> " + node
        if self.use_heuristic:
            print("A* Search\n---------")
        else:
            print("Dijkstra's Algorithm\n--------------------")
        print(f"Shortest path from {self.start} to {self.end}: {total_dist}")
        print(path_string)

    def draw(self, ds):
        visited = []
        for node1 in self.data.keys():
            start = self.nodes[node1]
            for node2, edge in self.data[node1].items():
                if node2 not in visited:
                    end = self.nodes[node2]
                    if (start.state == NODE_CURRENT and end.just_checked) or (start.just_checked and end.state == NODE_CURRENT):
                        line_color = (255, 0, 0)
                    elif (start.state == NODE_VISITED and end.state != NODE_UNVISITED) or (end.state == NODE_VISITED and start.state != NODE_UNVISITED):
                        line_color = (0, 0, 255)
                    elif start.state == NODE_PATH and end.state == NODE_PATH:
                        line_color = (0, 255, 0)
                    else:
                        line_color = (0, 0, 0)
                    pygame.draw.line(ds, line_color, (start.x, start.y),
                                     (end.x, end.y), 2)
                    mid_point = ((start.x + end.x) // 2,
                                 (start.y + end.y) // 2)
                    dist_text = self.font.render(str(edge), True, line_color)
                    text_rect = dist_text.get_rect()
                    text_rect.center = (mid_point[0] + 5, mid_point[1] - 5)
                    ds.blit(dist_text, text_rect)
            visited.append(node1)
        for node in self.nodes.values():
            node.draw(ds, self.font, self.use_heuristic)
