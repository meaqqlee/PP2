import pygame
pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("Red Ball")

clock = pygame.time.Clock()

def redrawGameWindow():
    win.fill((255, 255, 255))
    pygame.draw.circle(win, (255, 0, 0), (x, y), radius)
    pygame.display.update()

x = 250
y = 240
radius = 20
vel = 5

#mainloop
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    Keys = pygame.key.get_pressed()

    if Keys[pygame.K_LEFT] and x > radius:
        x -= vel
    if Keys[pygame.K_RIGHT] and x < 500 - radius:
        x += vel
    if Keys[pygame.K_UP] and y > radius:
        y -= vel
    if Keys[pygame.K_DOWN] and y < 480 - radius:
        y += vel

    redrawGameWindow()
pygame.quit()