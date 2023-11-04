import pygame
from random import randint

from GameFiles.Code.Settings import *
class Particles(pygame.sprite.Sprite):
    def __init__(self,pos, color = "white",**kwargs):
        if "groups" in kwargs:super().__init__(kwargs['groups'])
        else: super().__init__()
        self.pos = pygame.Vector2(pos)
        self.lifespan = randint(15,25)
        self.life_tick_speed = 1
        self.speed = randint(1,2)
        self.directions = pygame.Vector2(0,0)

        size = randint(5,15)
        self.image = pygame.Surface((size,size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center = self.pos)
        self.stable_rect = self.rect.copy() #for stability when camera shakes
        self.offset_rect = self.rect.copy() #for camera
        self.z_layer = layers['particles']
        self.visible = True
        self.has_light =  False
        self.light = pygame.image.load("GameFiles/Assets/TopDown/Effects/LightOutline.png")

    def move(self):
        self.pos.x += self.directions.x*self.speed
        self.pos.y += self.directions.y*self.speed

        self.stable_rect.center = self.pos
        self.rect.center = self.stable_rect.center

    def lifespan_tick(self):
        self.lifespan -= self.life_tick_speed
        if self.lifespan <= 0: self.kill()

    def update(self):
        self.move()
        self.lifespan_tick()

class PlayerParticles(Particles):
    def __init__(self,pos,color,**kwargs):
        super().__init__(pos,color,**kwargs)
        if "directions" in kwargs: self.directions.xy = kwargs["directions"]