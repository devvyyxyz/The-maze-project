import pygame
import sys
import random
import time
from player import Player
from maze import generate_maze, draw_maze
from utils import show_instructions, display_winner
from vars import WHITE, RED, GREEN, BLUE, PURPLE, WIDTH, HEIGHT, CELL_SIZE, ROWS, COLS, screen

# Initialize pygame
pygame.init()

# Clock
clock = pygame.time.Clock()


def draw_button(text, rect, color, font):
    """Draws a button with text"""
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, WHITE)
    screen.blit(label,
                (rect.x + (rect.width - label.get_width()) // 2, rect.y + (rect.height - label.get_height()) // 2))


def main_menu():
    """Displays the main menu and handles button interactions"""
    font = pygame.font.Font(None, 50)
    play_button = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 50)  # Play button
    exit_button = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)  # Exit button
    running = True

    while running:
        screen.fill(WHITE)

        # Draw buttons
        draw_button("PLAY", play_button, BLUE, font)
        draw_button("EXIT", exit_button, RED, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    start_game()
                    return  # Exit the menu
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()


def start_game():
    """Starts the game after 'Play' is selected"""
    round_number = 1
    virus_wins = 0
    anti_virus_wins = 0

    while round_number <= 3:
        maze = generate_maze(ROWS, COLS, round_number)
        virus = Player("../assets/virus_icon.png", (1, 1))
        anti_virus = Player("../assets/anti_virus_icon.png", (COLS - 2, ROWS - 2))
        center = (COLS // 2, ROWS // 2)
        power_up = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))
        running = True
        turn = "virus"
        start_time = time.time()
        round_time_limit = 30  # Time limit for each round

        while running:
            screen.fill(WHITE)
            draw_maze(maze)
            virus.draw()
            anti_virus.draw()

            pygame.draw.rect(screen, BLUE, (center[0] * CELL_SIZE, center[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, PURPLE, (power_up[0] * CELL_SIZE, power_up[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            elapsed_time = time.time() - start_time
            if elapsed_time >= round_time_limit:
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if turn == "virus":
                if keys[pygame.K_LEFT]: virus.move(-1, 0, maze)
                if keys[pygame.K_RIGHT]: virus.move(1, 0, maze)
                if keys[pygame.K_UP]: virus.move(0, -1, maze)
                if keys[pygame.K_DOWN]: virus.move(0, 1, maze)
                turn = "anti_virus"
            else:
                if keys[pygame.K_a]: anti_virus.move(-1, 0, maze)
                if keys[pygame.K_d]: anti_virus.move(1, 0, maze)
                if keys[pygame.K_w]: anti_virus.move(0, -1, maze)
                if keys[pygame.K_s]: anti_virus.move(0, 1, maze)
                turn = "virus"

            if virus.pos == power_up or anti_virus.pos == power_up:
                power_up = (-1, -1)
                maze[random.randint(1, ROWS - 2)][random.randint(1, COLS - 2)] = 1

            if virus.pos == center: virus_wins += 1; running = False
            if anti_virus.pos == center: anti_virus_wins += 1; running = False

            pygame.display.flip()
            clock.tick(10)

        round_number += 1

    display_winner("Virus" if virus_wins > anti_virus_wins else "Anti-Virus", screen)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_menu()  # Start the main menu
