import pygame
from random import randint
from math import ceil
from GameFiles.Code.Settings import *

class Camera(pygame.sprite.Group):
    def __init__(self,player,mouse_pos):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.max_shake_dur = 20 #duration
        self.shake_index = self.max_shake_dur
        self.shake_incr = 1 #increment
        self.offset = pygame.Vector2(0,0)
        self.dist_offset = pygame.Vector2(0,0)

        self.shake_camera = False

        #self.darkness_fx = pygame.surface.Surface((WIN_W,WIN_H))

        #self.darkness_fx.fill((30,0,70))
        #self.darkness_fx.set_alpha(170)

        #self.fx = self.darkness_fx.copy()
        #self.fx_rect = self.fx.get_rect(topleft = (0,0))

        self.player = player #GroupSingle() sprite
        self.mouse_pos = mouse_pos
        self.camera_pan_on = False
        self.view_range_divider = 4 #controls how far you can see when self.camera_pan_on is active. The smaller the number, the farther you can see
        self.error_printed = False



    def shake(self):
        self.shake_x = randint((-self.shake_index),(self.shake_index))
        self.shake_y = randint((-self.shake_index),(self.shake_index))
        for sprite in self.sprites():
            sprite.rect.center = sprite.stable_rect.center

            sprite.rect.centerx += self.shake_x
            sprite.rect.centery += self.shake_y
        self.shake_index-=self.shake_incr
        if self.shake_index <=0:
            self.shake_index = self.max_shake_dur
            self.shake_camera = False

    def draw_special(self):
        if self.shake_camera: self.shake()
        if self.player:
            player = self.player.sprite
            self.offset.x = player.hitbox.centerx - WIN_W/2
            self.offset.y = player.hitbox.centery - WIN_H/2

            msx,msy = self.mouse_pos.xy
            if self.camera_pan_on:
                self.dist_offset.x = -(player.hitbox.centerx - msx - self.offset.x)/self.view_range_divider
                self.dist_offset.y = -(player.hitbox.centery - msy - self.offset.y)/self.view_range_divider
            else: self.dist_offset.xy = 0,0

            for layer in layers.values():
                for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
                    if sprite.z_layer == layer:
                        sprite.offset_rect.centerx = sprite.rect.centerx - self.offset.x - self.dist_offset.x
                        sprite.offset_rect.centery = sprite.rect.centery - self.offset.y - self.dist_offset.y

                        if sprite.visible:
                            '''#lol the code below lags the game like hell, away it goes woooooo
                            if sprite.has_light:
                                sprite.light_rect.center = sprite.offset_rect.center
                                self.fx.blit(sprite.light, sprite.light_rect)'''
                            self.screen.blit(sprite.image,sprite.offset_rect)
            '''
            ###The code below also causes the game to lag like hell--------------
            #self.fx.set_colorkey((255,0,0))
            #self.screen.blit(self.fx,self.fx_rect)
            #self.fx = self.darkness_fx.copy()
            '''
        else:
            if not self.error_printed:
                print("Bruh, player can not be found, please insert one inside the game ya stupid idiot")
                self.error_printed = True