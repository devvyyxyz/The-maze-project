import pygame
from menu import show_menu
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Maze Race")
    
    choice = show_menu(screen)
    if choice == "start":
        game = Game(screen)
        game.run()
    elif choice == "settings":
        # Placeholder for future settings implementation.
        print("Settings not implemented yet.")
    pygame.quit()

if __name__ == "__main__":
    main()
