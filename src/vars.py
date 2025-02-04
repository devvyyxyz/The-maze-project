# vars.py
import pygame

# Screen dimensions
WIDTH, HEIGHT = 600, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Maze dimensions
ROWS = 15
COLS = 15
CELL_SIZE = 40

# Directions for maze generation
DIRECTIONS = [(-2, 0), (2, 0), (0, -2), (0, 2)]

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virus vs Anti-Virus Maze Race")