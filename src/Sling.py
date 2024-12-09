import math
import pygame


class GameSling:
    def __init__(self,resource):
        self.x=0
        self.sling_x, self.sling_y = 135, 450
        self.sling2_x, self.sling2_y = 160, 450
        self.sling_image = pygame.image.load(
            "./resources/images/sling-3.png").convert_alpha()
        self.resource=resource
    def sling_action(self,bird_image):
        """Set up sling behavior"""
        
        # Fixing bird to the sling rope
        v = self.vector((self.sling_x, self.sling_y), (self.resource.x_mouse, self.resource.y_mouse))
        uv = self.unit_vector(v)
        self.resource.mouse_distance = self.distance(self.sling_x,self.sling_y, self.resource.x_mouse,self.resource.y_mouse)
        uv1 = uv[0]
        uv2 = uv[1]
        
        pu = (uv1*self.resource.rope_lenght+self.sling_x, uv2*self.resource.rope_lenght+self.sling_y)
        bigger_rope = 102
        x_bird = self.resource.x_mouse - 20
        y_bird = self.resource.y_mouse - 20
        if self.resource.mouse_distance > self.resource.rope_lenght:
            pux, puy = pu
            pux -= 20
            puy -= 20
            pul = pux, puy
            self.resource.screen.blit(bird_image, pul)
            pu2 = (uv1*bigger_rope+self.sling_x, uv2*bigger_rope+self.sling_y)
            pygame.draw.line(self.resource.screen, (0, 0, 0), (self.sling2_x, self.sling2_y), pu2, 5)
            self.resource.screen.blit(bird_image, pul)
            pygame.draw.line(self.resource.screen, (0, 0, 0), (self.sling_x, self.sling_y), pu2, 5)
        else:
            self.resource.mouse_distance += 10
            pu3 = (uv1*self.resource.mouse_distance+self.sling_x, uv2*self.resource.mouse_distance+self.sling_y)
            pygame.draw.line(self.resource.screen, (0, 0, 0), (self.sling2_x, self.sling2_y), pu3, 5)
            self.resource.screen.blit(bird_image, (x_bird, y_bird))
            pygame.draw.line(self.resource.screen, (0, 0, 0), (self.sling_x, self.sling_y), pu3, 5)
        # Angle of impulse
        dy = self.resource.y_mouse - self.sling_y
        dx = self.resource.x_mouse - self.sling_x
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

