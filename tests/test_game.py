from unittest import TestCase, main
from space_rock.game import SpaceRocks


class GameTest(TestCase):
    def test_asteroids_count_on_start(self):
        s = SpaceRocks()
        self.assertEqual(len(s._get_game_objects()), s.ASTEROID_COUNT + 1)  # spaceship (lvl 1)

    def test_destroyed_asteroids(self):
        s = SpaceRocks()
        s.asteroids = []
        s._process_game_logic()
        self.assertEqual(s.message, "You won!")

    def test_destroyed_ship(self):
        s = SpaceRocks()
        s.spaceship = None
        s._process_game_logic()
        self.assertEqual(s.message, "You lost!")


if __name__ == '__main__':
    main()
