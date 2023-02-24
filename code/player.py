"""
Player class
"""

import arcade
import visualConstants as vc
import physicsConstants as pc
import paths as path

# Player movement constants
DEAD_ZONE = 0.1
RIGHT_FACING = 0
LEFT_FACING = 1
DISTANCE_TO_CHANGE_TEXTURE = 20


class Player(arcade.Sprite):
    def __init__(self, ladders: arcade.SpriteList):
        super().__init__()

        # Set player scaling
        self.scale = vc.PLAYER_SCALING

        # Load in idle textures
        self.idle_textures = []
        for i in range(1, 5):
            texture = arcade.load_texture_pair(
                f"{path.IDLE_PATH}/idle-{i}.png")
            self.idle_textures.append(texture)

        # Load in running textures
        self.run_textures = []
        for i in range(1, 9):
            texture = arcade.load_texture_pair(
                f"{path.RUN_SHOOT_PATH}/run-shoot-{i}.png")
            self.run_textures.append(texture)

        # Load in jumping textures
        self.jump_textures = []
        for i in range(1, 5):
            texture = arcade.load_texture_pair(
                f"{path.JUMP_PATH}/jump-{i}.png")
            self.jump_textures.append(texture)

        # Load in climbing textures
        self.climbing_textures = []
        for i in range(1, 7):
            texture = arcade.load_texture_pair(
                f"{path.CLIMB_PATH}/climb-{i}.png")
            self.climbing_textures.append(texture)

        # Set starting texture
        self.texture = arcade.load_texture_pair(
            f"{path.IDLE_PATH}/idle-1.png")[0]

        # Default player to face to the right
        self.character_face_direction = RIGHT_FACING

        # Index of current texture
        self.cur_texture = 0

        # Horizontal distance traveled since changing texture
        self.x_odometer = 0

        # Vertical distance traveled since changing texture
        self.y_odometer = 0

        # Timer for idle animation
        self.idle_timer = 0

        # Timer for jump animation
        self.jump_timer = 0

        self.ladders = ladders
        self.is_on_ladder = False

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        # Determing left or right facing
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        is_on_ground = physics_engine.is_on_ground(self)

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

        self.x_odometer += dx
        self.y_odometer += dy

        if self.is_on_ladder and not is_on_ground:
            self.change_y = dy
            if abs(self.y_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
                self.y_odometer = 0
                self.cur_texture += 1
            if self.cur_texture >= len(self.climbing_textures):
                self.cur_texture = 0
            self.texture = self.climbing_textures[self.cur_texture][self.character_face_direction]
            return

        # Jumping animation
        if not is_on_ground:
            self.jump_timer += 1
            if self.jump_timer % 7 == 0:
                self.cur_texture += 1
                if self.cur_texture >= len(self.jump_textures):
                    self.cur_texture = 0
                self.texture = self.jump_textures[self.cur_texture][self.character_face_direction]

        if abs(dx) <= DEAD_ZONE:
            self.idle_timer += 1

            # Change texture every 10 frames when idle
            if self.idle_timer % 10 == 0:
                self.cur_texture += 1
                if self.cur_texture >= len(self.idle_textures):
                    self.cur_texture = 0
                self.texture = self.idle_textures[self.cur_texture][self.character_face_direction]
        else:
            self.idle_timer = 0

            self.x_odometer += dx
            if abs(self.x_odometer) >= DISTANCE_TO_CHANGE_TEXTURE:
                self.x_odometer %= DISTANCE_TO_CHANGE_TEXTURE
                self.cur_texture += 1
                if self.cur_texture >= len(self.run_textures):
                    self.cur_texture = 0
                self.texture = self.run_textures[self.cur_texture][self.character_face_direction]
