from collections import deque
import time

# BFS Algorithm
def bfs(maze, start, end, draw_func):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, [start])])
    visited = set([start])
    explored_count = 0
    
    while queue:
        (current, path) = queue.popleft()
        if current == end:
            return path, explored_count
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_move = (current[0] + dx, current[1] + dy)
            if 0 <= next_move[0] < rows and 0 <= next_move[1] < cols and maze[next_move[0]][next_move[1]] == 0 and next_move not in visited:
                queue.append((next_move, path + [next_move]))
                visited.add(next_move)
                explored_count += 1
                draw_func(next_move, "yellow")
                time.sleep(0.01)
    return None, explored_count