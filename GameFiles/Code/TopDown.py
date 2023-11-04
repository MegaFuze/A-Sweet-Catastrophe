import pygame
import os

from GameFiles.Code.Player import *
from GameFiles.Code.Tiles import *
from GameFiles.Code.TestMap import *
from GameFiles.Code.Camera import *
from GameFiles.Code.ManageCSV import *
from GameFiles.Code.Boss import *
from GameFiles.Code.TextBox import TextBox

class TopDownLevel(pygame.sprite.Sprite):
    def __init__(self,screen,input,mouse_pos,level, all_tiles, parent):
        super().__init__()
        self.parent = parent
        self.screen = screen
        self.input = input
        self.mouse_pos = mouse_pos
        self.level = level

        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.plr_bullets = pygame.sprite.Group()
        self.enem_bullets = pygame.sprite.Group()
        self.pushable_obj = pygame.sprite.Group()
        self.triggers = pygame.sprite.Group()
        self.entities = pygame.sprite.Group() #walls, enemies, obstacles
        self.tile_size = 100
        self.camera = Camera(self.player,self.mouse_pos)
        self.all_tiles = all_tiles
        self.layers = {}
        self.boss = pygame.sprite.GroupSingle()
        self.items = pygame.sprite.Group()



        self.map_size_obtained = False
        self.map_size = pygame.Vector2(0,0)


        self.build_level()

        self.plr_hp_text = TextBox(f"Player HP:{self.player.sprite.hp}/{self.player.sprite.max_hp}","White",60,(0,WIN_H),"bottomleft")
        self.boss_hp_text = TextBox(f"BOSS HP:{self.boss.sprite.hp}/{self.boss.sprite.max_hp}", "White", 80, (WIN_W/2, 0), "midtop")

        self.shadow_shade = pygame.image.load("GameFiles/Assets/TopDown/Effects/ShadowShade.png").convert_alpha()
        self.shadow_shade.set_alpha(150)

        self.white_screen = pygame.Surface((WIN_W,WIN_H))
        self.white_screen.fill((255,255,255))
        self.white_screen_alpha = 0
        self.white_screen.set_alpha(self.white_screen_alpha)

        self.switch_level = False
        self.switch_level_sfx = pygame.mixer.Sound(sfx['NextLevel'])
        self.hurt_sfx = pygame.mixer.Sound(sfx['Hurt'])


    def build_level(self):
        for layer_name, layer_data in self.all_tiles.items():
            path = f"GameFiles/Levels/{self.level}/{self.level}_{layer_name}.csv"
            if os.path.exists(path):
                self.layers.update({str(layer_name) : import_csv(path)})

                if not self.map_size_obtained: self.map_size.xy = self.obtain_map_size(self.layers[layer_name])

                for row, row_array in enumerate(self.layers[layer_name]):
                    for col, tile_val in enumerate(row_array):
                        x,y = col*self.tile_size, row*self.tile_size
                        if tile_val != '-1':
                            if layer_name == "Player":

                                player = Player(self.camera, self.screen, (x, y), self.input, self.mouse_pos,self.obstacles, plr_bullets=self.plr_bullets,enem_bullets=self.enem_bullets, entities=self.entities, pushable = self)
                                self.player.add(player)
                            elif layer_name == "BOSS":
                                boss = BOSS(self.camera,(x,y),self.entities,self.player.sprite,self.enem_bullets, self.map_size,self)
                                self.boss.add(boss)
                            elif layer_name == "Buster":
                                tile_surf = layer_data['frames'][int(tile_val)]
                                item = Tile(self.camera, tile_surf, (x, y), layer_data)
                                self.items.add(item)
                            elif layer_name == "Pushable":
                                tile_surf = layer_data['frames'][int(tile_val)]
                                tile = PushableTile(self.camera, tile_surf, (x, y), layer_data)
                                self.tiles.add(tile)
                                self.pushable_obj.add(tile)
                            elif layer_name == "Trigger":

                                tile = Trigger(self.camera, (x, y), layer_data, tile_val)
                                self.tiles.add(tile)
                                self.triggers.add(tile)
                            else:
                                # picks surf from array of respective layer/tilesheet
                                tile_surf = layer_data['frames'][int(tile_val)]
                                tile = Tile(self.camera,tile_surf , (x, y),layer_data)
                                self.tiles.add(tile)
                            if layer_data['collidable']:
                                self.obstacles.add(tile)
                                self.entities.add(tile)



    '''    def kill_bullets(self):
        for bullet in self.plr_bullets:
            for entity in self.entities:
                if bullet.hitbox.colliderect(entity.hitbox): bullet.kill'''
    '''def push_objects(self):
        player = self.player.sprite
        for obj in self.pushable_obj:
            if obj.hitbox.colliderect(player.hitbox):'''


    def obtain_map_size(self,map):
        rows = len(map)-1 #No. of arrays in matrix
        columns = len(map[0])-1 #length of 1st array of matrix
        return columns*self.tile_size,rows*self.tile_size
    def player_died(self):
        self.parent.start_level()
        self.kill()

    def draw(self):
        self.tiles.draw(self.screen)
        self.player.draw(self.screen)

    def pick_up_item(self):
        """Buster is the only item that is in the game as of making this, so it will always pick a Buster up regardless of what you picked up"""
        for item in self.items:
            if item.rect.colliderect(self.player.sprite.hitbox):
                buster = Buster(self.camera,self.player.sprite,self.plr_bullets,self.player.sprite.shoot_bool)
                self.player.sprite.item.add(buster)
                item.kill()
                self.player.sprite.face_mouse = True
                self.camera.camera_pan_on = True
                self.boss.sprite.fight_mode =True
                self.switch_level_sfx.play()
                '''if self.parent.music_pick != 'BOSS':
                    #self.parent.music_pick = "BOSS"
                    pygame.mixer.music.load(self.parent.music[self.parent.music_pick])
                    pygame.mixer.music.play()'''

    def trigger_collision(self):
        if not self.switch_level:
            for trigger in self.triggers:
                if trigger.hitbox.colliderect(self.player.sprite):
                    self.switch_level = True
                    self.parent.level_name = str(trigger.val)
                    self.switch_level_sfx.play()

    def enem_bullet_collisions(self):
        '''Player bullet collisions are handled in player.py... dammit Im getting even more disorganized.
        like why tf didnt i do player bullet collisions in here instead of player.py
        oh well i will probably fix this if i ever update this messy game but for now

        "thank you mario! but our [player bullet collision function] is in [another fucking script]!"
        -NES toad probably (SMB)
        update: nvm i actually added it now under this function woo now less pain
        '''
        player = self.player.sprite
        for bullet in self.enem_bullets:
            if bullet.hitbox.colliderect(player.hitbox) and not player.invis:
                player.hp -= bullet.damage_val #gets hit
                player.invis = True
                self.plr_hp_text.update_text(f"Player HP:{self.player.sprite.hp}/{self.player.sprite.max_hp}")

                bullet.kill()
                self.hurt_sfx.play()
                break

    def plr_bullet_collisions(self):
        '''yay'''
        for bullet in self.plr_bullets:
            for entity in self.entities:
                if bullet.hitbox.colliderect(entity.hitbox):
                    bullet.bullet_landed = True
                    if entity.is_an_enemy: entity.hp -= bullet.damage_val
                    if entity == self.boss.sprite:
                        self.boss_hp_text.update_text(f"BOSS HP:{self.boss.sprite.hp}/{self.boss.sprite.max_hp}")
                        if self.boss.sprite.hp <=0 and not self.boss.sprite.killed:
                            self.boss.sprite.killed = True
                            self.camera.shake_index = 120
                            self.camera.shake_camera = True
                            self.enem_bullets.empty()
                    bullet.kill()
                # play sound here I guess...

    def boss_killed(self):
        self.white_screen_alpha+= 2
        self.white_screen.set_alpha(self.white_screen_alpha)
        self.screen.blit(self.white_screen,(0,0))
        if self.white_screen_alpha >= 300:
            self.parent.end_screen()
            self.kill()
            pygame.mixer.music.stop()



    def update(self):
        #if self.input['tap']['space']: self.camera.camera_pan_on = not self.camera.camera_pan_on
        self.camera.draw_special()
        self.player.update()
        self.plr_bullets.update()
        self.enem_bullets.update()
        self.plr_bullet_collisions()
        self.enem_bullet_collisions()
        self.boss.update()
        self.pick_up_item()
        self.pushable_obj.update()
        self.triggers.update()
        self.trigger_collision()
        self.screen.blit(self.shadow_shade, (0, 0))
        self.screen.blit(self.plr_hp_text.image,self.plr_hp_text.rect)
        if self.boss.sprite.fight_mode:self.screen.blit(self.boss_hp_text.image, self.boss_hp_text.rect)
        if self.player.sprite.hp <= 0:
            self.player_died()
        if self.boss.sprite.killed:self.boss_killed()




        return