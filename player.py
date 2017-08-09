import pygame

class Player(object):

    def __init__(self, pos=(0,0)):
        self.pos = pos
        self.size = 64
        self.color = (255, 255, 255)
        self.img = pygame.Surface((self.size, self.size))
        self.img.fill(self.color)

    def update(self, position):
        self.pos = position

    def render(self, surface):
        surface.blit(self.img, self.pos)
