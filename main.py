import operator as op
from functools import partial, reduce
from itertools import chain
from collections import UserList
import pygame
from pygame.locals import *
from pygame.math import Vector2 as vector

pygame.init()

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)
background = Color(161, 161, 161)
foreground = Color(255, 255, 255)
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
screen_rect = screen.get_rect()
fps = 0

post_event = lambda e:pygame.event.post(pygame.event.Event(e))


class Particle:
  def __init__(self, wave, index, _len=0):
    self.wave, self.index = wave, index
    self.wave.append(self)
    self.held = False
    self.pos, self.delta = 0, 0
    self.neighbours = []
    if self.index > 0:
      self.neighbours.append(self.wave[self.index - 1])
      self.wave[self.index - 1].neighbours.append(self)
  
  def update(self):
    self.held = False
    if self.neighbours:
      self.delta = [*map(op.attrgetter("pos"), self.neighbours)]
      self.delta = sum(self.delta)/len(self.delta)
  
  def move(self):
    self.pos = max(min(self.delta, 0.5), -0.5)


class Wave(UserList):
  def __init__(self, particles):
    super().__init__(map(partial(Particle, self, _len=particles), range(particles)))
    self._selected = 0
  
  def __call__(self, key):
    if key not in (K_LEFT, K_RIGHT):
      for particle in self:
        particle.update()
    if key == K_UP:
      self.selected.delta = self.selected.pos - 0.05
    elif key == K_DOWN:
      self.selected.delta = self.selected.pos + 0.05
    elif key == K_RIGHT:
      self._selected += 1
    elif key == K_LEFT:
      self._selected -= 1
    self._selected = (self._selected+len(self))%len(self)
    if key not in (K_LEFT, K_RIGHT):
      print(self.selected.pos, self.selected.delta)
      self.selected.held = key != K_BACKSPACE
      for particle in self:
        particle.move()
  
  @property
  def selected(self):
    return self[self._selected]
  
  def draw(self, surf, rect):
    for particle in self:
      pos = vector((particle.index + 0.5)/len(self), particle.pos + 0.5)
      pos = pos.elementwise()*rect.size + rect.topleft
      size = 5
      if particle.index == self._selected:
        size = 10
      pygame.draw.circle(surf, foreground, (int(pos.x), int(pos.y)), size)


wave1 = Wave(15)

while True:
  clock.tick(60)
  fps = clock.get_fps()
  screen.fill(background)
  
  if pygame.event.get(QUIT):
    break
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        pygame.event.post(pygame.event.Event(QUIT))
      elif event.key in (K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_BACKSPACE):
        wave1(event.key)
  
  wave1.draw(screen, screen_rect)
  
  screen.blit(font.render(str(int(fps)), 0, foreground), (0, 0))
  pygame.display.flip()
pygame.quit()
