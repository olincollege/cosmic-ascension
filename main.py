import pygame
from pygame.locals import *
import sys
import random
from view import View
from model import Model
from model import Platform
from controller import Controller

WIDTH = 450
HEIGHT = 400

FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
vector = pygame.math.Vector2

ground = Platform(
    surf=pygame.Surface((WIDTH, 20)), color=(255, 0, 0), topleft=(0, HEIGHT - 10)
)
platforms = pygame.sprite.Group()
platforms.add(ground)

model = Model(platforms)
view = View(model)
controller = Controller(model)

for x in range(random.randint(5, 6)):
    platform = Platform()
    platforms.add(platform)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                controller.jump()
    controller.move()

    displaysurface.fill((0, 0, 0))
    view.draw(displaysurface)
    pygame.display.update()
    FramePerSec.tick(60)
