import os
import pygame

class SkinManager:
    def __init__(self, folder):
        self.folder = folder
        self.skins = {}
        self.load_skins()

    def load_skins(self):
        for filename in os.listdir(self.folder):
            if filename.lower().endswith('.png'):
                skin_name = os.path.splitext(filename)[0]
                path = os.path.join(self.folder, filename)
                self.skins[skin_name] = pygame.image.load(path).convert_alpha()

    def get_skin(self, skin_name):
        return self.skins.get(skin_name)

    def available_skins(self):
        return list(self.skins.keys())