import os
import sys
import math
import time
import pygame
current_path = os.getcwd()
import pymunk as pm
from characters import Bird
from level import Level

class GameResources:
    """Manages game assets and resources"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 650))
        self.redbird = pygame.image.load(
            "./resources/images/red-bird3.png").convert_alpha()
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
        self.sling_image = pygame.image.load(
            "./resources/images/sling-3.png").convert_alpha()
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
        self.clock = pygame.time.Clock()
        self.rect = pygame.Rect(18, 212, 100, 100)
        self.play_button = self.buttons.subsurface(self.rect).copy()
        self.clock = pygame.time.Clock()
        self.running = True
        # the base of the physics
        self.space = pm.Space()
        self.space.gravity = (0.0, -700.0)
        self.pigs = []
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
        self.sling_x, self.sling_y = 135, 450
        self.sling2_x, self.sling2_y = 160, 450
        self.score = 0
        self.game_state = 0
        self.bird_path = []
        self.counter = 0
        self.restart_counter = False
        self.bonus_score_once = True
        self.bold_font = pygame.font.SysFont("arial", 30, bold=True)
        self.bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
        self.bold_font3 = pygame.font.SysFont("arial", 50, bold=True)
        self.wall = False
        self.level = Level(self.pigs, self.columns, self.beams, self.space)


        # Static floor
        self.static_body = pm.Body(body_type=pm.Body.STATIC)
        self.static_lines = [pm.Segment(self.static_body, (0.0, 060.0), (1200.0, 060.0), 0.0)]
        self.static_lines1 = [pm.Segment(self.static_body, (1200.0, 060.0), (1200.0, 800.0), 0.0)]
        for line in self.static_lines:
            line.elasticity = 0.95
            line.friction = 1
            line.collision_type = 3
        for line in self.static_lines1:
            line.elasticity = 0.95
            line.friction = 1
            line.collision_type = 3
        self.space.add(self.static_body)
        for line in self.static_lines:
            self.space.add(line)


def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)


class Sling:
    def __init__(self,resource):
        self.x=0
        self.resource=resource
    def sling_action(self,bird_image):
        """Set up sling behavior"""
        
        # Fixing bird to the sling rope
        v = self.vector((self.resource.sling_x, self.resource.sling_y), (self.resource.x_mouse, self.resource.y_mouse))
        uv = self.unit_vector(v)
        uv1 = uv[0]
        uv2 = uv[1]
        self.resource.mouse_distance = self.distance(self.resource.sling_x,self.resource.sling_y, self.resource.x_mouse,self.resource.y_mouse)
        pu = (uv1*self.resource.rope_lenght+self.resource.sling_x, uv2*self.resource.rope_lenght+self.resource.sling_y)
        bigger_rope = 102
        x_redbird = self.resource.x_mouse - 20
        y_redbird = self.resource.y_mouse - 20
        if self.resource.mouse_distance > self.resource.rope_lenght:
            pux, puy = pu
            pux -= 20
            puy -= 20
            pul = pux, puy
            self.resource.screen.blit(bird_image, pul)
            pu2 = (uv1*bigger_rope+self.resource.sling_x, uv2*bigger_rope+self.resource.sling_y)
            pygame.draw.line(self.resource.screen, (0, 0, 0), (self.resource.sling2_x, self.resource.sling2_y), pu2, 5)
            self.resource.screen.blit(bird_image, pul)
            pygame.draw.line(self.resource.screen, (0, 0, 0), (self.resource.sling_x, self.resource.sling_y), pu2, 5)
        else:
            self.resource.mouse_distance += 10
            pu3 = (uv1*self.resource.mouse_distance+self.resource.sling_x, uv2*self.resource.mouse_distance+self.resource.sling_y)
            pygame.draw.line(self.resource.screen, (0, 0, 0), (self.resource.sling2_x, self.resource.sling2_y), pu3, 5)
            self.resource.screen.blit(bird_image, (x_redbird, y_redbird))
            pygame.draw.line(self.resource.screen, (0, 0, 0), (self.resource.sling_x, self.resource.sling_y), pu3, 5)
        # Angle of impulse
        dy = self.resource.y_mouse - self.resource.sling_y
        dx = self.resource.x_mouse - self.resource.sling_x
        if dx == 0:
            dx = 0.00000000000001
        self.resource.angle = math.atan((float(dy))/dx)
    def vector(self,p0, p1):
        """Return the vector of the points
        p0 = (xo,yo), p1 = (x1,y1)"""
        a = p1[0] - p0[0]
        b = p1[1] - p0[1]
        return (a, b)


    def unit_vector(self,v):
        """Return the unit vector of the points
        v = (a,b)"""
        h = ((v[0]**2)+(v[1]**2))**0.5
        if h == 0:
            h = 0.000000000000001
        ua = v[0] / h
        ub = v[1] / h
        return (ua, ub)


    def distance(self,xo, yo, x, y):
        """distance between points"""
        dx = x - xo
        dy = y - yo
        d = ((dx ** 2) + (dy ** 2)) ** 0.5
        return d




def load_music():
    """Load the music"""
    song1 = './resources/sounds/angry-birds.ogg'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)


class GameStateManager:
    """Manages game objects like birds, pigs, and structures"""
    def __init__(self, resources):
        self.resource=resources

    def draw_level_cleared(self):
        """Draw level cleared"""
        
        level_cleared = self.resource.bold_font3.render("Level Cleared!", 1, self.resource.WHITE)
        self.resource.score_level_cleared = self.resource.bold_font2.render(str(self.resource.score), 1, self.resource.WHITE)
        if self.resource.level.number_of_birds >= 0 and len(self.resource.pigs) == 0:
            if self.resource.bonus_score_once:
                self.resource.score += (self.resource.level.number_of_birds-1) * 10000
            self.resource.bonus_score_once = False
            self.resource.game_state = 4
            rect = pygame.Rect(300, 0, 600, 800)
            pygame.draw.rect(self.resource.screen, self.resource.BLACK, rect)
            self.resource.screen.blit(level_cleared, (450, 90))
            if self.resource.score >= self.resource.level.one_star and self.resource.score <= self.resource.level.two_star:
                self.resource.screen.blit(self.resource.star1, (310, 190))
            if self.resource.score >= self.resource.level.two_star and self.resource.score <= self.resource.level.three_star:
                self.resource.screen.blit(self.resource.star1, (310, 190))
                self.resource.screen.blit(self.resource.star2, (500, 170))
            if self.resource.score >= self.resource.level.three_star:
                self.resource.screen.blit(self.resource.star1, (310, 190))
                self.resource.screen.blit(self.resource.star2, (500, 170))
                self.resource.screen.blit(self.resource.star3, (700, 200))
            self.resource.screen.blit(self.resource.score_level_cleared, (550, 400))
            self.resource.screen.blit(self.resource.replay_button, (510, 480))
            self.resource.screen.blit(self.resource.next_button, (620, 480))


    def draw_level_failed(self):
        """Draw level failed"""
        failed = self.resource.bold_font3.render("Level Failed", 1, self.resource.WHITE)
        if self.resource.level.number_of_birds <= 0 and time.time() - self.resource.t2 > 5 and len(self.resource.pigs) > 0:
            self.resource.game_state = 3
            rect = pygame.Rect(300, 0, 600, 800)
            pygame.draw.rect(self.resource.screen, self.resource.BLACK, rect)
            self.resource.screen.blit(failed, (450, 90))
            self.resource.screen.blit(self.resource.pig_happy, (380, 120))
            self.resource.screen.blit(self.resource.replay_button, (520, 460))


    def restart(self):
        """Delete all objects of the level"""
        pigs_to_remove = []
        self.resource.birds_to_remove = []
        columns_to_remove = []
        beams_to_remove = []
        for pig in self.resource.pigs:
            pigs_to_remove.append(pig)
        for pig in pigs_to_remove:
            self.resource.space.remove(pig.shape, pig.shape.body)
            self.resource.pigs.remove(pig)
        for bird in self.resource.birds:
            self.resource.birds_to_remove.append(bird)
        for bird in self.resource.birds_to_remove:
            self.resource.space.remove(bird.shape, bird.shape.body)
            self.resource.birds.remove(bird)
        for column in self.resource.columns:
            columns_to_remove.append(column)
        for column in columns_to_remove:
            self.resource.space.remove(column.shape, column.shape.body)
            self.resource.columns.remove(column)
        for beam in self.resource.beams:
            beams_to_remove.append(beam)
        for beam in beams_to_remove:
            self.resource.space.remove(beam.shape, beam.shape.body)
            self.resource.beams.remove(beam)

class GameObjectManager:
    """Manages game objects like birds, pigs, and structures"""
    def __init__(self, resources):
        self.resource=resources
    def post_solve_bird_pig(self,arbiter, space, _):
        """Collision between bird and pig"""
        surface=self.resource.screen
        a, b = arbiter.shapes
        bird_body = a.body
        pig_body = b.body
        p = to_pygame(bird_body.position)
        p2 = to_pygame(pig_body.position)
        r = 30
        pygame.draw.circle(surface, self.resource.BLACK, p, r, 4)
        pygame.draw.circle(surface, self.resource.RED, p2, r, 4)
        pigs_to_remove = []
        for pig in self.resource.pigs:
            if pig_body == pig.body:
                pig.life -= 20
                if pig.life <=0:

                    pigs_to_remove.append(pig)
                global score
                self.resource.score += 10000
        for pig in pigs_to_remove:
            self.resource.space.remove(pig.shape, pig.shape.body)
            self.resource.pigs.remove(pig)


    def post_solve_bird_wood(self,arbiter, space, _):
        """Collision between bird and wood"""
        poly_to_remove = []
        if arbiter.total_impulse.length > 1100:
            a, b = arbiter.shapes
            for column in self.resource.columns:
                if b == column.shape:
                    poly_to_remove.append(column)
            for beam in self.resource.beams:
                if b == beam.shape:
                    poly_to_remove.append(beam)
            for poly in poly_to_remove:
                if poly in self.resource.columns:
                    self.resource.columns.remove(poly)
                if poly in self.resource.beams:
                    self.resource.beams.remove(poly)
            self.resource.space.remove(b, b.body)
 
            
            global score
            self.resource.score += 5000


    def post_solve_pig_wood(self,arbiter, space, _):
        """Collision between pig and wood"""
        pigs_to_remove = []
        if arbiter.total_impulse.length > 700:
            pig_shape, wood_shape = arbiter.shapes
            for pig in self.resource.pigs:
                if pig_shape == pig.shape:
                    pig.life -= 20
                    global score
                    self.resource.score += 10000
                    if pig.life <= 0:
                        pigs_to_remove.append(pig)
        for pig in pigs_to_remove:
            self.resource.space.remove(pig.shape, pig.shape.body)
            self.resource.pigs.remove(pig)





class AngryBirdsGame:
    """Main game class that coordinates all game components"""
    def __init__(self):
        self.resource = GameResources()
        self.state = GameStateManager(self.resource) 
        self.object= GameObjectManager(self.resource)
        self.running = True
        self.sling= Sling(self.resource)
        self.clock = pygame.time.Clock()
    def run(self):
        # bird and pigs
        self.resource.space.add_collision_handler(0, 1).post_solve=self.object.post_solve_bird_pig
        # bird and wood
        self.resource.space.add_collision_handler(0, 2).post_solve=self.object.post_solve_bird_wood
        # pig and wood
        self.resource.space.add_collision_handler(1, 2).post_solve=self.object.post_solve_pig_wood
        load_music()
        
        self.resource.level.number = 0
        self.resource.level.load_level()
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            
            # Maintain frame rate
            self.clock.tick(50)
            pygame.display.set_caption(f"fps: {self.clock.get_fps():.2f}")
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                # Toggle wall
                if wall:
                    for line in self.resource.static_lines1:
                        self.resource.space.remove(line)
                    wall = False
                else:
                    for line in self.resource.static_lines1:
                        self.resource.space.add(line)
                    wall = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.resource.space.gravity = (0.0, -10.0)
                self.resource.level.bool_space = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                self.resource.space.gravity = (0.0, -700.0)
                self.resource.level.bool_space = False
            if (pygame.mouse.get_pressed()[0] and self.resource.x_mouse > 100 and
                    self.resource.x_mouse < 250 and self.resource.y_mouse > 370 and self.resource.y_mouse < 550):
                self.resource.mouse_pressed = True
            
            if (event.type == pygame.MOUSEBUTTONUP and
                    event.button == 1 and self.resource.mouse_pressed):
                # Release new bird
                self.resource.mouse_pressed = False
                
                if self.resource.level.number_of_birds > 0:
                    self.resource.level.number_of_birds -= 1
                    self.resource.t1 = time.time()*1000
                    xo = 154
                    yo = 156
                    # Lấy hình ảnh theo chỉ mục
                    
                    bird_image = self.resource.bird_image[len(self.resource.birds)]
                    if self.resource.mouse_distance > self.resource.rope_lenght:
                        self.resource.mouse_distance = self.resource.rope_lenght
                    if self.resource.x_mouse < self.resource.sling_x+5:
                        bird = Bird(self.resource.mouse_distance, self.resource.angle, xo, yo, self.resource.space,bird_image)
                        self.resource.birds.append(bird)
                    else:
                        bird = Bird(-self.resource.mouse_distance, self.resource.angle, xo, yo, self.resource.space, bird_image)
                        self.resource.birds.append(bird)
                    if self.resource.level.number_of_birds == 0:

                        self.resource.t2 = time.time()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if (self.resource.x_mouse < 60 and self.resource.y_mouse < 155 and self.resource.y_mouse > 90):
                    self.resource.game_state = 1
                if self.resource.game_state == 1:
                    if self.resource.x_mouse > 500 and self.resource.y_mouse > 200 and self.resource.y_mouse < 300:
                        # Resume in the paused screen
                        self.resource.game_state = 0
                    if self.resource.x_mouse > 500 and self.resource.y_mouse > 300:
                        # Restart in the paused screen
                        self.state.restart()
                        self.resource.level.load_level()
                        self.resource.game_state = 0
                        self.resource.bird_path = []
                if self.resource.game_state == 3:
                    # Restart in the failed level screen
                    if self.resource.x_mouse > 500 and self.resource.x_mouse < 620 and self.resource.y_mouse > 450:
                        self.state.restart()
                        self.resource.level.load_level()
                        self.resource.game_state = 0
                        self.resource.bird_path = []
                        self.resource.score = 0
                if self.resource.game_state == 4:
                    # Build next level
                    if self.resource.x_mouse > 610 and self.resource.y_mouse > 450:
                        self.state.restart()
                        self.resource.level.number += 1
                        self.resource.game_state = 0
                        self.resource.level.load_level()
                        self.resource.score = 0
                        self.resource.bird_path = []
                        self.resource.bonus_score_once = True
                    if self.resource.x_mouse < 610 and self.resource.x_mouse > 500 and self.resource.y_mouse > 450:
                        # Restart in the level cleared screen
                        self.state.restart()
                        self.resource.level.load_level()
                        self.resource.game_state = 0
                        self.resource.bird_path = []
                        self.resource.score = 0
    def update(self):
        x=0
        # Update game objects
        # ... (add logic for updating self.resource.birds, pigs, etc.)
    def render(self):
        self.resource.x_mouse, self.resource.y_mouse = pygame.mouse.get_pos()
        # Draw background
        self.resource.screen.fill((130, 200, 100))
        self.resource.screen.blit(self.resource.background2, (0, -50))
        # Draw first part of the sling
        self.resource.rect = pygame.Rect(50, 0, 70, 220)
        self.resource.screen.blit(self.resource.sling_image, (138, 420), self.resource.rect)
        # Draw the trail left behind
        for point in self.resource.bird_path:
            pygame.draw.circle(self.resource.screen, self.resource.WHITE, point, 3, 0)
        # Draw the self.resource.birds in the wait line
        if self.resource.level.number_of_birds > 0:
            for i in range(self.resource.level.number_of_birds-1):
                x = 100 - (i*35)
                self.resource.screen.blit(self.resource.bird_image[abs(len(self.resource.bird_image)-1-i)], (x, 498))
        # Draw sling behavior
        
        if self.resource.mouse_pressed and self.resource.level.number_of_birds > 0:
            self.sling.sling_action(self.resource.bird_image[abs(len(self.resource.bird_image)-self.resource.level.number_of_birds)  ])
        else:
            if time.time()*1000 - self.resource.t1 > 300 and self.resource.level.number_of_birds > 0:
                self.resource.screen.blit(self.resource.bird_image[abs(len(self.resource.bird_image)-self.resource.level.number_of_birds)  ], (130, 426))
            else:
                pygame.draw.line(self.resource.screen, (0, 0, 0), (self.resource.sling_x, self.resource.sling_y-8),
                                (self.resource.sling2_x, self.resource.sling2_y-7), 5)
        self.resource.birds_to_remove = []
        pigs_to_remove = []
        self.resource.counter += 1
        # Draw self.resource.birds
        for bird in self.resource.birds:

            if bird.shape.body.position.y < 0 :
                self.resource.birds_to_remove.append(bird)
            p = to_pygame(bird.shape.body.position)
            x, y = p
            x -= 22
            y -= 20
            self.resource.screen.blit(bird.image, (x, y))
            pygame.draw.circle(self.resource.screen, self.resource.BLUE,
                            p, int(bird.shape.radius), 1)
            if self.resource.counter >= 3 and time.time() - self.resource.t1 < 5:
                self.resource.bird_path.append(p)
                self.resource.restart_counter = True
        if self.resource.restart_counter:
            self.resource.counter = 0
            self.resource.restart_counter = False
        # Remove self.resource.birds and pigs
        for bird in self.resource.birds_to_remove:
            self.resource.space.remove(bird.shape, bird.shape.body)
            self.resource.birds.remove(bird)
        for pig in pigs_to_remove:
            self.resource.space.remove(pig.shape, pig.shape.body)
            self.resource.pigs.remove(pig)
        # Draw static lines
        for line in self.resource.static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = to_pygame(pv1)
            p2 = to_pygame(pv2)
            pygame.draw.lines(self.resource.screen, (150, 150, 150), False, [p1, p2])
        i = 0
        # Draw pigs
        for pig in self.resource.pigs:
            i += 1
            # print (i,pig.life)
            pig = pig.shape
            if pig.body.position.y < 0:
                pigs_to_remove.append(pig)

            p = to_pygame(pig.body.position)
            x, y = p

            self.resource.angle_degrees = math.degrees(pig.body.angle)
            img = pygame.transform.rotate(self.resource.pig_image, self.resource.angle_degrees)
            w,h = img.get_size()
            x -= w*0.5
            y -= h*0.5
            self.resource.screen.blit(img, (x, y))
            pygame.draw.circle(self.resource.screen, self.resource.BLUE, p, int(pig.radius), 2)
        # Draw columns and Beams
        for column in self.resource.columns:
            column.draw_poly('columns', self.resource.screen)
        for beam in self.resource.beams:
            beam.draw_poly('beams', self.resource.screen)
        # Update physics
        dt = 1.0/50.0/2.
        for x in range(2):
            self.resource.space.step(dt) # make two updates per frame for better stability
        # Drawing second part of the sling
        rect = pygame.Rect(0, 0, 60, 200)
        self.resource.screen.blit(self.resource.sling_image, (120, 420), rect)
        # Draw score
        score_font = self.resource.bold_font.render("SCORE", 1, self.resource.WHITE)
        number_font =self.resource.bold_font.render(str(self.resource.score), 1, self.resource.WHITE)
        self.resource.screen.blit(score_font, (1060, 90))
        if self.resource.score == 0:
            self.resource.screen.blit(number_font, (1100, 130))
        else:
            self.resource.screen.blit(number_font, (1060, 130))
        self.resource.screen.blit(self.resource.pause_button, (10, 90))
        # Pause option
        if self.resource.game_state == 1:
            self.resource.screen.blit(self.resource.play_button, (500, 200))
            self.resource.screen.blit(self.resource.replay_button, (500, 300))
        self.state.draw_level_cleared()
        self.state.draw_level_failed()
        pygame.display.flip()
def main():
    """Start the game"""
    game = AngryBirdsGame()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()