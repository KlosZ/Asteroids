from space_rock.models.game_object import GameObject
from space_rock.utils import load_sprite
from pygame.math import Vector2


class ExtraHeart(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("extra_heart"), Vector2(0))

    def update(self, game):
        if self.collides_with(game.spaceship) and game.spaceship.health < 5:
            game.spaceship.health += 1
