# maze.py
import random
import pygame
from vars import WHITE, BLACK, CELL_SIZE, ROWS, COLS, DIRECTIONS, screen
from collections import deque



def generate_maze(rows, cols, difficulty):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve_path(x, y):
        maze[y][x] = 0
        random.shuffle(DIRECTIONS)
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 < nx < cols - 1 and 0 < ny < rows - 1 and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0  # Remove wall between cells
                carve_path(nx, ny)

    carve_path(1, 1)
    maze[ROWS // 2][COLS // 2] = 0  # Ensure center is always reachable

    # Add difficulty by adding walls, but ensure solvability
    def is_solvable(start, end):
        visited = set()
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == end:
                return True
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0:
                    queue.append((nx, ny))
        return False

    # Add walls but ensure paths from players to center remain
    for _ in range(difficulty * 5):
        rand_x, rand_y = random.randint(1, cols - 2), random.randint(1, rows - 2)
        if maze[rand_y][rand_x] == 0:
            maze[rand_y][rand_x] = 1
            if not (is_solvable((1, 1), (COLS // 2, ROWS // 2)) and is_solvable((COLS - 2, ROWS - 2),
                                                                                (COLS // 2, ROWS // 2))):
                maze[rand_y][rand_x] = 0  # Revert if maze becomes unsolvable

    return maze

def draw_maze(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            color = BLACK if maze[i][j] == 1 else WHITE
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
