import pygame
from maze import Maze
from player import Player
from skin_manager import SkinManager  # For loading skins
from utils import wrap_text

class Game:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.tile_size = 40  # Adjust as desired
        self.rows = self.screen.get_height() // self.tile_size
        self.cols = self.screen.get_width() // self.tile_size
        self.maze = Maze(self.rows, self.cols, self.tile_size)  # Defaults: generate=True
        # Load skins using SkinManager.
        skin_manager = SkinManager(os.path.join("assets", "skins"))
        skin1 = skin_manager.get_skin(self.settings.get("player1_skin"))
        skin2 = skin_manager.get_skin(self.settings.get("player2_skin"))
        # Fallback if a skin is missing.
        if skin1 is None:
            skin1 = pygame.Surface((self.tile_size, self.tile_size))
            skin1.fill((255, 255, 255))
        if skin2 is None:
            skin2 = pygame.Surface((self.tile_size, self.tile_size))
            skin2.fill((255, 255, 255))
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
        self.player1 = Player(0, 0, skin1, self.tile_size, controls1)
        self.player2 = Player(0, self.cols - 1, skin2, self.tile_size, controls2)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 30)
        self.solution_path = None  # To store the solution if Ctrl+S is pressed

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(5)  # Slow, cell-by-cell movement.
        self.game_over()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    # Show solution: solve maze from (0,0) to center.
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
        # Simple DFS to find a path.
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
        if self.solution_path:
            points = []
            for cell in self.solution_path:
                x = cell.col * self.tile_size + self.tile_size // 2
                y = cell.row * self.tile_size + self.tile_size // 2
                points.append((x, y))
            if len(points) >= 2:
                pygame.draw.lines(self.screen, (255, 0, 0), False, points, 3)

    def update(self):
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
        # Draw a blue marker at the center cell.
        center_cell = self.maze.grid[self.rows // 2][self.cols // 2]
        center_rect = pygame.Rect(
            center_cell.col * self.tile_size,
            center_cell.row * self.tile_size,
            self.tile_size, self.tile_size)
        pygame.draw.rect(self.screen, (0, 0, 255), center_rect, 3)
        self.draw_solution()
        pygame.display.flip()

    def game_over(self):
        # Load and scale background image
        bg_path = os.path.join("assets", "endgame.png")
        bg_img = pygame.image.load(bg_path).convert()
        bg_img = pygame.transform.scale(bg_img, (self.screen.get_width(), self.screen.get_height()))

        # Load custom font
        font_path = os.path.join("assets", "fonts", "Daydream.ttf")
        game_over_font = pygame.font.Font(font_path, 50)

        self.screen.blit(bg_img, (0, 0))  # Set background

        # Text content
        message = "Game Over! Press any key to exit."

        # Wrap text dynamically
        max_width = self.screen.get_width() - 100  # Keep some padding
        wrapped_lines = wrap_text(message, game_over_font, max_width)

        # Render and center each line
        start_y = self.screen.get_height() // 2 - (len(wrapped_lines) * 30 // 2)  # Center vertically
        for line in wrapped_lines:
            text_surface = game_over_font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, start_y))
            self.screen.blit(text_surface, text_rect)
            start_y += 50  # Space between lines

        pygame.display.flip()

        # Wait for user input to exit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    waiting = False


# Import dependencies at the end to avoid circular issues.
import os
from maze import Maze
from skin_manager import SkinManager
from player import Player