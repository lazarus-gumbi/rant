import pygame
from pygame.locals import *

pygame.init()
width = 400
height = 650
screen = pygame.display.set_mode((width, height))
caption = "space mafia"
pygame.display.set_caption(caption)

running = True

class Player(object):
    def __init__(self):
        self.rect = pygame.rect.Rect((64,54,16,16))
        
    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 5
        if key[pygame.K_LEFT]:
            print("down")
            self.rect.move_ip(-dist,0)
        if key[pygame.K_RIGHT]:
           self.rect.move_ip(dist, 0)
        if key[pygame.K_UP]:
           self.rect.move_ip(0, -dist)
        if key[pygame.K_DOWN]:
           self.rect.move_ip(0, dist)
           
    def draw(self, surface):
        pygame.draw.rect(screen, (0,0,128), self.rect)
        
        
player = Player()

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        screen.fill((255,255,255))
        
        player.draw(screen)
        player.handle_keys()
        pygame.display.update()
        
        clock.tick(60)

