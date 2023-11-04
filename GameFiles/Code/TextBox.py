import pygame
from GameFiles.Code.RectPart import *
from GameFiles.Code.Settings import *

class TextBox(pygame.sprite.Sprite):
    def __init__(self,text, color, size, pos, rect_part = "topleft", **kwargs):
        self.font = None
        self.group = None #probably better if i named it group and not camera, im very inconsistent with variable names :D
        if "group" in kwargs: super().__init__(kwargs['group']); self.group = kwargs['group']
        else: super().__init__()
        if "font" in kwargs: self.font = kwargs['font']

        self.text = text
        self.color = color
        self.size = size
        self.pos = pygame.Vector2(pos)
        self.rect_part = rect_part

        self.z_layer = layers['overlap']
        self.visible = True

        #overwrites attribute
        if self.font: self.font = pygame.font.Font(f'{self.font}',self.size)
        else: self.font = pygame.font.Font(None,self.size)

        self.image = self.font.render(str(self.text),False,self.color)
        self.rect = get_rect_plus(self.image,self.pos,self.rect_part)

        if self.group:
            self.offset_rect = self.rect.copy()
            self.stable_rect = self.rect.copy()


    def update_text(self,text):
        self.text = text
        self.image = self.font.render(str(self.text),False,self.color)
        self.rect = get_rect_plus(self.image,self.pos,self.rect_part)

    def update_color(self,color):
        self.color = color
        self.image = self.font.render(self.text, False, self.color)
        self.rect = get_rect_plus(self.image, self.pos, self.rect_part)
