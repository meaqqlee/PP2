import pygame
import sys
import random
from pygame.math import Vector2
import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname='snake_game', user='postgres', password='magzhan0201', host='localhost', port='5432'
    )

def get_user_id(username):
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cur.fetchone()
        if user_id:
            return user_id[0]
        else:
            cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
            user_id = cur.fetchone()
            conn.commit()
            return user_id[0]

def get_user_score_and_level(user_id):
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("SELECT score, level FROM user_scores WHERE user_id = %s ORDER BY id DESC LIMIT 1", (user_id,))
        result = cur.fetchone()
        if result:
            return result[0], result[1]
        else:
            return 0, 1

def save_game_state(user_id, score, level):
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO user_scores (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
        conn.commit()

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
wall = pygame.image.load('Graphics/wall.png').convert_alpha()
wall = pygame.transform.scale(wall, (40, 40))
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

username = input("Enter your username: ")
user_id = get_user_id(username)
score, level = get_user_score_and_level(user_id)

level_maps = [
    [],
    [(2, i) for i in range(2, 18)] + [(17, i) for i in range(2, 18)],
    [(i, 4) for i in range(2, 19) if i != 10] + [(i, 14) for i in range(2, 19) if i != 10] + [(4, i) for i in range(5, 14)] + [(14, i) for i in range(5, 14)]  # Уровень 3
]


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class FRUIT:
    def __init__(self, level_maps, level, snake):
        self.level_maps = level_maps
        self.level = level
        self.snake = snake
        self.pos = Vector2(0, 0)
        self.randomize()

    def randomize(self):
        while True:
            x = random.randint(0, cell_number - 1)
            y = random.randint(0, cell_number - 1)
            new_pos = Vector2(x, y)
            if new_pos not in [Vector2(wall[0], wall[1]) for wall in self.level_maps[self.level - 1]] and new_pos not in self.snake.body:
                self.pos = new_pos
                break

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

class MAIN:
    def __init__(self, user_id, level_maps):
        self.level_maps = level_maps
        self.snake = SNAKE()
        self.level = 1
        self.score = 0
        self.user_id = user_id
        self.is_game_active = False
        self.load_game_state()
        self.fruit = FRUIT(self.level_maps, self.level, self.snake)

    def load_game_state(self):
        self.score, self.level = get_user_score_and_level(self.user_id)
        print(f"Loaded game state: Level {self.level}, Score {self.score}")

    def start_game(self):
        self.is_game_active = True

    def update(self):
        if self.is_game_active:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1
            if self.score > 20 and self.level < 3:
                self.level = 3
                self.fruit.level = self.level
            elif self.score > 10 and self.level < 2:
                self.level = 2
                self.fruit.level = self.level
            self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
        for wall_pos in level_maps[self.level - 1]:
            if self.snake.body[0] == Vector2(wall_pos[0], wall_pos[1]):
                self.game_over()

    def game_over(self):
        print(f"Game over! Score: {self.score}, Level: {self.level}")
        save_game_state(self.user_id, self.score, self.level)
        pygame.quit()
        sys.exit()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_walls()
        self.draw_score()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            for col in range(cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_walls(self):
        for wall_pos in level_maps[self.level - 1]:
            wall_rect = pygame.Rect(wall_pos[0] * cell_size, wall_pos[1] * cell_size, cell_size, cell_size)
            screen.blit(wall, wall_rect)

    def draw_score(self):
        score_text = 'Score: ' + str(self.score) + ' Level: ' + str(self.level)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 90)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

main_game = MAIN(user_id, level_maps)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if not main_game.is_game_active:
                main_game.start_game()
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_l:
                main_game.fruit.randomize()
                main_game.snake.add_block()
                main_game.snake.play_crunch_sound()
                main_game.score += 1
                if main_game.score > 20 and main_game.level < 3:
                    main_game.level = 3
                elif main_game.score > 10 and main_game.level < 2:
                    main_game.level = 2

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)