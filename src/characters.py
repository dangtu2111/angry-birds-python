import time
import pygame
import pymunk as pm
from pymunk import Vec2d


class Bird():
    def __init__(self, distance, angle, x, y, space,image):
        self.life = 20
        mass = 5
        radius = 12
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y
        power = distance * 53
        impulse = power * Vec2d(1, 0)
        angle = -angle
        body.apply_impulse_at_local_point(impulse.rotated(angle))
        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = 0.8
        space.damping = 0.8  # Giảm tốc nhanh hơn
        shape.friction = 0.9
        shape.collision_type = 0
        space.add(body, shape)
        self.body = body
        self.shape = shape
        self.image = image
        

class Pig():
    def __init__(self, x, y, space):
        self.life = 20
        mass = 5
        radius = 14
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y
        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 1
        space.add(body, shape)
        self.body = body
        self.shape = shape
class Boss():
    def __init__(self, x, y, space):
        self.life = 80
        mass = 100
        radius = 60
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y
        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 3
        space.add(body, shape)
        self.body = body
        self.shape = shape
        self.state=0
        self.image = [
            pygame.image.load(
            "./resources/images/boss/01.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/02.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/03.png").convert_alpha(),
        ]
        # Thiết lập các thuộc tính cho animation
        self.current_frame = 0  # Khung hình hiện tại
        self.last_update_time = time.time()  # Thời gian cập nhật hình ảnh
        self.frame_rate = 0.1  # Thời gian giữa các khung hình (0.1 giây = 10fps)
    def setState(self,state):
        if state == 0:
            self.image = [
            pygame.image.load(
            "./resources/images/boss/01.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/02.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/03.png").convert_alpha(),
            ]
            self.state=state
        elif state==1:
            self.image = [
            pygame.image.load(
            "./resources/images/boss/05.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/04.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/09.png").convert_alpha(),
            ]
        elif state==2:
            self.image = [
            pygame.image.load(
            "./resources/images/boss/06.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/07.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/08.png").convert_alpha(),
            ]
        else:
            self.image = [
            pygame.image.load(
            "./resources/images/boss/01.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/02.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/03.png").convert_alpha(),
            ]
    def update(self):
        """Cập nhật animation theo thời gian"""
        current_time = time.time()
        
        # Nếu thời gian qua đi đủ lâu để thay đổi khung hình
        if current_time - self.last_update_time > self.frame_rate:
            self.last_update_time = current_time
            self.current_frame = (self.current_frame + 1) % len(self.image)  # Chuyển sang khung hình tiếp theo
    def to_pygame(self,p):
        """Convert pymunk to pygame coordinates"""
        return int(p.x), int(-p.y+600)  
    def render(self, screen):
        """Vẽ animation lên màn hình"""
        p = self.to_pygame(self.body.position)
        x, y = p
        w,h = self.image[self.current_frame].get_size()
        x -= w*0.5
        y -= h*0.6
        screen.blit(self.image[self.current_frame], (x, y))