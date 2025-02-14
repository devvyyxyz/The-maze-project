import pygame

def show_menu(screen):
    font = pygame.font.SysFont("Arial", 40)
    options = ["Start", "Settings", "Exit"]
    selected = 0
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected else (100, 100, 100)
            text_surface = font.render(option, True, color)
            # Center the text horizontally.
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 300 + i * 50))
            screen.blit(text_surface, text_rect)
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
        clock.tick(30)
