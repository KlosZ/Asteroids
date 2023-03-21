from space_rock.models.game_object import GameObject
from space_rock.utils import load_sprite


class HitArea(GameObject):
    HIT_DELAY = 3000
    EXPLODE_RADIUS = 80

    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("black_hole"), velocity)
        self.hit_delay = self.HIT_DELAY

    def update(self, game):
        self.hit_delay -= game.clock.get_time()
        if self.hit_delay < 0:
            self.detonate(game)
            game.hit_areas.remove(self)

    def detonate(self, game):
        if self.position.distance_squared_to(game.spaceship.position) < self.EXPLODE_RADIUS * self.EXPLODE_RADIUS:
            game.spaceship.hp_down(game)
