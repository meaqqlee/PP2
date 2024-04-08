import pygame
import random

pygame.init()

coin_image = pygame.image.load('coin.png')
coin_image = pygame.transform.scale(coin_image, (50, 50))
car_image = pygame.image.load('car.png')
car_image = pygame.transform.scale(car_image, (100, 150))
enemy_image = pygame.image.load('enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (100, 150))
bg_image = pygame.image.load('bg.png')

window = pygame.display.set_mode((820, 630))
pygame.display.set_caption("racer")

# Classes
class Player:
    def __init__(self, x, y):  # Corrected '__init__'
        self.x = x
        self.y = y
        self.speed = 2

    def draw(self):
        window.blit(car_image, (self.x, self.y))

class Enemy:
    def __init__(self, speed):  # Corrected '__init__'
        self.x = random.randint(180, 620)
        self.y = -1 * random.randint(150, 600)
        self.speed = speed

    def draw(self):
        window.blit(enemy_image, (self.x, self.y))

    def move(self):
        self.y += self.speed
        if self.y >= 630:
            self.x = random.randint(180, 620)
            self.y = -1 * random.randint(150, 600)

class Coin:
    def __init__(self, speed):  # Corrected '__init__'
        self.x = random.randint(180, 620)
        self.y = -50
        self.speed = speed

    def draw(self):
        window.blit(coin_image, (self.x, self.y))

    def move(self):
        self.y += self.speed
        if self.y > 650:
            self.y = -50
            self.x = random.randint(160, 620)

class Background:
    def __init__(self, y, speed):  # Corrected '__init__'
        self.x = 0
        self.y = y
        self.speed = speed

    def draw(self):
        window.blit(bg_image, (self.x, self.y))

    def move(self):
        self.y += self.speed
        if self.y >= 650:
            self.y -= 650 * 2 + -speed

speed = 2

car = Player(400, 490)
enemy_car = Enemy(speed)
coin = Coin(speed)

road2 = Background(0, speed)
road = Background(-649, speed)

# Main loop
paused = False
running = True
score = 0
level_coin = 0
level = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                paused = False

    if paused:
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car.x > 160:
        car.x -= car.speed
    if keys[pygame.K_RIGHT] and car.x < 570:
        car.x += car.speed
    if keys[pygame.K_l]:
        car.speed += 0.2

    car_rect = pygame.Rect(car.x, car.y, car_image.get_width() - 30, car_image.get_height())
    coin_rect = pygame.Rect(coin.x, coin.y, coin_image.get_width(), coin_image.get_height() - 15)
    enemy_rect = pygame.Rect(enemy_car.x, enemy_car.y, enemy_image.get_width() - 30, enemy_image.get_height() - 15)

    if car_rect.colliderect(coin_rect):
        score += 1
        level_coin += 1
        car.speed += 0.1
        enemy_car.speed += 0.1
        if level_coin >= 5:
            speed += 0.3
            road.speed = speed
            road2.speed = speed
            coin.speed = speed
            level += 1
            level_coin = 0
        coin.y = -50
        coin.x = random.randint(180, 510)

    # Draw everything
    window.fill((0, 0, 0))
    road2.move()
    road2.draw()

    road.move()
    road.draw()

    car.draw()

    enemy_car.draw()
    enemy_car.move()

    coin.draw()
    coin.move()

    if car_rect.colliderect(enemy_rect):
        paused = True
        font = pygame.font.Font(None, 150)
        text = font.render("You Lose", True, (255, 0, 0))
        window.blit(text, (200, 200))

    font = pygame.font.Font(None, 36)
    text = font.render(f"Coins: {score}", True, (255, 255, 255))
    text_level = font.render(f"Level: {level}", True, (255, 255, 255))
    window.blit(text, (10, 10))
    window.blit(text_level, (10, 40))

    pygame.display.flip()

pygame.quit()
