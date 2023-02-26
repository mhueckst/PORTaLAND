"""
Portal class
"""

import arcade
import visualConstants as vc
import physicsConstants as pc
import paths as path

# Portal constants

DEAD_ZONE = 0.1

class Portal(arcade.Sprite):
    def __init__(self: arcade.SpriteList):
        super().__init__()

        self.scale = vc.PORTAL_SCALING

        self.load_portal_textures()

        # Set starting texture
        # TODO set starting texture depending on which portal already exists

        self.texture = arcade.load_texture_pair(
            f"{path.PORTAL_PATH}/blue_portal-1.png")[0]

        self.idle_timer = 0

    def load_portal_textures(self):
        self.active_textures = []
        for i in range(1, 5):
            texture = arcade.load_texture_pair(
                f"{path.PORTAL_PATH}/blue_portal-{i}.png")
            self.portal_textures.append(texture)

    def portal_animation(self, dx):
        if abs(dx) <= DEAD_ZONE:
            self.idle_timer += 1
            # Change texture every 10 frames
            if self.idle_timer % 10 == 0:
                self.cur_animation_texture += 1
