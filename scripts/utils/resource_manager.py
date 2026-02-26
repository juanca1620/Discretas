import pygame
import os
import sys

def _get_base_dir():
    """Returns the base project directory whether running normally or from a PyInstaller exe."""
    if getattr(sys, 'frozen', False):
        # Running inside a PyInstaller bundle
        return sys._MEIPASS
    else:
        # Running normally: go up two levels from scripts/utils/ to reach project root
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = _get_base_dir()

class ResourceManager:
    """
    Centralized Resource Manager to load and cache game assets.
    """
    _images = {}
    _sounds = {}
    _fonts = {}

    @classmethod
    def load_image(cls, name, path):
        if name not in cls._images:
            full_path = os.path.join(BASE_DIR, "assets", "images", path)
            try:
                image = pygame.image.load(full_path).convert_alpha()
                cls._images[name] = image
            except (pygame.error, FileNotFoundError) as e:
                print(f"Unable to load image at {full_path}: {e}")
                return None
        return cls._images[name]

    @classmethod
    def load_sound(cls, name, path):
        if name not in cls._sounds:
            full_path = os.path.join(BASE_DIR, "assets", "sounds", path)
            try:
                sound = pygame.mixer.Sound(full_path)
                cls._sounds[name] = sound
            except (pygame.error, FileNotFoundError) as e:
                print(f"Unable to load sound at {full_path}: {e}")
                return None
        return cls._sounds[name]

    @classmethod
    def get_image(cls, name):
        return cls._images.get(name)

    @classmethod
    def get_sound(cls, name):
        return cls._sounds.get(name)
