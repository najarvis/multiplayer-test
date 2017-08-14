import math
import pygame
from gametools.vector2 import Vector2 as vec2

class Player(object):

    def __init__(self, pos=(0,0)):
        self.pos = vec2(*pos)
        self.vel = vec2()
        self.acceleration = 0.1
        self.max_speed = 10

        self.orientation = 0

        self.health = 100
        self.base_img = pygame.image.load("res/player_ships/PlayerShip1.png").convert_alpha()

        self.max_reload = 0.25
        self.reload_timer = 0

    @classmethod
    def create_other(cls, data):
        to_return = cls()
        to_return.pos = vec2(data[0], data[1])
        to_return.orientation = data[2]
        to_return.health = data[3]
        return to_return

    def update(self, data):
        self.pos.x = data[0]
        self.pos.y = data[1]
        self.orientation = data[2]
        self.health = max(0, data[3])

    def render(self, surface, camera):
        self.img = pygame.transform.rotate(self.base_img, math.degrees(self.orientation))
        self.rect = self.img.get_rect()
        self.rect.center = camera.get_adjusted_coords(self.pos)

        surface.blit(self.img, self.rect)

def vec_to_int(vec):
    return (int(vec.x), int(vec.y))
