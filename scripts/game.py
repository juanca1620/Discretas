import pygame
import random
import constantes
from scripts.utils.resource_manager import ResourceManager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((constantes.APP_ANCHO, constantes.APP_ALTO), pygame.RESIZABLE)
        pygame.display.set_caption(constantes.TITULO)
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_hovering = False
        
        # Wink Effect Timer and State
        self.wink_timer = 0
        self.is_winking = False
        self.next_wink_time = random.randint(500, 2000) # milliseconds
        
        # Load Resources
        self.load_assets()
        self.resize_elements(constantes.APP_ANCHO, constantes.APP_ALTO)

    def load_assets(self):
        # Background
        self.bg_orig = ResourceManager.load_image("sala_inicio", "FondoInicio_Sala.png")
        
        # UI Elements
        self.dog_orig = ResourceManager.load_image("dog", "TobyOjosAbiertos.png")
        self.dog_closed_orig = ResourceManager.load_image("dog_closed", "TobyOjosCerrados.png")
        self.title_orig = ResourceManager.load_image("title", "TituloJuego.png")
        self.play_btn_orig = ResourceManager.load_image("play_button", "botonaJugar.png")
        self.play_btn_hover_orig = ResourceManager.load_image("play_button_hover", "BotosJugarMaus.png")
        self.vol_up_orig = ResourceManager.load_image("vol_up", "VolumenArriba.png")
        self.vol_mute_orig = ResourceManager.load_image("vol_mute", "Silencio.png")

    def resize_elements(self, width, height):
        # Scale Background
        if self.bg_orig:
            self.background = pygame.transform.scale(self.bg_orig, (width, height))
        
        # Scale and Position UI based on percentage of screen
        # Dog (Left side)
        if self.dog_orig:
            dog_h = int(height * 0.5)
            dog_w = int(self.dog_orig.get_width() * (dog_h / self.dog_orig.get_height()))
            # Ensure both use the exact same dimensions derived from the open state
            self.dog = pygame.transform.smoothscale(self.dog_orig, (dog_w, dog_h))
            self.dog_closed = pygame.transform.smoothscale(self.dog_closed_orig, (dog_w, dog_h))
            self.dog_pos = (int(width * 0.1), int(height * 0.4))
            
        # Title (Center-Right)
        if self.title_orig:
            title_w = int(width * 0.4)
            title_h = int(self.title_orig.get_height() * (title_w / self.title_orig.get_width()))
            self.title = pygame.transform.scale(self.title_orig, (title_w, title_h))
            self.title_pos = (int(width * 0.55), int(height * 0.3))
            
        # Play Button (Below Title)
        if self.play_btn_orig:
            btn_w = int(width * 0.2)
            btn_h = int(self.play_btn_orig.get_height() * (btn_w / self.play_btn_orig.get_width()))
            self.play_btn = pygame.transform.scale(self.play_btn_orig, (btn_w, btn_h))
            self.play_btn_hover = pygame.transform.scale(self.play_btn_hover_orig, (btn_w, btn_h))
            self.play_btn_pos = (int(width * 0.65), int(height * 0.65))
            self.play_btn_rect = self.play_btn.get_rect(topleft=self.play_btn_pos)
            
        # Volume Buttons (Top Right)
        if self.vol_up_orig:
            vol_size = int(width * 0.05)
            self.vol_up = pygame.transform.scale(self.vol_up_orig, (vol_size, vol_size))
            self.vol_up_pos = (int(width * 0.85), int(height * 0.05))
            
        if self.vol_mute_orig:
            vol_size = int(width * 0.05)
            self.vol_mute = pygame.transform.scale(self.vol_mute_orig, (vol_size, vol_size))
            self.vol_mute_pos = (int(width * 0.92), int(height * 0.05))

    def run(self):
        while self.running:
            self.clock.tick(constantes.FPS)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.size
                self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                self.resize_elements(new_width, new_height)

    def update(self):
        # Update hover state
        mouse_pos = pygame.mouse.get_pos()
        if hasattr(self, 'play_btn_rect'):
            self.is_hovering = self.play_btn_rect.collidepoint(mouse_pos)
            
        # Update Wink Logic
        dt = self.clock.get_time()
        self.wink_timer += dt
        
        if not self.is_winking:
            if self.wink_timer >= self.next_wink_time:
                self.is_winking = True
                self.wink_timer = 0
                self.wink_duration = random.randint(400, 700) # milliseconds (longer wink)
        else:
            if self.wink_timer >= self.wink_duration:
                self.is_winking = False
                self.wink_timer = 0
                self.next_wink_time = random.randint(500, 2500) # shorter wait

    def draw(self):
        # Draw Background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(constantes.COLOR_FONDO)
        
        # Draw UI Elements
        if hasattr(self, 'dog'):
            dog_img = self.dog_closed if self.is_winking else self.dog
            self.screen.blit(dog_img, self.dog_pos)
            
        if hasattr(self, 'title'): self.screen.blit(self.title, self.title_pos)
        
        if hasattr(self, 'play_btn'):
            img = self.play_btn_hover if self.is_hovering else self.play_btn
            self.screen.blit(img, self.play_btn_pos)
            
        if hasattr(self, 'vol_up'): self.screen.blit(self.vol_up, self.vol_up_pos)
        if hasattr(self, 'vol_mute'): self.screen.blit(self.vol_mute, self.vol_mute_pos)

        pygame.display.flip()
