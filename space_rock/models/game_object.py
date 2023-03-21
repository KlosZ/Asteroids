from pygame.math import Vector2
from space_rock.utils import wrap_position

UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        """
        :param position: The center of the object
        :param sprite: The image used to draw this object
        :param velocity: Updates the position of the object each frame
        """
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def update(self, game):
        pass

    def collides_with(self, other_obj):
        return self.position.distance_squared_to(other_obj.position) < (self.radius + other_obj.radius) * (
                self.radius + other_obj.radius)
