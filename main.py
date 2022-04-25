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

STEP = USEREVENT + 0

post_event = lambda e:pygame.event.post(pygame.event.Event(e))


class Particle:
  def __init__(self, wave, index, _len=0):
    self.wave, self.index = wave, index
    self.wave.append(self)
    self.held = False
    self.pos, self.velocity, self.accel = 0, 0, 0
    self.neighbours = []
    if self.index:
      self.neighbours.append(self.wave[self.index - 1])
      self.wave[self.index - 1].neighbours.append(self)
  
  def screen_pos(self, rect):
    pos = vector((self.index + 0.5)/len(self.wave), self.pos + 0.5)
    pos = pos.elementwise()*rect.size + rect.topleft
    return int(pos.x), int(pos.y)
  
  def update(self):
    if self.neighbours:
      self.accel = sum(i.pos-self.pos for i in self.neighbours)
  
  def move(self):
    if not self.held:
      self.velocity += self.accel
      self.pos += self.velocity
      self.pos = round(self.pos, 10)


class Wave(UserList):
  def __init__(self, particles):
    super().__init__(map(partial(Particle, self, _len=particles), range(particles)))
    self._selected = 0
    self[0].held, self[-1].held = True, True
  
  def __call__(self, key):
    if key == K_UP:
      self.selected.pos -= 0.05
    elif key == K_DOWN:
      self.selected.pos += 0.05
    elif key == K_RIGHT:
      self._selected += 1
    elif key == K_LEFT:
      self._selected -= 1
    elif key == K_BACKSPACE:
      self.selected.held = not self.selected.held
    self._selected = (self._selected+len(self))%len(self)
  
  @property
  def selected(self):
    return self[self._selected]
  
  def draw(self, surf, rect):
    for pair in zip(self, self.data[1:]):
      pygame.draw.line(surf, (0, 0, 0), pair[0].screen_pos(rect), pair[1].screen_pos(rect))
    
    for particle in self:
      size = 20 if particle.index == self._selected else 10
      color = (0, 0, 0) if particle.held else foreground
      pygame.draw.circle(surf, color, particle.screen_pos(rect), size)


wave1 = Wave(15)
pause = True

while True:
  clock.tick(30)
  fps = clock.get_fps()
  screen.fill(background)
  
  if pygame.event.get(QUIT):
    break
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        pygame.event.post(pygame.event.Event(QUIT))
      elif event.key == K_p:
        pygame.time.set_timer(USEREVENT, 150 * pause)
        pause = not pause
      elif event.key == K_SPACE:
        if pause:
          post_event(STEP)
      elif event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_BACKSPACE):
        wave1(event.key)
    elif event.type == STEP:
      for particle in wave1:
        particle.update()
      for particle in wave1:
        particle.move()
  
  wave1.draw(screen, screen_rect)
  if pause:
    pygame.draw.rect(screen, foreground, (vector(screen_rect.topright) + (-55, 5), (20, 50)))
    pygame.draw.rect(screen, foreground, (vector(screen_rect.topright) + (-25, 5), (20, 50)))
  
  screen.blit(font.render(str(int(fps)), 0, foreground), (0, 0))
  pygame.display.flip()
pygame.quit()
