from gametools.vector2 import Vector2 as vec2

class Entity(object):

    def __init__(self, position, velocity, orientation):
        self.position = vec2(*position)
        self.velocity = vec2(*velocity)
        self.orientation = orientation
