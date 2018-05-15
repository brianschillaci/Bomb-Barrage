import pygame

from Settings import WIDTH, HEIGHT, TITLE, WHITE
from Sprites import Player

pygame.init()
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption(TITLE)
carryOn = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player1 = Player()
all_sprites.add(player1)
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                carryOn = False
    keys = pygame.key.get_pressed()
    all_sprites.draw(screen)

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player1.walk_left()
    elif keys[pygame.K_RIGHT]or keys[pygame.K_d]:
        player1.walk_right()
    elif keys[pygame.K_UP]or keys[pygame.K_w]:
        player1.walk_forward()
    elif keys[pygame.K_DOWN]or keys[pygame.K_s]:
        player1.walk_backward()
    else:
        player1.walking = False
        player1.animate_player()

    all_sprites.update()

    pygame.display.flip()
    screen.fill(WHITE)
    clock.tick(60)

pygame.quit()






