import os
import sys
import math
import time
import pygame
import pymunk as pm

from characters import Bird
from level import Level

class GameResources:
    """Manages game assets and resources"""
    def __init__(self):
        pygame.init()
        self.counter = 0
        self.restart_counter = False
        self.t1=0
        self.t2=0
        self.x_mouse=0
        self.y_mouse=0
        self.angle = 0
        self.rope_lenght = 90
        self.bird_path=[]
        # Screen setup
        self.screen_width = 1200
        self.screen_height = 650
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # Load images
        self.background = pygame.image.load("./resources/images/background3.png").convert_alpha()
        self.sling_image = pygame.image.load("./resources/images/sling-3.png").convert_alpha()
        
        # Bird image
        self.redbird = pygame.image.load("./resources/images/red-bird3.png").convert_alpha()
        
        # Pig image
        full_sprite = pygame.image.load("./resources/images/full-sprite.png").convert_alpha()
        rect = pygame.Rect(181, 1050, 50, 50)
        cropped = full_sprite.subsurface(rect).copy()
        self.pig_image = pygame.transform.scale(cropped, (30, 30))
        
        # UI elements
        buttons = pygame.image.load("./resources/images/selected-buttons.png").convert_alpha()
        stars = pygame.image.load("./resources/images/stars-edited.png").convert_alpha()
        
        # Buttons and stars
        self.pause_button = buttons.subsurface(pygame.Rect(164, 10, 60, 60)).copy()
        self.replay_button = buttons.subsurface(pygame.Rect(24, 4, 100, 100)).copy()
        self.next_button = buttons.subsurface(pygame.Rect(142, 365, 130, 100)).copy()
        self.play_button = buttons.subsurface(pygame.Rect(18, 212, 100, 100)).copy()
        
        # Stars
        self.stars = [
            stars.subsurface(pygame.Rect(0, 0, 200, 200)).copy(),
            stars.subsurface(pygame.Rect(204, 0, 200, 200)).copy(),
            stars.subsurface(pygame.Rect(426, 0, 200, 200)).copy()
        ]
        
        # Fonts
        self.bold_font = pygame.font.SysFont("arial", 30, bold=True)
        self.bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
        self.bold_font3 = pygame.font.SysFont("arial", 50, bold=True)
        
        # Colors
        self.COLORS = {
            'RED': (255, 0, 0),
            'BLUE': (0, 0, 255),
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255)
        }

class PhysicsEngine:
    """Manages the physics simulation using Pymunk"""
    def __init__(self):
        self.space = pm.Space()
        self.space.gravity = (0.0, -700.0)
        
        # Create static floor
        self.static_body = pm.Body(body_type=pm.Body.STATIC)
        self.static_lines = [
            [pm.Segment(self.static_body, (0.0, 60.0), (1200.0, 60.0), 0.0)],
            [pm.Segment(self.static_body, (1200.0, 60.0), (1200.0, 800.0), 0.0)]
        ]
        
        for line in self.static_lines[0]:
            line.elasticity = 0.95
            line.friction = 1
            line.collision_type = 3
        for line in self.static_lines[1]:
            line.elasticity = 0.95
            line.friction = 1
            line.collision_type = 3
        self.space.add(self.static_body)
        for line in self.static_lines[0]:
            self.space.add(line)

    
    def step(self, dt=1.0/100.0):
        """Update physics simulation"""
        for _ in range(2):
            self.space.step(dt)
    
    def add_collision_handlers(self, game_objects):
        """Set up collision handlers"""
        # Bird and Pig collision
        self.space.add_collision_handler(0, 1).post_solve = game_objects.post_solve_bird_pig
        
        # Bird and Wood collision
        self.space.add_collision_handler(0, 2).post_solve = game_objects.post_solve_bird_wood
        
        # Pig and Wood collision
        self.space.add_collision_handler(1, 2).post_solve = game_objects.post_solve_pig_wood

class GameObjectManager:
    """Manages game objects like birds, pigs, and structures"""
    def __init__(self, space, resources):
        self.space = space
        self.resources = resources
        self.pigs = []
        self.birds = []
        self.columns = []
        self.beams = []
        self.score = 0
    
    def post_solve_bird_pig(self, arbiter,space, _):
        """Handle collision between bird and pig"""
        a, b = arbiter.shapes
        pig_body = b.body
        
        for pig in self.pigs:
            if pig_body == pig.body:
                pig.life -= 20
                self.score += 10000
                
                if pig.life <= 0:
                    self.space.remove(pig.shape, pig.shape.body)
                    self.pigs.remove(pig)
    
    def post_solve_bird_wood(self, arbiter, space, _):
        """Handle collision between bird and wood"""
        if arbiter.total_impulse.length > 1100:
            _, b = arbiter.shapes
            
            # Remove columns or beams
            for poly_list in [self.columns, self.beams]:
                for poly in poly_list.copy():
                    if b == poly.shape:
                        poly_list.remove(poly)
                        self.space.remove(b, b.body)
                        self.score += 5000
    
    def post_solve_pig_wood(self, arbiter, space, _):
        """Handle collision between pig and wood"""
        if arbiter.total_impulse.length > 700:
            pig_shape, _ = arbiter.shapes
            
            for pig in self.pigs.copy():
                if pig_shape == pig.shape:
                    pig.life -= 20
                    self.score += 10000
                    
                    if pig.life <= 0:
                        self.space.remove(pig.shape, pig.shape.body)
                        self.pigs.remove(pig)

class GameStateManager:
    """Manages different states of the game"""
    def __init__(self, resources, game_objects,physics_engine):
        self.resources = resources
        self.game_objects = game_objects
        self.physics_engine=physics_engine
        self.state = 0  # 0: playing, 1: paused, 3: failed, 4: cleared
        self.level = Level(self.game_objects.pigs, self.game_objects.columns, self.game_objects.beams, physics_engine.space)
        self.birds_remaining = 0
        self.bonus_score_once = True
    def restart(self):
        """Delete all objects of the level and restart the game"""
        pigs_to_remove = []
        birds_to_remove = []
        columns_to_remove = []
        beams_to_remove = []

        # Add pigs to remove list and remove from the space
        for pig in self.game_objects.pigs:
            pigs_to_remove.append(pig)
        for pig in pigs_to_remove:
            self.physics_engine.space.remove(pig.shape, pig.shape.body)
            self.game_objects.pigs.remove(pig)

        # Add birds to remove list and remove from the space
        for bird in self.game_objects.birds:
            birds_to_remove.append(bird)
        for bird in birds_to_remove:
            self.physics_engine.space.remove(bird.shape, bird.shape.body)
            self.game_objects.birds.remove(bird)

        # Add columns to remove list and remove from the space
        for column in self.game_objects.columns:
            columns_to_remove.append(column)
        for column in columns_to_remove:
            self.physics_engine.space.remove(column.shape, column.shape.body)
            self.game_objects.columns.remove(column)

        # Add beams to remove list and remove from the space
        for beam in self.game_objects.beams:
            beams_to_remove.append(beam)
        for beam in beams_to_remove:
            self.physics_engine.space.remove(beam.shape, beam.shape.body)
            self.game_objects.beams.remove(beam)

        # Reset game state and level
        self.state = 0  # Reset game state to playing
        self.level = Level(self.game_objects.pigs, self.game_objects.columns, self.game_objects.beams, self.physics_engine.space)  # Reset level

        # Reset game variables
        self.birds_remaining = 0
        self.bonus_score_once = True
    def draw_level_failed(self):
        """Draw level failed"""
        self.state
        failed = self.resources.bold_font3.render("Level Failed", 1, self.resources.COLORS['WHITE'])
        if self.level.number_of_birds <= 0 and time.time() - self.resources.t2 > 5 and len(self.game_objects.pigs) > 0:
            self.state = 3
            rect = pygame.Rect(300, 0, 600, 800)
            pygame.draw.rect(self.resources.screen, self.resources.COLORS['BLACK'], rect)
            self.resources.screen.blit(failed, (450, 90))
            self.resources.screen.blit(self.resources.pig_happy, (380, 120))
            self.resources.screen.blit(self.resources.replay_button, (520, 460))

    def draw_level_cleared(self):
        """Draw level cleared screen"""
        if self.birds_remaining >= 0 and len(self.game_objects.pigs) == 0:
            if self.bonus_score_once:
                self.game_objects.score += (self.birds_remaining - 1) * 10000
            self.bonus_score_once = False
            self.state = 4
            
            # Draw black overlay
            rect = pygame.Rect(300, 0, 600, 800)
            self.resources.screen.fill(self.resources.COLORS['BLACK'], rect)
            
            # Level cleared text
            level_cleared = self.resources.bold_font3.render("Level Cleared!", 1, self.resources.COLORS['WHITE'])
            self.resources.screen.blit(level_cleared, (450, 90))
            
            # Stars based on score
            star_positions = [(310, 190), (500, 170), (700, 200)]
            score_thresholds = [
                (0, self.level.one_star),
                (self.level.one_star, self.level.two_star),
                (self.level.two_star, self.level.three_star)
            ]
            
            for i, (min_score, max_score) in enumerate(score_thresholds):
                if self.game_objects.score >= min_score and self.game_objects.score <= max_score:
                    self.resources.screen.blit(self.resources.stars[i], star_positions[i])
            
            # Score display
            score_text = self.resources.bold_font2.render(str(self.game_objects.score), 1, self.resources.COLORS['WHITE'])
            self.resources.screen.blit(score_text, (550, 400))
            
            # Replay and next buttons
            self.resources.screen.blit(self.resources.replay_button, (510, 480))
            self.resources.screen.blit(self.resources.next_button, (620, 480))
class Sling:
    def __init__(self):
        self.mouse_distance=0
        self.rope_lenght=0
        self.angle=0
        self.x_mouse=0
        self.y_mouse=0
        self.sling_x, self.sling_y = 135, 450
        self.sling2_x, self.sling2_y = 160, 450
    def sling_action(self):
        """Set up sling behavior"""
        
        # Fixing bird to the sling rope
        v = self.vector((self.sling_x, self.sling_y), (self.x_mouse, self.y_mouse))
        uv = self.unit_vector(v)
        uv1 = uv[0]
        uv2 = uv[1]
        self.mouse_distance = self.distance(self.sling_x, self.sling_y, self.x_mouse, self.y_mouse)
        pu = (uv1*self.rope_lenght+self.sling_x, uv2*self.rope_lenght+self.sling_y)
        bigger_rope = 102
        x_redbird = self.x_mouse - 20
        y_redbird = self.y_mouse - 20
        if self.mouse_distance > self.rope_lenght:
            pux, puy = pu
            pux -= 20
            puy -= 20
            pul = pux, puy
            self.resources.screen.blit(self.resources.redbird, pul)
            pu2 = (uv1*bigger_rope+self.sling_x, uv2*bigger_rope+self.sling_y)
            pygame.draw.line(self.resources.screen, (0, 0, 0), (self.sling2_x, self.sling2_y), pu2, 5)
            self.resources.screen.blit(self.resources.redbird, pul)
            pygame.draw.line(self.resources.screen, (0, 0, 0), (self.sling_x, self.sling_y), pu2, 5)
        else:
            self.mouse_distance += 10
            pu3 = (uv1*self.mouse_distance+self.sling_x, uv2*self.mouse_distance+self.sling_y)
            pygame.draw.line(self.resources.screen, (0, 0, 0), (self.sling2_x, self.sling2_y), pu3, 5)
            self.resources.screen.blit(self.resources.redbird, (x_redbird, y_redbird))
            pygame.draw.line(self.resources.screen, (0, 0, 0), (self.sling_x, self.sling_y), pu3, 5)
        # Angle of impulse
        dy = self.y_mouse - self.sling_y
        dx = self.x_mouse - self.sling_x
        if dx == 0:
            dx = 0.00000000000001
        angle = math.atan((float(dy))/dx)
    def vector(p0, p1):
        """Return the vector of the points
        p0 = (xo,yo), p1 = (x1,y1)"""
        a = p1[0] - p0[0]
        b = p1[1] - p0[1]
        return (a, b)


    def unit_vector(v):
        """Return the unit vector of the points
        v = (a,b)"""
        h = ((v[0]**2)+(v[1]**2))**0.5
        if h == 0:
            h = 0.000000000000001
        ua = v[0] / h
        ub = v[1] / h
        return (ua, ub)


    def distance(xo, yo, x, y):
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

class AngryBirdsGame:
    """Main game class that coordinates all game components"""
    def __init__(self):
        # Initialize game components
        self.resources = GameResources()
        self.physics_engine = PhysicsEngine()
        self.game_objects = GameObjectManager(self.physics_engine.space, self.resources)
        self.state_manager = GameStateManager(self.resources, self.game_objects,self.physics_engine)
        self.sling = Sling()
        # Set up collision handlers
        self.physics_engine.add_collision_handlers(self.game_objects)
        
        # Game loop variables
        self.clock = pygame.time.Clock()
        self.running = True
        self.mouse_pressed = False
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            
            # Maintain frame rate
            self.clock.tick(50)
            pygame.display.set_caption(f"fps: {self.clock.get_fps():.2f}")
    
    def handle_events(self):
        """Process game events"""
        for event in pygame.event.get():
            # Quit events
            if event.type in [pygame.QUIT, pygame.KEYDOWN] and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                # Toggle wall
                if wall:
                    for line in self.physics_engine.static_lines[1]:
                        self.physics_engine.space.remove(line)
                    wall = False
                else:
                    for line in self.physics_engine.static_lines[1]:
                        self.physics_engine.space.add(line)
                    wall = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.physics_engine.space.gravity = (0.0, -10.0)
                self.state_manager.level.bool_space = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                self.physics_engine.space.gravity = (0.0, -700.0)
                self.state_manager.level.bool_space = False
            if (pygame.mouse.get_pressed()[0] and self.resources.x_mouse > 100 and
                    self.resources.x_mouse < 250 and self.resources.y_mouse > 370 and self.y_mouse < 550):
                mouse_pressed = True
            if (event.type == pygame.MOUSEBUTTONUP and
                    event.button == 1 and mouse_pressed):
                # Release new bird
                self.mouse_pressed = False
                if self.state_manager.level.number_of_birds > 0:
                    self.state_manager.level.number_of_birds -= 1
                    self.resources.t1 = time.time()*1000
                    xo = 154
                    yo = 156
                    if mouse_distance > self.rope_lenght:
                        mouse_distance = self.rope_lenght
                    if self.x_mouse < self.sling.sling_x+5:
                        bird= Bird(mouse_distance, self.angle, xo, yo, self.physics_engine.space)
                        self.game_objects.bird.append(bird)
                    else:
                        bird = Bird(-mouse_distance, self.angle, xo, yo, self.physics_engine.space)
                        self.game_objects.bird.append(bird)
                    if self.state_manager.level.number_of_birds == 0:
                        t2 = time.time()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if (self.x_mouse < 60 and self.y_mouse < 155 and self.y_mouse > 90):
                    self.state_manager.state = 1
                if self.state_manager.state == 1:
                    if self.x_mouse > 500 and self.y_mouse > 200 and self.y_mouse < 300:
                        # Resume in the paused screen
                        self.state_manager.state = 0
                    if self.x_mouse > 500 and self.y_mouse > 300:
                        # Restart in the paused screen
                        self.state_manager.restart()
                        self.state_manager.level.load_level()
                        self.state_manager.state = 0
                        self.resources.bird_path = []
                if self.state_manager.state == 3:
                    # Restart in the failed level screen
                    if self.x_mouse > 500 and self.x_mouse < 620 and self.y_mouse > 450:
                        self.state_manager.restart()
                        self.state_manager.level.load_level()
                        self.state_manager.state = 0
                        self.resources.bird_path = []
                        score = 0
                if self.state_manager.state == 4:
                    # Build next level
                    if self.x_mouse > 610 and self.y_mouse > 450:
                        self.state_manager.restart()
                        self.state_manager.level.number += 1
                        self.state_manager.state = 0
                        self.state_manager.level.load_level()
                        self.game_objects.score = 0
                        self.resources.bird_path = []
                        bonus_score_once = True
                    if self.x_mouse < 610 and self.x_mouse > 500 and self.y_mouse > 450:
                        # Restart in the level cleared screen
                        self.state_manager.restart()
                        self.state_manager.level.load_level()
                        self.state_manager.state = 0
                        self.resources.bird_path = []
                        self.game_objects.score = 0
            
            # Rest of the event handling logic (bird launching, UI interactions)
            # ... (would be implemented similar to the original game logic)
    
    def update(self):
        """Update game state"""
        # Physics update
        self.physics_engine.step()
        
        # Update game objects
        # ... (add logic for updating birds, pigs, etc.)
    
    def render(self):
        """Render game screen"""
        # Clear screen and draw background
        self.resources.screen.fill((130, 200, 100))
        self.resources.screen.blit(self.resources.background, (0, -50))
        # Draw first part of the sling
        rect = pygame.Rect(50, 0, 70, 220)
        self.resources.screen.blit(self.resources.sling_image, (138, 420), rect)
        # Draw the trail left behind
        for point in self.resources.bird_path:
            pygame.draw.circle(self.resources.screen, self.resources.COLORS['WHITE'], point, 5, 0)
        # Draw the birds in the wait line
        if self.state_manager.level.number_of_birds > 0:
            for i in range(self.state_manager.level.number_of_birds-1):
                x = 100 - (i*35)
                self.resources.screen.blit(self.resources.redbird, (x, 508))
        # Draw sling behavior
        if self.mouse_pressed and self.state_manager.level.number_of_birds > 0:
            self.state_manager.sling_action()
        else:
            if time.time()*1000 - self.resources.t1 > 300 and self.state_manager.level.number_of_birds > 0:
                self.resources.screen.blit(self.resources.redbird, (130, 426))
            else:
                pygame.draw.line(self.resources.screen, (0, 0, 0), (self.sling.sling_x, self.sling.sling_y-8),
                                (self.sling.sling2_x, self.sling.sling2_y-7), 5)
        birds_to_remove = []
        pigs_to_remove = []
        self.resources.counter += 1
        # Draw birds
        for bird in self.game_objects.birds:
            if bird.shape.body.position.y < 0:
                birds_to_remove.append(bird)
            p = self.to_pygame(bird.shape.body.position)
            x, y = p
            x -= 22
            y -= 20
            self.resources.screen.blit(self.resources.redbird, (x, y))
            pygame.draw.circle(self.resources.screen, self.resources['BLUE'],
                            p, int(bird.shape.radius), 2)
            if self.resources.counter >= 3 and time.time() - self.resources.t1 < 5:
                self.bird_path.append(p)
                self.resources.restart_counter = True
        if self.resources.restart_counter:
            self.resources.counter = 0
            self.resources.restart_counter = False
        # Remove birds and pigs
        for bird in birds_to_remove:
            self.physics_engine.space.remove(bird.shape, bird.shape.body)
            self.game_objects.birds.remove(bird)
        for pig in pigs_to_remove:
            self.physics_engine.space.remove(pig.shape, pig.shape.body)
            self.game_objects.pigs.remove(pig)
        # Draw static lines
        for line in self.physics_engine.static_lines[0]:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = self.to_pygame(pv1)
            p2 = self.to_pygame(pv2)
            pygame.draw.lines(self.resources.screen, (150, 150, 150), False, [p1, p2])
        i = 0
        # Draw pigs
        for pig in self.game_objects.pigs:
            i += 1
            # print (i,pig.life)
            pig = pig.shape
            if pig.body.position.y < 0:
                pigs_to_remove.append(pig)

            p = self.to_pygame(pig.body.position)
            x, y = p

            self.angle_degrees = math.degrees(pig.body.angle)
            img = pygame.transform.rotate(self.resources.pig_image, self.angle_degrees)
            w,h = img.get_size()
            x -= w*0.5
            y -= h*0.5
            self.resources.screen.blit(img, (x, y))
            pygame.draw.circle(self.resources.screen, self.resources.COLORS['BLUE'], p, int(pig.radius), 2)
        # Draw columns and Beams
        for column in self.game_objects.columns:
            column.draw_poly('columns', self.resources.screen)
        for beam in self.game_objects.beams:
            beam.draw_poly('beams', self.resources.screen)
        # Update physics
        dt = 1.0/50.0/2.
        for x in range(2):
            self.physics_engine.space.step(dt) # make two updates per frame for better stability
        # Drawing second part of the sling
        rect = pygame.Rect(0, 0, 60, 200)
        self.resources.screen.blit(self.resources.sling_image, (120, 420), rect)
        # Draw score
        score_font = self.resources.bold_font.render("SCORE", 1, self.resources.COLORS['WHITE'])
        number_font = self.resources.bold_font.render(str(self.game_objects.score), 1, self.resources.COLORS['WHITE'])
        self.resources.screen.blit(score_font, (1060, 90))
        if self.game_objects.score == 0:
            self.resources.screen.blit(number_font, (1100, 130))
        else:
            self.resources.screen.blit(number_font, (1060, 130))
        self.resources.screen.blit(self.resources.pause_button, (10, 90))
        # Pause option
        if self.state_manager.state == 1:
            self.resources.screen.blit(self.resources.play_button, (500, 200))
            self.resources.screen.blit(self.resources.replay_button, (500, 300))
        self.state_manager.draw_level_cleared()
        self.state_manager.draw_level_failed()
        # Draw game objects
        # ... (implement drawing of sling, birds, pigs, etc.)
        
        # Update display
        pygame.display.flip()
    def to_pygame(self,p):
        """Convert pymunk to pygame coordinates"""
        return int(p.x), int(-p.y+600)

def main():
    """Start the game"""
    game = AngryBirdsGame()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()