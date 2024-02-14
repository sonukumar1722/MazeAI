import sys
from util import Node, StackFrontier, QueueFrontier, GreedyFrontier, AStarFrontier
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# Define a class to represent the maze and solve it
class Maze():

    def __init__(self, filename):
        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1 or contents.count("B") != 1:
            raise Exception("Maze must have exactly one start point and one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls and other properties
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    # Print the maze, including walls, start, goal, and solution path
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("#", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    # Find neighboring states that are accessible
    def neighbors(self, state):
        row, col = state
        candidates = [("up", (row - 1, col)), ("down", (row + 1, col)), ("left", (row, col - 1)), ("right", (row, col + 1))]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    # Solve the maze using depth-first search
    def solve(self, method):

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = method
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        while True:
            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("No solution")

            # Choose a node from the frontier
            if sys.argv[2] in ['gbfs', 'GBFS']:
                node = frontier.remove(self.goal)
            elif sys.argv[2] in ['A*', 'a*']:
                node = frontier.remove(self.start, self.goal)
            else:
                node = frontier.remove()

            # number of explored nodes 
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            # Mark node as explored
            self.explored.add(node.state)
            
            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    # Output an image representation of the maze
    def output_image(self, filename, show_solution=True, show_explored=False):
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )

        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        font = ImageFont.load_default()

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                end_steps = start_steps = ""

                # Determine fill color based on cell type
                if  col:
                    fill = (40, 40, 40)  # Wall
                elif (i, j) == self.start:
                    fill = (255, 0, 0)  # Start
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)  # Goal
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)  # Solution path
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)  # Explored cells
                else:
                    fill = (237, 240, 252)  # Empty cell
                    
                
                if not col:
                    end_steps = AStarFrontier.heuristic(self.goal, (i, j))
                    start_steps = AStarFrontier.path_function(self.start, (i, j))


                # Draw cell on the canvas
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                        ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

                 # Draw number in the cell 
                font = ImageFont.truetype("arial.ttf", 15,  index=0, encoding="unic")
                if (start_steps or end_steps) is not None:
                    if sys.argv[2] in ['A*', 'a*']:
                        text = str (start_steps) + str("+") + str(end_steps)
                    elif sys.argv[2] in ['gbfs', 'GBFS']:
                        text = str(end_steps)
                    else:
                        text = ""
                    text_position = ((j * cell_size + (cell_size) // 8),
                                     (i * cell_size + (cell_size) // 3))
                    draw.text(text_position, text, font=font, fill=(0, 0, 0))

        img.save(filename)



if __name__ == "__main__":
    try:
        # Check if a maze file argument is provided
        if len(sys.argv) != 3:
            sys.exit("Usage: python maze.py maze.txt [DFS/BFS/GBFS]")

        m = Maze(sys.argv[1])
        print("Maze:")
        m.print()
        print("Solving...")

        # Algorithms
        if sys.argv[2] in ("DFS", "dfs"):
            m.solve(StackFrontier())
        elif sys.argv[2] in ("BFS", "bfs"):
            m.solve(QueueFrontier())
        elif sys.argv[2] in ("GBFS", "gbfs"):
            m.solve(GreedyFrontier())
        elif sys.argv[2] in ("A*", "a*"):
            m.solve(AStarFrontier())
        else:
            print("Algorithm not found!")

        print("States Explored:", m.num_explored)
        print("Solution:")
        m.print()
        m.output_image("maze.png", show_explored=True)
        
    except FileNotFoundError:
        print("File not found!")
    except Exception as e:
        print(e)
