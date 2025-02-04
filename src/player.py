# player.py
import pygame
from maze import COLS, ROWS, CELL_SIZE
from vars import screen

class Player:
    def __init__(self, icon_path, start_pos):
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))  # Resize icon to fit the cell
        self.pos = start_pos
        self.speed_boost = False

    def move(self, dx, dy, maze):
        new_x = self.pos[0] + dx
        new_y = self.pos[1] + dy
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
            self.pos = (new_x, new_y)

    def draw(self):
        screen.blit(self.icon, (self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE))  # Draw the icon
