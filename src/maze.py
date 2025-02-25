import random
import pygame

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

class Maze:
    def __init__(self, rows, cols, tile_size, generate=True):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        if generate:
            self.generate_maze()

    def generate_maze(self):
        stack = []
        current = self.grid[0][0]
        current.visited = True
        total_cells = self.rows * self.cols
        visited_cells = 1

        while visited_cells < total_cells:
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                next_cell = random.choice(neighbors)
                self.remove_walls(current, next_cell)
                stack.append(current)
                current = next_cell
                current.visited = True
                visited_cells += 1
            elif stack:
                current = stack.pop()

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        r, c = cell.row, cell.col
        if r > 0 and not self.grid[r - 1][c].visited:
            neighbors.append(self.grid[r - 1][c])
        if c < self.cols - 1 and not self.grid[r][c + 1].visited:
            neighbors.append(self.grid[r][c + 1])
        if r < self.rows - 1 and not self.grid[r + 1][c].visited:
            neighbors.append(self.grid[r + 1][c])
        if c > 0 and not self.grid[r][c - 1].visited:
            neighbors.append(self.grid[r][c - 1])
        return neighbors

    def remove_walls(self, current, next_cell):
        dx = next_cell.col - current.col
        dy = next_cell.row - current.row
        if dx == 1:
            current.walls["right"] = False
            next_cell.walls["left"] = False
        elif dx == -1:
            current.walls["left"] = False
            next_cell.walls["right"] = False
        if dy == 1:
            current.walls["bottom"] = False
            next_cell.walls["top"] = False
        elif dy == -1:
            current.walls["top"] = False
            next_cell.walls["bottom"] = False

    def draw(self, screen):
        for row in self.grid:
            for cell in row:
                x = cell.col * self.tile_size
                y = cell.row * self.tile_size
                if cell.walls["top"]:
                    pygame.draw.line(screen, (255, 255, 255), (x, y), (x + self.tile_size, y), 2)
                if cell.walls["right"]:
                    pygame.draw.line(screen, (255, 255, 255), (x + self.tile_size, y), (x + self.tile_size, y + self.tile_size), 2)
                if cell.walls["bottom"]:
                    pygame.draw.line(screen, (255, 255, 255), (x + self.tile_size, y + self.tile_size), (x, y + self.tile_size), 2)
                if cell.walls["left"]:
                    pygame.draw.line(screen, (255, 255, 255), (x, y + self.tile_size), (x, y), 2)