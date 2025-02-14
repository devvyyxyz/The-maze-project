import pygame
from menu import show_menu
from game import Game
from settings import SettingsMenu

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Maze Race")
    
    # Default settings dictionary.
    settings = {"volume": 50}
    
    choice = show_menu(screen)
    if choice == "start":
        game = Game(screen, settings)
        game.run()
    elif choice == "settings":
        settings_menu = SettingsMenu(screen, settings)
        result, updated_settings = settings_menu.run()
        # Update settings based on changes.
        settings.update(updated_settings)
        # Return to main menu.
        main()
    pygame.quit()

if __name__ == "__main__":
    main()
