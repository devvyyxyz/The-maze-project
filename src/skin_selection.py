import pygame
import os

def skin_selection_menu(screen, skin_manager, title_text):
    # Load and scale background image.
    bg_path = os.path.join("assets", "background.png")
    bg_img = pygame.image.load(bg_path).convert()
    bg_img = pygame.transform.scale(bg_img, (screen.get_width(), screen.get_height()))
    
    font = pygame.font.SysFont("Arial", 30)
    selected = 0
    clock = pygame.time.Clock()
    available = skin_manager.available_skins()
    
    while True:
        screen.blit(bg_img, (0, 0))
        # Draw title.
        title_surf = font.render(title_text, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surf, title_rect)
        
        # Display available skins as thumbnails.
        for i, skin_name in enumerate(available):
            skin_img = skin_manager.get_skin(skin_name)
            preview = pygame.transform.scale(skin_img, (80, 80))
            x = 100 + i * 100
            y = 200
            rect = preview.get_rect(topleft=(x, y))
            if i == selected:
                pygame.draw.rect(screen, (0, 255, 0), rect, 3)
            screen.blit(preview, rect)
            text_surf = font.render(skin_name, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(x + 40, y + 100))
            screen.blit(text_surf, text_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(available)
                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(available)
                elif event.key == pygame.K_RETURN:
                    return available[selected]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, skin_name in enumerate(available):
                        skin_img = skin_manager.get_skin(skin_name)
                        preview = pygame.transform.scale(skin_img, (80, 80))
                        x = 100 + i * 100
                        y = 200
                        rect = preview.get_rect(topleft=(x, y))
                        if rect.collidepoint(event.pos):
                            return available[i]
        clock.tick(30)