import math
import pygame
from gametools.vector2 import Vector2 as vec2

class Player(object):

    def __init__(self, pos=(0,0)):
        self.pos = vec2(*pos)
        self.orientation = 0
        self.size = 64
        # self.color = (255, 255, 255)
        self.health = 100
        self.base_img = pygame.image.load("res/player_ships/PlayerShip1.png").convert_alpha()
        # self.img.fill(self.color)

    def update(self, data):
        self.pos.x = data[0]
        self.pos.y = data[1]
        self.orientation = data[2]
        self.health = max(0, data[3])

        self.img = pygame.transform.rotate(self.base_img, math.degrees(self.orientation))
        self.rect = self.img.get_rect()
        self.rect.center = self.pos

    def render(self, surface):
        # pygame.draw.circle(surface, self.color, vec_to_int(self.pos), self.size // 2)
        surface.blit(self.img, self.rect)

def vec_to_int(vec):
    return (int(vec.x), int(vec.y))
