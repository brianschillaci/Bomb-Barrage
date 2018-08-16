import pygame


def animate(sprite, interval, images):
    now = pygame.time.get_ticks()
    if now - sprite.last_update > interval:
        sprite.last_update = now
        sprite.current_frame = (sprite.current_frame + 1) % len(images)
        sprite.image = images[sprite.current_frame]


def animate_time_limit(sprite, interval, images):
    now = pygame.time.get_ticks()
    timePassed = now - sprite.last_update
    if timePassed > interval:
        sprite.last_update = now
        sprite.current_frame += 1
        if sprite.current_frame == len(images):
            sprite.current_frame = 0
            return True
        else:
            sprite.image = images[sprite.current_frame]
            return False
