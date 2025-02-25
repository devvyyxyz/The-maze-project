import pygame
import os

class Game:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.tile_size = 40  # Adjust as desired
        self.rows = self.screen.get_height() // self.tile_size
        self.cols = self.screen.get_width() // self.tile_size
        self.maze = Maze(self.rows, self.cols, self.tile_size)  # generate defaults to True
        # Define two players with different control mappings.
        # For player skins, load via SkinManager; here we use a default colored surface if not provided.
        if self.settings.get("skin"):
            # Assume settings["skin"] holds a key for the skin.
            skin_surface = SkinManager(os.path.join("assets", "skins")).get_skin(self.settings["skin"])
        else:
            # Fallback: create a dummy surface
            skin_surface = pygame.Surface((self.tile_size, self.tile_size))
            skin_surface.fill((255, 255, 255))
        controls1 = {
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right"
        }
        controls2 = {
            pygame.K_w: "up",
            pygame.K_s: "down",
            pygame.K_a: "left",
            pygame.K_d: "right"
        }
        self.player1 = Player(0, 0, skin_surface, self.tile_size, controls1)
        self.player2 = Player(0, self.cols - 1, skin_surface, self.tile_size, controls2)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 30)
        self.solution_path = None  # To store the solution if Ctrl+S is pressed

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(5)  # Slow down for discrete, cell-by-cell movement.
        self.game_over()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                # If Ctrl+S is pressed, compute and store the solution.
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    start_cell = self.maze.grid[0][0]
                    goal_cell = self.maze.grid[self.rows // 2][self.cols // 2]
                    self.solution_path = self.solve_maze(start_cell, goal_cell)
                else:
                    if event.key in self.player1.controls:
                        direction = self.player1.controls[event.key]
                        self.player1.move(direction, self.maze)
                    if event.key in self.player2.controls:
                        direction = self.player2.controls[event.key]
                        self.player2.move(direction, self.maze)

    def get_neighbors(self, cell):
        """Return neighbors (cells connected by passages). Adjust if needed."""
        neighbors = []
        r, c = cell.row, cell.col
        if r > 0 and not cell.walls.get("top", True):
            neighbors.append(self.maze.grid[r - 1][c])
        if c < self.cols - 1 and not cell.walls.get("right", True):
            neighbors.append(self.maze.grid[r][c + 1])
        if r < self.rows - 1 and not cell.walls.get("bottom", True):
            neighbors.append(self.maze.grid[r + 1][c])
        if c > 0 and not cell.walls.get("left", True):
            neighbors.append(self.maze.grid[r][c - 1])
        return neighbors

    def solve_maze(self, start, goal):
        """Simple DFS to find a path from start to goal; returns list of cells."""
        stack = [(start, [start])]
        visited = set()
        while stack:
            current, path = stack.pop()
            if current == goal:
                return path
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited and neighbor not in path:
                    stack.append((neighbor, path + [neighbor]))
        return None

    def draw_solution(self):
        """If a solution exists, draw it as a red line through cell centers."""
        if self.solution_path:
            points = []
            for cell in self.solution_path:
                x = cell.col * self.tile_size + self.tile_size // 2
                y = cell.row * self.tile_size + self.tile_size // 2
                points.append((x, y))
            if len(points) >= 2:
                pygame.draw.lines(self.screen, (255, 0, 0), False, points, 3)

    def update(self):
        # Win condition: if any player reaches the maze center.
        center_row = self.rows // 2
        center_col = self.cols // 2
        if (self.player1.row == center_row and self.player1.col == center_col) or \
           (self.player2.row == center_row and self.player2.col == center_col):
            self.running = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.maze.draw(self.screen)
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        # Draw a marker at the center.
        center_cell = self.maze.grid[self.rows // 2][self.cols // 2]
        center_rect = pygame.Rect(
            center_cell.col * self.tile_size,
            center_cell.row * self.tile_size,
            self.tile_size, self.tile_size)
        pygame.draw.rect(self.screen, (0, 0, 255), center_rect, 3)
        # Draw solution if available.
        self.draw_solution()
        pygame.display.flip()

    def game_over(self):
        self.screen.fill((0, 0, 0))
        text_surface = self.font.render("Game Over! Press any key to exit.", True, (255, 255, 255))
        self.screen.blit(text_surface, (50, self.screen.get_height() // 2))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    waiting = False

# Ensure Maze and SkinManager are imported.
from maze import Maze
from skin_manager import SkinManager
from player import Player
