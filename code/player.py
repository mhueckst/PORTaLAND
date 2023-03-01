"""
Player class
"""

import arcade
import visualConstants as vc
import physicsConstants as pc
import paths as path

# Player movement constants

# Value to to indicate when to change back to idle animation
DEAD_ZONE = 0.1

RIGHT_FACING = 0
LEFT_FACING = 1
DISTANCE_TO_CHANGE_TEXTURE = 20


class Player(arcade.Sprite):
    def __init__(self, ladders: arcade.SpriteList):
        super().__init__()

        self.scale = vc.PLAYER_SCALING

        self.load_player_textures()

        # Set starting texture
        self.texture = arcade.load_texture_pair(
            f"{path.IDLE_PATH}/idle-1.png")[0]

        self.player_face_direction = RIGHT_FACING

        self.cur_animation_texture = 0

        self.idle_timer = 0

        self.jump_timer = 0

        self.ladders = ladders
        self.is_on_ladder = False

        # Horizontal distance traveled since changing texture
        self.x_odometer = 0

        # Vertical distance traveled since changing texture
        self.y_odometer = 0

    def load_player_textures(self):
        self.idle_textures = []
        for i in range(1, 5):
            texture = arcade.load_texture_pair(
                f"{path.IDLE_PATH}/idle-{i}.png")
            self.idle_textures.append(texture)

        self.run_textures = []
        for i in range(1, 9):
            texture = arcade.load_texture_pair(
                f"{path.RUN_SHOOT_PATH}/run-shoot-{i}.png")
            self.run_textures.append(texture)

        self.jump_textures = []
        for i in range(1, 5):
            texture = arcade.load_texture_pair(
                f"{path.JUMP_PATH}/jump-{i}.png")
            self.jump_textures.append(texture)

        self.climbing_textures = []
        for i in range(1, 7):
            texture = arcade.load_texture_pair(
                f"{path.CLIMB_PATH}/climb-{i}.png")
            self.climbing_textures.append(texture)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.x_odometer += dx
        self.y_odometer += dy
        is_on_ground = physics_engine.is_on_ground(self)

        self.update_player_face_direction(dx)
        self.update_physics_on_ladder_collision()

        # If player is on a ladder, cycle through climbing textures
        if self.is_on_ladder and not is_on_ground:
            self.change_y = dy
            if abs(self.y_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
                self.y_odometer = 0
                self.cur_animation_texture += 1
            if self.cur_animation_texture >= len(self.climbing_textures):
                self.cur_animation_texture = 0
            self.texture = self.climbing_textures[self.cur_animation_texture][self.player_face_direction]
            # Return to prevent jumping animation while on ladder
            return

        self.player_jumping_animation(is_on_ground)
        self.player_running_or_idle_animation(dx)

    def update_player_face_direction(self, dx):
        if dx < -DEAD_ZONE and self.player_face_direction == RIGHT_FACING:
            self.player_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.player_face_direction == LEFT_FACING:
            self.player_face_direction = RIGHT_FACING

    def update_physics_on_ladder_collision(self):
        if len(arcade.check_for_collision_with_list(self, self.ladders)) > 0:
            if not self.is_on_ladder:
                self.is_on_ladder = True
                self.pymunk.gravity = (0, 0)
                self.pymunk.damping = 0.0001
                self.pymunk.max_vertical_velocity = pc.PLAYER_MAX_SPEED_HORIZ
        elif self.is_on_ladder:
            self.pymunk.damping = 1.0
            self.pymunk.max_vertical_velocity = pc.PLAYER_MAX_SPEED_VERT
            self.is_on_ladder = False
            self.pymunk.gravity = (0, -(pc.GRAVITY))

    def player_jumping_animation(self, is_on_ground):
        if not is_on_ground:
            self.jump_timer += 1
            # Change texture every 7 frames when jumping
            if self.jump_timer % 7 == 0:
                self.cur_animation_texture += 1
                if self.cur_animation_texture >= len(self.jump_textures):
                    self.cur_animation_texture = 0
                self.texture = self.jump_textures[self.cur_animation_texture][self.player_face_direction]

    def player_running_or_idle_animation(self, dx):
        # If the player is idle
        if abs(dx) <= DEAD_ZONE:
            self.idle_timer += 1

            # Change texture every 10 frames when idle
            if self.idle_timer % 10 == 0:
                self.cur_animation_texture += 1
                if self.cur_animation_texture >= len(self.idle_textures):
                    self.cur_animation_texture = 0
                self.texture = self.idle_textures[self.cur_animation_texture][self.player_face_direction]
        else:
            # If the player is not idle, they're running
            self.idle_timer = 0

            if abs(self.x_odometer) >= DISTANCE_TO_CHANGE_TEXTURE:
                # Ensures that player's running animation cycles through
                # available textures at regular intervals while running
                self.x_odometer %= DISTANCE_TO_CHANGE_TEXTURE
                self.cur_animation_texture += 1
                if self.cur_animation_texture >= len(self.run_textures):
                    self.cur_animation_texture = 0
                self.texture = self.run_textures[self.cur_animation_texture][self.player_face_direction]

    #def player_portal_collision_handler(self, dx, dy, physics_engine):
     #   if 