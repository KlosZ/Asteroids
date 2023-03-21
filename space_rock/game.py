import pygame
from space_rock.models.asteroid import Asteroid
from space_rock.models.bonuses import ExtraHeart
from space_rock.models.spaceship import Spaceship
from space_rock.models.ufo import Ufo
from space_rock.utils import load_sprite, get_random_position, print_text, load_sound, WIDTH, HEIGHT


class InputBox:
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.font = pygame.font.Font(None, 40)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.is_written = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.is_written = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, surface):
        surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(surface, self.color, self.rect, 2)


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    ASTEROID_COUNT = 6

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Asteroids!")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.player_nickname = self._get_nickname(self.screen, self.clock)  # - игровой вариант
        # self.player_nickname = "krutoi"                                     - для тестов вариант

        self.background = load_sprite("space", False)
        self._create_sounds()

        self.level_changing = self.clock.get_time()
        self.is_level_changing = False
        self.level = 1

        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.score = "0"

        self.extra_heart_bonus = None

        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        self.asteroids = []
        self.ufos = []
        self.hit_areas = []
        self.__create_asteroids()

    @staticmethod
    def _get_nickname(screen, clock):
        screen.fill((30, 30, 30))
        x, y = screen.get_size()
        x /= 2
        y /= 2
        input_box = InputBox(x - 100, y + 40, 140, 32)
        done = False
        print_text(screen, "Input nickname below", input_box.font)

        while not done and not input_box.is_written:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                input_box.handle_event(event)
            input_box.update()
            input_box.draw(screen)
            pygame.display.flip()
            clock.tick(60)
        return input_box.text

    def _create_sounds(self):
        self.mission_start_sound = load_sound("mission_start")
        self.mission_start_sound.set_volume(0.5)
        self.mission_start_sound.play()
        self.background_sound = load_sound("bg")
        self.background_sound.set_volume(0.1)
        self.background_sound.play(-1)

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _write_score(self):
        with open("cache_records_table.txt", "a", encoding="utf-8") as f:
            f.write(f"{self.player_nickname} - {self.score}\n")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self._write_score()
                quit()
            elif self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.spaceship.shoot()
            elif self._restart_game_checker(event):
                self._write_score()
                self.__init__()
        is_key_pressed = pygame.key.get_pressed()
        if self.spaceship:
            self.spaceship.handle_input(is_key_pressed)

    def _restart_game_checker(self, event):
        return True if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.message else False

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        for ufo in self.ufos[:]:
            ufo.update(self)

        for area in self.hit_areas[:]:
            area.update(self)

        for bullet in self.bullets[:]:
            bullet.update(self)

        if self.spaceship:
            self.spaceship.update(self)
        else:
            self.background_sound.stop()
            self.message = "You lost!"

        if self.extra_heart_bonus:
            self.extra_heart_bonus.update(self)

        if not self.asteroids and self.spaceship:
            self.message = "You won!"
            self.change_level()

    def change_level(self):
        if not self.is_level_changing:
            self.level_changing = 5000
            self.is_level_changing = True
        if self.is_level_changing:
            self.level_changing -= self.clock.get_time()
        if self.is_level_changing and 0 >= self.level_changing:
            self.message = ""
            self.ufos = [Ufo((200, 300))]
            self.is_level_changing = False
            self.level += 1
            self.extra_heart_bonus = ExtraHeart(get_random_position(self.screen))
            if self.level >= 3:
                self.ASTEROID_COUNT += 1
            self.__create_asteroids()

    def _get_game_objects(self):
        game_objects = [*self.hit_areas, *self.ufos, *self.asteroids, *self.bullets]
        if self.extra_heart_bonus:
            game_objects.append(self.extra_heart_bonus)
        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects

    def _draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        if self.message:
            print_text(self.screen, self.message, self.font)
        print_text(self.screen, self.score, self.font, (WIDTH, 80))
        pygame.display.flip()
        self.clock.tick(60)

    def __create_asteroids(self):
        self.asteroids.append(Asteroid(pygame.Vector2(WIDTH / 2, HEIGHT + 50), self.asteroids.append))

    def _create_asteroids(self):
        for _ in range(self.ASTEROID_COUNT):
            while True:
                position = get_random_position(self.screen)
                if position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE:
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append))
