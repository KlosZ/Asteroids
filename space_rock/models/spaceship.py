from space_rock.models.game_object import GameObject
from space_rock.models.bullet import Bullet
from space_rock.utils import load_sprite, load_sound
from pygame.math import Vector2
from pygame.transform import rotozoom
import pygame

UP = Vector2(0, -1)


class Spaceship(GameObject):
    MANEUVERABILITY = 4
    ACCELERATION = 0.2
    BULLET_SPEED = 5
    MAX_SPEED = 10
    MAX_HEALTH = 5
    EXPLOSION_RADIUS = 100

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self._create_sounds_spaceship()
        self.direction = Vector2(UP)
        self.health = self.MAX_HEALTH
        self.invincibility = 0
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def _create_sounds_spaceship(self):
        self.laser_sound = load_sound("shoot")
        self.laser_sound.set_volume(0.2)
        self.destruction_sound = load_sound("boom")
        self.destruction_sound.set_volume(2)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def slow_down(self):
        if self.velocity.length_squared() != 0:
            velocity = self.velocity - self.velocity.normalize() * self.ACCELERATION
            self.velocity = velocity if velocity.length_squared() > 2 else self.velocity

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        surface.blit(load_sprite(f"hearts/hearts_{self.health}"), (40, 40))

    def handle_input(self, is_key_pressed):
        if is_key_pressed[pygame.K_RIGHT]:
            self.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.rotate(clockwise=False)
        if is_key_pressed[pygame.K_UP]:
            self.accelerate()
        if is_key_pressed[pygame.K_DOWN]:
            self.slow_down()

    def update(self, game):
        if self.invincibility > 0:
            self.invincibility -= game.clock.get_time()
        else:
            self.collide_with_asteroids(game)

    def set_invincibility(self, ticks):
        self.invincibility += ticks

    def collide_with_asteroids(self, game):
        for asteroid in game.asteroids:
            if asteroid.collides_with(self):
                self.hp_down(game)
                break

    def hp_down(self, game):
        if self.invincibility <= 0:
            self.destruction_sound.play()
            self.health -= 1
            self.set_invincibility(400)
            destroy_near(game, self)
            if self.health == 0:
                game.spaceship = None


def destroy_near(game, spaceship: Spaceship):
    for asteroid in list(game.asteroids):
        if asteroid.position.distance_squared_to(
                spaceship.position) < spaceship.EXPLOSION_RADIUS * spaceship.EXPLOSION_RADIUS:
            asteroid.split()
            game.asteroids.remove(asteroid)
