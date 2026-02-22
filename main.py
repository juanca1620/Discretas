import pygame
import sys
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
