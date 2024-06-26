import tkinter as tk
from tkinter import ttk
from src.bfs import bfs
from src.dfs import dfs
import random
import time

# Function to generate a random maze
def generate_maze(rows, cols):
    maze = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    return maze

# Function to generate random start and end points
def generate_start_and_end(maze, rows, cols):
    start = (random.randint(0, rows-1), random.randint(0, cols-1))
    end = (random.randint(0, rows-1), random.randint(0, cols-1))
    while start == end or maze[start[0]][start[1]] == 1 or maze[end[0]][end[1]] == 1:
        start = (random.randint(0, rows-1), random.randint(0, cols-1))
        end = (random.randint(0, rows-1), random.randint(0, cols-1))
    return start, end

class MazeSolverApp(tk.Tk):
    def __init__(self, maze_size):
        super().__init__()
        self.title("Maze Solver")
        self.maze_size = maze_size
        self.maze = generate_maze(maze_size, maze_size)
        self.start, self.end = generate_start_and_end(self.maze, maze_size, maze_size)
        self.canvas = tk.Canvas(self, width=500, height=500, bg="white")
        self.canvas.pack()
        
        self.algo_var = tk.StringVar(value="BFS")
        self.bfs_radio = ttk.Radiobutton(self, text="BFS", variable=self.algo_var, value="BFS", command=self.reset_solution)
        self.bfs_radio.pack()
        self.dfs_radio = ttk.Radiobutton(self, text="DFS", variable=self.algo_var, value="DFS", command=self.reset_solution)
        self.dfs_radio.pack()
        
        self.solve_button = ttk.Button(self, text="Solve Maze", command=self.solve_maze)
        self.solve_button.pack()
        
        self.refresh_button = ttk.Button(self, text="Refresh", command=self.refresh_maze)
        self.refresh_button.pack()
        
        self.result_label = tk.Label(self, text="", bg="white")
        self.result_label.pack(fill=tk.BOTH, expand=True)

        self.draw_maze()

    def draw_maze(self):
        self.canvas.delete("all")
        rows, cols = len(self.maze), len(self.maze[0])
        cell_width = 500 // cols
        cell_height = 500 // rows
        for r in range(rows):
            for c in range(cols):
                if (r, c) == self.start:
                    color = "blue"
                elif (r, c) == self.end:
                    color = "red"
                else:
                    color = "white" if self.maze[r][c] == 0 else "black"
                self.canvas.create_rectangle(c * cell_width, r * cell_height, (c + 1) * cell_width, (r + 1) * cell_height, fill=color)
    
    def draw_path(self, path, color="blue"):
        if not path:
            return
        cell_width = 500 // len(self.maze[0])
        cell_height = 500 // len(self.maze)
        for (r, c) in path:
            if (r, c) != self.start and (r, c) != self.end:
                self.canvas.create_rectangle(c * cell_width, r * cell_height, (c + 1) * cell_width, (r + 1) * cell_height, fill=color)

    def solve_maze(self):
        algo = self.algo_var.get()
        start_time = time.time()
        if algo == "BFS":
            path, explored_count = bfs(self.maze, self.start, self.end, self.draw_step)
        else:
            path, explored_count = dfs(self.maze, self.start, self.end, self.draw_step)
        end_time = time.time()
        if path:
            self.draw_path(path, color="green")
            self.result_label.config(text=f"{algo} Path Length: {len(path)}\nTime: {end_time - start_time:.6f} seconds\nExplored Cells: {explored_count}")
        else:
            self.result_label.config(text=f"{algo} found no path\nExplored Cells: {explored_count}")

    def draw_step(self, position, color):
        rows, cols = len(self.maze), len(self.maze[0])
        cell_width = 500 // cols
        cell_height = 500 // rows
        r, c = position
        if (r, c) != self.start and (r, c) != self.end:
            self.canvas.create_rectangle(c * cell_width, r * cell_height, (c + 1) * cell_width, (r + 1) * cell_height, fill=color)
        self.update()

    def refresh_maze(self):
        self.maze = generate_maze(self.maze_size, self.maze_size)
        self.start, self.end = generate_start_and_end(self.maze, self.maze_size, self.maze_size)
        self.result_label.config(text="")
        self.draw_maze()

    def reset_solution(self):
        self.result_label.config(text="")
        self.draw_maze()
