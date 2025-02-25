import pygame
import os
import math

def show_menu(screen):
    # Load background image.
    bg_path = os.path.join("assets", "background.png")
    bg_img = pygame.image.load(bg_path).convert()

    FONT_PATH = os.path.join("assets", "fonts", "Daydream.ttf") 
    title_font = pygame.font.Font(FONT_PATH, 60)
    option_font = pygame.font.Font(FONT_PATH, 40)
    
    # Render the game title.
    title_text = title_font.render("Maze Race", True, (255, 215, 0))  # Gold color
    base_y = 150  # Base Y position for the title.
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, base_y))
    
    options = ["Start", "Settings", "Exit"]
    option_rects = []
    start_y = 300
    spacing = 60
    
    for i, option in enumerate(options):
        surf = option_font.render(option, True, (255, 255, 255))
        rect = surf.get_rect(center=(screen.get_width() // 2, start_y + i * spacing))
        option_rects.append(rect)
    
    selected = 0
    clock = pygame.time.Clock()
    
    while True:
        # Draw background first.
        screen.blit(bg_img, (0, 0))
        
        # Update title bobbing using sine.
        t = pygame.time.get_ticks() / 1000.0  # Time in seconds.
        amplitude = 10  # pixels up/down
        frequency = 0.5  # cycles per second
        offset = amplitude * math.sin(2 * math.pi * frequency * t)
        title_rect.centery = base_y + offset

        screen.blit(title_text, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw options with hover highlighting.
        for i, option in enumerate(options):
            if option_rects[i].collidepoint(mouse_pos):
                text_color = (0, 255, 0)
                selected = i
            else:
                text_color = (255, 255, 255)
            option_surf = option_font.render(option, True, text_color)
            screen.blit(option_surf, option_rects[i])
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected].lower()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            return options[i].lower()
        clock.tick(30)
