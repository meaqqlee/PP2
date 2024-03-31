import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake
snake_blocks = [(400, 300), (390, 300), (380, 300)]
snake_speed = 10
direction = 'RIGHT'

# Food
def generate_food():
    while True:
        x = random.randint(0, 79) * 10
        y = random.randint(0, 59) * 10
        if (x, y) not in snake_blocks:
            return (x, y)

food_position = generate_food()

# Score and Level
score = 0
level = 1
foods_eaten = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
            elif event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'

    # Move the snake
    x, y = snake_blocks[0]
    if direction == 'RIGHT':
        x += 10
    elif direction == 'LEFT':
        x -= 10
    elif direction == 'UP':
        y -= 10
    elif direction == 'DOWN':
        y += 10
    new_head = (x, y)

    # Check for border collision
    if x < 0 or x >= 800 or y < 0 or y >= 600:
        running = False  # End the game

    # Check for self collision
    if new_head in snake_blocks:
        running = False

    # Check for food collision
    if new_head == food_position:
        food_position = generate_food()
        score += 1
        foods_eaten += 1
        if foods_eaten >= 3:
            level += 1
            snake_speed += 2
            foods_eaten = 0
    else:
        snake_blocks.pop()  # Remove the tail

    snake_blocks.insert(0, new_head)

    # Draw everything
    screen.fill(WHITE)
    for block in snake_blocks:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], 10, 10])
    pygame.draw.rect(screen, RED, [food_position[0], food_position[1], 10, 10])

    # Display score and level
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    pygame.display.flip()
    pygame.time.Clock().tick(snake_speed)

pygame.quit()
