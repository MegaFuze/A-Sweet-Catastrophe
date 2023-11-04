import pygame

def create_barrier(size):
    surf = pygame.Surface(size)
    surf.set_colorkey("black")
    return surf

def import_sprites(path = None,size = (64,64)):
    if size == (64,64): print("USING DEFAULT SPRITE SIZE OF 64 x 64 PX")
    sprite_size = pygame.Vector2(size)
    if not path: surf = create_barrier(sprite_size); return surf
    else:
        surface = pygame.image.load(path).convert_alpha()
        sheet_size = pygame.Vector2(surface.get_size())

        max_row = int(sheet_size.y // sprite_size.y)
        max_col = int(sheet_size.x // sprite_size.x)




        #Checks if there are any leftover space from the spritesheet when imported and divided
        if int(max_row*sprite_size.y) != int(sheet_size.y):
            print("spritesheet's y-size is not perfectly dividable by desired sprite's y-size, there may be some space not imported in the spritesheet array")
            print(f'path: {path},sheet_size.y = {sheet_size.y}, sprite_size.y = {sprite_size.y}')
        if max_col * sprite_size.x != sheet_size.x:
            print("spritesheet's x-size is not perfectly dividable by desired sprite's x-size, there may be some space not imported in the spritesheet array")
            print(f'path: {path},sheet_size.x = {sheet_size.x}, sprite_size.x = {sprite_size.x}')
        sprites = []

        for row in range(max_row):
            for col in range(max_col):
                x,y = col*sprite_size.x, row*sprite_size.y
                sprite = pygame.Surface(sprite_size)
                sprite. set_colorkey("black")
                sprite.blit(surface,((0,0)),pygame.Rect(x,y,sprite_size.x,sprite_size.y))
                sprites.append(sprite)
        return sprites

def import_json_sprites(path:str,json_sprites:dict,object_name:str):
    surf = pygame.image.load(path).convert_alpha()
    if object_name == "player":
        sprite_dict ={
            "bottom":[],"bottomright":[],"right":[],
            "topright":[],"top":[],"topleft":[],"left":[],
            "bottomleft":[]
        }

    else:
        sprite_dict = {str(object_name):[]}

    for status in sprite_dict.keys():
        status_sprites = []
        for index,sprite in enumerate(json_sprites):
            frame_dict = json_sprites[index]['frame']
            x,y,w,h = frame_dict['x'], frame_dict['y'],\
                      frame_dict['w'], frame_dict['h']
            if json_sprites[index]['filename'] == status:
                new_surf = pygame.Surface((w,h))
                new_surf.set_colorkey("black")
                new_surf.blit(surf,((0,0)),pygame.Rect(x,y,w,h))
                status_sprites.append(new_surf)
        frame_dict[status] = status_sprites
    return frame_dict