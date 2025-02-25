import pygame
from menu import MainMenu
from settings import SettingsMenu
from instructions import InstructionsScreen
from game import GameScreen
from skin_selection import SkinSelectionScreen

class ScreenManager:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.current_screen = "menu"
        self.screens = {
            "menu": MainMenu(self),
            "settings": SettingsMenu(self),
            "instructions": InstructionsScreen(self),
            "game": GameScreen(self),
            "skin_selection": SkinSelectionScreen(self)
        }

    def switch_screen(self, new_screen):
        """Switch to a new screen."""
        if new_screen in self.screens:
            self.current_screen = new_screen

    def run(self):
        """Main loop to run the current screen."""
        clock = pygame.time.Clock()
        while True:
            result = self.screens[self.current_screen].run()
            if result:
                self.switch_screen(result)
            clock.tick(60)
