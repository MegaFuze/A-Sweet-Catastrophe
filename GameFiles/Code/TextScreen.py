import pygame
from GameFiles.Code.TextBox import *
from GameFiles.Code.Settings import *
from GameFiles.Code.RectPart import *

class TextScreen(pygame.sprite.Sprite):
    def __init__(self,screen, inputs, parent,text=None,rect_part = None, **kwargs ):
        super().__init__()
        self.screen = screen
        self.inputs = inputs
        self.parent = parent
        self.text_size = 50

        self.image = pygame.Surface((WIN_W,WIN_H))
        self.rect = self.image.get_rect(topleft = (0,0))

        if not text:self.text = TextBox(ControlsText,"White",50,(WIN_W/2,100),"midtop")
        else: self.text = TextBox(text, "White", 50, (WIN_W / 2, WIN_H/2), rect_part)
        self.switch_level = False #Never to be updated here, only in topdown mode
        self.special = None
    def get_input(self):
        if self.inputs['tap']['space']:
            self.parent.start_level()
            self.kill()
    def update(self):
        self.screen.blit(self.image,self.rect)
        self.screen.blit(self.text.image, self.text.rect)
        self.get_input()

