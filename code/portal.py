"""
Portal class, initializes portal animation
"""
import arcade
import visual_constants as vc
import physics_constants as pc
import paths as path


class Portal(arcade.Sprite):
    """ This class creates a portal animation """

    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list


    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        # else:
            # self.remove_from_sprite_lists()

    def load_portal_textures(self):
        self.active_textures = []
        for i in range(1, 5):
            texture = arcade.load_texture_pair(
                f"{path.PORTAL_PATH}/blue_portal-{i}.png")
            self.portal_textures.append(texture)
