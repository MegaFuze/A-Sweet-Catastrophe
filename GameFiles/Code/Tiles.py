import pygame
from GameFiles.Code.Settings import *
from math import floor

class Tile(pygame.sprite.Sprite):
    def __init__(self,camera,surf,pos,layer_data,**kwargs):
        super().__init__(camera)
        self.special = layer_data['special']

        self.image = surf
        self.pos = pygame.Vector2(pos)
        self.offset_pos = layer_data['offset']
        self.pos.x -= self.offset_pos.x
        self.pos.y -= self.offset_pos.y
        self.stable_rect = self.image.get_rect(topleft = pos)
        self.stable_rect.center = self.pos
        self.rect = self.stable_rect.copy()
        self.hitbox = self.rect.copy().inflate(0,-40)
        self.offset_rect = self.rect.copy()
        self.z_layer = layers[layer_data['z_layer']]
        self.is_an_enemy = False
        self.visible = True
        self.has_light = False

class PushableTile(Tile):
    def __init__(self,camera,surf,pos,layer_data,**kwargs):
        super().__init__(camera,surf,pos,layer_data)
        self.push_speed = 10
        self.push_index = 0
        self.push_max = pygame.Vector2(tile_size,tile_size)
        self.pushing = False
        self.push_direction = pygame.Vector2(0,0)
    def push_tile(self):
        if self.pushing:
            if self.push_direction.x !=0:
                self.hitbox.centerx += self.push_speed*self.push_direction.x
                self.push_index+= self.push_speed
                if self.push_index>= self.push_max.x:
                    gap = (self.push_index- self.push_max.x)*self.push_direction.x #overlap val
                    self.hitbox.centerx += gap
                    self.pushing = False
                    self.push_index = 0
                    self.push_direction.x = 0
                self.stable_rect.centerx = self.hitbox.centerx
                self.rect.centerx = self.stable_rect.centerx
            elif self.push_direction.y != 0:
                self.hitbox.centery += self.push_speed*self.push_direction.y
                self.push_index += self.push_speed
                if self.push_index >= self.push_max.y:
                    gap = (self.push_index - self.push_max.y) * self.push_direction.y  # overlap val
                    self.hitbox.centery += gap
                    self.pushing = False
                    self.push_index = 0
                    self.push_direction.y = 0
                self.stable_rect.centery = self.hitbox.centery
                self.rect.centery = self.stable_rect.centery

    def update(self):
        self.push_tile()

class Trigger(pygame.sprite.Sprite):
    def __init__(self,camera,pos,layer_data,val,**kwargs):
        super().__init__(camera)
        self.frames = layer_data['frames']
        self.image = self.frames[0]
        self.image.set_colorkey("black")
        self.val = val
        self.anim_index = 0
        self.anim_speed = .15

        self.pos = pygame.Vector2(pos)
        self.offset_pos = layer_data['offset']
        self.pos.x -= self.offset_pos.x
        self.pos.y -= self.offset_pos.y

        self.stable_rect = self.image.get_rect(topleft=pos)
        self.stable_rect.center = self.pos
        self.rect = self.stable_rect.copy()
        self.hitbox = self.rect.copy()
        self.offset_rect = self.rect.copy()
        self.z_layer = layers[layer_data['z_layer']]
        self.is_an_enemy = False
        self.visible = True
        self.has_light = False
    def animate(self):
        self.anim_index += self.anim_speed
        if self.anim_index >= len(self.frames): self.anim_index = 0
        self.image= self.frames[floor(self.anim_index)]
    def update(self):
        self.animate()

