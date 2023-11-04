import pygame
from math import ceil
from GameFiles.Code.Settings import *
from GameFiles.Code.SpriteSheetManagement import *
class Background(pygame.sprite.Sprite):
    def __init__(self, screen):
        #self.image = pygame.image.load("GameFiles/Assets/Topdown/Background/BG.png")
        self.screen = screen
        self.fps = FPS
        self.anim_speed = 8
        self.prev_anim_index = 0
        self.anim_index = 0

        self.image_frames = import_sprites("GameFiles/Assets/Topdown/Background/BG.png",(320,180))
        self.image = self.image_frames[0]

        self.image_size = pygame.Vector2(self.image.get_size())
        self.screen_size = pygame.Vector2(self.screen.get_size())
        self.img_rect_speed = 2

        self.all_bg_images = pygame.sprite.Group()
        self.background_setup()

    def background_setup(self):
        for row in range(ceil(self.screen_size.y/self.image_size.y)+1):
            for col in range(ceil(self.screen_size.x/self.image_size.x)+1):
                x = col*self.image_size.x-self.image_size.x
                y = row*self.image_size.y-self.image_size.y
                image = BackgroundImage(self.screen,self.image,(x,y),self.img_rect_speed)
                self.all_bg_images.add(image)
    def update(self):
        self.all_bg_images.update()
        self.all_bg_images.draw(self.screen)

class BackgroundImage(pygame.sprite.Sprite):
    def __init__(self,screen,surf,pos,speed):
        super().__init__()
        self.screen = screen
        self.image = surf
        self.pos = pygame.Vector2(pos)
        self.speed = speed
        self.rect = self.image.get_rect(topleft = self.pos)
        self.image_size = pygame.Vector2(self.image.get_size())

    def move(self):
        self.pos.x += self.speed
        self.pos.y += self.speed
        if self.pos.x >= WIN_W: self.pos.x -= (ceil(WIN_W/ self.image_size.x)+1)*self.image_size.x
        if self.pos.y >= WIN_H: self.pos.y -= (ceil(WIN_H/ self.image_size.y)+1)*self.image_size.y
        self.rect.topleft = self.pos

    def update(self):
        self.move()

