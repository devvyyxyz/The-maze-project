import pygame

def show_menu(screen):
    # Fonts for title and menu options.
    title_font = pygame.font.SysFont("Arial", 60)
    option_font = pygame.font.SysFont("Arial", 40)
    
    # Render the game title.
    title_text = title_font.render("Maze Race", True, (255, 215, 0))  # Gold color
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 150))
    
    # Define your menu options.
    options = ["Start", "Settings", "Exit"]
    option_surfaces = []
    option_rects = []
    
    start_y = 300
    spacing = 60
    
    # Create text surfaces and rects for each option.
    for i, option in enumerate(options):
        surf = option_font.render(option, True, (255, 255, 255))
        rect = surf.get_rect(center=(screen.get_width() // 2, start_y + i * spacing))
        option_surfaces.append(surf)
        option_rects.append(rect)
    
    selected = 0
    clock = pygame.time.Clock()
    
    while True:
        screen.fill((0, 0, 0))
        # Draw the title.
        screen.blit(title_text, title_rect)
        
        # Get current mouse position.
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw options. Highlight option if mouse is hovering.
        for i, option in enumerate(options):
            if option_rects[i].collidepoint(mouse_pos):
                # Use a highlight color when hovering.
                text_color = (0, 255, 0)
                selected = i  # update selected index based on hover
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
                if event.button == 1:  # left mouse button
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            return options[i].lower()
        clock.tick(30)
