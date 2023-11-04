import pygame

from GameFiles.Code.InputManager import *
from GameFiles.Code.Game import *
from sys import exit

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(64)
WIN_W,WIN_H = 1280, 720
SCREEN = pygame.display.set_mode((WIN_W,WIN_H), pygame.DOUBLEBUF)
FPS = 60
clock = pygame.Clock()

all_inputs = {
    "l_click": False,
    "w": False,
    "a": False,
    "s": False,
    "d": False,
    "l_shift":False,
    "space":False,
    "r":False,
    "l_alt":False
}
fullscreen = False
inputs = {
    "hold":all_inputs.copy(),
    "tap":all_inputs.copy()
}
game = Game(SCREEN,inputs)

while True:
    for input in inputs['tap'].keys(): inputs['tap'][input] = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        if event.type == pygame.KEYDOWN: take_key_inputs(event,inputs)
        if event.type == pygame.KEYUP: let_go_inputs(event,inputs)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: set_active_inputs("l_click",inputs)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: inputs['hold']['l_click'] = False
    if inputs['tap']['l_alt']:
        fullscreen = not fullscreen
        if fullscreen: SCREEN = pygame.display.set_mode((SCREEN.get_width(),SCREEN.get_height()), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        else: SCREEN = pygame.display.set_mode((SCREEN.get_width(),SCREEN.get_height()), pygame.RESIZABLE | pygame.DOUBLEBUF)
    SCREEN.fill ((0,0,0))
    game.update()

    pygame.display.update()
    clock.tick(FPS)