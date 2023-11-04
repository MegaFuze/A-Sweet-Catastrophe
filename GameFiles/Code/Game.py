import pygame
from GameFiles.Code.TopDown import *
from GameFiles.Code.TrickOrTreatMode import *
from GameFiles.Code.ManageJSON import *
from GameFiles.Code.SpriteSheetManagement import *
from GameFiles.Code.Background import *
from GameFiles.Code.TextScreen import TextScreen
from GameFiles.Code.Settings import *
class Game():
    def __init__(self,screen,input):
        self.screen = screen
        self.inputs = input
        self.mode = "menu"
        self.level_name = str(1)
        self.mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        #asset setup
        self.tiles_json_path = "GameFiles/Levels/Tiles.json"
        self.all_tiles = self.get_all_spritesheets()
        #self.every_level = self.get_all_levels() #may not be used idk

        self.level = pygame.sprite.GroupSingle()
        self.level_name = "1"#for TopDown Mode ONLY

        self.music_dir = "GameFiles/Audio/Music/"
        self.music = {
            "Sweetness": f"{self.music_dir}Sweetness.wav",
            "Chase": f"{self.music_dir}Chase.wav",
             "BOSS": f"{self.music_dir}BOSS.wav"
        }
        self.music_pick ="Sweetness"
        pygame.mixer.music.load(self.music['Sweetness'])
        pygame.mixer.music.play(-1)
        self.mode = "TrickOrTreat"

        if self.mode == "TrickOrTreat":
            level = TrickOrTreat(self.screen,self.inputs, self.mouse_pos,self)
            self.level.add(level)
        elif self.mode == "TextScreen":
            text_screen = TextScreen(self.screen,self.inputs,self)
            self.level.add(text_screen)
        else:
            if self.music_pick != 'Chase':
                self.music_pick = "Chase"
                pygame.mixer.music.load(self.music[self.music_pick])
                pygame.mixer.music.play(-1)
            level = TopDownLevel(self.screen, self.inputs, self.mouse_pos, self.level_name, self.all_tiles,self)
            self.level.add(level)




        self.bg = None
        if self.mode == 'TopDown': self.bg = Background(self.screen)

    def start_text_screen(self):
        self.mode = "TextScreen"
        text_screen = TextScreen(self.screen, self.inputs, self)
        self.level.add(text_screen)
    def start_level(self):
        if self.music_pick != 'Chase':
            self.music_pick = "Chase"
            pygame.mixer.music.load(self.music[self.music_pick])
            pygame.mixer.music.play(-1 )
        if self.mode != "TopDown": self.mode = "TopDown"
        level = TopDownLevel(self.screen, self.inputs, self.mouse_pos, self.level_name, self.all_tiles,self)
        self.level.add(level)
        if not self.bg: self.bg = Background(self.screen)

    def end_screen(self):
        #God why have i gotten to this point, this is so rushed lmao
        end_screen = TextScreen(self.screen,self.inputs,self,"Thank You For Playing!\n\nsorry for rushing the game :(\n\n to rematch boss, press SPACE","center")
        self.level.add(end_screen)

    def get_all_spritesheets(self):
        '''stores literally every spritesheet that are ARRAYS, no dicts.
        the ones in dicts are locally stored within their respective instances...

        oh yeah, i know this may seem kinda useless since the json stores most of these but
        this function exists to store this data in a way that can be passed around without redoing the process when
        heading to the next level. This will also store every single tile in an array stored in dict["tile_name"]["frames"]'''
        tiles_data = {}
        for name, data in import_json(self.tiles_json_path).items():

            path = data['path']
            size = pygame.Vector2(data['size']['w'],data['size']['h'])
            offset = pygame.Vector2(data['offset']['x'],data['offset']['y'])
            z_layer = data['z_layer']
            collidable = data["collidable"]
            special = data['special']
            hitbox_inflation = pygame.Vector2(data['hitbox_inflation']['x'],data['hitbox_inflation']['y'])
            if data['save_sprites']: frames = import_sprites(path,size);
            else: frames = None #NOT SUPPORTED / REQUIRES DIFFERENT SPRITE IMPORTING FORMAT
            tile = {
                "frames": frames,
                "path":path,
                "size": size,
                "offset":offset,
                "z_layer":z_layer,
                "collidable":collidable,
                "special": special,
                "hitbox_inflation":hitbox_inflation
            }
            tiles_data.update({name:tile})
        print(tiles_data)
        return tiles_data

    def switch_level(self):
        if self.level.sprite.switch_level:
            self.start_level()
    def update_level(self):
        self.level.update()
        return
    def update(self):
        if self.bg: self.bg.update()
        self.mouse_pos.xy = pygame.mouse.get_pos()
        self.update_level()
        self.switch_level()
        if self.inputs['tap']['r']: self.start_level()
