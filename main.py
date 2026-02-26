import pygame
import sys
import os

# Anchor the working directory to the project root regardless of where the exe is launched from
if getattr(sys, 'frozen', False):
    # PyInstaller bundle: _MEIPASS contains all bundled files
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(BASE_DIR)

from scripts.game import Game

def main():
    # Inicialización central de Pygame
    pygame.init()
    
    # Instanciar el gestor del juego
    game = Game()
    
    # Ejecutar el bucle principal
    game.run()
    
    # Salida limpia
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
