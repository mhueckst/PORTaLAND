"""
Gameview Class

written by the Firm (trying out creepy anonymous corporation names)
"""
import arcade
import visualConstants as vc
import physicsConstants as pc
from paths import ASSETS_PATH
from typing import Optional


class Player(arcade.Sprite):
    def update(self):
        if self.left < 0:
            self.left = 0
        elif self.right > vc.SCREEN_WIDTH - 1:
            self.right = vc.SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > vc.SCREEN_WIDTH - 1:
            self.top = vc.SCREEN_HEIGHT - 1


class GameView(arcade.View):

    def __init__(self) -> None:
        super().__init__()

        self.background = None
        self.background2 = None
        self.ground = None
        self.ladders = None
        self.buildings = None
        self.exit = None
        self.portal_walls = None

        self.player_list = None

        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

        self.level = 1

        self.A_pressed: bool = False
        self.D_pressed: bool = False

    def setup(self):

        # Map name
        map_name = f"level_{self.level:02}.tmx"
        map_path = ASSETS_PATH / "maps" / map_name

        # Load in TileMap
        tile_map = arcade.load_tilemap(str(map_path), vc.TILE_SCALING)

        # self.scene = arcade.Scene.from_tilemap(tile_map)

        # Pull sprite layers out of tile map
        self.background = tile_map.sprite_lists["background"]
        self.background2 = tile_map.sprite_lists["background2"]
        self.ground = tile_map.sprite_lists["ground"]
        self.buildings = tile_map.sprite_lists["building"]
        self.ladders = tile_map.sprite_lists["ladders"]
        self.exit = tile_map.sprite_lists["exit"]
        self.portal_walls = tile_map.sprite_lists["portal walls"]

        # Set default background color
        background_color = arcade.color.FRESH_AIR
        arcade.set_background_color(background_color)

        # Create sprite list
        self.player_list = arcade.SpriteList()

        # Create player sprite
        self.player_sprite = arcade.Sprite(
            ASSETS_PATH /
            "images" /
            "SPRITES" /
            "player" /
            "idle" /
            "idle-1.png",
            vc.PLAYER_SCALING)

        # Set player starting location
        self.player_sprite.center_x = vc.STARTING_X
        self.player_sprite.center_y = vc.STARTING_Y

        # Add to player sprite list
        self.player_list.append(self.player_sprite)

        # Set damping and gravity
        damping = pc.DEF_DAMPING
        gravity = (0, -(pc.GRAVITY))

        # Create physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=damping, gravity=gravity)

        # Add player to physics engine
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=pc.PLAYER_FRICTION,
                                       mass=pc.PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=pc.PLAYER_MAX_SPEED_HORIZ,
                                       max_vertical_velocity=pc.PLAYER_MAX_SPEED_VERT)

        # Add ground to physics engine
        self.physics_engine.add_sprite_list(self.ground,
                                            friction=pc.GROUND_FRICTION,
                                            collision_type="ground",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.A_pressed = True
        elif key == arcade.key.D:
            self.D_pressed = True
        elif key == arcade.key.W:
            if self.physics_engine.is_on_ground(self.player_sprite):
                strength = (0, pc.PLAYER_JUMP_STRENGTH)
                self.physics_engine.apply_impulse(self.player_sprite, strength)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.A_pressed = False
        elif key == arcade.key.D:
            self.D_pressed = False

    def on_update(self, delta: float) -> None:
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)

        # Update player force based on keys pressed
        if self.A_pressed and not self.D_pressed:
            if is_on_ground:
                force = (-(pc.PLAYER_MOVE_FORCE_ON_GROUND), 0)
            else:
                force = (-(pc.PLAYER_MOVE_FORCE_IN_AIR), 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.D_pressed and not self.A_pressed:
            if is_on_ground:
                force = (pc.PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (pc.PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)
        else:
            self.physics_engine.set_friction(self.player_sprite, 1.0)

        # Update movement in physics engine
        self.physics_engine.step()

    def on_draw(self):
        self.clear()
        self.background.draw()
        self.background2.draw()
        self.ground.draw()
        self.buildings.draw()
        self.portal_walls.draw()
        self.ladders.draw()
        self.exit.draw()
        self.player_list.draw()
