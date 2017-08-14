from gametools.vector2 import Vector2 as vec2

class Camera(object):
    """The Camera class will keep it's object centered on the screen.
    Once a camera is created, each thing that needs to be rendered in
    relation to the center object needs to render at the location given
    by get_adjusted_coords with the input their in-game world position."""

    def __init__(self, ob, screen_size):
        """Basic initialization. ob is the object we want to keep center.
        It needs to have a pos variable that is a vector2 instance that
        stores it's position in relation to the world.
        
        screen_size is just the size of the screen (so it knows where to
        center)."""

        self.ob = ob
        self.screen_size = screen_size

    def get_adjusted_coords(self, coord):
        """By passing in a tuple of coordinates or a vector2 instance into
        coord, we can draw it in relation to the main object."""

        center_x = self.screen_size[0] / 2
        center_y = self.screen_size[1] / 2

        return vec2(*coord) + vec2(center_x, center_y) - self.ob.pos


