import pygame
import os
from utils import wrap_text

def show_instructions(screen):
    # Load and scale background image
    bg_path = os.path.join("assets", "background.png")
    bg_img = pygame.image.load(bg_path).convert()
    bg_img = pygame.transform.scale(bg_img, (screen.get_width(), screen.get_height()))

    font_path = os.path.join("assets", "fonts", "Daydream.ttf")
    title_font = pygame.font.Font(font_path, 50)
    body_font = pygame.font.Font(font_path, 30)

    # Instruction text
    title_text = "How to Play"
    instructions = [
        "Player 1: Use the Arrow Keys to move.",
        "Player 2: Use WASD to move.",
        "Reach the maze center to win.",
        "Press Ctrl+S to display the solution.",
        "",
        "Press Enter to start the game."
    ]

    # Render title
    title_surf = title_font.render(title_text, True, (255, 215, 0))
    title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 100))

    # Wrap instructions
    max_width = screen.get_width() - 100  # Keep some padding
    wrapped_lines = []
    for line in instructions:
        wrapped_lines.extend(wrap_text(line, body_font, max_width))

    clock = pygame.time.Clock()
    
    while True:
        screen.blit(bg_img, (0, 0))  # Reset screen with background image
        screen.blit(title_surf, title_rect)  # Draw the title

        # Reset `start_y` at the beginning of each frame
        start_y = 180  
        line_spacing = 40  

        # Draw each wrapped line, maintaining correct spacing
        for line in wrapped_lines:
            text_surf = body_font.render(line, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(screen.get_width() // 2, start_y))
            screen.blit(text_surf, text_rect)
            start_y += line_spacing  # Move to next line

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"

        clock.tick(30)
