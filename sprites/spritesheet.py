import pygame


class Spritesheet:
    def __init__(self, filename):
        """
        Constructor for a Spritesheet object.
        Creates a pygame image object from the input filename parameter.
        :param filename: Filename string to create pygame image for this Spritesheet/image of sprites.
        """
        # Loading the full spritesheet image and storing it as a variable in this object
        self.sheet_image = pygame.image.load(filename).convert()

    def get_image(self, x: object, y: object, width: object, height: object) -> object:
        """
        Cuts an image out from the larger Spritesheet and returns it as a regular pygame image.
        :param x: x-coordinate on spritesheet of the top left pixel of the image.
        :param y: y-coordinate on spritesheet of the top left pixel of the image.
        :param width: Width amount of pixels of the image.
        :param height: Height amount of pixels of the image.
        :return:
        """
        image = pygame.Surface((width, height))
        image.blit(self.sheet_image, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width, height))
        return image
