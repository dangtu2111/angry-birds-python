import pygame


import pymunk as pm

from level import Level

class GameResources:
    """Manages game assets and resources"""
    def __init__(self):
       
        self.SCREEN_WIDTH= 1200
        self.SCREEN_HEIGHT=650
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        false_score = pygame.image.load(
            "./resources/images/XYZ.png").convert_alpha()
        # Kích thước ban đầu của hình ảnh
        original_width, original_height = false_score.get_size()

        # Phóng to hình ảnh
        scale_factor = 2  # Tỉ lệ phóng to
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self.scaled_false_score = pygame.transform.scale(false_score, (new_width, new_height))
        self.bird_image=[
            pygame.image.load(
            "./resources/images/red-bird3.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/black_bird.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/pink_bird.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/yellow_bird.png").convert_alpha(),
        ]
        self.backBird = pygame.image.load(
            "./resources/images/black_bird.png").convert_alpha()
        self.background2 = pygame.image.load(
            "./resources/images/background3.png").convert_alpha()
        
        self.full_sprite = pygame.image.load(
            "./resources/images/full-sprite.png").convert_alpha()
        self.rect = pygame.Rect(181, 1050, 50, 50)
        self.cropped = self.full_sprite.subsurface(self.rect).copy()
        self.pig_image = pygame.transform.scale(self.cropped, (30, 30))

        self.buttons = pygame.image.load(
            "./resources/images/selected-buttons.png").convert_alpha()
        self.pig_happy = pygame.image.load(
            "./resources/images/pig_failed.png").convert_alpha()
        self.stars = pygame.image.load(
            "./resources/images/stars-edited.png").convert_alpha()
        self.rect = pygame.Rect(0, 0, 200, 200)
        self.star1 = self.stars.subsurface(self.rect).copy()
        self.rect = pygame.Rect(204, 0, 200, 200)
        self.star2 = self.stars.subsurface(self.rect).copy()
        self.rect = pygame.Rect(426, 0, 200, 200)
        self.star3 = self.stars.subsurface(self.rect).copy()
        self.rect = pygame.Rect(164, 10, 60, 60)
        self.pause_button = self.buttons.subsurface(self.rect).copy()
        self.rect = pygame.Rect(24, 4, 100, 100)
        self.replay_button = self.buttons.subsurface(self.rect).copy()
        self.rect = pygame.Rect(142, 365, 130, 100)
        self.next_button = self.buttons.subsurface(self.rect).copy()
        self.rect = pygame.Rect(18, 212, 100, 100)
        self.play_button = self.buttons.subsurface(self.rect).copy()
        self.running = True
        self.count_start=0
        # the base of the physics
        self.space = pm.Space()
        self.space.gravity = (0.0, -700.0)
        self.pigs = []
        self.pigsBoss = []
        self.birds = []
        self.balls = []
        self.polys = []
        self.beams = []
        self.columns = []
        self.poly_points = []
        self.ball_number = 0
        self.polys_dict = {}
        self.mouse_distance = 0
        self.rope_lenght = 90
        self.angle = 0
        self.x_mouse = 0
        self.y_mouse = 0
        self.count = 0
        self.mouse_pressed = False
        self.t1 = 0
        self.t2 = 0
        self.tick_to_next_circle = 10
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.score = -60000
        self.bird_path = []
        self.counter = 0
        self.restart_counter = False
        self.bonus_score_once = True
        # Tải font (font mặc định hoặc từ tệp)
        font_path = "./resources/font/feast_of_flesh_bb/FEASFBI_.TTF"  # Đường dẫn tới tệp font (nếu có)
       
        self.font01 = pygame.font.Font(font_path, 50) 
        self.bold_font = pygame.font.SysFont("arial", 30, bold=True)
        self.bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
        self.bold_font3 = pygame.font.SysFont("arial", 50, bold=True)
        self.wall = False
        self.level = Level(self.pigs, self.columns, self.beams, self.space,self.pigsBoss)
        # Static floor
        self.static_body = pm.Body(body_type=pm.Body.STATIC)
        self.static_lines = [pm.Segment(self.static_body, (0.0, 060.0), (1200.0, 060.0), 0.0)]
        self.static_lines1 = [pm.Segment(self.static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]
        for line in self.static_lines:
            line.elasticity = 0.9
            line.friction = 0.95
            line.collision_type = 3
        for line in self.static_lines1:
            line.elasticity = 0.5
            line.friction = 0.95
            line.collision_type = 3
        self.space.add(self.static_body)
        for line in self.static_lines:
            self.space.add(line)
        for line in self.static_lines1:
            self.space.add(line)