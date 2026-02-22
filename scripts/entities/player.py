import pygame
import constantes

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Por ahora usamos un rectángulo simple hasta que el usuario cargue imágenes
        self.image = pygame.Surface((constantes.PLAYER_ANCHO, constantes.PLAYER_ALTO))
        self.image.fill(constantes.COLOR_PLAYER)
        self.rect = self.image.get_rect()
        self.rect.center = (constantes.APP_ANCHO // 2, constantes.APP_ALTO // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= constantes.PLAYER_VEL
        if keys[pygame.K_RIGHT]:
            self.rect.x += constantes.PLAYER_VEL
        if keys[pygame.K_UP]:
            self.rect.y -= constantes.PLAYER_VEL
        if keys[pygame.K_DOWN]:
            self.rect.y += constantes.PLAYER_VEL

        # Mantener al jugador dentro de la pantalla
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    # Método para cambiar el sprite usando el ResourceManager en el futuro
    def set_sprite(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=self.rect.center)
