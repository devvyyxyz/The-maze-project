import pygame
import os

def skin_selection_menu(screen, skin_manager, title_text):
    # Load and scale background image.
    bg_path = os.path.join("assets", "background.png")
    bg_img = pygame.image.load(bg_path).convert()
    bg_img = pygame.transform.scale(bg_img, (screen.get_width(), screen.get_height()))
    
    font = pygame.font.SysFont("Arial", 30)
    selected = 0
    scroll_offset = 0  # Tracks scrolling position
    clock = pygame.time.Clock()
    available = skin_manager.available_skins()

    max_columns = 6  # Max skins per row
    row_height = 130  # Space between rows
    max_visible_rows = 3  # Number of rows visible on screen
    max_skins_per_page = max_columns * max_visible_rows

    def get_visible_skins():
        """ Returns a slice of skins based on the scroll offset. """
        start_idx = scroll_offset * max_columns
        return available[start_idx:start_idx + max_skins_per_page]

    while True:
        screen.blit(bg_img, (0, 0))
        title_surf = font.render(title_text, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surf, title_rect)
        
        # Display available skins with scrolling
        visible_skins = get_visible_skins()
        for i, skin_name in enumerate(visible_skins):
            skin_img = skin_manager.get_skin(skin_name)
            preview = pygame.transform.scale(skin_img, (80, 80))

            row = i // max_columns
            col = i % max_columns

            x = 100 + col * 120
            y = 200 + row * row_height
            rect = preview.get_rect(topleft=(x, y))

            if i + (scroll_offset * max_columns) == selected:
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
                elif event.key == pygame.K_DOWN and (selected + max_columns) < len(available):
                    selected += max_columns
                elif event.key == pygame.K_UP and (selected - max_columns) >= 0:
                    selected -= max_columns
                elif event.key == pygame.K_RETURN:
                    return available[selected]
                elif event.key == pygame.K_w:  # Scroll up
                    if scroll_offset > 0:
                        scroll_offset -= 1
                elif event.key == pygame.K_s:  # Scroll down
                    if (scroll_offset + max_visible_rows) * max_columns < len(available):
                        scroll_offset += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll_offset > 0:  # Scroll up
                    scroll_offset -= 1
                elif event.button == 5 and (scroll_offset + max_visible_rows) * max_columns < len(available):  # Scroll down
                    scroll_offset += 1

        clock.tick(30)
