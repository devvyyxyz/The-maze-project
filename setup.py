import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virus vs Anti-Virus Maze Race")

# Clock
clock = pygame.time.Clock()

# Maze dimensions
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Generate a simple maze (0 = path, 1 = wall)
def generate_maze(rows, cols):
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Add some random walls
    for i in range(rows):
        for j in range(cols):
            if random.random() < 0.2:  # 20% chance to be a wall
                maze[i][j] = 1
    
    # Ensure the center is accessible
    maze[rows//2][cols//2] = 0
    return maze

# Draw the maze
def draw_maze(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Player class
class Player:
    def __init__(self, color, start_pos):
        self.color = color
        self.pos = start_pos

    def move(self, dx, dy, maze):
        new_x = self.pos[0] + dx
        new_y = self.pos[1] + dy
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
            self.pos = (new_x, new_y)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.pos[0] * CELL_SIZE + CELL_SIZE//2, self.pos[1] * CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)

# Main game loop
def main():
    maze = generate_maze(ROWS, COLS)
    virus = Player(RED, (0, 0))
    anti_virus = Player(GREEN, (COLS-1, ROWS-1))
    center = (COLS//2, ROWS//2)

    running = True
    while running:
        screen.fill(WHITE)
        draw_maze(maze)
        virus.draw()
        anti_virus.draw()

        # Draw the center
        pygame.draw.rect(screen, BLUE, (center[0] * CELL_SIZE, center[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            virus.move(-1, 0, maze)
        if keys[pygame.K_RIGHT]:
            virus.move(1, 0, maze)
        if keys[pygame.K_UP]:
            virus.move(0, -1, maze)
        if keys[pygame.K_DOWN]:
            virus.move(0, 1, maze)

        if keys[pygame.K_a]:
            anti_virus.move(-1, 0, maze)
        if keys[pygame.K_d]:
            anti_virus.move(1, 0, maze)
        if keys[pygame.K_w]:
            anti_virus.move(0, -1, maze)
        if keys[pygame.K_s]:
            anti_virus.move(0, 1, maze)

        # Check for win condition
        if virus.pos == center:
            print("Virus wins!")
            running = False
        if anti_virus.pos == center:
            print("Anti-Virus wins!")
            running = False

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()