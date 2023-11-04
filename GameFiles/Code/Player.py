import pygame
from math import floor,ceil, atan2, degrees, pi
from GameFiles.Code.Settings import *
from GameFiles.Code.Bullets import *
from GameFiles.Code.Particles import *
from GameFiles.Code.SpriteSheetManagement import *

#holy shit this is so hardcoded lol, used for assigning self.image with array value based on self.directions.xy.
#there are a total of 8 directions
face_dir ={
    "-1,0":0,
    "-1,-1":1,
    "0,-1":2,
    "1,-1":3,
    "1,0":4,
    "1,1":5,
    "0,1":6,
    "-1,1":7,
}

class Player (pygame.sprite.Sprite):
    def __init__(self,camera,screen,pos,input,mouse_pos, obstacles, **kwargs):
        super().__init__(camera)
        self.camera = camera

        self.plr_bullets = None
        self.enem_bullets = None
        self.entities = None
        self.parent = None
        #use kwargs to add a reference to the player and enemy bullet sprite groups to make bullet collision detection much easier
        for key,val in kwargs.items():
            if key == 'plr_bullets': self.plr_bullets = val; continue
            elif key == 'enem_bullets': self.enem_bullets = val ; continue
            elif key == 'entities': self.entities = val; continue
            elif key == 'pushable': self.parent = val; continue
        self.image = None

        self.frames = import_sprites("GameFiles/Assets/Topdown/Player/Player.png",(50,100))

        self.anim_index = 0 #Based on player's facing angle and not through adding increments
        self.image = self.frames[0]
        #self.image.fill((0,255,0))
        self.screen = screen
        self.obstacles = obstacles

        self.inputs = input
        self.mouse_pos = mouse_pos

        self.inflate_size = -20,-50

        self.stable_rect = self.image.get_rect(topleft = (pos))
        self.pos = pygame.Vector2(self.stable_rect.center)
        #self.pos.x +=
        self.stable_rect.centerx = self.pos.x

        self.rect = self.stable_rect.copy()
        self.hitbox = self.rect.copy()
        self.hitbox = self.hitbox.inflate(self.inflate_size)
        self.offset_rect = self.rect.copy()

        self.speed = 9

        self.face_directions = pygame.Vector2(0,0)
        self.face_angle = 0 #degrees
        self.face_rads = 0  #radians
        self.anim_status = "Idle"
        self.anim_index = 0
        self.anim_speed = .13
        self.anim_type = f'{self.anim_status}_deg{self.face_angle}'

        self.shoot_bool = False
        self.bullet_dmg_val = 20 #Grows in value if shop feature ever comes in this game

        self.directions = pygame.Vector2(0,0)

        self.z_layer = layers["main"]

        self.hover_rads = 0
        self.hover_speed = .2
        self.hover_intensity = 4

        self.plr_particles = pygame.sprite.Group()
        self.particles_spwn_rate = 5
        self.particles_tick_rate = 1
        self.particles_tick_index = self.particles_spwn_rate

        self.visible = True
        self.face_mouse = False
        self.special = None

        self.item = pygame.sprite.GroupSingle()
        #self.item.add(Buster(self.camera,self,self.plr_bullets,self.shoot_bool))

        self.has_light = True
        self.light = pygame.image.load("GameFiles/Assets/TopDown/Effects/LightOutline.png").convert_alpha()
        self.light = pygame.transform.scale(self.light,(400,400))
        self.light_rect = self.light.get_rect(center = self.rect.center)

        self.invis = False
        self.invis_max_duration = 60
        self.invis_duration = self.invis_max_duration

        self.max_hp = 500
        self.hp = self.max_hp
        self.take_inputs = True

        self.hurt_sfx = pygame.mixer.Sound(sfx['Hurt'])
        self.push_sfx = pygame.mixer.Sound(sfx['BOSSShoot'])



    def get_input(self):
        if self.take_inputs:
            self.shoot_bool = False #resets bool for every screen refresh
            self.directions.xy = 0,0 #resets Vector2 back to origin

            input = self.inputs['hold']
            mouse_hold = self.inputs['hold']

            if input['w']: self.directions.y = -1
            if input['s']: self.directions.y =  1
            if input['a']: self.directions.x = -1
            if input['d']: self.directions.x = 1

            if mouse_hold['l_click']: self.shoot_bool = True

    def get_angle(self):
        x_dist = self.mouse_pos.x - self.offset_rect.centerx
        y_dist = self.mouse_pos.y - self.offset_rect.centery

        self.face_rads = atan2(y_dist,x_dist)
        self.face_directions.xy = cos(self.face_rads),sin(self.face_rads)

        self.face_angle = ceil(degrees(self.face_rads))
        #print(self.face_angle)

        return





    def move(self):
        if self.directions.x: self.pos.x += self.speed*self.directions.x

        self.hitbox.centerx = round(self.pos.x)
        self.stable_rect.centerx = self.hitbox.centerx
        self.rect.centerx = self.stable_rect.centerx
        self.check_collisions("horizontal")

        if self.directions.y: self.pos.y += self.speed*self.directions.y

        self.hitbox.bottom = round(self.pos.y)
        self.stable_rect.bottom = self.hitbox.bottom
        self.rect.bottom = self.stable_rect.bottom
        self.check_collisions("vertical")

    def hover_effect(self):
        self.hover_rads+= self.hover_speed
        if self.hover_rads > 2*pi: self.hover_rads = 0
        self.rect.centery += sin(self.hover_rads)* self.hover_intensity

    def check_collisions(self,direction):
        for obs in self.obstacles:
            if obs.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.directions.x > 0 and self.hitbox.right > obs.hitbox.left:
                        self.hitbox.right = obs.hitbox.left
                    elif self.directions.x < 0 and self.hitbox.left < obs.hitbox.right:
                        self.hitbox.left = obs.hitbox.right


                    self.pos.x = self.hitbox.centerx
                    self.stable_rect.centerx = self.hitbox.centerx
                    self.rect.centerx = self.stable_rect.centerx

                    if obs.special == "pushable": self.push_obstacles(obs,direction)

                elif direction == 'vertical':
                    if self.directions.y > 0 and self.hitbox.bottom > obs.hitbox.top:
                        self.hitbox.bottom = obs.hitbox.top
                    elif self.directions.y < 0 and self.hitbox.top < obs.hitbox.bottom:
                        self.hitbox.top = obs.hitbox.bottom

                    self.pos.y = self.hitbox.bottom
                    self.stable_rect.bottom = self.hitbox.bottom
                    self.rect.bottom = self.stable_rect.bottom

                    if obs.special == "pushable": self.push_obstacles(obs, direction)

    def push_obstacles(self,obj,directions):
        if not obj.pushing:
            #print("AAAA")
            if directions == "horizontal":
                obj.hitbox.centerx+= (obj.push_max.x*self.directions.x)
                collided = False
                for entity in self.entities:
                    if obj.hitbox.colliderect(entity.hitbox) and entity!= obj:
                        collided = True
                if not collided:
                    obj.pushing = True
                    obj.push_direction.x = self.directions.x
                    self.push_sfx.play()
                obj.hitbox.centerx -= (obj.push_max.x*self.directions.x)
            elif directions == "vertical":
                obj.hitbox.centery+= (obj.push_max.y*self.directions.y)
                collided = False
                for entity in self.entities:
                    if obj.hitbox.colliderect(entity.hitbox) and entity!= obj:
                        collided = True
                if not collided:
                    obj.pushing = True
                    obj.push_direction.y = self.directions.y
                    self.push_sfx.play()
                obj.hitbox.centery -= (obj.push_max.y*self.directions.y)
    def spawn_particles(self):
        self.particles_tick_index-= self.particles_tick_rate
        if self.particles_tick_index <= 0:
            self.particles_tick_index = self.particles_spwn_rate
            particles = PlayerParticles(self.rect.midbottom,"orange",groups = self.camera, directions = (0,1) )
            self.plr_particles.add(particles)

    def animate_v1(self):
        '''
        i dont like this anymore, time for animate_v2
        update: nvm im too lazy lol, hardcoding time!
        '''
        #invis animation
        if self.invis:
            self.visible = not self.visible
            if self.item: self.item.sprite.visible = not self.item.sprite.visible

            self.invis_duration -= 1
            if self.invis_duration <= 0:
                self.invis_duration = self.invis_max_duration
                self.invis = False
                self.visible = True
                if self.item: self.item.sprite.visible = True

        if self.face_mouse:
            angle_offset = 22
            angle = self.face_angle+180+angle_offset
            angle_div_by_floor45 = angle//45
            if angle_div_by_floor45 >= 8: angle_div_by_floor45 = 0
            self.image = self.frames[abs(angle_div_by_floor45)]
        else:
            #lol you can tell i gave up with this one, god im lazy
            #face_dir has keys that match every possible directions.xy combination
            #except for 0,0... which when called will spit out a number that'll be thrown into
            #the self.frames array. they're assigned to give the right player_sprite based on input
            #This is some dogshit code and im too lazy to fix/optimize thisxD
            #i'll probably do it another time... or maybe never
            x,y = int(self.directions.x),int(self.directions.y)
            try:self.image = self.frames[face_dir[f'{x},{y}']]
            except: pass
    def run_particles(self):
        self.spawn_particles()
        self.plr_particles.update()


    def update(self):
        self.get_input()
        self.get_angle()
        self.move()
        self.hover_effect()
        self.animate_v1()
        self.run_particles()
        self.item.update()
        return

class Buster(pygame.sprite.Sprite):
    def __init__(self,camera, player, bullets, shoot_bool):
        super().__init__(camera)
        self.camera = camera
        self.shoot_bool = shoot_bool
        self.bullets = bullets
        self.player = player
        self.face_rads = player.face_rads
        self.face_angle = player.face_angle
        self.mouse_pos = player.mouse_pos
        self.inputs = player.inputs
        self.face_directions = player.face_directions

        self.shoot_cooldown_max = 10
        self.shoot_cooldown = self.shoot_cooldown_max


        self.pos = pygame.Vector2(0,0)

        self.distance = 25

        self.image = pygame.image.load("GameFiles/Assets/TopDown/Player/Buster.png").convert_alpha()
        self.og_image = self.image.copy() #image without any rotations

        self.rect = self.image.get_rect(center = player.stable_rect.center)
        self.stable_rect = self.rect.copy()
        self.offset_rect = self.rect.copy()

        self.visible = True
        self.z_layer = layers['main']

        self.has_light = True
        self.light = pygame.image.load("GameFiles/Assets/TopDown/Effects/LightOutline.png").convert_alpha()
        self.light = pygame.transform.scale(self.light, (200,200))
        self.light_rect = self.light.get_rect(center=self.rect.center)
        self.special = None

        self.shoot_sfx = pygame.mixer.Sound(sfx['PlrShoot'])

    def move(self):
        origin = self.player.stable_rect.center
        origin_x,origin_y = origin
        self.pos.x = origin_x + (self.face_directions.x * self.distance)
        self.pos.y = origin_y + (self.face_directions.y * self.distance)
        self.stable_rect.centerx = self.pos.x
        self.stable_rect.centery = self.pos.y

        self.image = self.og_image
        self.image = pygame.transform.rotate(self.image,-self.player.face_angle)
        self.rect = self.image.get_rect(center = self.pos)


        #self.rect.center = self.stable_rect.center

    def shoot(self):
        self.shoot_cooldown -= 1
        if self.player.shoot_bool and self.shoot_cooldown <=0:
            self.shoot_cooldown = self.shoot_cooldown_max
            player = self.player
            bullet = PlayerBullets(self.camera,self.stable_rect.center,player.bullet_dmg_val,player.face_rads)
            self.bullets.add(bullet)
            self.shoot_sfx.play()



    def update(self):
        self.move()
        self.shoot()
