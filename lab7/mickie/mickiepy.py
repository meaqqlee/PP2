import pygame
import datetime
'''import math
import time '''

pygame.init()

screen = pygame.display.set_mode((1400, 1050))
clock = pygame.time.Clock()
angle = 0
pygame.display.set_caption("mickie clock")

rightarm = pygame.image.load('rightarm.png')
leftarm = pygame.image.load('leftarm.png')
bg = pygame.image.load('mainclock.png')

def blitRotate(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft = (pos[0]-originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    rotated_offset = offset_center_to_pivot.rotate(angle)

    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    rotated_image = pygame.transform.rotate(image, -angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    surf.blit(rotated_image, rotated_image_rect)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    now = datetime.datetime.now()

    angleH = (now.hour % 12) * (360 / 12) + (now.minute / 60) * (360 / 12) + 60
    angleM = now.minute * (360 / 60)

    screen.blit(bg, (0, 0))
    blitRotate(screen, rightarm, (700, 525), ( rightarm.get_width()//2, rightarm.get_height()//2), angleH)
    blitRotate(screen, leftarm, (700, 525), (leftarm.get_width() // 2, leftarm.get_height() // 2), angleM)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()


'''for am and pm'''
"""current_time = datetime.datetime.now()
    hour = current_time.hour % 12
    minute = current_time.minute
    second = current_time.second

    # Calculate angles for the hands
    angleH = (hour + minute / 60) * 30 + 60
    angleM = minute * 6
    print(f"Current time: {hour}:{minute}:{second}")"""