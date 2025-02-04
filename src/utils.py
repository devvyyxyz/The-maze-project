# utils.py
import pygame
import sys

WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

def display_winner(winner, screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)
    text = font.render(f"{winner} Wins!", True, YELLOW)
    screen.blit(text, (WIDTH // 3, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

def show_instructions(screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 30)
    instructions = [
        "VIRUS Controls: Arrow Keys",
        "ANTI-VIRUS Controls: W, A, S, D",
        "Reach the center before your opponent!",
        "Press any key to start!"
    ]
    y_offset = 200
    for line in instructions:
        text = font.render(line, True, BLACK)
        screen.blit(text, (WIDTH // 4, y_offset))
        y_offset += 40
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
