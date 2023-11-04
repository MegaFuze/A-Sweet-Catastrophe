import pygame

def set_active_inputs(key,input_dicts):
    input_dicts['hold'][key] = True
    input_dicts['tap'][key] = True

def take_key_inputs(event,input_dict):
    if event.key == pygame.K_a: set_active_inputs("a",input_dict)
    if event.key == pygame.K_s: set_active_inputs("s", input_dict)
    if event.key == pygame.K_d: set_active_inputs("d", input_dict)
    if event.key == pygame.K_w: set_active_inputs("w", input_dict)
    if event.key == pygame.K_LSHIFT: set_active_inputs("l_shift", input_dict)
    if event.key == pygame.K_SPACE: set_active_inputs("space", input_dict)
    if event.key == pygame.K_r: set_active_inputs("r", input_dict)
    if event.key == pygame.K_LALT: set_active_inputs("l_alt", input_dict)
    return

def let_go_inputs(event,input_dict):
    if event.key == pygame.K_a: input_dict["hold"]['a'] = False
    if event.key == pygame.K_s: input_dict["hold"]['s'] = False
    if event.key == pygame.K_d: input_dict["hold"]['d'] = False
    if event.key == pygame.K_w: input_dict["hold"]['w'] = False
    if event.key == pygame.K_LSHIFT: input_dict["hold"]['l_shift'] = False
    if event.key == pygame.K_SPACE: input_dict["hold"]['space'] = False
    if event.key == pygame.K_r: input_dict["hold"]['r'] = False
    if event.key == pygame.K_LALT: input_dict['hold']["l_alt"] = False
