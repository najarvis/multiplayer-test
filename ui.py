import pygame

class UI(object):

    def __init__(self, player):
        self.player = player
        self.ui_font = pygame.font.SysFont("Arial", 24)
        self.ui_font_s = pygame.font.SysFont("Arial", 12)

    def render(self, surface):
        w, h = surface.get_size()

        # Draw health bar. Red behind green.
        pygame.draw.rect(surface, (255, 0, 0), (20, h - 70, 100, 50))
        pygame.draw.rect(surface, (0, 255, 0), (20, h - 70, self.player.health, 50))

        coord_text = "Coordinates - X: {0:.0f}, Y: {1:.0f}".format(self.player.pos.x, self.player.pos.y)
        rendered_coord_text = self.ui_font.render(coord_text, True, (255, 255, 255))

        surface.blit(rendered_coord_text, (20, 20))
