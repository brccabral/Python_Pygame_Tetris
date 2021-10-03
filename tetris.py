# pip install pygame
import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
block_size = 30
# 10 columns, 20 rows
columns = 10
rows = 20
play_width = block_size*columns  # meaning 300 // 10 = 30 width per block
play_height = block_size*rows  # meaning 600 // 20 = 20 height per block

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
    '......',
    '..00..',
    '.00...',
    '.....'],
     ['.....',
    '..0..',
    '..00.',
    '...0.',
    '.....']]

Z = [['.....',
    '.....',
    '.00..',
    '..00.',
    '.....'],
     ['.....',
    '..0..',
    '.00..',
    '.0...',
    '.....']]

I = [['..0..',
    '..0..',
    '..0..',
    '..0..',
    '.....'],
     ['.....',
    '0000.',
    '.....',
    '.....',
    '.....']]

O = [['.....',
    '.....',
    '.00..',
    '.00..',
    '.....']]

J = [['.....',
    '.0...',
    '.000.',
    '.....',
    '.....'],
     ['.....',
    '..00.',
    '..0..',
    '..0..',
    '.....'],
     ['.....',
    '.....',
    '.000.',
    '...0.',
    '.....'],
     ['.....',
    '..0..',
    '..0..',
    '.00..',
    '.....']]

L = [['.....',
    '...0.',
    '.000.',
    '.....',
    '.....'],
     ['.....',
    '..0..',
    '..0..',
    '..00.',
    '.....'],
     ['.....',
    '.....',
    '.000.',
    '.0...',
    '.....'],
     ['.....',
    '.00..',
    '..0..',
    '..0..',
    '.....']]

T = [['.....',
    '..0..',
    '.000.',
    '.....',
    '.....'],
     ['.....',
    '..0..',
    '..00.',
    '..0..',
    '.....'],
     ['.....',
    '.....',
    '.000.',
    '..0..',
    '.....'],
     ['.....',
    '..0..',
    '.00..',
    '..0..',
    '.....']]

shapes = [S, Z, I, O, J, L, T]
# one color per shape
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    """
    locked_positions contains colors on each block coordinate
    """
    # black color for all blocks
    grid = [[(0,0,0) for _ in range(columns)] for _ in range(rows)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)] # get color in locked_positions
                grid[i][j] = c


def convert_shape_format(shape):
    pass

def valid_space(shape, grid):
    pass

def check_lost(positions):
    pass

def get_shape():
    return random.choice(shapes)


def draw_text_middle(text, size, color, surface):
    pass
   
def draw_grid(surface, row, col):
    pass

def clear_rows(grid, locked):
    pass

def draw_next_shape(shape, surface):
    pass

def draw_window(surface):
    pass

def main():
    pass

def main_menu():
    pass

main_menu()  # start game