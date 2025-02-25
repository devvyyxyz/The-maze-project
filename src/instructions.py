import pygame
import os

def show_instructions(screen):
    # Load and scale background image.
    bg_path = os.path.join("assets", "background.png")
    bg_img = pygame.image.load(bg_path).convert()
    bg_img = pygame.transform.scale(bg_img, (screen.get_width(), screen.get_height()))
    
    FONT_PATH = os.path.join("assets", "fonts", "Daydream.ttf")
    title_font = pygame.font.Font(FONT_PATH, 50)
    body_font = pygame.font.Font(FONT_PATH, 30)
    
    # Instruction text.
    title_text = "How to Play"
    instructions = [
        "Player 1: Use the Arrow Keys to move.",
        "Player 2: Use WASD to move.",
        "Reach the maze center to win.",
        "Press Ctrl+S to display the solution.",
        "",
        "Press Enter to start the game."
    ]
    
    title_surf = title_font.render(title_text, True, (255, 215, 0))
    title_rect = title_surf.get_rect(center=(screen.get_width()//2, 100))
    
    body_surfs = []
    spacing = 40
    start_y = 180
    for i, line in enumerate(instructions):
        surf = body_font.render(line, True, (255, 255, 255))
        rect = surf.get_rect(center=(screen.get_width()//2, start_y + i * spacing))
        body_surfs.append((surf, rect))
        
    clock = pygame.time.Clock()
    while True:
        screen.blit(bg_img, (0, 0))
        screen.blit(title_surf, title_rect)
        for surf, rect in body_surfs:
            screen.blit(surf, rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
        clock.tick(30)
