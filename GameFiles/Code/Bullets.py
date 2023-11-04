import pygame
from math import sin,cos
from GameFiles.Code.Settings import *
class Bullets(pygame.sprite.Sprite):
    def __init__(self,camera,pos,damage_val,radians):
        super().__init__(camera)
        self.image = pygame.Surface((40,40))
        self.image.fill((255,255,0))
        self.stable_rect = self.image.get_rect(center = pos)
        self.rect = self.stable_rect.copy()
        size_x,size_y = (self.stable_rect.size)
        self.hitbox = self.stable_rect.copy().inflate(-(size_x/2),-(size_y/2))
        self.offset_rect = self.rect.copy()
        #self.image = pygame.image.load("").convert_alpha()
        self.speed = 15
        self.z_layer = layers['main']

        self.angle_direction = pygame.Vector2(cos(float(radians)),sin(float(radians))) #After calculating where the angle of the mouse was set prior to shooting, the data will be passed here to have it move in specific angles

        self.bullet_landed = False #bool that will be used to kill bullet if set to true
        #self.entities = entities #a sprite group that stores every obstacle, enemy, and outer walls.
        if damage_val:self.damage_val = damage_val
        else: self.damage_val = 20
        self.visible = True
        self.has_light = True
        self.light = pygame.image.load("GameFiles/Assets/TopDown/Effects/LightOutline.png").convert_alpha()
        self.light = pygame.transform.scale(self.light,(200,200))
        self.light_rect = self.light.get_rect(center=self.rect.center)
        self.special = "bullet"

    def move(self):
        self.hitbox.centerx += self.speed * self.angle_direction.x
        self.hitbox.centery += self.speed * self.angle_direction.y

        self.stable_rect.center = self.hitbox.center
        self.rect.center = self.stable_rect.center


        #self.check_collisions()

    '''def check_collisions(self):
        for entity in self.entities:
            if self.hitbox.colliderect(entity.hitbox):
                self.bullet_landed = True
                if entity.is_an_enemy: entity.health -= self.damage_val
                self.kill()
                #play sound here I guess...'''
    def update(self):
        self.move()

class PlayerBullets(Bullets):
    def __init__(self,camera,pos,damage_val,radians):
        super().__init__(camera,pos,damage_val,radians)
        self.image = pygame.image.load("GameFiles/Assets/TopDown/Player/PlrBullets.png").convert_alpha()

        self.stable_rect = self.image.get_rect(center=pos)
        self.rect = self.stable_rect.copy()
        size_x, size_y = (self.stable_rect.size)
        self.hitbox = self.stable_rect.copy().inflate(-(size_x / 2), -(size_y / 2))
        self.offset_rect = self.rect.copy()

        self.speed = 15


class BOSSBullets(Bullets):
    def __init__(self,camera,pos,damage_val,radians,speed):
        super().__init__(camera,pos,damage_val,radians)
        self.image = pygame.image.load("GameFiles/Assets/TopDown/Enemies/BOSSBullets.png").convert_alpha()

        self.stable_rect = self.image.get_rect(center=pos)
        self.rect = self.stable_rect.copy()
        size_x, size_y = (self.stable_rect.size)
        self.speed = speed
        self.hitbox = self.stable_rect.copy().inflate(-(size_x / 2), -(size_y / 2))
        self.offset_rect = self.rect.copy()

        self.speed = speed
        self.lifespan = 250
        self.z_layer =layers['overlap']

    def update(self):
        self.move()
        self.lifespan-= 1
        if self.lifespan <= 0: self.kill()
