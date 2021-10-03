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
    locked_positions contains colors from pieces alread posioned
    grid contains the colors on each coordiante
    """
    # black color for all blocks
    grid = [[(0,0,0) for _ in range(columns)] for _ in range(rows)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)] # get color in locked_positions
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    shp_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(shp_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    
    # this "trims" the dots from the shape
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    
    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j,i) for j in range(columns) if grid[i][j] == (0,0,0)] for i in range(rows)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        # check if formatted shape can fit in grid
        if pos not in accepted_pos:
            # something to do with the "trim" above
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 0:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, top_left_y + play_height/2 - label.get_height()/2))

def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        # surface, color, (x1, y1), (x2, y2)
        pygame.draw.line(surface, (128,128,128), (sx, sy+i*block_size), (sx+play_width, sy+i*block_size))
    for j in range(len(grid[0])):
        pygame.draw.line(surface, (128,128,128), (sx+j*block_size, sy), (sx+j*block_size, sy+play_height))

def clear_rows(grid, locked):
    # inc = how many rows to shift down
    inc = 0
    # loop backwards
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        # there is no black space
        if (0,0,0) not in row:
            inc += 1
            removed_line_index = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)] # remove the line from locked list
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            # move locked positions that are above the removed line index
            if y < removed_line_index:
                newKey = (x, y+inc)
                locked[newKey] = locked.pop(key)
    
    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape", 1, (255,255,255))
    
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    surface.blit(label, (sx + 10, sy - 30))

    shp_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(shp_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
    


def draw_window(surface, grid, score=0):
    surface.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 60)
    label = font.render("Tetris", 1, (255,255,255))
    surface.blit(label,(top_left_x + play_width/2 - label.get_width()/2, 30))

    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Score "+str(score), 1, (255,255,255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # surface, color, top left x,y, width, height, 1 draws a border
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 4)
    

def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        # constantly update the grid
        grid = create_grid(locked_positions)

        fall_time += clock.get_rawtime() # get time since last tick
        level_time += clock.get_rawtime() # get time since last tick
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005
        
        # move piece at every "fall_speed" seconds
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            # lock current_pice - it either hit the bottom or another piece
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
        
        # put piece color in grid
        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions)
        
        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        
        if check_lost(locked_positions):
            draw_text_middle(win, "You lost! Score "+str(score), 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

    pygame.display.quit()

def main_menu(win):
    main(win)
    pass

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")
main_menu(win)  # start game