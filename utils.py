import random

def fill_with_outline(surface, fill_color, outline_color, border=1):
  surface.fill(outline_color)
  surface.fill(fill_color, surface.get_rect().inflate(-border, -border))


def get_random_color():
  colors = [
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 127, 0)
  ]
  return random.choice(colors)
  