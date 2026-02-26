import pygame
import random
import constantes
import os
from scripts.utils.resource_manager import ResourceManager
from scripts.entities.player import Player
try:
    import imageio.v2 as imageio
except Exception:
    imageio = None
import numpy as np


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
        self.state = "menu"
        self.fade_alpha = 0
        self.player = Player()
        self.is_hover_yes = False
        self.is_hover_no = False

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
        def ph(w, h, color=(200, 120, 120, 255)):
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            s.fill((0, 0, 0, 0))
            pygame.draw.rect(s, color, s.get_rect(), border_radius=8)
            return s

        self.bg_orig = ResourceManager.load_image("sala_inicio", "FondoInicio_Sala.png") or ph(800, 600, (60, 60, 60, 255))
        self.dog_orig = ResourceManager.load_image("dog", "TobyOjosAbiertos.png") or ph(300, 500, (180, 140, 90, 255))
        self.dog_closed_orig = ResourceManager.load_image("dog_closed", "TobyOjosCerrados.png") or self.dog_orig
        self.title_orig = ResourceManager.load_image("title", "TituloJuego.png") or ph(800, 220, (230, 200, 80, 255))
        self.play_btn_orig = ResourceManager.load_image("play_button", "botonaJugar.png") or ph(500, 150, (90, 180, 250, 255))
        self.play_btn_hover_orig = ResourceManager.load_image("play_button_hover", "BotosJugarMaus.png") or self.play_btn_orig
        self.vol_on_orig = ResourceManager.load_image("vol_on", "VolumenArriba.png") or ph(256, 256, (120, 220, 120, 255))
        self.vol_off_orig  = ResourceManager.load_image("vol_off", "Silencio.png") or ph(256, 256, (220, 120, 120, 255))
        self.loading_bg_orig = ResourceManager.load_image("loading_bg", "FondoCarga.png") or ph(800, 600, (20, 20, 20, 255))
        self.question_bg_orig = ResourceManager.load_image("question_bg", "ImagenFondo.png") or ph(800, 600, (30, 30, 30, 255))
        
        # New Backgrounds for Level 2
        self.bg_decision_enfermo_orig = ResourceManager.load_image("decision_enfermo", "../ELEMENTOS ESCENA 2/Imagenes/ENFERMO/Decisio╠ün Toby se va con mateo.png") or ph(800, 600, (100, 50, 50, 255))
        self.bg_decision_sano_orig = ResourceManager.load_image("decision_sano", "../ELEMENTOS ESCENA 2/Imagenes/SANO/Toby se va con mateo.png") or ph(800, 600, (50, 100, 50, 255))
        
        # New Background for Level 3
        self.bg_level3_orig = ResourceManager.load_image("level3_bg", "../Nivel3/ImagenPrincipalDecisionNivel3.png") or ph(800, 600, (80, 80, 120, 255))

        self.btn_yes_orig = ResourceManager.load_image("btn_yes", "BotonSi.png") or ph(300, 120, (120, 220, 120, 255))
        self.btn_no_orig = ResourceManager.load_image("btn_no", "BotonNo.png") or ph(300, 120, (220, 120, 120, 255))
        self.bg_level4_orig = ResourceManager.load_image("level4_bg", "../Nivel4/ImagenFondoPregunta.png") or ph(800, 600, (60, 80, 100, 255))
        self.btn_yes_lvl4_orig = ResourceManager.load_image("btn_yes_lvl4", "../Nivel4/BotonSi.png") or self.btn_yes_orig
        self.btn_no_lvl4_orig = ResourceManager.load_image("btn_no_lvl4", "../Nivel4/BotonNo.png") or self.btn_no_orig
        self.bg_level5_intro_orig = ResourceManager.load_image("level5_intro_bg", "../ELEMENTOS ESCENA 5/INTRO/Toby frente al abuelo en la sala.png") or ph(800, 600, (90, 90, 110, 255))
        self.btn_sentarse_orig = ResourceManager.load_image("btn_sentarse", "../ELEMENTOS ESCENA 5/INTRO/Botón Sentarse con él.png") or ph(300, 120, (120, 180, 240, 255))
        self.btn_traer_orig = ResourceManager.load_image("btn_traer", "../ELEMENTOS ESCENA 5/INTRO/Boton Traer la Pelota.png") or ph(300, 120, (240, 180, 120, 255))

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
        if self.loading_bg_orig:
            self.loading_bg = pygame.transform.scale(self.loading_bg_orig, (width, height))
        if self.question_bg_orig:
            self.question_bg = pygame.transform.scale(self.question_bg_orig, (width, height))
        
        if self.bg_decision_enfermo_orig:
            self.bg_decision_enfermo = pygame.transform.scale(self.bg_decision_enfermo_orig, (width, height))
        if self.bg_decision_sano_orig:
            self.bg_decision_sano = pygame.transform.scale(self.bg_decision_sano_orig, (width, height))
        
        if self.bg_level3_orig:
            self.bg_level3 = pygame.transform.scale(self.bg_level3_orig, (width, height))
        if self.bg_level4_orig:
            self.bg_level4 = pygame.transform.scale(self.bg_level4_orig, (width, height))
        if self.bg_level5_intro_orig:
            self.bg_level5_intro = pygame.transform.scale(self.bg_level5_intro_orig, (width, height))

        # DOG
        dog_width = int(width * 0.3)
        dog_height = int(height * 0.5)

        self.dog = pygame.transform.smoothscale(self.dog_orig, (dog_width, dog_height))
        self.dog_closed = pygame.transform.smoothscale(self.dog_closed_orig, (dog_width, dog_height))

        self.dog_rect = self.dog.get_rect(
            center=(int(width * 0.25), int(height * 0.65))
        )

        title_w_by_width = int(width * 0.56)
        title_h_by_width = int(self.title_orig.get_height() * (title_w_by_width / self.title_orig.get_width()))
        title_h_cap = int(height * 0.4)
        if title_h_by_width > title_h_cap:
            title_h = title_h_cap
            title_w = int(self.title_orig.get_width() * (title_h / self.title_orig.get_height()))
        else:
            title_w = title_w_by_width
            title_h = title_h_by_width
        self.title = pygame.transform.scale(self.title_orig, (title_w, title_h))
        title_rect = self.title.get_rect(center=(int(width * 0.62), int(height * 0.46)))
        self.title_pos = title_rect.topleft

        btn_w = max(int(width * 0.18), int(title_w * 0.34))
        btn_w = min(btn_w, int(width * 0.42))
        btn_h = int(self.play_btn_orig.get_height() * (btn_w / self.play_btn_orig.get_width()))
        self.play_btn = pygame.transform.scale(self.play_btn_orig, (btn_w, btn_h))
        self.play_btn_hover = pygame.transform.scale(self.play_btn_hover_orig, (btn_w, btn_h))
        
        spacing = int(height * 0.03)
        btn_centerx = title_rect.centerx
        btn_centery = title_rect.bottom + spacing + btn_h // 2
        # Subir ligeramente el botón (≈5 px)
        btn_centery -= 5
        
        # Asegurar que no quede por debajo del cuello del perro
        dog_neck_y = self.dog_rect.top + int(self.dog_rect.height * 0.55)
        btn_centery = min(btn_centery, dog_neck_y)
        max_y = height - btn_h - int(height * 0.06)
        btn_centery = min(btn_centery, max_y + btn_h // 2)
        self.play_btn_pos = (btn_centerx - btn_w // 2, btn_centery - btn_h // 2)
        self.play_btn_rect = self.play_btn.get_rect(topleft=self.play_btn_pos)

        # VOLUME BUTTON (UNO SOLO)
        vol_size = int(width * 0.10)

        self.vol_on = pygame.transform.scale(self.vol_on_orig, (vol_size, vol_size))
        self.vol_off = pygame.transform.scale(self.vol_off_orig, (vol_size, vol_size))

        self.vol_pos = (int(width * 0.85), int(height * 0.05))
        self.vol_rect = self.vol_on.get_rect(topleft=self.vol_pos)
        bar_w = int(width * 0.58)
        bar_h = int(height * 0.11)
        self.loading_outer_rect = pygame.Rect(0, 0, bar_w, bar_h)
        self.loading_outer_rect.center = (int(width * 0.5), int(height * 0.81) - 12)
        pad = int(bar_h * 0.15)
        self.loading_inner_rect = pygame.Rect(
            self.loading_outer_rect.left + pad,
            self.loading_outer_rect.top + pad,
            self.loading_outer_rect.width - pad * 2,
            self.loading_outer_rect.height - pad * 2
        )
        self.load_progress = 0
        self.fade_surface = pygame.Surface((width, height))
        self.fade_surface.fill((0, 0, 0))
        self.shine_offset = 0

        # Botones Sí/No
        if self.btn_yes_orig and self.btn_no_orig:
            btn_w = int(width * 0.30)
            btn_h_yes = int(self.btn_yes_orig.get_height() * (btn_w / self.btn_yes_orig.get_width()))
            btn_h_no = int(self.btn_no_orig.get_height() * (btn_w / self.btn_no_orig.get_width()))
            self.btn_yes = pygame.transform.smoothscale(self.btn_yes_orig, (btn_w, btn_h_yes))
            self.btn_no = pygame.transform.smoothscale(self.btn_no_orig, (btn_w, btn_h_no))
            y = int(height * 0.80)
            self.btn_yes_rect = self.btn_yes.get_rect(center=(int(width * 0.36), y))
            self.btn_no_rect = self.btn_no.get_rect(center=(int(width * 0.64), y))
        # Botones Sí/No específicos para Nivel 4
        if self.btn_yes_lvl4_orig and self.btn_no_lvl4_orig:
            btn_w = int(width * 0.30)
            btn_h_yes4 = int(self.btn_yes_lvl4_orig.get_height() * (btn_w / self.btn_yes_lvl4_orig.get_width()))
            btn_h_no4 = int(self.btn_no_lvl4_orig.get_height() * (btn_w / self.btn_no_lvl4_orig.get_width()))
            self.btn_yes_lvl4 = pygame.transform.smoothscale(self.btn_yes_lvl4_orig, (btn_w, btn_h_yes4))
            self.btn_no_lvl4 = pygame.transform.smoothscale(self.btn_no_lvl4_orig, (btn_w, btn_h_no4))
            y4 = int(height * 0.80)
            self.btn_yes_lvl4_rect = self.btn_yes_lvl4.get_rect(center=(int(width * 0.36), y4))
            self.btn_no_lvl4_rect = self.btn_no_lvl4.get_rect(center=(int(width * 0.64), y4))
        # Botones de Escena 5 Intro (Sentarse / Traer la pelota)
        if self.btn_sentarse_orig and self.btn_traer_orig:
            btn_w5 = int(width * 0.28)
            btn_h_sent = int(self.btn_sentarse_orig.get_height() * (btn_w5 / self.btn_sentarse_orig.get_width()))
            btn_h_traer = int(self.btn_traer_orig.get_height() * (btn_w5 / self.btn_traer_orig.get_width()))
            self.btn_sentarse = pygame.transform.smoothscale(self.btn_sentarse_orig, (btn_w5, btn_h_sent))
            self.btn_traer = pygame.transform.smoothscale(self.btn_traer_orig, (btn_w5, btn_h_traer))
            y5 = int(height * 0.84)
            self.btn_sentarse_rect = self.btn_sentarse.get_rect(center=(int(width * 0.30), y5))
            self.btn_traer_rect = self.btn_traer.get_rect(center=(int(width * 0.70), y5))
        # Área donde se dibuja el video
        self.video_draw_rect = pygame.Rect(0, 0, width, height)

        # VIDEO OVERLAY: smaller title (top-right) & volume (top-left)
        vid_title_w = int(width * 0.55)
        vid_title_h = int(self.title_orig.get_height() * (vid_title_w / self.title_orig.get_width()))
        self.title_video = pygame.transform.smoothscale(self.title_orig, (vid_title_w, vid_title_h))
        self.title_video_pos = (width - vid_title_w + int(width * 0.13), -int(vid_title_h * 0.22))
        self.vol_pos_video = (int(width * 0.03), int(height * 0.03))
        self.vol_rect_video = self.vol_on.get_rect(topleft=self.vol_pos_video)

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
                if self.state == "menu" and self.play_btn_rect.collidepoint(event.pos):
                    self.state = "fading"
                    self.fade_alpha = 0
                elif self.vol_rect.collidepoint(event.pos):
                    if self.music_muted:
                        self.unmute_music()
                    else:
                        self.mute_music()
                elif self.state == "level1":
                    if self.btn_yes_rect and self.btn_yes_rect.collidepoint(event.pos):
                        self.start_video("PerroentraCaja.mp4", return_state="level2_sano")
                    elif self.btn_no_rect and self.btn_no_rect.collidepoint(event.pos):
                        self.start_video("LluviaPerroNoEntra.mp4", return_state="level2_enfermo")
                elif self.state == "level2_enfermo":
                    if self.btn_yes_rect and self.btn_yes_rect.collidepoint(event.pos):
                        # SI -> ConfioEnMateo -> Level 3
                        self.start_video("../ELEMENTOS ESCENA 2/Videos/ENFERMO/SI/ConfioEnMateo.mp4", return_state="level3")
                    elif self.btn_no_rect and self.btn_no_rect.collidepoint(event.pos):
                        # NO -> TOMA 2 Toby huye de mateo -> Level 3
                        self.start_video("../ELEMENTOS ESCENA 2/Videos/ENFERMO/NO/TOMA 2 Toby huye de mateo.mp4", return_state="level3")

                elif self.state == "level2_sano":
                    if self.btn_yes_rect and self.btn_yes_rect.collidepoint(event.pos):
                        # SI -> TOMA 2 Toby se va con Mateo -> Level 3
                        self.start_video("../ELEMENTOS ESCENA 2/Videos/SANO/SI/TOMA 2 Toby se va con Mateo.mp4", return_state="level3")
                    elif self.btn_no_rect and self.btn_no_rect.collidepoint(event.pos):
                        # NO -> TobySeAsustahuyendo -> Level 3
                        self.start_video("../ELEMENTOS ESCENA 2/Videos/SANO/NO/TobySeAsustahuyendo.mp4", return_state="level3")
                
                elif self.state == "level3":
                    if self.btn_yes_rect and self.btn_yes_rect.collidepoint(event.pos):
                        # SI -> SiEnfrenta -> (Wait 1s) -> 2Enfrenta
                        self.start_video_sequence([
                            "../Nivel3/SiEnfrenta.mp4",
                            "WAIT:1000",
                            "../Nivel3/2Enfrenta.mp4"
                        ], return_state="level4")
                    elif self.btn_no_rect and self.btn_no_rect.collidepoint(event.pos):
                        # NO -> NoEnfrenta -> (Wait 1s) -> 2NoEnfrenta
                        self.start_video_sequence([
                            "../Nivel3/NoEnfrenta.mp4",
                            "WAIT:1000",
                            "../Nivel3/2NoEnfrenta.mp4"
                        ], return_state="level4")
                
                elif self.state == "level4":
                    if getattr(self, "btn_no_lvl4_rect", None) and self.btn_no_lvl4_rect.collidepoint(event.pos):
                        self.start_video("../Nivel4/VideoDeNo.mp4", return_state="level5_intro")
                    elif getattr(self, "btn_yes_lvl4_rect", None) and self.btn_yes_lvl4_rect.collidepoint(event.pos):
                        self.start_video("../Nivel4/VideoDeSi.mp4", return_state="level5_intro")
                
                elif self.state == "level5_intro":
                    if getattr(self, "btn_sentarse_rect", None) and self.btn_sentarse_rect.collidepoint(event.pos):
                        self.start_video_sequence([
                            "../ELEMENTOS ESCENA 5/VIDEOS/Toby se sienta junto al abuelo y él lo acaricia..mp4",
                            "WAIT:800",
                            "../ELEMENTOS ESCENA 5/VIDEOS/(máxima aceptación)..mp4"
                        ], return_state="menu")
                    elif getattr(self, "btn_traer_rect", None) and self.btn_traer_rect.collidepoint(event.pos):
                        self.start_video("../ELEMENTOS ESCENA 5/VIDEOS/Toby trae la pelota y el abuelo sonríe..mp4", return_state="menu")
                
                elif self.state == "playing_video":
                    # Permitir saltar el video con clic
                    self.state = "fading_from_video"
                    self.fade_alpha = 0
                        
    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------
    def update(self):
        if self.state == "menu":
            mouse_pos = pygame.mouse.get_pos()
            self.is_hovering = self.play_btn_rect.collidepoint(mouse_pos)
        elif self.state == "fading":
            self.fade_alpha = min(255, self.fade_alpha + int(600 * self.clock.get_time() / 1000))
            if self.fade_alpha >= 255:
                self.state = "loading"
                self.load_progress = 0

        dt = self.clock.get_time()
        self.wink_timer += dt

        if self.state == "menu":
            if not self.is_winking and self.wink_timer >= self.next_wink_time:
                self.is_winking = True
                self.wink_timer = 0
                self.wink_duration = random.randint(400, 700)
            elif self.is_winking and self.wink_timer >= self.wink_duration:
                self.is_winking = False
                self.wink_timer = 0
                self.next_wink_time = random.randint(500, 2500)
        elif self.state == "loading":
            self.load_progress = min(100, self.load_progress + 20 * dt / 1000)
            self.shine_offset = (self.shine_offset + int(140 * dt / 1000)) % (self.loading_inner_rect.width + 1)
            if self.load_progress >= 100:
                self.state = "fading_to_level"
                self.fade_alpha = 0
        elif self.state == "level1":
            mouse_pos = pygame.mouse.get_pos()
            self.is_hover_yes = self.btn_yes_rect.collidepoint(mouse_pos) if self.btn_yes_rect else False
            self.is_hover_no = self.btn_no_rect.collidepoint(mouse_pos) if self.btn_no_rect else False
            if self.fade_alpha > 0:
                self.fade_alpha = max(0, self.fade_alpha - int(800 * dt / 1000))
        elif self.state in ("level2_sano", "level2_enfermo", "level3"):
            mouse_pos = pygame.mouse.get_pos()
            self.is_hover_yes = self.btn_yes_rect.collidepoint(mouse_pos) if self.btn_yes_rect else False
            self.is_hover_no = self.btn_no_rect.collidepoint(mouse_pos) if self.btn_no_rect else False
            if self.fade_alpha > 0:
                self.fade_alpha = max(0, self.fade_alpha - int(800 * dt / 1000))
        elif self.state == "level4":
            mouse_pos = pygame.mouse.get_pos()
            self.is_hover_yes = self.btn_yes_lvl4_rect.collidepoint(mouse_pos) if getattr(self, "btn_yes_lvl4_rect", None) else False
            self.is_hover_no = self.btn_no_lvl4_rect.collidepoint(mouse_pos) if getattr(self, "btn_no_lvl4_rect", None) else False
            if self.fade_alpha > 0:
                self.fade_alpha = max(0, self.fade_alpha - int(800 * dt / 1000))
        elif self.state == "level5_intro":
            mouse_pos = pygame.mouse.get_pos()
            self.is_hover_yes = self.btn_sentarse_rect.collidepoint(mouse_pos) if getattr(self, "btn_sentarse_rect", None) else False
            self.is_hover_no = self.btn_traer_rect.collidepoint(mouse_pos) if getattr(self, "btn_traer_rect", None) else False
            if self.fade_alpha > 0:
                self.fade_alpha = max(0, self.fade_alpha - int(800 * dt / 1000))
        elif self.state == "black_screen_wait":
            self.wait_timer += dt
            if self.wait_timer >= self.wait_duration:
                self.play_next_in_sequence()
        elif self.state == "fading_to_level":
            self.fade_alpha = min(255, self.fade_alpha + int(800 * dt / 1000))
            if self.fade_alpha >= 255:
                self.state = "level1"
                self.fade_alpha = 255
        elif self.state == "playing_video" and getattr(self, "video_reader", None):
            self.video_time += dt / 1000.0
            target_index = int(self.video_time * self.video_fps)
            if target_index != getattr(self, "video_frame_index", -1):
                self.video_frame_index = target_index
                if self.video_frame_index >= self.video_total_frames:
                    self.state = "fading_from_video"
                    self.fade_alpha = 0
                else:
                    try:
                        frame = self.video_reader.get_data(self.video_frame_index)
                        frame_surface = pygame.surfarray.make_surface(np.swapaxes(frame, 0, 1))
                        self.video_frame_surface = frame_surface
                        self.video_last_frame_surface = frame_surface
                    except Exception:
                        self.state = "fading_from_video"
                        self.fade_alpha = 0
            if self.video_time >= self.video_duration:
                self.state = "fading_from_video"
                self.fade_alpha = 0
        elif self.state == "fading_from_video":
            self.fade_alpha = min(255, self.fade_alpha + int(1000 * dt / 1000))
            if self.fade_alpha >= 255:
                if self.next_state_after_video == "NEXT_IN_SEQUENCE":
                    self.play_next_in_sequence()
                else:
                    self.state = self.next_state_after_video or "menu"
                    self.fade_alpha = 255
                    # Resume background music when video sequence/video ends
                    self.play_background_music()

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------
    def draw(self):
        if self.state in ("menu", "fading"):
            self.screen.blit(self.background, (0, 0))
            dog_img = self.dog_closed if self.is_winking else self.dog
            self.screen.blit(dog_img, self.dog_rect)
            self.screen.blit(self.title, self.title_pos)
            btn_img = self.play_btn_hover if self.is_hovering else self.play_btn
            self.screen.blit(btn_img, self.play_btn_pos)
            vol_img = self.vol_off if self.music_muted else self.vol_on
            self.screen.blit(vol_img, self.vol_rect)
            if self.state == "fading":
                self.fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(self.fade_surface, (0, 0))
        elif self.state == "loading":
            bg = getattr(self, "loading_bg", None)
            if bg:
                self.screen.blit(bg, (0, 0))
            else:
                self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (240, 210, 120), self.loading_outer_rect, border_radius=int(self.loading_outer_rect.height/2))
            pygame.draw.rect(self.screen, (200, 170, 90), self.loading_outer_rect, width=6, border_radius=int(self.loading_outer_rect.height/2))
            pct = self.load_progress / 100.0
            fill_w = max(0, int(self.loading_inner_rect.width * pct))
            fill_rect = pygame.Rect(self.loading_inner_rect.left, self.loading_inner_rect.top, fill_w, self.loading_inner_rect.height)
            pygame.draw.rect(self.screen, constantes.COLOR_LOADING, fill_rect, border_radius=int(self.loading_inner_rect.height/2))
            if fill_w > 0:
                shine_w = int(self.loading_inner_rect.height * 0.35)
                sx = self.loading_inner_rect.left + (self.shine_offset % max(1, self.loading_inner_rect.width))
                shine_rect = pygame.Rect(sx, self.loading_inner_rect.top, shine_w, self.loading_inner_rect.height)
                shine_surface = pygame.Surface((shine_rect.width, shine_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(shine_surface, (255, 255, 255, 60), shine_surface.get_rect(), border_radius=int(self.loading_inner_rect.height/2))
                self.screen.blit(shine_surface, shine_rect)
            vol_img = self.vol_off if self.music_muted else self.vol_on
            self.screen.blit(vol_img, self.vol_rect)
        elif self.state == "fading_to_level":
            bg = getattr(self, "loading_bg", None)
            if bg:
                self.screen.blit(bg, (0, 0))
            else:
                self.screen.fill((0, 0, 0))
            self.fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(self.fade_surface, (0, 0))
            vol_img = self.vol_off if self.music_muted else self.vol_on
            self.screen.blit(vol_img, self.vol_rect)
        elif self.state == "level1":
            if getattr(self, "question_bg", None):
                self.screen.blit(self.question_bg, (0, 0))
            else:
                self.screen.fill((0, 0, 0))
            if getattr(self, "btn_yes", None):
                self.screen.blit(self.btn_yes, self.btn_yes_rect)
            if getattr(self, "btn_no", None):
                self.screen.blit(self.btn_no, self.btn_no_rect)
            vol_img = self.vol_off if self.music_muted else self.vol_on
            self.screen.blit(vol_img, self.vol_rect)
            if self.fade_alpha > 0:
                self.fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(self.fade_surface, (0, 0))
        elif self.state == "level4":
            if getattr(self, "bg_level4", None):
                self.screen.blit(self.bg_level4, (0, 0))
            else:
                self.screen.fill((60, 80, 100))
            if getattr(self, "btn_yes_lvl4", None):
                self.screen.blit(self.btn_yes_lvl4, self.btn_yes_lvl4_rect)
            if getattr(self, "btn_no_lvl4", None):
                self.screen.blit(self.btn_no_lvl4, self.btn_no_lvl4_rect)
            vol_img = self.vol_off if self.music_muted else self.vol_on
            self.screen.blit(vol_img, self.vol_rect)
            if self.fade_alpha > 0:
                self.fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(self.fade_surface, (0, 0))
        elif self.state == "level5_intro":
            if getattr(self, "bg_level5_intro", None):
                self.screen.blit(self.bg_level5_intro, (0, 0))
            else:
                self.screen.fill((90, 90, 110))
            if getattr(self, "btn_sentarse", None):
                self.screen.blit(self.btn_sentarse, self.btn_sentarse_rect)
            if getattr(self, "btn_traer", None):
                self.screen.blit(self.btn_traer, self.btn_traer_rect)
            vol_img = self.vol_off if self.music_muted else self.vol_on
            self.screen.blit(vol_img, self.vol_rect)
            if self.fade_alpha > 0:
                self.fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(self.fade_surface, (0, 0))
        elif self.state == "level2_sano":
            if getattr(self, "bg_decision_sano", None):
                self.screen.blit(self.bg_decision_sano, (0, 0))
            else:
                self.screen.fill((50, 100, 50))
            if getattr(self, "btn_yes", None):
                self.screen.blit(self.btn_yes, self.btn_yes_rect)
            if getattr(self, "btn_no", None):
                self.screen.blit(self.btn_no, self.btn_no_rect)
            vol_img = self.vol_off if self.music_muted else self.vol_on
            self.screen.blit(vol_img, self.vol_rect)
            if self.fade_alpha > 0:
                self.fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(self.fade_surface, (0, 0))
        elif self.state == "level2_enfermo":
            if getattr(self, "bg_decision_enfermo", None):
                self.screen.blit(self.bg_decision_enfermo, (0, 0))
            else:
                self.screen.fill((100, 50, 50))
            if getattr(self, "btn_yes", None):
                self.screen.blit(self.btn_yes, self.btn_yes_rect)
            if getattr(self, "btn_no", None):
                self.screen.blit(self.btn_no, self.btn_no_rect)
            vol_img = self.vol_off if self.music_muted else self.vol_on
            self.screen.blit(vol_img, self.vol_rect)
            if self.fade_alpha > 0:
                self.fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(self.fade_surface, (0, 0))
        elif self.state == "level3":
            if getattr(self, "bg_level3", None):
                self.screen.blit(self.bg_level3, (0, 0))
            else:
                self.screen.fill((80, 80, 120))
            if getattr(self, "btn_yes", None):
                self.screen.blit(self.btn_yes, self.btn_yes_rect)
            if getattr(self, "btn_no", None):
                self.screen.blit(self.btn_no, self.btn_no_rect)
            vol_img = self.vol_off if self.music_muted else self.vol_on
            self.screen.blit(vol_img, self.vol_rect)
            if self.fade_alpha > 0:
                self.fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(self.fade_surface, (0, 0))
        elif self.state == "black_screen_wait":
            self.screen.fill((0, 0, 0))
        elif self.state == "playing_video":
            surface = getattr(self, "video_frame_surface", None)
            if surface is not None:
                target = pygame.transform.smoothscale(surface, (self.video_draw_rect.width, self.video_draw_rect.height))
                self.screen.blit(target, self.video_draw_rect)
                # Title overlay (top-right, smaller)
                self.screen.blit(self.title_video, self.title_video_pos)
                # Volume button (top-left)
                vol_img = self.vol_off if self.music_muted else self.vol_on
                self.screen.blit(vol_img, self.vol_pos_video)
        elif self.state == "fading_from_video":
            if self.video_last_frame_surface:
                target = pygame.transform.smoothscale(self.video_last_frame_surface, (self.video_draw_rect.width, self.video_draw_rect.height))
                self.screen.blit(target, self.video_draw_rect)
            # Title overlay (top-right, smaller)
            self.screen.blit(self.title_video, self.title_video_pos)
            self.fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(self.fade_surface, (0, 0))
            # Volume button (top-left)
            vol_img = self.vol_off if self.music_muted else self.vol_on
            self.screen.blit(vol_img, self.vol_pos_video)

        pygame.display.flip()

    def start_video(self, filename, return_state="menu"):
        base_path = os.path.dirname(os.path.abspath(__file__))
        video_path = os.path.join(base_path, "..", "assets", "images", filename)
        if not imageio:
            print("ImageIO no está disponible.")
            return
        try:
            reader = imageio.get_reader(video_path)
            meta = reader.get_meta_data()
            self.video_reader = reader
            self.video_fps = int(meta.get("fps", 24))
            self.video_duration = float(meta.get("duration", 0)) or 0.0
            self.video_total_frames = max(1, int(self.video_duration * max(1, self.video_fps)))
            self.video_time = 0.0
            self.video_frame_index = -1
            self.video_frame_surface = None
            self.next_state_after_video = return_state
            self.state = "playing_video"
            
            # Stop background music to play video audio properly (if available)
            pygame.mixer.music.stop()
            try:
                mp3_path = os.path.splitext(video_path)[0] + ".mp3"
                if os.path.exists(mp3_path):
                    pygame.mixer.music.load(mp3_path)
                    pygame.mixer.music.set_volume(self.music_volume if not self.music_muted else 0)
                    pygame.mixer.music.play()
            except Exception:
                pass
            
            # Switch to rain sound during video (Only if needed, but requested behavior is video audio)
            # The previous code was forcing 'Rain Sound.mp3'. 
            # If the video has its own audio, we might want to let it play via moviepy/imageio (imageio standard doesn't play audio easily with pygame mixer)
            # However, standard imageio 'get_reader' does NOT play audio automatically in Pygame.
            # Pygame doesn't support video audio playback from imageio out of the box without extracting it.
            # BUT, the user said "que se escuche el audio del video".
            # The current implementation uses 'imageio' which is video-only usually unless we extract audio.
            # AND the previous code was loading "Rain Sound.mp3" explicitly.
            
            # Let's COMMENT OUT the rain sound forcing so at least it doesn't overlap if the video somehow has audio handling (or if user thinks video has audio).
            # If the user wants the ACTUAL video audio, that's complex with just imageio + pygame.
            # But let's first do what is asked: stop background music.
            
            # base_path2 = os.path.dirname(os.path.abspath(__file__))
            # rain_path = os.path.join(base_path2, "..", "assets", "sounds", "Rain Sound.mp3")
            # pygame.mixer.music.load(rain_path)
            # pygame.mixer.music.set_volume(self.music_volume if not self.music_muted else 0)
            # pygame.mixer.music.play(-1)
            
            # Since we are using imageio, it DOES NOT play audio by default.
            # If the user expects video audio, we need to extract it or use a different method.
            # However, simpler step first: STOP the background music as requested.
            
        except Exception as e:
            print(f"No se pudo cargar el video {filename}: {e}")
            self.state = self.next_state_after_video or "menu"

    def start_video_sequence(self, sequence, return_state="menu"):
        self.video_sequence = sequence
        self.video_sequence_index = 0
        self.final_return_state = return_state
        self.play_next_in_sequence()

    def play_next_in_sequence(self):
        if self.video_sequence_index >= len(self.video_sequence):
            self.state = self.final_return_state
            self.play_background_music()
            return

        item = self.video_sequence[self.video_sequence_index]
        self.video_sequence_index += 1

        if item.startswith("WAIT:"):
            try:
                ms = int(item.split(":")[1])
            except:
                ms = 1000
            self.state = "black_screen_wait"
            self.wait_timer = 0
            self.wait_duration = ms
        else:
            # If it's a video, we set 'next_state_after_video' to trigger this method again
            # We need a special handling in update loop for 'fading_from_video' -> calls play_next_in_sequence
            self.start_video(item, return_state="NEXT_IN_SEQUENCE")

    # Override return state logic in update
    # We need to change line 314 logic to support sequence
    # But since I can't easily change just that line without context, I will rely on 'NEXT_IN_SEQUENCE' check
    # Let's modify the 'fading_from_video' block logic instead with a small trick or just search/replace it.

