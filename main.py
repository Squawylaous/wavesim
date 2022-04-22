import math
import operator as op
from functools import partial, reduce
from itertools import chain
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
  def __init__(self, wave):
    self.wave = wave
    self.index = len(self.wave)
    self.wave.particles.append(self)
    self.pos = 0
    self.neighbours = []
    if self.index > 0:
      self.neighbours.append(self.wave.particles[self.index - 1])
    if self.index < len(self.wave)-1:
      self.neighbours.append(self.wave.particles[self.index + 1])


class Wave:
  inputs = {K_UP:(op.attrgetter("selected.pos"), 0.05), K_DOWN:(op.attrgetter("selected.pos"), -0.05),
            K_LEFT:(op.attrgetter("_selected"), 1), K_RIGHT:(op.attrgetter("_selected"), -1)}
  
  def __init__(self, particles):
    self.particles = []
    for _ in range(particles):
      Particle(self)
    self._selected = 0
  
  def __len__(self):
    return len(self.particles)
  
  def __call__(self, key):
    try:
      key = self.inputs[key]
    except KeyError:
      pass
    else:
      key[0](self) += key[1]
    self._selected = self._selected+len(self)
    
  
  @property
  def selected(self):
    return self.particles[self._selected]
  
  def draw(self, surf, rect):
    for particle in self.particles:
      pos = vector((particle.index + 0.5)/len(self.particles), particle.pos + 0.5).elementwise()*rect.size
      pygame.draw.circle(surf, foreground, (int(pos.x), int(pos.y)), 5)


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
        wave(event.key)
  
  wave1.draw(screen, screen_rect)
  
  screen.blit(font.render(str(int(fps)), 0, foreground), (0, 0))
  pygame.display.flip()
pygame.quit()
