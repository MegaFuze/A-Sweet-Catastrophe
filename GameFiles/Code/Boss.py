import pygame
from math import sin, cos, atan2,radians,pi

from GameFiles.Code.SpriteSheetManagement import *
from GameFiles.Code.Settings import *
from GameFiles.Code.Bullets import BOSSBullets
from random import randint

class BOSS(pygame.sprite.Sprite):
    def __init__(self,camera, pos, entity_group, player,enem_bullets, map_size,parent):
        super().__init__(camera)
        self.parent = parent
        self.camera = camera
        self.spawn_timer = 60
        self.timer_tick = 1
        self.spawned = False
        self.map_size = map_size


        self.image = pygame.image.load("GameFiles/Assets/TopDown/Enemies/BOSS.png").convert_alpha()
        self.og_image = self.image.copy()
        self.size = pygame.Vector2(self.image.get_size())
        self.rect = self.image.get_rect(topleft=pos)
        self.stable_rect =self.rect.copy()
        self.hitbox =self.rect.copy().inflate(-75,-75)
        self.offset_rect = self.rect.copy()

        self.pos = pygame.Vector2(self.hitbox.center)
        self.fight_mode = False

        self.speed = 2.7
        self.face_rads = 0
        self.directions = pygame.Vector2(0,0)

        #idea: to make sure that the player doesnt crash into the boss before it spawns, add a reference to the entities group to later have the boss be added on
        self.entities = entity_group #SPRITE GROUP()
        self.player = player #sprite
        self.enem_bullets = enem_bullets #SPRITE GROUP()

        self.is_an_enemy = True

        self.max_hp = 2100
        self.hp = self.max_hp
        self.collision_dmg = 100
        self.bullet_dmg = 100
        self.killed = False

        self.z_layer = layers['overlap']

        self.visible = False

        self.has_light = True
        self.light = pygame.image.load("GameFiles/Assets/TopDown/Effects/LightOutline.png").convert_alpha()
        self.light = pygame.transform.scale(self.light,(600,600))
        self.light_rect = self.light.get_rect(center=self.rect.center)

        self.pupil_img = pygame.image.load("GameFiles/Assets/TopDown/Enemies/pupil.png").convert_alpha()
        self.pupil_origin = pygame.Vector2(self.size.x/2, self.size.y/2)
        self.pupil_rect = self.pupil_img.get_rect(center = self.pupil_origin)
        self.pupil_range = 15

        #Attack Attributes
        #origin position of where the boss's position will be based off of
        self.attack_origin = pygame.Vector2(self.map_size.x/2,self.map_size.y/2)
        self.attack_speed = 2.5
        self.shoot_speed = 4
        self.dash_speed = 4
        self.spin_range = 200
        self.spin_speed = 5

        self.angle = 0 #degrees
        self.angle_speed = 4 #degrees
        self.rads = 0

        self.spray_bullet_count = 8
        self.spray_bullet_speed = 5
        self.spray_shot_cooldown_max = 15
        self.spray_shot_cooldown_index = self.spray_shot_cooldown_max
        self.shoot_shake_intensity = 10

        self.attack_duration_max = 200
        self.attack_duration_min = 150
        self.attack_duration = randint(self.attack_duration_min,self.attack_duration_max)

        self.chase_speed = 2

        self.cone_shot_cooldown_max = 20
        self.cone_shot_cooldown= self.cone_shot_cooldown_max
        self.cone_shot_count = 3
        self.cone_rads = pi/8*3 #shoots in a 90 degree cone
        self.cone_shot_speed = 10

        self.attack_dict ={
            "0":"spin_spray",
            "1":"sprayer",
            "2":"chase_n_shoot"
        }
        self.attack_type = "chase_n_shoot"#self.attack_dict[str(randint(0, len(self.attack_dict) - 1))]

        self.hover_rads = 0 #only updates when player has obtained weapon
        self.special = None

        self.shoot_sfx = pygame.mixer.Sound(sfx['BOSSShoot'])
        self.appear_sfx = pygame.mixer.Sound(sfx['BOSSAppear'])
        self.hurt_sfx = pygame.mixer.Sound(sfx['Hurt'])

    def tick_spawn_timer(self):
        self.spawn_timer -= self.timer_tick
        if self.spawn_timer <= 0:
            self.spawned = True
            self.entities.add(self)
            self.visible = True
            self.camera.shake_camera = True
            self.appear_sfx.play()
    def get_angle(self):
        distance_x = self.player.hitbox.centerx - self.pos.x
        distance_y = self.player.hitbox.centery - self.pos.y

        self.face_rads = atan2(distance_y,distance_x)
        self.directions.xy = cos(self.face_rads)*self.speed,sin(self.face_rads)*self.speed

    def move_basic(self):
        self.pos.x += self.directions.x*self.speed
        self.pos.y += self.directions.y*self.speed

        self.hitbox.center = round(self.pos)
        self.stable_rect.center = self.hitbox.center
        self.rect.center = self.hitbox.center

    def animate_pupil(self):
        x = self.pupil_origin.x+(self.directions.x*self.pupil_range)
        y = self.pupil_origin.y+(self.directions.y*self.pupil_range)

        self.pupil_rect.center = (x,y)
        self.image.blit(self.pupil_img,self.pupil_rect)

    def collision_check(self):
        #note to self: maybe write this on the topdown.py file instead?
        if self.hitbox.colliderect(self.player.hitbox) and not self.player.invis:
            self.player.invis = True
            self.player.hp -= self.collision_dmg
            self.parent.plr_hp_text.update_text(f"Player HP:{self.player.hp}/{self.player.max_hp}")
            self.hurt_sfx.play()

    def fight_actions(self):
        '''Overall BossFight Mode is here, calls some functions outside of this function,
         function underneath this function except for self.update() will contribute to this function'''
        self.angle += self.angle_speed
        if self.angle >= 360: self.angle-=360
        self.rads = radians(self.angle)
        self.attack_duration-=1
        if self.attack_duration <= 0:
            self.attack_duration = randint(self.attack_duration_min,self.attack_duration_max)
            self.attack_type = self.attack_dict[str(randint(0, len(self.attack_dict) - 1))]

        #self.spin_sprayer_attack()
        if self.attack_type == "spin_spray":self.spin_sprayer_attack()
        elif self.attack_type == "sprayer": self.spray_shot()
        elif self.attack_type == "chase_n_shoot": self.chase_n_shoot()
        pass

    def spin_sprayer_attack(self):
        self.pos.x = self.attack_origin.x+(cos(self.rads)*self.spin_range)
        self.pos.y = self.attack_origin.y+(sin(self.rads)*self.spin_range)

        self.hitbox.center = self.pos
        self.rect.center = self.hitbox.center
        self.stable_rect.center = self.hitbox.center
        self.spray_shot()

    def chase_n_shoot(self):
        self.pos.x += self.directions.x*self.chase_speed
        self.pos.y += self.directions.y*self.chase_speed

        self.hitbox.center = self.pos
        self.rect.center = self.hitbox.center
        self.stable_rect.center = self.hitbox.center

        self.cone_shot_cooldown -= 1
        if self.cone_shot_cooldown <= 0:
            self.cone_shot_cooldown = self.cone_shot_cooldown_max
            for bullet_count in range(self.cone_shot_count):
                single_rad = self.cone_rads/ self.cone_shot_count
                rads = (self.face_rads-(self.cone_rads/2)+(bullet_count*single_rad))
                bullet = BOSSBullets(self.camera, self.rect.center, self.bullet_dmg, rads, self.cone_shot_speed)
                self.enem_bullets.add(bullet)
            self.shoot_sfx.play()


    def spray_shot(self):

        self.spray_shot_cooldown_index-= 1
        if self.spray_shot_cooldown_index <= 0:
            self.spray_shot_cooldown_index = self.spray_shot_cooldown_max

            #CameraShakeEffect
            self.camera.shake_camera = True
            self.camera.shake_index = self.shoot_shake_intensity

            #spray shots vvvvvvvvvvvvvvvv
            for bullet_count in range(self.spray_bullet_count):
                #divides a full circle (2*pi radians) by spray bullet counter to split all rads into even directions
                #also adds self.rads to make the next set of bullets not go in the same direction as the previous set of bullets
                rads = (2*pi)/self.spray_bullet_count*bullet_count + self.rads

                bullet = BOSSBullets(self.camera,self.rect.center,self.bullet_dmg,rads,self.spray_bullet_speed)
                self.enem_bullets.add(bullet)
            self.shoot_sfx.play()



    def update(self):
        if not self.killed:
            if not self.spawned: self.tick_spawn_timer()
            else:
                self.image = self.og_image.copy()
                self.get_angle()
                self.animate_pupil()
                self.collision_check()
                #fight mode is enabled when player obtains weapon, enabled in Game.py with the self.pick_up_item() function
                if self.fight_mode: self.fight_actions()
                else: self.move_basic()
