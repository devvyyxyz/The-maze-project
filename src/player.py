import pygame

class Player:
    def __init__(self, row, col, color, tile_size, controls):
        self.row = row
        self.col = col
        self.color = color
        self.tile_size = tile_size
        # controls: dictionary mapping pygame key constants to direction strings ("up", "down", etc.)
        self.controls = controls

    def move(self, direction, maze):
        # Get the current cell from the maze grid.
        cell = maze.grid[self.row][self.col]
        if direction == "up" and not cell.walls["top"] and self.row > 0:
            self.row -= 1
        elif direction == "down" and not cell.walls["bottom"] and self.row < maze.rows - 1:
            self.row += 1
        elif direction == "left" and not cell.walls["left"] and self.col > 0:
            self.col -= 1
        elif direction == "right" and not cell.walls["right"] and self.col < maze.cols - 1:
            self.col += 1

    def draw(self, screen):
        # Draw the player as a square slightly inset within the cell.
        x = self.col * self.tile_size + self.tile_size // 4
        y = self.row * self.tile_size + self.tile_size // 4
        size = self.tile_size // 2
        pygame.draw.rect(screen, self.color, (x, y, size, size))
