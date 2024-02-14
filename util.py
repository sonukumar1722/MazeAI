# Define a class to represent nodes in the search tree
class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

# Define a class for the frontier
class Frontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

# Define a class for the frontier in depth-first search
class StackFrontier(Frontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        return self.frontier.pop()

# Define a class for the frontier in Greedy-best-frist search
class QueueFrontier(Frontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        return self.frontier.pop(0)

# Define a class for the frontier in Greedy-best-frist search
class GreedyFrontier(Frontier):
    @staticmethod
    def heuristic(goal, pos):
        return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])

    def remove(self, goal):
        if self.empty():
            raise Exception("empty frontier")
        
        min_distance = GreedyFrontier.heuristic(goal, self.frontier[0].state)
        min_index = 0
        
        for i, front in enumerate(self.frontier[1:]):
            distance = GreedyFrontier.heuristic(goal, front.state)
            if distance < min_distance:
                min_distance = distance
                min_index = i + 1  # Add 1 because of the offset in the loop
        
        return self.frontier.pop(min_index)

# Define a class for the frontier in Greedy-best-frist search
class AStarFrontier(GreedyFrontier):
    
    @staticmethod
    def path_function(start, pos):
        return abs(pos[0] - start[0]) + abs(pos[1] - start[1])

    def remove(self, source, goal):
        if self.empty():
            raise Exception("empty frontier")
        
        min_distance = AStarFrontier.heuristic(goal, self.frontier[0].state) + AStarFrontier.path_function(source, self.frontier[0].state)
        min_index = 0

        for i, front in enumerate(self.frontier[1:]):
            distance = GreedyFrontier.heuristic(goal, front.state) + AStarFrontier.path_function(source, front.state)
            if distance < min_distance:
                min_distance = distance
                min_index = i + 1  # Add 1 because of the offset in the loop
        
        return self.frontier.pop(min_index)


