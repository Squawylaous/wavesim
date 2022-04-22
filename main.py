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
  def __init__(self, wave, index):
    self.wave = wave
    self.index = index
    self.wave.particles.append(self)
    self.pos, self.prev_delta, self.delta = 0, 0, 0
    self._neighbours = []
    if self.index > 0:
      self._neighbours.append(self.index - 1)
    if self.index < len(self.wave)-1:
      self._neighbours.append(self.index + 1)
  
  @property
  def neighbours(self):
    return [self.wave.particles[i] for i in self._neighbours]
  
  def update(self):
    self.delta = sum(map(op.attrgetter("prev_delta"), self.neighbours))
  
  def move(self):
    self.pos += self.delta
    self.pos = max(min(self.pos, 0.5), -0.5)
    self.prev_delta, self.delta = self.delta, 0


class Wave(UserList):
  def __init__(self, particles):
    self.data = range(particles)
    super().__init__(map(partial(Particle, self), self.data))
    print(self.data)
    self._selected = 0
  
  def __call__(self, key):
    if key not in (K_LEFT, K_RIGHT):
      for particle in self.particles:
        particle.update()
    if key == K_UP:
      self.selected.delta = -0.05
    elif key == K_DOWN:
      self.selected.delta = 0.05
    elif key == K_RIGHT:
      self._selected += 1
    elif key == K_LEFT:
      self._selected -= 1
    self._selected = (self._selected+len(self))%len(self)
    if key not in (K_LEFT, K_RIGHT):
      for particle in self.particles:
        particle.move()
  
  @property
  def selected(self):
    return self.particles[self._selected]
  
  def draw(self, surf, rect):
    for particle in self.particles:
      pos = vector((particle.index + 0.5)/len(self.particles), particle.pos + 0.5)
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
      elif event.key in (K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT):
        wave1(event.key)
  
  wave1.draw(screen, screen_rect)
  
  screen.blit(font.render(str(int(fps)), 0, foreground), (0, 0))
  pygame.display.flip()
pygame.quit()
