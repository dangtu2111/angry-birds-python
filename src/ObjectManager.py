


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
                    pig.life -= 10
                    global score
                    self.resource.score += 10000
                    if pig.life <= 0:
                        pigs_to_remove.append(pig)
        for pig in pigs_to_remove:
            self.resource.space.remove(pig.shape, pig.shape.body)
            self.resource.pigs.remove(pig)

