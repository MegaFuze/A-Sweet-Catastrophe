import pygame
from GameFiles.Code.Settings import *
class NPCs(pygame.sprite.Sprite):
    def __init__(self,frames, candy_val):
        super().__init__()
        self.frames = frames #[0] = Neutral, [1] = Happy, [2] = Angry
        self.candy_val = candy_val

        self.image = self.frames[0]
        self.og_image = self.image.copy()
        self.rect = self.image.get_rect(center = (WIN_W/4*3,WIN_H/2+50))
        self.hitbox = self.rect.copy()
        self.pos = pygame.Vector2(self.rect.center)

        self.enter_centerx_goal = WIN_W/2
        self.speed = 4
        self.phase = "enter"
        self.has_light = True
        self.light = pygame.image.load("GameFiles/Assets/TopDown/Effects/LightOutline.png").convert_alpha()
        self.light = pygame.transform.scale(self.light, (300,300))

        self.settled = False

    def enter(self):
        self.pos.x -= self.speed
        if self.pos.x <= self.enter_centerx_goal:
            self.pos.x = self.enter_centerx_goal
            self.phase = "idle"
            self.settled = True
        self.rect.centerx = self.pos.x
        self.hitbox.centerx = self.pos.x

    def leave(self):
        self.pos.x -= self.speed

        self.rect.centerx = self.pos.x
        self.hitbox.centerx = self.pos.x

        if self.rect.left <= WIN_W/4: self.kill()

    def update(self):
        if self.phase == "enter": self.enter()
        elif self.phase == "leave": self.leave()

