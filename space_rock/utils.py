from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame import Color
from pathlib import Path
import random

HEIGHT = 600
WIDTH = 800


def load_sprite(name, with_alpha=True):
    loaded_sprite = load(Path(Path.cwd(), 'assets', 'sprites', f'{name}.png'))
    return loaded_sprite.convert_alpha() if with_alpha else loaded_sprite.convert()


def load_sound(name):
    return Sound(Path(Path.cwd(), 'assets', 'sounds', f'{name}.mp3'))


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)


def get_random_position(surface):
    return Vector2(random.randrange(surface.get_width()), random.randrange(surface.get_height()))


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def print_text(surface, text, font, position="center", color=Color("tomato")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size() if position == "center" else position) / 2
    surface.blit(text_surface, rect)
