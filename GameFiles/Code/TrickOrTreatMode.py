import pygame
from random import randint
from GameFiles.Code.Settings import *
from GameFiles.Code.Candy import *
from GameFiles.Code.SpriteSheetManagement import *
from GameFiles.Code.NPCs import *

#ya know what? I noticed that the longer I go working on this project, the lazier I get... Im legit just manually putting candy sprites in rn lol
class TrickOrTreat(pygame.sprite.Sprite):
    def __init__(self,screen, inputs, mouse_pos, parent):
        super().__init__()
        self.parent = parent #game Instance
        self.screen = screen
        self.inputs = inputs
        self.mouse_pos = mouse_pos

        self.NPC_frames ={
            "0": import_sprites("GameFiles/Assets/TrickOrTreat/NPCs/PumpkinMan.png",(240,270)),
            "1": import_sprites("GameFiles/Assets/TrickOrTreat/NPCs/Soystein.png", (240, 270)),
            "2": import_sprites("GameFiles/Assets/TrickOrTreat/NPCs/Ghost.png", (240, 270)),
            "3": import_sprites("GameFiles/Assets/TrickOrTreat/NPCs/PygameDrip.png", (240, 270)),
            "4": import_sprites("GameFiles/Assets/TrickOrTreat/NPCs/BOSS.png", (240, 270)),

        }

        self.NPC_counter = 0
        self.points = 0
        self.NPC = pygame.sprite.GroupSingle()
        self.NPC_sprites = import_sprites("",)

        self.candy_grabbed = False
        self.selected_candy = pygame.sprite.GroupSingle()
        self.requested_candy = pygame.sprite.GroupSingle()
        self.req_candy_pos = (WIN_W/2,50)

        self.candies = pygame.sprite.Group()
        self.candy_sprites = import_sprites("GameFiles/Assets/TrickOrTreat/Candies/Candies.png",(200,200))
        self.candy_mini_sprites = import_sprites("GameFiles/Assets/TrickOrTreat/Candies/CandiesMini.png", (100,100) )



        self.center_spacing = 50
        self.center_pos = pygame.Vector2(WIN_W/2,WIN_H-100)

        self.candy_1 = Candy(self.candy_sprites[0], self.center_pos,0,"midright")
        self.candy_2 = Candy(self.candy_sprites[1], self.center_pos,1,"midleft")

        self.candies.add(self.candy_1)
        self.candies.add(self.candy_2)

        self.bg_img = pygame.image.load('GameFiles/Assets/TrickOrTreat/Background/TrickOrTreatBG.png').convert_alpha()
        self.bg_rect = self.bg_img.get_rect(topleft = (0,0))

        self.fg_img = pygame.image.load('GameFiles/Assets/TrickOrTreat/Background/TrickOrTreatFG.png').convert_alpha()
        self.fg_rect = self.fg_img.get_rect(topleft = (0,0))

        self.BOSS_spawn_requirement = 4
        self.BOSS_incoming = False

        self.red_screen = pygame.Surface((WIN_W,WIN_H))
        self.red_screen.fill((255,0,0))
        self.red_screen_alpha = 0
        self.red_screen_speed = 5
        self.red_Screen_max_alpha = 180
        self.red_screen.set_alpha(self.red_screen_alpha)

        self.BOSS_settled_duration = 60
        self.BOSS_grow_speed = 20

        self.spawn_npc()

        self.NPC_overlap = False
        self.switch_level = False #never to be flipped in this mode, only in topdown mode

        self.correct_sfx = pygame.mixer.Sound(sfx['Correct'])
        self.wrong_sfx = pygame.mixer.Sound(sfx['Wrong'])
        self.jumpscare_sfx = pygame.mixer.Sound(sfx['Jumpscare'])
    def grab_candy(self):
        for candy in self.candies:
            if candy.hitbox.collidepoint(self.mouse_pos) and self.inputs['tap']['l_click']:
                self.selected_candy.add(Candy(candy.image,candy.pos,candy.val,candy.rect_part))
                self.candy_grabbed = True

    def drag_candy(self):
        if self.selected_candy:
            candy = self.selected_candy.sprite
            if self.inputs['hold']['l_click']:
                candy.hitbox.center = self.mouse_pos
                candy.follow_mouse(self.mouse_pos)

            else:
                self.candy_grabbed = False
                NPC = self.NPC.sprite
                if candy.hitbox.colliderect(NPC.rect):
                    if NPC.candy_val == candy.val:
                        NPC.image = NPC.frames[1] #Happy
                        self.correct_sfx.play()
                    else:
                        NPC.image = NPC.frames[2] #Angry
                        self.wrong_sfx.play()
                    NPC.phase = "leave"
                    NPC.settled = False


                candy.kill()

    def spawn_npc(self):
        if not self.BOSS_incoming: candy_val = randint(0,1)
        else: candy_val = 2
        self.requested_candy.add(Candy(self.candy_mini_sprites[candy_val],self.req_candy_pos,candy_val,"midtop"))
        NPC = NPCs(self.NPC_frames[f'{self.NPC_counter}'],candy_val)
        self.NPC.add(NPC)
        pass

    def BOSS_cutscene(self):
        if self.BOSS_settled_duration: self.BOSS_settled_duration -=1
        else:
            if self.red_screen_alpha < self.red_Screen_max_alpha:
                self.red_screen_alpha+= self.red_screen_speed
                self.red_screen.set_alpha(self.red_screen_alpha)
            else: self.BOSS_jumpscare()

            self.screen.blit(self.red_screen,(0,0))

    def BOSS_jumpscare(self):
        if not self.NPC_overlap:
            self.NPC_overlap = True
            self.jumpscare_sfx.play()
            pygame.mixer.music.stop()
        BOSS = self.NPC.sprite
        BOSS_size = BOSS.image.get_size()
        BOSS.image = pygame.transform.scale(BOSS.og_image.copy(),(BOSS_size[0]+self.BOSS_grow_speed, BOSS_size[1]+self.BOSS_grow_speed))
        BOSS.rect = BOSS.image.get_rect(center = BOSS.pos)
        if BOSS.image.get_size()[0] >= WIN_W:
            self.parent.start_text_screen()
            self.kill()

    def update(self):
        self.screen.blit(self.bg_img,self.bg_rect)

        #reorders Screen Blitting based on Bool Value
        if not self.NPC_overlap:
            self.NPC.draw(self.screen)
            self.screen.blit(self.fg_img,self.fg_rect)
        else:
            self.screen.blit(self.fg_img,self.fg_rect)
            self.NPC.draw(self.screen)

        if self.NPC and self.NPC.sprite:
            if self.NPC.sprite.settled and not self.BOSS_incoming:
                self.candies.draw(self.screen)
                self.requested_candy.draw(self.screen)
                self.selected_candy.draw(self.screen)

                if not self.candy_grabbed: self.grab_candy()
                else: self.drag_candy()
            elif self.NPC.sprite.settled and self.BOSS_incoming:
                self.requested_candy.draw(self.screen)
                self.BOSS_cutscene()
            self.NPC.update()

        else:
            self.NPC_counter += 1
            if self.NPC_counter == self.BOSS_spawn_requirement: self.BOSS_incoming = True
            self.spawn_npc()



