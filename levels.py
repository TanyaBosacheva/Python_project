from snake import *

def start_screen(screen):  # рисуем заставку
    size = width, height = (600, 400)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    GREEN = (0, 51, 51)
    pygame.display.set_caption("Game snake")
    image(screen)
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
    screen = pygame.display.set_mode((900, 650))
    clock = pygame.time.Clock()
    background_image = pygame.image.load("zas1.jpg").convert()
    entities, total_level_width, total_level_height, proverka = prep()
    camera = Camera(camera_configure, total_level_width, total_level_height)
    while True:
        snake.change_to = game.event_loop(snake.change_to)
        snake.validate_direction_and_change()
        game.score, food.food_pos = snake.snake_body_mechanism(game.score, food.food_pos, game.screen_width,
                                                               game.screen_height)
        snake.change_head_position3(game.play_surface, game.score)
        screen.blit(background_image, (0, 0))
        snake.draw_snake(game.play_surface, game.black)
        food.draw_food(game.play_surface)
        snake.check_for_boundaries(game.game_over, game.screen_width, game.screen_height)
        game.show_score()
        for e in entities: # для работы методов камеры update и apply
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(50)


WIN_WIDTH = 900
WIN_HEIGHT = 650


size = width, height = (600, 400)
screen = pygame.display.set_mode(size)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("play.mp3")
pygame.mixer.music.play()
pygame.mixer.music.play(loops=-1) # бесконечное проигрывание музыки
pygame.mixer.music.get_busy() # проверка, что музыка играет
start_screen(screen)
while pygame.event.wait().type != pygame.QUIT:
    pygame.display.flip()
pygame.quit()