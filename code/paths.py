"""
All paths used to access game assets
"""

import pathlib

ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"

GAMEOVER_IMAGE_PATH = ASSETS_PATH/"images"/"gameover_image.png"

INSTRUCTIONS_PATH = ASSETS_PATH/"images"/"instructions.png"

LYING_CAKE_PATH = ASSETS_PATH/"images"/"theCakeIsALie.png"

TITLE_PATH = ASSETS_PATH/"images"/"portaland.png"

PLAYER_PATH = ASSETS_PATH/"images"/"SPRITES"/"player"

IDLE_PATH = PLAYER_PATH/"idle"
