import pygame

class Player:
    def __init__(self, row, col, skin, tile_size, controls):
        self.row = row
        self.col = col
        self.tile_size = tile_size
        self.controls = controls
        self.skin = pygame.transform.scale(skin, (tile_size, tile_size))
    
    def move(self, direction, maze):
        cell = maze.grid[self.row][self.col]
        if direction == "up" and not cell.walls.get("top", True) and self.row > 0:
            self.row -= 1
        elif direction == "down" and not cell.walls.get("bottom", True) and self.row < maze.rows - 1:
            self.row += 1
        elif direction == "left" and not cell.walls.get("left", True) and self.col > 0:
            self.col -= 1
        elif direction == "right" and not cell.walls.get("right", True) and self.col < maze.cols - 1:
            self.col += 1

    def draw(self, screen):
        x = self.col * self.tile_size
        y = self.row * self.tile_size
        screen.blit(self.skin, (x, y))
