import pygame
import random

pygame.init()

#display
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("PyGame Racer")

# Load and resize images
bg_image = pygame.image.load('bg.png')
car_image = pygame.image.load('car.png')
car_image = pygame.transform.scale(car_image, (300, 100))  # Resize the car image
coin_image = pygame.image.load('coin.png')
coin_image = pygame.transform.scale(coin_image, (30, 30))  # Resize the coin image

# Player car
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 20

    def draw(self):
        screen.blit(car_image, (self.x, self.y))

# Coin
class Coin:
    def __init__(self):
        self.x = random.randint(0, 1250)
        self.y = 0
        self.speed = 5

    def draw(self):
        screen.blit(coin_image, (self.x, self.y))

    def move(self):
        self.y += self.speed
        if self.y > 720:
            self.y = 0
            self.x = random.randint(0, 1250)


# Initialize player and coins
player = Car(375, 550)
coins = [Coin() for _ in range(5)]
collected_coins = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player.speed
    if keys[pygame.K_RIGHT]:
        player.x += player.speed

    # Move coins
    for coin in coins:
        coin.move()

    # Check for collision with coins
    player_rect = pygame.Rect(player.x, player.y, car_image.get_width(), car_image.get_height())
    for coin in coins:
        coin_rect = pygame.Rect(coin.x, coin.y, coin_image.get_width(), coin_image.get_height())
        if player_rect.colliderect(coin_rect):
            collected_coins += 1
            coins.remove(coin)
            coins.append(Coin())

    # Draw everything
    screen.blit(bg_image, (0,0))
    player.draw()
    for coin in coins:
        coin.draw()

    # Display collected coins
    font = pygame.font.Font(None, 36)
    text = font.render(f"Coins: {collected_coins}", True, (255, 255, 255))
    screen.blit(text, (650, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
