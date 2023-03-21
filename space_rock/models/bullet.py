from space_rock.models.game_object import GameObject
from space_rock.utils import load_sprite


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        self.position += self.velocity

    def update(self, game):
        if not game.screen.get_rect().collidepoint(self.position):
            game.bullets.remove(self)
        for asteroid in game.asteroids[:]:
            if asteroid.collides_with(self):
                game.asteroids.remove(asteroid)
                game.bullets.remove(self)
                game.score = str(int(game.score) + asteroid.size_to_score[asteroid.size])
                asteroid.split()
                break
