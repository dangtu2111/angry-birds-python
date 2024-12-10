


import time
import pygame

class Explosion:
    def __init__(self, position, screen, images):
        self.position = self.to_pygame(position)
        self.screen = screen
        self.images = images
        self.current_frame = 0
        self.start_time = pygame.time.get_ticks()  # Lấy thời điểm bắt đầu hiệu ứng
        self.finished = False

    def to_pygame(self, p):
        """Chuyển tọa độ từ pymunk sang pygame"""
        return int(p.x), int(-p.y + 600)  # 600 là chiều cao của màn hình


    def update(self):
        now = pygame.time.get_ticks()
        # Nếu đã qua 100ms, chuyển sang ảnh kế tiếp
        if now - self.start_time >= 50:
            self.start_time = now
            self.current_frame += 1
        
        if self.current_frame >= len(self.images):
            self.finished = True  # Hiệu ứng hoàn tất
        else:
            self.draw()

    def draw(self):
        if not self.finished:
            image = self.images[self.current_frame]
            self.screen.blit(image, (self.position[0] - image.get_width() // 2,
                                    self.position[1] - image.get_height() // 2))

class GameObjectManager:
    """Manages game objects like birds, pigs, and structures"""
    def __init__(self, resources):
        self.resource=resources
    def to_pygame(self,p):
        """Convert pynk to pygame coordinates"""
        return int(p.x), int(-p.y+600)
    def post_solve_bird_pig(self,arbiter, space, _):
        """Collision between bird and pig"""
        surface=self.resource.screen
        a, b = arbiter.shapes
        bird_body = a.body
        pig_body = b.body
        p = self.to_pygame(bird_body.position)
        p2 = self.to_pygame(pig_body.position)
        r = 30
        pigs_to_remove = []
        a.has_collided = True 
        if arbiter.total_impulse.length > 700:
            for pig in self.resource.pigs:
                if pig_body == pig.body:
                    pig.life -= 20
                    if pig.life <=0:

                        pigs_to_remove.append(pig)
                    global score
                    self.resource.score += 10000
            position = b.body.position
            explosion = Explosion(position, self.resource.screen, self.resource.explosions_images)
            self.resource.explosions.append(explosion)  # Lưu vào danh sách hiệu ứng
            for pig in pigs_to_remove:
                self.resource.space.remove(pig.shape, pig.shape.body)
                self.resource.pigs.remove(pig)
    def post_solve_bird_boss(self,arbiter ,space, _):
        a, b = arbiter.shapes
        bird_body = a.body
        boss_body = b.body
        p = self.to_pygame(bird_body.position)
        p2 = self.to_pygame(boss_body.position)
        r = 30
        a.has_collided = True 
        boss_to_remove = []
        if arbiter.total_impulse.length > 1500:
            for boss in self.resource.pigsBoss:
                if boss_body == boss.body:
                    boss.life -= 20
                    print(boss.life)
                    if boss.life <=0:

                        boss_to_remove.append(boss)
                    global score
                    self.resource.score += 10000
                if boss.life == 40:
                    boss.setState(1)
                if boss.life == 20:
                    boss.setState(2)
            for boss in boss_to_remove:
                self.resource.space.remove(boss.shape, boss.shape.body)
                self.resource.pigsBoss.remove(boss)
    def post_solve_bird_wood(self,arbiter, space, _):
        """Collision between bird and wood"""
        poly_to_remove = []
        a, b = arbiter.shapes
        a.has_collided = True 
        if arbiter.total_impulse.length > 1100:
            for column in self.resource.columns:
                if b == column.shape:
                    poly_to_remove.append(column)
            for beam in self.resource.beams:
                if b == beam.shape:
                    poly_to_remove.append(beam)
            position = b.body.position
            explosion = Explosion(position, self.resource.screen, self.resource.explosions_images)
            self.resource.explosions.append(explosion)  # Lưu vào danh sách hiệu ứng
            for poly in poly_to_remove:
                if poly in self.resource.columns:
                    self.resource.columns.remove(poly)
                if poly in self.resource.beams:
                    self.resource.beams.remove(poly)
            self.resource.space.remove(b, b.body)
            global score
            self.resource.score += 5000
        # return False  # Trả về False để không có tác động sau va chạm


    def post_solve_pig_wood(self,arbiter, space, _):
        """Collision between pig and wood"""
        pigs_to_remove = []
        if arbiter.total_impulse.length > 700:
            pig_shape, wood_shape = arbiter.shapes
            for pig in self.resource.pigs:
                if pig_shape == pig.shape:
                    pig.life -= 10
                    global score
                    self.resource.score += 10000
                    if pig.life <= 0:
                        pigs_to_remove.append(pig)
                        position = pig_shape.body.position
                        explosion = Explosion(position, self.resource.screen, self.resource.explosions_images)
                        self.resource.explosions.append(explosion)  # Lưu vào danh sách hiệu ứng
        for pig in pigs_to_remove:
            self.resource.space.remove(pig.shape, pig.shape.body)
            self.resource.pigs.remove(pig)

