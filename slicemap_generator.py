#!/usr/bin/env python3.9

"""Generate Slicemaps of 4d Menger Sponges"""

import sys
import math

import pygame
import pygame.gfxdraw
from pygame.constants import *


# Setup

# levels
ITER = 3

# border width between slices
slice_diff = 3

# file to wich is written
out_file = "./slice_view_menger_nohighlight_3.png"


# calculated constants
grid_cell_size = 3**ITER
grid_cell_offset = grid_cell_size + slice_diff

total_size = grid_cell_size * grid_cell_offset - slice_diff


# pygame Init
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), RESIZABLE)
screen.fill((255, 255, 255))
pygame.display.set_caption('slicemap generation')
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

fill_color = WHITE
origin_color = GRAY
if "-d" in sys.argv:
    fill_color = GRAY
    origin_color = WHITE

def get_pos(x, y, z, w):
    return grid_cell_offset * x + y, grid_cell_offset * z + w

def get_coord(x, y):
    return (x // grid_cell_offset, x % grid_cell_offset,
            y // grid_cell_offset, y % grid_cell_offset)

main_tex = pygame.Surface((total_size, total_size))
main_tex.fill((255, 255, 255))

# uncomment to create light gray background 
##for i in range(grid_cell_size):
##    for j in range(grid_cell_size):
##        pygame.draw.rect(main_tex, (200, 200, 200), (get_pos(i, 0, j, 0), (grid_cell_size, grid_cell_size)))

MENGER_OFFSETS = [
    (-1, -1, -1, -1),
    (-1, -1, -1, 0),
    (-1, -1, -1, 1),
    (-1, -1, 0, -1),
    (-1, -1, 0, 1),
    (-1, -1, 1, -1),
    (-1, -1, 1, 0),
    (-1, -1, 1, 1),
    (-1, 0, -1, -1),
    (-1, 0, -1, 1),
    (-1, 0, 1, -1),
    (-1, 0, 1, 1),
    (-1, 1, -1, -1),
    (-1, 1, -1, 0),
    (-1, 1, -1, 1),
    (-1, 1, 0, -1),
    (-1, 1, 0, 1),
    (-1, 1, 1, -1),
    (-1, 1, 1, 0),
    (-1, 1, 1, 1),
    (0, -1, -1, -1),
    (0, -1, -1, 1),
    (0, -1, 1, -1),
    (0, -1, 1, 1),
    (0, 1, -1, -1),
    (0, 1, -1, 1),
    (0, 1, 1, -1),
    (0, 1, 1, 1),
    (1, -1, -1, -1),
    (1, -1, -1, 0),
    (1, -1, -1, 1),
    (1, -1, 0, -1),
    (1, -1, 0, 1),
    (1, -1, 1, -1),
    (1, -1, 1, 0),
    (1, -1, 1, 1),
    (1, 0, -1, -1),
    (1, 0, -1, 1),
    (1, 0, 1, -1),
    (1, 0, 1, 1),
    (1, 1, -1, -1),
    (1, 1, -1, 0),
    (1, 1, -1, 1),
    (1, 1, 0, -1),
    (1, 1, 0, 1),
    (1, 1, 1, -1),
    (1, 1, 1, 0),
    (1, 1, 1, 1),
]


TIGHT_MENGER_OFFSETS = [
    (-1, -1, -1, -1),
    (-1, -1, -1, 0),
    (-1, -1, -1, 1),
    (-1, -1, 0, -1),
    (-1, -1, 0, 0),
    (-1, -1, 0, 1),
    (-1, -1, 1, -1),
    (-1, -1, 1, 0),
    (-1, -1, 1, 1),
    (-1, 0, -1, -1),
    (-1, 0, -1, 0),
    (-1, 0, -1, 1),
    (-1, 0, 0, -1),
    (-1, 0, 0, 1),
    (-1, 0, 1, -1),
    (-1, 0, 1, 0),
    (-1, 0, 1, 1),
    (-1, 1, -1, -1),
    (-1, 1, -1, 0),
    (-1, 1, -1, 1),
    (-1, 1, 0, -1),
    (-1, 1, 0, 0),
    (-1, 1, 0, 1),
    (-1, 1, 1, -1),
    (-1, 1, 1, 0),
    (-1, 1, 1, 1),
    (0, -1, -1, -1),
    (0, -1, -1, 0),
    (0, -1, -1, 1),
    (0, -1, 0, -1),
    (0, -1, 0, 1),
    (0, -1, 1, -1),
    (0, -1, 1, 0),
    (0, -1, 1, 1),
    (0, 0, -1, -1),
    (0, 0, -1, 1),
    (0, 0, 1, -1),
    (0, 0, 1, 1),
    (0, 1, -1, -1),
    (0, 1, -1, 0),
    (0, 1, -1, 1),
    (0, 1, 0, -1),
    (0, 1, 0, 1),
    (0, 1, 1, -1),
    (0, 1, 1, 0),
    (0, 1, 1, 1),
    (1, -1, -1, -1),
    (1, -1, -1, 0),
    (1, -1, -1, 1),
    (1, -1, 0, -1),
    (1, -1, 0, 0),
    (1, -1, 0, 1),
    (1, -1, 1, -1),
    (1, -1, 1, 0),
    (1, -1, 1, 1),
    (1, 0, -1, -1),
    (1, 0, -1, 0),
    (1, 0, -1, 1),
    (1, 0, 0, -1),
    (1, 0, 0, 1),
    (1, 0, 1, -1),
    (1, 0, 1, 0),
    (1, 0, 1, 1),
    (1, 1, -1, -1),
    (1, 1, -1, 0),
    (1, 1, -1, 1),
    (1, 1, 0, -1),
    (1, 1, 0, 0),
    (1, 1, 0, 1),
    (1, 1, 1, -1),
    (1, 1, 1, 0),
    (1, 1, 1, 1),
]

# per-coordinate lookup
def is_in_sponge(x, y, z, w):
    for i in (range(ITER)):
        div = 3 ** i
        local_x = (x // div) % 3
        local_y = (y // div) % 3
        local_z = (z // div) % 3
        local_w = (w // div) % 3

        # rule for menger sponge
        # you could also use lookup table
        # use different values for comparison to get more enclosed values
        # use `> 2` for the "tight" menger sponge (with "face central" hypercubes)
        if [local_x, local_y, local_z, local_w].count(1) > 1:
            return 0
        
    return 1

# recursive generator
def gen_map(x, y, z, w, it):
##    print(it * " ", it, x, y, z, w)
    if it == 0:
        return
    delta = 3 ** (it - 1)
    # use TIGHT_MENGER_OFFSETS for other representation
    for dx, dy, dz, dw in MENGER_OFFSETS:
        newx = x + dx * delta
        newy = y + dy * delta
        newz = z + dz * delta
        neww = w + dw * delta

        if it == 1:
##            pygame.draw.rect(main_tex, BLACK, (get_pos(newx, newy, newz, neww), (1, 1)))
            pygame.gfxdraw.pixel(main_tex, *get_pos(newx, newy, newz, neww), BLACK)
##            print(newx, newy, newz, neww, get_pos(newx, newy, newz, neww))
        else:
            gen_map(newx, newy, newz, neww, it-1)

# generating loop
for i in range(total_size):
    if i % grid_cell_offset >= grid_cell_size:
        continue
    print(f"line {i} / {total_size}", end="\r")
    for j in range(total_size):
        if j % grid_cell_offset >= grid_cell_size:
            continue
        if is_in_sponge(*get_coord(i, j)):
            pygame.gfxdraw.pixel(main_tex, i, j, BLACK)
print(" " * 100)

# old version
##middle = grid_cell_size // 2
##gen_map(middle, middle, middle, middle, ITER)

pygame.image.save(main_tex, out_file)

# main loop (no real functionality)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit


    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

    screen.fill(fill_color)

    screen.blit(main_tex, (0, 0))

    
    pygame.display.flip()
    clock.tick(60)
    
    print(round(clock.get_fps(), 5), end='\r')
