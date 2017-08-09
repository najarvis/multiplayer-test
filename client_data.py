from gametools.vector2 import Vector2 as vec2

class ClientData(object):

    def __init__(self, id, position, health, delta=0):
        self.id = id
        self.pos = vec2(*position)
        self.health = health

        self.CLIENT_AGE = delta

    def get_transmit_data(self):
        return (self.pos.x, self.pos.y)
