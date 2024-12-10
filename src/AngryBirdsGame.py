import math
import pymunk as pm
import time
import pygame

from ObjectManager import Explosion, GameObjectManager 
from StateManager import GameStateManager
from Sling import GameSling
from characters import Bird
from Resources import GameResources 


class AngryBirds:
    """Main game class that coordinates all game components"""
    def __init__(self,song,resource):
        
        # pygame.mixer.music.load(song)
        # pygame.mixer.music.play(-1)
        logo=pygame.image.load("./resources/images/logo.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Angry Bird")
        self.resource = resource
        self.state = GameStateManager(self.resource) 
        self.object= GameObjectManager(self.resource)
        self.sling= GameSling(self.resource)
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        # bird and pigs
        self.resource.space.add_collision_handler(0, 1).post_solve=self.object.post_solve_bird_pig
        # bird and wood
        self.resource.space.add_collision_handler(0, 2).post_solve=self.object.post_solve_bird_wood
        # self.resource.space.add_collision_handler(0, 2).begin=self.object.post_solve_bird_wood
        # pig and wood
        self.resource.space.add_collision_handler(1, 2).post_solve=self.object.post_solve_pig_wood

        self.resource.space.add_collision_handler(0, 3).post_solve=self.object.post_solve_bird_boss
        # load_music()
        
        self.resource.level.number = 0
        self.resource.level.load_level()
        """Main game loop"""
        while self.running:
            self.handle_events()
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
                    self.resource.score= self.resource.score-20000
                    self.resource.t1 = time.time()*1000
                    xo = 154
                    yo = 156
                    # Lấy hình ảnh theo chỉ mục
                    bird_image = self.resource.bird_image[abs(len(self.resource.bird_image)-1-self.resource.level.number_of_birds)]
                    if self.resource.mouse_distance > self.resource.rope_lenght:
                        self.resource.mouse_distance = self.resource.rope_lenght
                    if self.resource.x_mouse < self.sling.sling_x+5:
                        bird = Bird(self.resource.mouse_distance, self.resource.angle, xo, yo, self.resource.space,bird_image)
                        self.resource.birds.append(bird)
                        
                        if len(self.resource.birds)>1:
                            position=self.resource.birds[0].body.position
                            explosion = Explosion(position, self.resource.screen, self.resource.explosions1_images)
                            self.resource.explosions.append(explosion)  # Lưu vào danh sách hiệu ứng
                            self.resource.birds.pop(0)
                    else:
                        bird = Bird(-self.resource.mouse_distance, self.resource.angle, xo, yo, self.resource.space, bird_image)
                        self.resource.birds.append(bird)
                        if len(self.resource.birds)>1:
                            position=self.resource.birds[0].body.position
                            explosion = Explosion(position, self.resource.screen, self.resource.explosions1_images)
                            self.resource.explosions.append(explosion)  # Lưu vào danh sách hiệu ứng
                            self.resource.birds.pop(0)
                    if self.resource.level.number_of_birds == 0:
                        self.resource.t2 = time.time()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if (self.resource.x_mouse < 60 and self.resource.y_mouse < 155 and self.resource.y_mouse > 90):
                    self.state.game_state = 1
                if self.state.game_state == 1:
                    if self.resource.x_mouse > 500 and self.resource.y_mouse > 200 and self.resource.y_mouse < 300:
                        # Resume in the paused screen
                        self.state.game_state = 0
                    if self.resource.x_mouse > 500 and self.resource.y_mouse > 300:
                        # Restart in the paused screen
                        self.state.restart()
                        self.resource.level.load_level()
                        self.state.game_state = 0
                        self.resource.bird_path = []
                if self.state.game_state == 3:
                    # Restart in the failed level screen
                    if self.resource.x_mouse > 500 and self.resource.x_mouse < 620 and self.resource.y_mouse > 450:
                        self.state.restart()
                        self.resource.level.load_level()
                        self.state.game_state = 0
                        self.resource.bird_path = []
                        self.resource.score = 60000
                if self.state.game_state == 4:
                    # Build next level
                    if self.resource.x_mouse > 610 and self.resource.y_mouse > 450:
                        self.state.restart()
                        self.resource.level.number += 1
                        self.state.game_state = 0
                        self.resource.level.load_level()
                        self.resource.score = 60000
                        self.resource.bird_path = []
                        self.resource.bonus_score_once = True
                    if self.resource.x_mouse < 610 and self.resource.x_mouse > 500 and self.resource.y_mouse > 450:
                        # Restart in the level cleared screen
                        self.state.restart()
                        self.resource.level.load_level()
                        self.state.game_state = 0
                        self.resource.bird_path = []
                        self.resource.score = 0
    def to_pygame(self,p):
        """Convert pynk to pygame coordinates"""
        return int(p.x), int(-p.y+600)
    def render(self):
        self.resource.x_mouse, self.resource.y_mouse = pygame.mouse.get_pos()
        # Draw background
        self.resource.screen.fill((130, 200, 100))
        self.resource.screen.blit(self.resource.background2, (0, -50))
        # Draw first part of the sling
        self.resource.rect = pygame.Rect(50, 0, 70, 220)
        self.resource.screen.blit(self.sling.sling_image, (138, 420), self.resource.rect)
        # Draw the trail left behind
        for point in self.resource.bird_path:
            pygame.draw.circle(self.resource.screen, self.resource.WHITE, point, 2, 0)
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
                pygame.draw.line(self.resource.screen, (0, 0, 0), (self.sling.sling_x, self.sling.sling_y-8),
                                (self.sling.sling2_x, self.sling.sling2_y-7), 5)
        self.resource.birds_to_remove = []
        pigs_to_remove = []
        self.resource.counter += 1
        # Draw self.resource.birds
        for bird in self.resource.birds:
            x, y = bird.body.position 
            if y<=73:
                if bird.body.velocity.x< 70:
                    if bird.body.velocity.y< 40:
                        if bird.body.velocity.x < 1 and bird.body.velocity.y<0.4:
                            bird.body.velocity = pm.Vec2d(0,0)  # Chỉ thay đổi trục x

                        friction_factor = 0.99  # Hệ số giảm vận tốc, gần 1 để giảm từ từ
                        bird.body.velocity *= friction_factor  

            if bird.shape.body.position.y < 0 :
                self.resource.birds_to_remove.append(bird)
            p = self.to_pygame(bird.shape.body.position)
            x, y = p
            x -= 22
            y -= 20
            self.resource.screen.blit(bird.image, (x, y))
            x, y = bird.body.position 
     
            if y <= 73 :
                # Đánh dấu bird đã va chạm hoặc tiếp đất, không lưu đường bay nữa
                bird.has_collided = True  # Đặt cờ trạng thái va chạm/tiếp đất
            if not getattr(bird, "has_collided", False):  # Nếu chưa va chạm/tiếp đất
                p = self.to_pygame(bird.shape.body.position)
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
        
        # Draw static lines
        for line in self.resource.static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = self.to_pygame(pv1)
            p2 = self.to_pygame(pv2)
            pygame.draw.lines(self.resource.screen, (150, 150, 150), False, [p1, p2])
        
        for explosion in self.resource.explosions:  # Duyệt qua danh sách
            explosion.update()  # Cập nhật trạng thái hiệu ứng
            if explosion.finished:  # Nếu hiệu ứng hoàn tất
                self.resource.explosions.remove(explosion)  # Xóa khỏi danh sách
        i = 0
        pigsBoss_to_remove=[]
        # Draw pigsBoss
        for pigBoss in self.resource.pigsBoss:
            i += 1
            if pigBoss.body.position.y < 0:
                pigsBoss_to_remove.append(pigBoss)
            pigBoss.update()
           
            pigBoss.render(self.resource.screen)
        i = 0
        # Draw pigs
        for pig in self.resource.pigs:
            i += 1
            # print (i,pig.life)
            if pig.body.position.y < 0:
                pigs_to_remove.append(pig)
            pig = pig.shape
            

            p = self.to_pygame(pig.body.position)
            x, y = p

            self.resource.angle_degrees = math.degrees(pig.body.angle)
            img = pygame.transform.rotate(self.resource.pig_image, self.resource.angle_degrees)
            w,h = img.get_size()
            x -= w*0.5
            y -= h*0.5
            self.resource.screen.blit(img, (x, y))
        for pig in pigsBoss_to_remove:
            # Kiểm tra xem pig có body không
            if pig.body is None or pig.body not in self.resource.space.bodies:
                pigs_to_remove.append(pig)
            else:
                self.resource.space.remove(pig.shape.body)
                self.resource.pigsBoss.remove(pig) 
        
        
           
        for pig in pigs_to_remove:
            # Kiểm tra xem pig có body không
            if pig.body is None or pig.body not in self.resource.space.bodies:
                pigs_to_remove.append(pig)
            else:
                self.resource.space.remove(pig.shape.body)
                self.resource.pigs.remove(pig)
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
        self.resource.screen.blit(self.sling.sling_image, (120, 420), rect)
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
        if self.state.game_state == 1:
            self.resource.screen.blit(self.resource.play_button, (500, 200))
            self.resource.screen.blit(self.resource.replay_button, (500, 300))
        self.state.draw_level_cleared()
        self.state.draw_level_failed()
        pygame.display.flip()
