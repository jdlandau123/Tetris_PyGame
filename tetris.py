import sys
import pygame
from classes.Block import Block

FPS = 30

class Game:
  def __init__(self):
    pygame.init()
    pygame.display.set_caption('Tetris in Python!')
    pygame.font.init()
    self.block_size = 16
    self.clock = pygame.time.Clock()
    board_size = (10 * self.block_size, 20 * self.block_size)
    self.screen = pygame.display.set_mode((
      board_size[0] * 3, board_size[1] * 2
    ))
    self.board = pygame.Surface(board_size)
    self.frames_passed = 0
    self.current_block = None
    self.placed_blocks = []
    self.score = 0
  

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
            if self.current_block.is_valid_movement("left", self.get_placed_block_locations()):
              self.current_block.x -= self.block_size
          if event.key == pygame.K_RIGHT:
            if self.current_block.is_valid_movement("right", self.get_placed_block_locations()):
              self.current_block.x += self.block_size
          if event.key == pygame.K_SPACE:
            self.current_block.rotate()

      if pygame.key.get_pressed()[pygame.K_DOWN] and self.frames_passed % 2 == 0:
        if self.current_block.is_valid_movement("down", self.get_placed_block_locations()):
          self.current_block.y += self.block_size
    
      self.draw_ui()
      self.draw_board()

      if self.frames_passed % (FPS // 2) == 0 and self.current_block is not None:
        if self.current_block.is_valid_movement("down", self.get_placed_block_locations()):
          self.current_block.y += self.block_size
        else:
          self.current_block.is_falling = False
          self.placed_blocks.append(self.current_block)

      if self.current_block is None or self.current_block.is_falling == False:
        self.current_block = Block(self.board, self.block_size)
      
      self.current_block.draw()

      for loc in self.get_placed_block_locations():
        if loc[1] <= self.block_size * 2:
          self.game_over()

      lines_cleared = self.check_complete_lines()
      if len(lines_cleared) > 0:
        self.shift_placed_blocks(lines_cleared)
      
      pygame.display.update()
      self.clock.tick(FPS)
      self.frames_passed += 1


  def draw_board(self):
    self.screen.blit(
      self.board,
      (self.screen.get_width() / 3, self.screen.get_height() / 4)
    )
    self.board.fill((200, 200, 200))
    for block in self.placed_blocks:
      block.draw()

  
  def draw_ui(self):
    self.screen.fill((255, 255, 255))
    title_font = pygame.font.SysFont("Arial", 30)
    title_surface = title_font.render("Tetris!", False, (0, 0, 0))
    self.screen.blit(title_surface, (
      (self.screen.get_width() / 2) - (title_surface.get_width() / 2),
      self.block_size
    ))
    score_font = pygame.font.SysFont("Arial", 20)
    score_surface = score_font.render(f"Score: {self.score}", False, (0, 0, 0))
    self.screen.blit(score_surface, (
      self.screen.get_width() - (score_surface.get_width() * 1.5),
      (self.screen.get_height() / 2) - (score_surface.get_height() / 2)
    ))
  

  def get_placed_block_locations(self):
    return [i for b in self.placed_blocks for i in b.locations]
  

  def check_complete_lines(self):
    lines_cleared = []
    board_bottom = self.board.get_height()
    for row in range(board_bottom, self.block_size, -self.block_size):
      blocks = self.get_placed_block_locations()
      row_blocks = [b for b in blocks if b[1] == row]
      if len(row_blocks) == 10:
        for b in row_blocks:
          for block in self.placed_blocks:
            block.remove_location(b)
        self.score += 1
        lines_cleared.append(row)
    return lines_cleared
  

  def shift_placed_blocks(self, lines_cleared):
    for line in lines_cleared:
      locs = [l for l in self.get_placed_block_locations() if l[1] < line]
      for l in locs:
        l[1] += self.block_size * len(lines_cleared)

  
  def game_over(self):
    self.screen.fill((255, 255, 255))
    font = pygame.font.SysFont("Arial", 30)
    surface = font.render("Game Over!", False, (0, 0, 0))
    self.screen.blit(surface, (
      (self.screen.get_width() / 2) - (surface.get_width() / 2),
      (self.screen.get_height() / 2) - (surface.get_height() / 2)
    ))
    score_font = pygame.font.SysFont("Arial", 20)
    score_surface = score_font.render(f"Final Score: {self.score}", False, (0, 0, 0))
    self.screen.blit(score_surface, (
      (self.screen.get_width() / 2) - (score_surface.get_width() / 2),
      (self.screen.get_height() / 2) - (surface.get_height() / 2) + 50
    ))


Game().run()
