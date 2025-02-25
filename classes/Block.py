import pygame
import random
from utils import get_random_color, fill_with_outline

O = [
  [[1, 1, 0, 0],
  [1, 1, 0, 0]]
]

I = [
  [[1, 1, 1, 1],
  [0, 0, 0, 0]],

  [[1, 0, 0, 0],
  [1, 0, 0, 0],
  [1, 0, 0, 0],
  [1, 0, 0, 0]]
]

J = [
  [[1, 0, 0, 0],
  [1, 1, 1, 0]],

  [[0, 1, 0, 0],
  [0, 1, 0, 0],
  [1, 1, 0, 0]],

  [[1, 1, 1, 0],
  [0, 0, 1, 0]],

  [[1, 1, 0, 0],
  [1, 0, 0, 0],
  [1, 0, 0, 0]]
]

L = [
  [[0, 0, 1, 0],
  [1, 1, 1, 0]],

  [[1, 0, 0, 0],
  [1, 0, 0, 0],
  [1, 1, 0, 0]],

  [[1, 1, 1, 0],
  [1, 0, 0, 0]],

  [[1, 1, 0, 0],
  [0, 1, 0, 0],
  [0, 1, 0, 0]],
]

S = [
  [[0, 1, 1, 0],
  [1, 1, 0, 0]],

  [[1, 0, 0, 0],
  [1, 1, 0, 0],
  [0, 1, 0, 0]]
]

T = [
  [[0, 1, 0, 0],
  [1, 1, 1, 0]],

  [[1, 0, 0, 0],
  [1, 1, 0, 0],
  [1, 0, 0, 0]],

  [[1, 1, 1, 0],
  [0, 1, 0, 0]],

  [[0, 1, 0, 0],
  [1, 1, 0, 0],
  [0, 1, 0, 0]]
]

Z = [
  [[1, 1, 0, 0],
  [0, 1, 1, 0]],

  [[0, 1, 0, 0],
  [1, 1, 0, 0],
  [1, 0, 0, 0]]
]

BLOCK_SHAPES = [O, I, J, L, S, T, Z]

class Block:
  def __init__(self, board, block_size=16):
    self.board = board
    self.block_size = block_size
    self.x = self.board.get_rect().center[0]
    self.y = self.board.get_rect()[1]
    self.shape = random.choice(BLOCK_SHAPES)
    self.rotation = 0
    self.color = get_random_color()
    self.is_falling = True
    self.locations = []


  def draw(self):
    if not self.is_falling:
      for loc in self.locations:
        surface = pygame.Surface((self.block_size, self.block_size))
        fill_with_outline(surface, self.color, (0, 0, 0))
        self.board.blit(surface, loc)
      return
    self.locations = []
    shape = self.shape[self.rotation]
    for row, arr in enumerate(shape):
      for col, i in enumerate(arr):
        if i == 1:
          x = self.x + (col * self.block_size)
          y = self.y + (row * self.block_size)
          origin = [x, y]
          self.locations.append(origin)
          surface = pygame.Surface((self.block_size, self.block_size))
          fill_with_outline(surface, self.color, (0, 0, 0))
          self.board.blit(surface, origin)


  def rotate(self):
    if self.rotation + 1 < len(self.shape):
      self.rotation += 1
    else:
      self.rotation = 0
  

  # movement can be left, right, or down
  def is_valid_movement(self, movement, collision_rects=[]):
    if movement == "left":
      for loc in self.locations:
        if loc[0] - self.block_size < self.board.get_rect()[0]:
          return False
        new_loc = [loc[0] - self.block_size, loc[1]]
        if new_loc in collision_rects:
          return False
    elif movement == "right":
      for loc in self.locations:
        if loc[0] + self.block_size >= self.board.get_width():
          return False
        new_loc = [loc[0] + self.block_size, loc[1]]
        if new_loc in collision_rects:
          return False
    elif movement == "down":
      for loc in self.locations:
        if loc[1] + self.block_size >= self.board.get_height():
          return False
        new_loc = [loc[0], loc[1] + self.block_size]
        if new_loc in collision_rects:
          return False
    return True
  

  def remove_location(self, location):
    if location in self.locations:
      self.locations.remove(location)

