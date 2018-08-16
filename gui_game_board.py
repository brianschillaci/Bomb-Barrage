import game_board
import pygame


class GUIGameBoard(game_board.GameBoard):
    """
    Extends game_board.GameBoard to contain additional state for screen and
    background color to be used in drawing the board to the given screen.

    For box_drawing_map, must pass in a list of tuples with the following
    pattern: [('char', COLOR), ('char', PATH\\To\\File), ...]
    """

    def __init__(self,
                 screen,
                 box_drawing_map_path,
                 board_loc):
        super(GUIGameBoard, self).__init__(board_loc)
        self.screen = screen
        #: :type: dictionary
        self.box_drawing_map = None
        self.box_width = 0
        self.read_drawing_map(box_drawing_map_path)
        self.initialize()

    def read_drawing_map(self, box_drawing_map_path):
        fd = open(box_drawing_map_path, 'r')
        lines = [line.strip() for line in fd.readlines()]
        fd.close()

        box_drawing_map = {}
        self.box_width = int(lines[0])
        for line in lines[1:]:
            words = line.split()
            if words[1] == "color":
                color = (int(words[2]), int(words[3]), int(words[4]))
                box_drawing_map.update({words[0]: [words[1], color, None, words[3], words[4], words[5]]})
            else:
                box_drawing_map.update({words[0]: [words[1], words[2], None, words[3], words[4], words[5]]})

        self.box_drawing_map = box_drawing_map

    def initialize_board_sprites(self, spriteGroups, spriteClassMap):
        """
        This function will initialize the spriteGroups with sprites defined in the brd file.
        It won't create a sprite if the line in the cfg file says no_sprite_class.
        The sprite class name is retrieved from the 4th index.
        Its x and y coordinate are retrived from the location in the corresponding character in the brd file.
        :param spriteGroups: List of sprite.Group()'s to add the gameboard sprites to, the sprite.group() to choose is
                             determined by the index given in the cfg file.
        :param spriteClassMap: Map of string sprite class names to the actual class's object - used to call the
                               constructors of the sprites dynamically based on the sprite class string in the cfg file
        :return: void
        """
        for i, box in enumerate(self.board_state):
            (x, y) = self.get_pixel_coord_from_pos(i)

            # '~' means there is no image to be drawn for that location
            if box is '~':
                continue

            if self.box_drawing_map[box][0] != "color" and self.box_drawing_map[box][4] != 'no_sprite_class':
                # If this element has a sprite class associated with it, we need to create a sprite object for it
                # and add it to the correct spriteGroup.
                # The sprite groups are passed in as a list and their index is in the .cfg file.
                # The spriteClassMap contains mapping between sprite objects and their string name.
                # This is needed so we can instantiate these sprite objects calling their constructor.
                spriteName = self.box_drawing_map[box][4]
                spriteToAdd = spriteClassMap[spriteName](self.box_drawing_map[box][2], x, y)
                spriteGroups[int(self.box_drawing_map[box][5])].add(spriteToAdd)

    def update_non_board_sprites(self):
        """
        The method used whenever to update the screen that holds the game_boardgame board images to the screen
        It will either update the background, or draw unchanging game board images to the screen.
        :return: void
        """
        for i, box in enumerate(self.board_state):
            (x, y) = self.get_pixel_coord_from_pos(i)

            # '~' means there is no image to be drawn for that location
            if box is '~':
                continue

            if self.box_drawing_map[box][0] == "color":
                pygame.draw.rect(self.screen,
                                 self.box_drawing_map[box][1],
                                 [x,
                                  y,
                                  self.box_width,
                                  self.box_width])
            else:
                # Drawing non Sprite board image to the screen
                if self.box_drawing_map[box][4] == 'no_sprite_class':
                    self.screen.blit(self.box_drawing_map[box][2], (x, y))

    def get_pixel_coord_from_pos(self, pos):
        """
        Given a board position number, return the pixel coordinates for the
        given position.
        :param pos: Position on the board.
        :return: Success: [x_pixel, y_pixel] Failure: [-1, -1]
        """
        (x, y) = self.get_coord_from_pos(pos)
        if x == -1 and y == -1:
            return [-1, -1]
        return [x * self.box_width, y * self.box_width]

    def initialize(self):
        """
        Initializes the images for each of the board elements.
        :return: void
        """
        for entry in self.box_drawing_map.items():
            if entry[1][0] == "img":
                img_path = entry[1][1]
                # loading the actual image for this game board element
                entry[1][2] = pygame.image.load(img_path).convert()
