import pygame

class SettingsMenu:
    def __init__(self, screen, settings):
        """
        settings: a dict containing game settings (e.g. {'volume': 50})
        """
        self.screen = screen
        self.settings = settings.copy()  # copy to allow modifications
        self.font = pygame.font.SysFont("Arial", 30)
        self.running = True

        # Setup a volume slider.
        # Slider will be drawn as a horizontal bar.
        self.slider_rect = pygame.Rect(300, 300, 200, 10)
        # Handle is a smaller rectangle that can be dragged.
        self.slider_handle_rect = pygame.Rect(0, 290, 20, 30)
        self.volume = self.settings.get("volume", 50)
        self.update_handle_position()

    def update_handle_position(self):
        # Map volume (0-100) to slider handle position.
        ratio = self.volume / 100.0
        self.slider_handle_rect.x = self.slider_rect.x + ratio * self.slider_rect.width - self.slider_handle_rect.width / 2

    def set_volume_from_mouse(self, pos):
        # Determine new volume based on mouse x position.
        relative_x = pos[0] - self.slider_rect.x
        relative_x = max(0, min(relative_x, self.slider_rect.width))
        self.volume = int((relative_x / self.slider_rect.width) * 100)
        self.settings["volume"] = self.volume
        self.update_handle_position()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit entire game if the window is closed.
                    self.running = False
                    return "exit", self.settings
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Exit settings and go back.
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (self.slider_rect.collidepoint(event.pos) or
                        self.slider_handle_rect.collidepoint(event.pos)):
                        self.set_volume_from_mouse(event.pos)
                if event.type == pygame.MOUSEMOTION:
                    # If the left mouse button is held down, update the slider.
                    if event.buttons[0]:
                        self.set_volume_from_mouse(event.pos)

            self.draw()
            clock.tick(60)
        return "back", self.settings

    def draw(self):
        self.screen.fill((30, 30, 30))
        # Title
        title = self.font.render("Settings", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() / 2 - title.get_width() / 2, 50))
        # Volume label
        volume_label = self.font.render(f"Volume: {self.volume}", True, (255, 255, 255))
        self.screen.blit(volume_label, (100, 280))
        # Draw slider bar
        pygame.draw.rect(self.screen, (100, 100, 100), self.slider_rect)
        # Draw slider handle
        pygame.draw.rect(self.screen, (200, 200, 200), self.slider_handle_rect)
        # Instruction to exit settings
        exit_label = self.font.render("Press ESC to go back", True, (255, 255, 255))
        self.screen.blit(exit_label, (self.screen.get_width() / 2 - exit_label.get_width() / 2,
                                      self.screen.get_height() - 50))
        pygame.display.flip()
