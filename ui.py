import pygame

class UI(object):

    def __init__(self, player):
        self.player = player

    def render(self, surface):
        w, h = surface.get_size()

        # Draw health bar
        pygame.draw.rect(surface, (255, 0, 0), (20, h - 70, 100, 50))
        pygame.draw.rect(surface, (0, 255, 0), (20, h - 70, self.player.health, 50))
