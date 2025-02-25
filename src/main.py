import pygame
import os
from menu import show_menu
from game import Game
from settings import SettingsMenu
from skin_manager import SkinManager
from skin_selection import skin_selection_menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Maze Race")
    
    # Default settings dictionary.
    settings = {"volume": 50, "skin": None}
    
    choice = show_menu(screen)
    if choice == "start":
        # If no skin selected, show skin selection menu.
        if settings["skin"] is None:
            skin_manager = SkinManager(os.path.join("assets", "skins"))
            chosen_skin = skin_selection_menu(screen, skin_manager)
            if chosen_skin is None:
                return  # User quit the skin menu.
            settings["skin"] = chosen_skin
        game = Game(screen, settings)
        game.run()
    elif choice == "settings":
        settings_menu = SettingsMenu(screen, settings)
        result, updated_settings = settings_menu.run()
        settings.update(updated_settings)
        main()  # Return to main menu after settings.
    elif choice == "exit":
        pygame.quit()
        return
    pygame.quit()

if __name__ == "__main__":
    main()
