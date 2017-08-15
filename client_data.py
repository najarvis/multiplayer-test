from gametools.vector2 import Vector2 as vec2
import math

class ClientData(object):

    def __init__(self, id, position=(0, 0), orientation=0, health=100, delta=0):
        self.id = id
        self.pos = vec2(*position)
        self.vel = vec2()

        self.acceleration = 0.15
        self.max_speed = 10

        self.orientation = orientation
        self.health = health

        self.CLIENT_AGE = delta

        self.rotation_speed = 0.1
        self.drag = 0.05

        self.speed = 5

        self.last_input = None

    def update(self, form_input):
        # [w, a, s, d, SPACE]
        if form_input[1]: self.orientation += self.rotation_speed
        if form_input[3]: self.orientation -= self.rotation_speed

        if self.orientation > math.pi *  2: self.orientation -= math.pi * 2
        if self.orientation < math.pi * -2: self.orientation += math.pi * 2

        if form_input[0]: self.vel += vec2(math.cos(self.orientation),
                                           -math.sin(self.orientation)) * self.acceleration

        if form_input[2]: self.vel -= vec2(math.cos(self.orientation),
                                           -math.sin(self.orientation)) * (self.acceleration / 2)

        self.vel = self.vel * (1-self.drag)

        if self.vel.get_magnitude() > self.max_speed:
            self.vel = self.vel.get_normalised() * self.max_speed

        self.pos += self.vel

    def get_transmit_data(self):
        return (self.pos.x, self.pos.y, self.orientation, self.health)
