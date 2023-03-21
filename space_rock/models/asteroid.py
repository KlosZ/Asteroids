from space_rock.models.game_object import GameObject
from pygame.transform import rotozoom
from space_rock.utils import load_sprite, get_random_velocity


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size
        self.size_to_scale = {3: 1, 2: 0.5, 1: 0.25}
        self.size_to_score = {i: int(200 * self.size_to_scale[i]) for i in [1, 2, 3]}
        sprite = rotozoom(load_sprite("asteroid"), 0, self.size_to_scale[size])
        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(self.position, self.create_asteroid_callback, self.size - 1)
                self.create_asteroid_callback(asteroid)
