import pygame
from maze import Maze
from player import Player

class Game:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.tile_size = 40  # Adjust as desired
        self.rows = self.screen.get_height() // self.tile_size
        self.cols = self.screen.get_width() // self.tile_size
        self.maze = Maze(self.rows, self.cols, self.tile_size)
        # Define two players with different control mappings.
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
        self.player1 = Player(0, 0, (255, 0, 0), self.tile_size, controls1)
        self.player2 = Player(0, self.cols - 1, (0, 255, 0), self.tile_size, controls2)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 30)

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
            if event.type == pygame.KEYDOWN:
                # Handle player 1 movement.
                if event.key in self.player1.controls:
                    direction = self.player1.controls[event.key]
                    self.player1.move(direction, self.maze)
                # Handle player 2 movement.
                if event.key in self.player2.controls:
                    direction = self.player2.controls[event.key]
                    self.player2.move(direction, self.maze)

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
        # Optionally, draw a marker at the center.
        center_cell = self.maze.grid[self.rows // 2][self.cols // 2]
        center_rect = pygame.Rect(
            center_cell.col * self.tile_size,
            center_cell.row * self.tile_size,
            self.tile_size, self.tile_size)
        pygame.draw.rect(self.screen, (0, 0, 255), center_rect, 3)
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
