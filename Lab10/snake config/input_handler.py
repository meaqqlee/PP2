import pygame
import sys

def get_user_id():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Введите User ID')
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box_color = (255, 255, 255)
    input_text_color = (0, 0, 0)
    input_box = pygame.Rect(200, 200, 140, 32)
    active = False
    user_text = ''

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        pygame.quit()
                        return user_text
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(user_text, True, input_text_color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, input_box_color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)