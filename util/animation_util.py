import pygame


def animate(sprite, interval, images):
    """
    Animates a sprite using an input list of images. This function HAS NO LIMIT and will always run as long as the
    the sprite exists.
    :param sprite: The sprite object to animate.
    :param interval: The time in between images.
    :param images: List of images to loop through to create animation.
    """
    now = pygame.time.get_ticks()
    if now - sprite.last_update > interval:
        sprite.last_update = now
        sprite.current_frame = (sprite.current_frame + 1) % len(images)
        sprite.image = images[sprite.current_frame]


def animate_with_limit(sprite, interval, images):
    """
    Animates a sprite using an input list of images. This function HAS A LIMIT and will run until it displays every
    image in the input array.
    :param sprite: The sprite object to animate.
    :param interval: The time in between images.
    :param images: List of images to loop through to create animation.
    :return: True - when the animation is done, False - if the animation still needs to run more
    """
    now = pygame.time.get_ticks()
    time_passed = now - sprite.last_update
    if time_passed > interval:
        sprite.last_update = now
        sprite.current_frame += 1
        if sprite.current_frame == len(images):
            sprite.current_frame = 0
            return True
        else:
            sprite.image = images[sprite.current_frame]
            return False
