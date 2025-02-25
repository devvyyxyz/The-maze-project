import pygame
import os
from menu import show_menu
from instructions import show_instructions
from game import Game
from settings import SettingsMenu
from skin_manager import SkinManager
from skin_selection import skin_selection_menu

def main():
    pygame.init()
    
    # Load settings with default values
    settings = {
        "volume": 50,
        "player1_skin": None,
        "player2_skin": None,
        "resolution": (800, 600),  # Default resolution
        "fullscreen": False
    }

    # Apply initial resolution and fullscreen mode
    if settings["fullscreen"]:
        screen = pygame.display.set_mode(settings["resolution"], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(settings["resolution"])
    
    pygame.display.set_caption("Maze Race")

    while True:
        choice = show_menu(screen)

        if choice == "start":
            # Show instructions screen before starting the game
            if show_instructions(screen) == "exit":
                pygame.quit()
                return

            # Instantiate the skin manager
            skin_manager = SkinManager(os.path.join("assets", "skins"))

            # If a player's skin hasn't been selected, run skin selection
            if settings["player1_skin"] is None:
                chosen_skin1 = skin_selection_menu(screen, skin_manager, "Player 1: Choose Your Skin")
                if chosen_skin1 is None:
                    pygame.quit()
                    return
                settings["player1_skin"] = chosen_skin1

            if settings["player2_skin"] is None:
                chosen_skin2 = skin_selection_menu(screen, skin_manager, "Player 2: Choose Your Skin")
                if chosen_skin2 is None:
                    pygame.quit()
                    return
                settings["player2_skin"] = chosen_skin2

            # Start the game with selected settings
            game = Game(screen, settings)
            game.run()

        elif choice == "settings":
            settings_menu = SettingsMenu(screen, settings)
            result, updated_settings = settings_menu.run()
            settings.update(updated_settings)

            # Apply settings immediately
            if settings["fullscreen"]:
                screen = pygame.display.set_mode(settings["resolution"], pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode(settings["resolution"])


        elif choice == "exit":
            pygame.quit()
            return

if __name__ == "__main__":
    main()
