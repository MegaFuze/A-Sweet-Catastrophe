WIN_W,WIN_H = 1280, 720

FPS = 60

tile_size = 100
layers = {
    "bg":0,
    "bottom_floor":1,
    "top_floor":2,
    "particles":3,
    "main":4,
    "overlap":5
}

ControlsText = "" \
               "A mysterious creature appeared on your door and is now hunting you down\n" \
               "you must run to the end to obtain a weapon and fight back\n" \
               "Controls:\n" \
               "\n" \
               "WASD: Move\n" \
               "r: reset level\n" \
                "left_alt: fullscreen\n:" \
               "\n" \
               "When gun is obtained:\n" \
               "\n" \
               "mouse: look_around / aim\n" \
               "left_click: shoot \n" \
               "\n" \
               "PRESS SPACE TO CONTINUE\n"

sfx_dir = "GameFiles/Audio/SFX/"
sfx = {
    "BOSSShoot": f"{sfx_dir}BOSSShoot.wav",
    "PlrShoot": f"{sfx_dir}PlrShoot.wav",
    "NextLevel": f"{sfx_dir}NextLevel.wav",
    "BOSSAppear": f"{sfx_dir}BOSSAppear.wav",
    "Hurt": f"{sfx_dir}Hurt.wav",
    "Wrong": f"{sfx_dir}Wrong.wav",
    "Correct": f"{sfx_dir}Correct.wav",
    "Jumpscare": f"{sfx_dir}Jumpscare.wav",


}