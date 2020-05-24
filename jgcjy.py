import pygame
import sys
import random
import time

class Game():
    def __init__(self):     # задаем размеры экрана и необходимые цвета
        self.screen_width = 900
        self.screen_height = 650
        self.black = pygame.Color(0, 0, 0)
        self.red = pygame.Color(255, 0, 0)
        self.fon = pygame.Color(123, 104, 238)
        self.fps_controller = pygame.time.Clock() # задает количество кадров в секунду
        self.score = 0 # переменная для количества съеденной еды

    def init_and_check_for_errors(self): # функция для проверки кода и запуска игры
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print("Ok")

    def set_surface_and_title(self): # создаем холст для рисования и заголовок
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game snake")

    def event_loop(self, change_to): #отслеживание нажатий клавиш
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: # если нажал клавишу
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

    def refresh_screen(self, score): # задаем фпс
        pygame.display.flip()
        game.fps_controller.tick(25)

    def show_score(self, choice=1): # отображение результата
        s_font = pygame.font.SysFont("calibri", 46)
        s_surf = s_font.render("Score: {0}".format(self.score), True, self.fon)
        s_rect = s_surf.get_rect()
        if choice == 1: # отображаем результат слева сверху
            s_rect.midtop = (80, 10)
        else: # при game overe отображаем результат по центру под надписью game over
            s_rect.midtop = (450, 100)
        self.play_surface.blit(s_surf, s_rect) # рисуем прямоугольник поверх surface

    def game_over(self): # вывода надписи Game Over и результатов в случае завершения игры и выход из игры
        go_font = pygame.font.SysFont("monaco", 72)
        go_surf = go_font.render("Game over", True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (450, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            pass
        pygame.quit()
        sys.exit()

class Snake():
    def __init__(self, snake_color):
        self.snake_head_pos = [100, 50]  # [x, y] важные переменные - позиция головы змеи и его тела
        self.snake_body = [[100, 50], [90, 50]] # начальное тело змеи
        self.snake_color = snake_color
        self.direction = "RIGHT" # начальное направление движения
        self.change_to = self.direction  # куда будет меняться напрвление движения змеи при нажатии соответствующих клавиш

    def validate_direction_and_change(self): # зменияем направление движения змеи только в том случае, если оно не прямо противоположно текущему
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT", self.change_to == "LEFT" and not self.direction == "RIGHT",
            self.change_to == "UP" and not self.direction == "DOWN", self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self): #Изменияем положение головы змеи
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos)) # увеличение змеи
        if (self.snake_head_pos[0] == food_pos[0] and  self.snake_head_pos[1] == food_pos[1]): # если съели еду
            food_pos = [random.randrange(1, screen_width/10)*10, random.randrange(1, screen_height/10)*10]   # если съели еду то задаем новое положение еды случайным
            score += 1
        else:
            self.snake_body.pop() # если не нашли еду, то убираем последний сегмент
        return score, food_pos

    def draw_snake(self, play_surface, surface_color): # Отображаем все сегменты змеи
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(play_surface, self.snake_color, pygame.Rect(pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, game_over, screen_width, screen_height): # Проверка, что столкунлись с концами экрана или сами с собой
        if any((self.snake_head_pos[0] > screen_width-10 or self.snake_head_pos[0] < 0, self.snake_head_pos[1] > screen_height - 10 or self.snake_head_pos[1] < 0)):
            # pygame.mixer.music.stop()
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and block[1] == self.snake_head_pos[1]):# проверка на то, что первый элемент(голова) врезался в любой другой элемент змеи (закольцевались)
                # pygame.mixer.music.stop()
                game_over()

class Food():
    def __init__(self, food_color, screen_width, screen_height):
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width/10)*10, random.randrange(1, screen_height/10)*10]

    def draw_food(self, play_surface): # Отображение еды
        pygame.draw.rect(play_surface, self.food_color, pygame.Rect(self.food_pos[0], self.food_pos[1],self.food_size_x, self.food_size_y))

size = width, height = (600, 400)
screen = pygame.display.set_mode(size)
pygame.init()

def start_screen(): # рисуем заставку
    screen.fill((0, 0, 0))
    pygame.display.set_caption("Game snake")
    font = pygame.font.SysFont("monaco", 35)
    screen.blit(font.render("Привет! Давай начнем игру!", True, (123, 104, 238)), (150, 40))
    pygame.draw.rect(screen, (0, 51, 51), (130, 30, 370, 50), 1)
    level_1 = pygame.draw.rect(screen, (0, 51, 51), (250, 90, 130, 40))
    screen.blit(font.render("Легкий", True, (255, 0, 0)), (275, 100, 100, 40))
    level_2 = pygame.draw.rect(screen, (0, 51, 51), (250, 150, 130, 40))
    screen.blit(font.render("Средний", True, (255, 0, 0)), (260, 160, 100, 40))
    level_3 = pygame.draw.rect(screen, (0, 51, 51), (250, 210, 130, 40))
    screen.blit(font.render("Сложный", True, (255, 0, 0)), (260, 220, 100, 40))
    rules = pygame.draw.rect(screen, (0, 51, 51), (250, 270, 130, 40))
    screen.blit(font.render("Правила", True, (255, 0, 0)), (260, 280, 100, 40))
    exit = pygame.draw.rect(screen, (0, 51, 51), (250, 330, 130, 40))
    screen.blit(font.render("Выход", True, (255, 0, 0)), (275, 340, 100, 40))

start_screen()
while pygame.event.wait().type != pygame.QUIT:
    pygame.display.flip()
pygame.quit()


game = Game()

'''
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048) # инициализация звуковой системы
pygame.mixer.music.load("Play.wav")
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)
'''



snake = Snake(game.fon)
food = Food(game.red, game.screen_width, game.screen_height)
game.init_and_check_for_errors()
game.set_surface_and_title()
while True:
    snake.change_to = game.event_loop(snake.change_to)
    snake.validate_direction_and_change()
    snake.change_head_position()
    game.score, food.food_pos = snake.snake_body_mechanism(game.score, food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.play_surface, game.black)
    food.draw_food(game.play_surface)
    snake.check_for_boundaries(game.game_over, game.screen_width, game.screen_height)
    game.show_score()
    game.refresh_screen(game.score)