# Maze Solver

#### Video Demo:

#### Description
This project is a maze solver implemented in Python using various search algorithms. The maze is read from a text file, and different solving methods are applied to find a path from the start point to the goal. The solution path, explored cells, and maze walls are visualized in an image.

#### Features
- **Multiple Solving Algorithms**: Supports Depth-First Search (DFS), Breadth-First Search (BFS), Greedy Best-First Search (GBFS), and A* Search algorithms.
- **Maze Visualization**: Generates an image representation of the maze, showing walls, start and goal points, solution path, and explored cells.
- **Customizable Input**: Allows passing the maze file and solving method as command-line arguments.

#### Dependencies
The program relies on the following dependencies:
- **Python 3.x**: The programming language used to develop the application.
- **PIL (Pillow)**: Python Imaging Library for generating maze images.
- **matplotlib**: Library for additional plotting and visualization.

#### Usage
1. **Prepare the Maze File**: Create a text file with the maze layout. Use 'A' for the start point, 'B' for the goal, '#' for walls, and ' ' for open spaces.
2. **Run the Program**: Execute the Python script with the maze file and desired solving algorithm. For example:
    ```bash
    python maze.py maze.txt DFS
    ```
   Supported algorithms are DFS, BFS, GBFS, and A*.

3. **View the Maze**: The solution and visualization will be displayed in the console and saved as `maze.png` in the current directory. The image will show walls, start and goal points, solution path, and explored cells.

#### Example
```bash
python maze.py example_maze.txt A*
```
This command will solve the maze in example_maze.txt using the A* algorithm and save the visualization to maze.png.

#### Contributing
Contributions to this maze solver project are welcome. If you find any bugs, or issues, or have suggestions for enhancements, please feel free to open an issue or submit a pull request.
