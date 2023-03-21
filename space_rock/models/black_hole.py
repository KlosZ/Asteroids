from space_rock.models.game_object import GameObject
from space_rock.models.asteroid import Asteroid
from space_rock.utils import load_sprite, HEIGHT, WIDTH, get_random_velocity, wrap_position
from pygame.math import Vector2
from pygame.transform import rotozoom
from math import copysign

UP = Vector2(0, -1)


class BlackHole(GameObject):
    VOID_SIZE = 200

    def __init__(self, position):
        super().__init__(position, load_sprite("black_hole"), get_random_velocity(1, 3))

    def draw(self, surface):
        rotated_surface = rotozoom(self.sprite, 0, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def update(self, game):
        for asteroid in game.asteroids:
            self.changeVelocity(asteroid)

    def changeVelocity(self, asteroid: Asteroid):
        dx = self.position.x - asteroid.position.x
        if abs(dx) > (WIDTH - abs(dx)):
            dx = copysign(WIDTH - abs(dx), -dx)

        dy = self.position.y - asteroid.position.y
        if abs(dy) > (HEIGHT - abs(dy)):
            dy = copysign(HEIGHT - abs(dy), -dy)

        if dx * dx + dy * dy < 200 * 200:
            if dx != 0 and dy != 0:
                asteroid.velocity += Vector2(dx, dy).normalize() / 20
