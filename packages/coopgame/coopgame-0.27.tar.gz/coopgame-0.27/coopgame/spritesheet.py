# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

# Additional notes
# - Further adaptations from https://www.pygame.org/wiki/Spritesheet
# - Cleaned up overall formatting.
# - Updated from Python 2 -> Python 3.

import pygame
from coopstructs.vectors import Vector2
import struct
import imghdr

class SpriteSheet:

    def __init__(self, filename, n_rows, n_columns, x_margin_left=0, x_margin_right=None, x_padding=0,
                         y_margin_top=0, y_margin_bottom = None, y_padding=0):
        self.file_size = self.get_image_size(filename)
        self.n_images_in_row = n_columns
        self.n_images_in_column = n_rows

        self.x_margin_left = x_margin_left
        self.x_margin_right = x_margin_right if x_margin_right else x_margin_left
        self.x_padding = x_padding
        self.y_margin_top = y_margin_top
        self.y_margin_bottom = y_margin_bottom if y_margin_bottom else y_margin_top
        self.y_padding = y_padding

        self.pixel_width = (self.file_size[0] - (self.x_margin_left + self.x_margin_right)
                         - (self.n_images_in_row - 1) * self.x_padding) // self.n_images_in_row
        self.pixel_height = (self.file_size[1] - (self.y_margin_top + self.y_margin_bottom)
                         - (self.n_images_in_column - 1) * self.y_padding) // self.n_images_in_column




        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)



    def image_at(self, pos: Vector2, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rectangle = (pos.x * self.pixel_width, pos.y * self.pixel_height, self.pixel_width, self.pixel_height)
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def image_at_rect(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at_rect(rect, colorkey) for rect in rects]


    def load_row_strip(self, row, colorkey = None, n_images: int = None):
        grid_images = self.load_grid_images(colorkey=colorkey)

        if n_images is None or n_images < 0:
            return grid_images[row]
        else:
            return grid_images[row][:n_images]

    def load_column_strip(self, column, colorkey = None, n_images: int = None):
        grid_images = self.load_grid_images(colorkey=colorkey)

        images =  [row[column] for row in grid_images]
        if n_images is None or n_images < 0:
            return images
        else:
            return images[:n_images]

    def load_grid_images(self, colorkey = None):
        """Load a grid of images.
        x_margin is space between top of sheet and top of first row.
        x_padding is space between rows.
        Assumes symmetrical padding on left and right.
        Same reasoning for y.
        Calls self.images_at() to get list of images.
        """
        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # To calculate the size of each sprite, subtract the two margins,
        #   and the padding between each row, then divide by num_cols.
        # Same reasoning for y.
        # x_sprite_size = (sheet_width - 2 * self.x_margin
        #                  - (self.n_images_in_row - 1) * self.x_padding) // self.n_images_in_row
        # y_sprite_size = (sheet_height - 2 * self.y_margin
        #                  - (self.n_images_in_column - 1) * self.y_padding) // self.n_images_in_column

        grid_images = []
        for row_num in range(self.n_images_in_column):
            grid_images.append([])
            for col_num in range(self.n_images_in_row):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = self.x_margin_left + 1 + col_num * (self.pixel_width + self.x_padding)
                y = self.y_margin_top + 1 + row_num * (self.pixel_height + self.y_padding)
                sprite_rect = x, y, self.pixel_width, self.pixel_height
                grid_images[row_num].append(self.image_at_rect(sprite_rect, colorkey=colorkey))

        return grid_images

    def get_image_size(self, fname):
        '''Determine the image type of fhandle and return its size.
        from draco'''
        with open(fname, 'rb') as fhandle:
            head = fhandle.read(24)
            if len(head) != 24:
                return
            if imghdr.what(fname) == 'png':
                check = struct.unpack('>i', head[4:8])[0]
                if check != 0x0d0a1a0a:
                    return
                width, height = struct.unpack('>ii', head[16:24])
            elif imghdr.what(fname) == 'gif':
                width, height = struct.unpack('<HH', head[6:10])
            elif imghdr.what(fname) == 'jpeg':
                try:
                    fhandle.seek(0)  # Read 0xff next
                    size = 2
                    ftype = 0
                    while not 0xc0 <= ftype <= 0xcf:
                        fhandle.seek(size, 1)
                        byte = fhandle.read(1)
                        while ord(byte) == 0xff:
                            byte = fhandle.read(1)
                        ftype = ord(byte)
                        size = struct.unpack('>H', fhandle.read(2))[0] - 2
                    # We are at a SOFn block
                    fhandle.seek(1, 1)  # Skip `precision' byte.
                    height, width = struct.unpack('>HH', fhandle.read(4))
                except Exception:  # IGNORE:W0703
                    return
            else:
                return
            return width, height