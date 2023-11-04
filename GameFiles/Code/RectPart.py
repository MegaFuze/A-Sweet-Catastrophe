import pygame

def get_rect_plus(surf,pos,rect_part = "topleft"):
    '''literally get_rect() but rect_part is changeable based on string arg of rect_part '''
    match rect_part:
        case "topleft": rect = surf.get_rect(topleft = pos)
        case "midtop": rect = surf.get_rect(midtop = pos)
        case "topright": rect = surf.get_rect(topright = pos)
        case "midleft": rect = surf.get_rect(midleft= pos)
        case "midright": rect = surf.get_rect(midright = pos)
        case "bottomleft": rect = surf.get_rect(bottomleft = pos)
        case "midbottom": rect = surf.get_rect(midbottom= pos)
        case "bottomright": rect = surf.get_rect(bottomright = pos)
        case _: rect = surf.get_rect(center=pos)
    return rect