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
        self.life = 100
        mass = 50
        radius = 40
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
        self.state=0
        self.image = [
            pygame.image.load(
            "./resources/images/boss/01.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/02.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/03.png").convert_alpha(),
        ]
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
            "./resources/images/boss/04.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/05.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/06.png").convert_alpha(),
            ]
        elif state==2:
            self.image = [
            pygame.image.load(
            "./resources/images/boss/07.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/08.png").convert_alpha(),
            pygame.image.load(
            "./resources/images/boss/09.png").convert_alpha(),
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
    