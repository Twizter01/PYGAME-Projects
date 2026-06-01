# src/asset_manager.py
import pygame
import os

class AssetManager:
    def __init__(self, base_dir):
        self.base_dir    = base_dir
        self._sheets     = {}  # cache de sprite sheets
        self._sounds     = {}  # cache de sonidos
        self._fonts      = {}  # cache de fuentes

    def get_sheet(self, path):
        """Carga un sprite sheet una sola vez y lo cachea."""
        if path not in self._sheets:
            full_path = os.path.join(self.base_dir, path)
            self._sheets[path] = pygame.image.load(full_path).convert_alpha()
        return self._sheets[path]

    def get_sound(self, path):
        if path not in self._sounds:
            full_path = os.path.join(self.base_dir, path)
            self._sounds[path] = pygame.mixer.Sound(full_path)
        return self._sounds[path]

    def get_font(self, name, size):
        key = (name, size)
        if key not in self._fonts:
            self._fonts[key] = pygame.font.SysFont(name, size)
        return self._fonts[key]

    def unload(self, path):
        """Liberar un asset de la memoria cuando ya no lo necesitas."""
        self._sheets.pop(path, None)
        self._sounds.pop(path, None)

    def unload_all(self):
        self._sheets.clear()
        self._sounds.clear()
        self._fonts.clear()

