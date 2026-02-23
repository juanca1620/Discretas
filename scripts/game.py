import pygame
import random
import constantes
import os
from scripts.utils.resource_manager import ResourceManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(
            (constantes.APP_ANCHO, constantes.APP_ALTO),
            pygame.RESIZABLE
        )
        pygame.display.set_caption(constantes.TITULO)

        self.clock = pygame.time.Clock()
        self.running = True
        self.is_hovering = False

        # ---------------- AUDIO ----------------
        self.music_volume = 1.0
        self.music_muted = False

        # ---------------- WINK -----------------
        self.wink_timer = 0
        self.is_winking = False
        self.next_wink_time = random.randint(500, 2000)

        # ---------------- ASSETS ---------------
        self.load_assets()
        self.resize_elements(constantes.APP_ANCHO, constantes.APP_ALTO)

        # ---------------- MUSIC ----------------
        self.play_background_music()

    # --------------------------------------------------
    # ASSETS
    # --------------------------------------------------
    def load_assets(self):
        self.bg_orig = ResourceManager.load_image("sala_inicio", "FondoInicio_Sala.png")
        self.dog_orig = ResourceManager.load_image("dog", "TobyOjosAbiertos.png")
        self.dog_closed_orig = ResourceManager.load_image("dog_closed", "TobyOjosCerrados.png")
        self.title_orig = ResourceManager.load_image("title", "TituloJuego.png")
        self.play_btn_orig = ResourceManager.load_image("play_button", "botonaJugar.png")
        self.play_btn_hover_orig = ResourceManager.load_image("play_button_hover", "BotosJugarMaus.png")
        self.vol_up_orig = ResourceManager.load_image("vol_up", "VolumenArriba.png")
        self.vol_mute_orig = ResourceManager.load_image("vol_mute", "Silencio.png")

    # --------------------------------------------------
    # AUDIO
    # --------------------------------------------------
    def play_background_music(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        music_path = os.path.join(
            base_path, "..", "assets", "sounds", "Background sound effect home.mp3"
        )

        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def mute_music(self):
        pygame.mixer.music.set_volume(0)
        self.music_muted = True

    def unmute_music(self):
        pygame.mixer.music.set_volume(self.music_volume)
        self.music_muted = False

    # --------------------------------------------------
    # RESIZE
    # --------------------------------------------------
    def resize_elements(self, width, height):
        self.background = pygame.transform.scale(self.bg_orig, (width, height))

        # DOG
        dog_width = int(width * 0.3)
        dog_height = int(height * 0.5)

        self.dog = pygame.transform.smoothscale(self.dog_orig, (dog_width, dog_height))
        self.dog_closed = pygame.transform.smoothscale(self.dog_closed_orig, (dog_width, dog_height))

        self.dog_rect = self.dog.get_rect(
            center=(int(width * 0.25), int(height * 0.65))
        )

        # TITLE
        title_w = int(width * 0.4)
        title_h = int(self.title_orig.get_height() * (title_w / self.title_orig.get_width()))
        self.title = pygame.transform.scale(self.title_orig, (title_w, title_h))
        self.title_pos = (int(width * 0.55), int(height * 0.3))

        # PLAY BUTTON
        btn_w = int(width * 0.2)
        btn_h = int(self.play_btn_orig.get_height() * (btn_w / self.play_btn_orig.get_width()))

        self.play_btn = pygame.transform.scale(self.play_btn_orig, (btn_w, btn_h))
        self.play_btn_hover = pygame.transform.scale(self.play_btn_hover_orig, (btn_w, btn_h))
        self.play_btn_pos = (int(width * 0.65), int(height * 0.65))
        self.play_btn_rect = self.play_btn.get_rect(topleft=self.play_btn_pos)

        # VOLUME BUTTONS (DOS FIJOS)
        vol_size = int(width * 0.05)

        self.vol_up = pygame.transform.scale(self.vol_up_orig, (vol_size, vol_size))
        self.vol_mute = pygame.transform.scale(self.vol_mute_orig, (vol_size, vol_size))

        self.vol_up_pos = (int(width * 0.88), int(height * 0.05))
        self.vol_mute_pos = (int(width * 0.94), int(height * 0.05))

        self.vol_up_rect = self.vol_up.get_rect(topleft=self.vol_up_pos)
        self.vol_mute_rect = self.vol_mute.get_rect(topleft=self.vol_mute_pos)

    # --------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------
    def run(self):
        while self.running:
            self.clock.tick(constantes.FPS)
            self.handle_events()
            self.update()
            self.draw()

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                self.resize_elements(*event.size)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.vol_up_rect.collidepoint(event.pos):
                    self.unmute_music()

                elif self.vol_mute_rect.collidepoint(event.pos):
                    self.mute_music()

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovering = self.play_btn_rect.collidepoint(mouse_pos)

        dt = self.clock.get_time()
        self.wink_timer += dt

        if not self.is_winking and self.wink_timer >= self.next_wink_time:
            self.is_winking = True
            self.wink_timer = 0
            self.wink_duration = random.randint(400, 700)

        elif self.is_winking and self.wink_timer >= self.wink_duration:
            self.is_winking = False
            self.wink_timer = 0
            self.next_wink_time = random.randint(500, 2500)

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        dog_img = self.dog_closed if self.is_winking else self.dog
        self.screen.blit(dog_img, self.dog_rect)

        self.screen.blit(self.title, self.title_pos)

        btn_img = self.play_btn_hover if self.is_hovering else self.play_btn
        self.screen.blit(btn_img, self.play_btn_pos)

        # VOLUME BUTTONS (SIEMPRE VISIBLES)
        self.screen.blit(self.vol_up, self.vol_up_rect)
        self.screen.blit(self.vol_mute, self.vol_mute_rect)

        pygame.display.flip()