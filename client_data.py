from gametools.vector2 import Vector2 as vec2
import math

class ClientData(object):

    def __init__(self, id, position=(0, 0), orientation=0, health=100, delta=0):
        self.id = id
        self.pos = vec2(*position)
        self.orientation = orientation
        self.health = health

        self.CLIENT_AGE = delta

        self.rotation_speed = 0.1
        self.speed = 5

    def update(self, form_input):
        # [w, a, s, d, SPACE]
        if form_input[1]: self.orientation += self.rotation_speed
        if form_input[3]: self.orientation -= self.rotation_speed

        if self.orientation > math.pi *  2: self.orientation -= math.pi * 2
        if self.orientation < math.pi * -2: self.orientation += math.pi * 2

        if form_input[0]: self.pos += vec2(math.cos(self.orientation),
                                           -math.sin(self.orientation)) * self.speed

        if form_input[2]: self.pos -= vec2(math.cos(self.orientation),
                                           -math.sin(self.orientation)) * (self.speed / 2)

    def get_transmit_data(self):
        return (self.pos.x, self.pos.y, self.orientation, self.health)
