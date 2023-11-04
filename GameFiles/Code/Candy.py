import pygame
from GameFiles.Code.RectPart import *
class Candy(pygame.sprite.Sprite):
    def __init__(self,surf,pos,val,rect_part = "topleft"):
        super().__init__()
        self.image = surf
        self.pos = pygame.Vector2(pos)
        self.rect_part = rect_part
        self.rect = get_rect_plus(self.image,pos,rect_part)
        self.hitbox = self.rect.copy()

        self.val = val
        self.name = None

    def follow_mouse(self,mouse_pos):
        self.rect.center = mouse_pos
        self.hitbox.center = mouse_pos







