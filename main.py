from game import Game

if __name__ == '__main__':
    game = Game()
    game.start()

# import pygame
# from pygame.locals import *
# import sys
# import random
# from view import View
# from model import Model
# from model import Platform
# from controller import Controller

# WIDTH = 450
# HEIGHT = 400

# FramePerSec = pygame.time.Clock()
# displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
# vector = pygame.math.Vector2

# ground = Platform(surf=pygame.Surface((WIDTH, 20)), color=(255,0,0), topleft=(0, HEIGHT - 10))
# platforms = pygame.sprite.Group()
# platforms.add(ground)

# model = Model(platforms)
# view = View(model)
# controller = Controller(model)

# # for x in range(random.randint(5, 6)):
# #     platform = Platform()
# #     platforms.add(platform)

# while True:
#     # print(model.platforms)
#     for platform in model.platforms:
#         print(platform.rect)
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 controller.jump()
#     plat = Platform(surf=pygame.Surface((10, 5)), topleft=(0, 430))
#     model._platforms.add(plat)
#     # model.platform_generation()
#     controller.move()
#     if model.player.rect.top <= HEIGHT / 3:
#         model.player.position.y += abs(controller._velocity.y)
#         for plat in model.platforms:
#             plat.rect.y += abs(controller._velocity.y)
#             if plat.rect.top >= HEIGHT:
#                 plat.kill()
#     # print(pygame.sprite.spritecollide(model.player, model.platforms, False))
#     displaysurface.fill((0,0,0))
#     view.draw(displaysurface)
#     pygame.display.update()
#     FramePerSec.tick(60)
