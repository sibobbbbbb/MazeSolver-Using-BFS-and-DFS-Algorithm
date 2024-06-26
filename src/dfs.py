import time

# DFS Algorithm
def dfs(maze, start, end, draw_func):
    stack = [(start, [start])]
    visited = set([start])
    explored_count = 0
    
    while stack:
        (current, path) = stack.pop()
        if current == end:
            return path, explored_count
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_move = (current[0] + dx, current[1] + dy)
            if 0 <= next_move[0] < len(maze) and 0 <= next_move[1] < len(maze[0]) and maze[next_move[0]][next_move[1]] == 0 and next_move not in visited:
                stack.append((next_move, path + [next_move]))
                visited.add(next_move)
                explored_count += 1
                draw_func(next_move, "yellow")
                time.sleep(0.01)
    return None, explored_count