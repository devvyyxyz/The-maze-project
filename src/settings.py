import pygame

class SettingsMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings.copy()
        self.font = pygame.font.SysFont("Arial", 30)
        self.running = True

        # Volume slider setup
        self.slider_rect = pygame.Rect(300, 300, 200, 10)
        self.slider_handle_rect = pygame.Rect(0, 290, 20, 30)
        self.volume = self.settings.get("volume", 50)
        self.update_handle_position()

        # Resolutions
        self.resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
        default_resolution = (800, 600)  # Ensure a valid resolution
        self.current_resolution_index = self.resolutions.index(self.settings.get("resolution", default_resolution))
        self.settings["resolution"] = self.resolutions[self.current_resolution_index]  # Ensure valid setting

        self.fullscreen = self.settings.get("fullscreen", False)

        self.options = ["Volume", "Resolution", "Fullscreen", "Apply", "Back"]
        self.selected_option = 0

    def update_handle_position(self):
        ratio = self.volume / 100.0
        self.slider_handle_rect.x = self.slider_rect.x + ratio * self.slider_rect.width - self.slider_handle_rect.width / 2

    def set_volume_from_mouse(self, pos):
        relative_x = pos[0] - self.slider_rect.x
        relative_x = max(0, min(relative_x, self.slider_rect.width))
        self.volume = int((relative_x / self.slider_rect.width) * 100)
        self.settings["volume"] = self.volume
        self.update_handle_position()

    def toggle_fullscreen(self):
        self.settings.setdefault("fullscreen", False)  # Ensure fullscreen key exists
        self.fullscreen = self.settings["fullscreen"]


    def change_resolution(self):
        """Cycle through available resolutions."""
        self.current_resolution_index = (self.current_resolution_index + 1) % len(self.resolutions)
        self.settings["resolution"] = self.resolutions[self.current_resolution_index]

    def apply_changes(self):
        """Apply resolution and fullscreen settings."""
        if self.settings["fullscreen"]:
            self.screen = pygame.display.set_mode(self.settings["resolution"], pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.settings["resolution"])  # Windowed mode

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            self.screen.fill((30, 30, 30))

            title = self.font.render("Settings", True, (255, 255, 255))
            self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))

            # Display settings options
            for i, option in enumerate(self.options):
                color = (0, 255, 0) if i == self.selected_option else (255, 255, 255)
                option_text = option

                if option == "Volume":
                    option_text = f"Volume: {self.volume}%"
                elif option == "Resolution":
                    option_text = f"Resolution: {self.resolutions[self.current_resolution_index][0]}x{self.resolutions[self.current_resolution_index][1]}"
                elif option == "Fullscreen":
                    option_text = f"Fullscreen: {'ON' if self.fullscreen else 'OFF'}"

                text_surface = self.font.render(option_text, True, color)
                text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 150 + i * 50))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit", self.settings
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.selected_option] == "Volume":
                            pass  # Volume is adjusted using the slider
                        elif self.options[self.selected_option] == "Resolution":
                            self.change_resolution()
                        elif self.options[self.selected_option] == "Fullscreen":
                            self.toggle_fullscreen()
                        elif self.options[self.selected_option] == "Apply":
                            self.apply_changes()
                        elif self.options[self.selected_option] == "Back":
                            self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.slider_rect.collidepoint(event.pos) or self.slider_handle_rect.collidepoint(event.pos):
                        self.set_volume_from_mouse(event.pos)
                if event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:  # Left mouse button held
                        self.set_volume_from_mouse(event.pos)

            clock.tick(60)

        return "back", self.settings
