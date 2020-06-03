import pygame
import sys
import random
import time


class Game():
    def __init__(self):  # задаем размеры экрана и необходимые цвета
        self.screen_width = 900
        self.screen_height = 650
        self.black = pygame.Color(0, 0, 0)
        self.red = pygame.Color(255, 0, 0)
        self.fon = pygame.Color(123, 104, 238)
        self.fps_controller = pygame.time.Clock()  # задает количество кадров в секунду
        self.score = 0  # переменная для количества съеденной еды

    def init_and_check_for_errors(self):  # функция для проверки кода и запуска игры
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print("Ok")

    def set_surface_and_title(self):  # создаем холст для рисования и заголовок
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game snake")

    def event_loop(self, change_to):  # отслеживание нажатий клавиш
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # если нажал клавишу
                if event.key == pygame.K_RIGHT or event.key == ord("d"):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord("a"):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord("w"):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord("s"):
                    change_to = "DOWN"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to

    def show_score(self, choice=1):  # отображение результата
        s_font = pygame.font.SysFont("calibri", 46)
        s_surf = s_font.render("Score: {0}".format(self.score), True, self.fon)
        s_rect = s_surf.get_rect()
        if choice == 1:  # отображаем результат слева сверху
            s_rect.midtop = (80, 10)
        else:  # при game overe отображаем результат по центру под надписью game over
            s_rect.midtop = (450, 100)
        self.play_surface.blit(s_surf, s_rect)  # рисуем прямоугольник поверх surface

    def game_over(self):  # вывода надписи Game Over и результатов в случае завершения игры и выход из игры
        go_font = pygame.font.SysFont("monaco", 72)
        go_surf = go_font.render("Game over", True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (450, 15)
        GREEN = (0, 51, 51)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        restart = pygame.Rect(310, 350, 300, 60)
        pygame.draw.rect(screen, GREEN, restart)
        screen.blit(go_font.render("Повторить", True, (0, 191, 255)), (330, 360, 100, 40))
        exit = pygame.Rect(310, 420, 300, 60)
        pygame.draw.rect(screen, GREEN, exit)
        screen.blit(go_font.render("Выход", True, (0, 191, 255)), (375, 430, 100, 40))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if restart.collidepoint(mouse_pos):
                        pygame.mixer.music.unpause()
                        pygame.display.flip()
                        start_screen()

                    if exit.collidepoint(mouse_pos):
                        sys.exit()
            pygame.display.update()
            pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            pass
        pygame.quit()
        sys.exit()


class Snake():
    def __init__(self, snake_color):
        self.snake_head_pos = [100, 50]  # позиция головы змеи и его тела
        self.snake_body = [[100, 50], [90, 50]]  # начальное тело змеи
        self.snake_color = snake_color
        self.direction = "RIGHT"  # начальное направление движения
        self.change_to = self.direction  # куда будет меняться напрвление движения змеи при нажатии соответствующих клавиш

    def validate_direction_and_change(self):  # заменияем направление движения змеи только в том случае, если оно не прямо противоположно текущему
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):  # Изменияем положение головы змеи
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))  # увеличение змеи
        if (self.snake_head_pos[0] == food_pos[0] and self.snake_head_pos[1] == food_pos[1]):  # если съели еду
            food_pos = [random.randrange(1, screen_width / 10) * 10, random.randrange(1, screen_height / 10) * 10]  # если съели еду то задаем новое положение еды случайным
            score += 1
        else:
            self.snake_body.pop()  # если не нашли еду, то убираем последний сегмент
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):  # Отображаем все сегменты змеи
        for pos in self.snake_body:
            pygame.draw.rect(play_surface, self.snake_color, pygame.Rect(pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, game_over, screen_width, screen_height):  # Проверка, что столкунлись с концами экрана или сами с собой
        if any((self.snake_head_pos[0] > screen_width - 10 or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height - 10 or self.snake_head_pos[1] < 0)):
            pygame.mixer.music.pause()
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and block[1] == self.snake_head_pos[1]):  # проверка на то, что первый элемент(голова) врезался в любой другой элемент змеи (закольцевались)
                pygame.mixer.music.pause()
                game_over()


class Food():
    def __init__(self, food_color, screen_width, screen_height):
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width / 10) * 10, random.randrange(1, screen_height / 10) * 10]

    def draw_food(self, play_surface):  # Отображение еды
        pygame.draw.rect(play_surface, self.food_color,
                         pygame.Rect(self.food_pos[0], self.food_pos[1], self.food_size_x, self.food_size_y))


def start_screen():  # рисуем заставку
    size = width, height = (600, 400)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    GREEN = (0, 51, 51)
    pygame.display.set_caption("Game snake")
    image()
    font = pygame.font.SysFont("monaco", 35)
    screen.blit(font.render("Привет! Давай начнем игру!", True, (0, 191, 255)), (130, 40))
    pygame.draw.rect(screen, (0, 191, 255), (115, 30, 370, 50), 1)
    level_1 = pygame.Rect(235, 90, 130, 40)
    pygame.draw.rect(screen, GREEN, level_1)
    screen.blit(font.render("Легкий", True, (0, 191, 255)), (260, 100, 100, 40))
    level_2 = pygame.Rect(235, 150, 130, 40)
    pygame.draw.rect(screen, GREEN, level_2)
    screen.blit(font.render("Средний", True, (0, 191, 255)), (245, 160, 100, 40))
    level_3 = pygame.Rect(235, 210, 130, 40)
    pygame.draw.rect(screen, GREEN, level_3)
    screen.blit(font.render("Сложный", True, (0, 191, 255)), (245, 220, 100, 40))
    rules = pygame.Rect(235, 270, 130, 40)
    pygame.draw.rect(screen, GREEN, rules)
    screen.blit(font.render("Правила", True, (0, 191, 255)), (250, 280, 100, 40))
    exit = pygame.Rect(235, 330, 130, 40)
    pygame.draw.rect(screen, GREEN, exit)
    screen.blit(font.render("Выход", True, (0, 191, 255)), (260, 340, 100, 40))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if level_1.collidepoint(mouse_pos):
                    pygame.display.flip()
                    uroven1()

                if level_2.collidepoint(mouse_pos):
                    pygame.display.flip()
                    uroven2()

                if level_3.collidepoint(mouse_pos):
                    pygame.display.flip()
                    uroven3()

                if rules.collidepoint(mouse_pos):
                    pygame.display.flip()
                    rules_1()

                if exit.collidepoint(mouse_pos):
                    sys.exit()

        pygame.display.update()
        pygame.display.flip()


def uroven1():
    game = Game()
    snake = Snake(game.fon)
    food = Food(game.red, game.screen_width, game.screen_height)
    game.init_and_check_for_errors()
    game.set_surface_and_title()
    screen = pygame.display.set_mode((900, 650))
    clock = pygame.time.Clock()
    background_image = pygame.image.load("zas1.jpg").convert()
    while True:
        snake.change_to = game.event_loop(snake.change_to)
        snake.validate_direction_and_change()
        snake.change_head_position()
        game.score, food.food_pos = snake.snake_body_mechanism(game.score, food.food_pos, game.screen_width,
                                                               game.screen_height)
        screen.blit(background_image, (0, 0))
        snake.draw_snake(game.play_surface, game.black)
        food.draw_food(game.play_surface)
        snake.check_for_boundaries(game.game_over, game.screen_width, game.screen_height)
        game.show_score()
        pygame.display.update()
        clock.tick(20)


def uroven2():
    game = Game()
    snake = Snake(game.fon)
    food = Food(game.red, game.screen_width, game.screen_height)
    game.init_and_check_for_errors()
    game.set_surface_and_title()
    screen = pygame.display.set_mode((900, 650))
    clock = pygame.time.Clock()
    background_image = pygame.image.load("zas1.jpg").convert()
    while True:
        snake.change_to = game.event_loop(snake.change_to)
        snake.validate_direction_and_change()
        snake.change_head_position()
        game.score, food.food_pos = snake.snake_body_mechanism(game.score, food.food_pos, game.screen_width,
                                                               game.screen_height)
        screen.blit(background_image, (0, 0))
        snake.draw_snake(game.play_surface, game.black)
        food.draw_food(game.play_surface)
        snake.check_for_boundaries(game.game_over, game.screen_width, game.screen_height)
        game.show_score()
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(40)


def uroven3():
    game = Game()
    snake = Snake(game.fon)
    food = Food(game.red, game.screen_width, game.screen_height)
    game.init_and_check_for_errors()
    game.set_surface_and_title()
    entities, total_level_width, total_level_height = prep()
    camera = Camera(camera_configure, total_level_width, total_level_height)
    while True:
        snake.change_to = game.event_loop(snake.change_to)
        snake.validate_direction_and_change()
        snake.change_head_position()
        game.score, food.food_pos = snake.snake_body_mechanism(game.score, food.food_pos, game.screen_width,
                                                               game.screen_height)
        snake.draw_snake(game.play_surface, game.black)
        food.draw_food(game.play_surface)
        snake.check_for_boundaries(game.game_over, game.screen_width, game.screen_height)
        game.show_score()
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(60)


WIN_WIDTH = 900
WIN_HEIGHT = 650


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


PLATFORM_WIDTH = 10
PLATFORM_HEIGHT = 10


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill((0, 100, 0))
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


def prep():
    size = width, height = (900, 660)
    screen = pygame.display.set_mode(size)
    bg = pygame.Surface((width, height))
    bg.fill((0, 0, 0))
    entities = pygame.sprite.Group()  # Все объекты
    level = [
        "------------------------------------------------------------------------------------------",
        "-                                                                      ---               -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                ----                    -",
        "--                                                                                       -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-               ---                                                                      -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                     ---                                -",
        "-                                                                                       --",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                      ---                                               -",
        "-                                                                                        -",
        "-                                                                      ---               -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-            --                                                                          -",
        "-                                                                                        -",
        "--                                                                                       -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                       --",
        "-                                        ----                                            -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-     --                                                                                 -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                ----                    -",
        "--                                                                                       -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-               ---                                                                      -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                       --",
        "-                                         ---                                            -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-     --                                                          ---                    -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                       --",
        "-                                         ---                                            -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-                                                                                        -",
        "-     --                                                                                 -",
        "-                                                                                        -",
        "------------------------------------------------------------------------------------------"]
    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":  # создаем блок, заливаем его цветом и рисеум его
                pf = Platform(x, y)
                entities.add(pf)
            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_WIDTH  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

        total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
        total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

        camera = Camera(camera_configure, total_level_width, total_level_height)
    return entities, total_level_width, total_level_height


def image():
    fon = pygame.image.load("zas2.jpg")
    fon_top = screen.get_height() - fon.get_height()
    fon_left = screen.get_width() / 2 - fon.get_width() / 2
    screen.blit(fon, (fon_left, fon_top))
    pygame.display.update()


def rules_1():
    size = width, height = (600, 400)
    screen = pygame.display.set_mode(size)
    GREEN = (0, 51, 51)
    pygame.display.set_caption("Game snake")
    image()
    font = pygame.font.SysFont("monaco", 25)
    r = pygame.Rect(30, 30, 540, 310)
    pygame.draw.rect(screen, GREEN, r)
    text = font.render("Игрок управляет длинным, тонким существом, напоминающим", True, (0, 191, 255))
    text2 = font.render("змею, которое ползает по плоскости, ограниченной стенками,", True, (0, 191, 255))
    text3 = font.render("собирая еду, избегая столкновения с собственным хвостом и", True, (0, 191, 255))
    text4 = font.render("краями игрового поля. В самом сложном уровне на поле", True, (0, 191, 255))
    text5 = font.render("присутствуют дополнительные препятствия. Каждый раз,", True, (0, 191, 255))
    text6 = font.render("когда змея съедает кусок пищи, она становится длиннее,", True, (0, 191, 255))
    text7 = font.render("что постепенно усложняет игру. Игрок управляет направлением", True, (0, 191, 255))
    text8 = font.render("движения головызмеи (есть 4 направления: вверх, вниз, влево,", True, (0, 191, 255))
    text9 = font.render("вправо), а хвост змеи движется следом. Игрок не может", True, (0, 191, 255))
    text10 = font.render("остановить движение змеи.", True, (0, 191, 255))
    screen.blit(text, (40, 40, 520, 40))
    screen.blit(text2, (45, 70, 520, 40))
    screen.blit(text3, (45, 100, 520, 40))
    screen.blit(text4, (65, 130, 520, 40))
    screen.blit(text5, (60, 160, 520, 40))
    screen.blit(text6, (60, 190, 520, 40))
    screen.blit(text7, (40, 220, 520, 40))
    screen.blit(text8, (40, 250, 520, 40))
    screen.blit(text9, (70, 280, 520, 40))
    screen.blit(text10, (190, 310, 520, 40))
    exit = pygame.Rect(250, 350, 130, 40)
    pygame.draw.rect(screen, GREEN, exit)
    screen.blit(font.render("Вернуться", True, (0, 191, 255)), (275, 360, 100, 40))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if exit.collidepoint(mouse_pos):
                    pygame.display.flip()
                    start_screen()
        pygame.display.update()
        pygame.display.flip()

size = width, height = (600, 400)
screen = pygame.display.set_mode(size)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("play.mp3")
pygame.mixer.music.play()
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.get_busy()
start_screen()
while pygame.event.wait().type != pygame.QUIT:
    pygame.display.flip()
pygame.quit()
