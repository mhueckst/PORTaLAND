"""
Gameview Class

written by the Firm (trying out creepy anonymous corporation names)
"""
import arcade
import player
import visualConstants as vc
import physicsConstants as pc
from paths import ASSETS_PATH
from typing import Optional


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
        self.W_pressed: bool = False
        self.S_pressed: bool = False

        # Set default background color
        background_color = arcade.color.FRESH_AIR
        arcade.set_background_color(background_color)

    def setup(self):

        # Map name
        map_name = f"level_{self.level:02}.tmx"
        map_path = ASSETS_PATH / "maps" / map_name

        # Load in TileMap
        tile_map = arcade.load_tilemap(str(map_path), vc.TILE_SCALING)

        self.scene = arcade.Scene.from_tilemap(tile_map)

        # Pull sprite layers out of tile map
        self.background = tile_map.sprite_lists["background"]
        self.background2 = tile_map.sprite_lists["background2"]
        self.ground = tile_map.sprite_lists["ground"]
        self.buildings = tile_map.sprite_lists["building"]
        self.ladders = tile_map.sprite_lists["ladders"]
        self.exit = tile_map.sprite_lists["exit"]
        self.portal_walls = tile_map.sprite_lists["portal walls"]

        # Create sprite list
        self.player_list = arcade.SpriteList()

        # Create player sprite
        self.player_sprite = player.Player(self.ladders)

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

        # Add portal wall sprite to physics engine
        # NOTE: We may need to adjust the following line, as it currently
        #       prevents the player from going through a portal_wall/off
        #       the screen where a portal wall is located.
        self.physics_engine.add_sprite_list(self.portal_walls,
                                            friction=pc.WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.A_pressed = True
        elif key == arcade.key.D:
            self.D_pressed = True
        elif key == arcade.key.W:
            self.W_pressed = True
            if self.physics_engine.is_on_ground(self.player_sprite) \
                    and not self.player_sprite.is_on_ladder:
                strength = (0, pc.PLAYER_JUMP_STRENGTH)
                self.physics_engine.apply_impulse(self.player_sprite, strength)
        elif key == arcade.key.S:
            self.S_pressed = True
            if self.player_sprite.is_on_ladder:
                self.player_sprite.change_y = -(pc.PLAYER_MAX_SPEED_VERT)
                self.physics_engine.set_velocity(
                    self.player_sprite, (self.player_sprite.change_x, self.player_sprite.change_y))

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.A_pressed = False
        elif key == arcade.key.D:
            self.D_pressed = False
        elif key == arcade.key.W:
            self.W_pressed = False
        elif key == arcade.key.S:
            if self.player_sprite.is_on_ladder:
                self.player_sprite.change_y = 0
            self.S_pressed = False

    def on_update(self, delta: float):
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)

        # Update player force based on keys pressed
        if self.A_pressed and not self.D_pressed:
            if is_on_ground or self.player_sprite.is_on_ladder:
                force = (-(pc.PLAYER_MOVE_FORCE_ON_GROUND), 0)
            else:
                force = (-(pc.PLAYER_MOVE_FORCE_IN_AIR), 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.D_pressed and not self.A_pressed:
            if is_on_ground or self.player_sprite.is_on_ladder:
                force = (pc.PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (pc.PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.W_pressed and not self.S_pressed:
            if self.player_sprite.is_on_ladder:
                force = (0, pc.PLAYER_MOVE_FORCE_ON_GROUND)
                self.physics_engine.apply_force(self.player_sprite, force)
                self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.S_pressed and not self.W_pressed:
            if self.player_sprite.is_on_ladder:
                force = (0, -(pc.PLAYER_MOVE_FORCE_ON_GROUND))
                self.physics_engine.set_friction(self.player_sprite, 0)

        else:
            self.physics_engine.set_friction(self.player_sprite, 1.0)

        # Update movement in physics engine
        self.physics_engine.step()
        self.keep_sprites_within_bounds()

    def keep_sprites_within_bounds(self):
        for sprite in self.player_list:
            if sprite.right > vc.SCREEN_WIDTH:
                sprite.right = vc.SCREEN_WIDTH - 24
            elif sprite.left < 0:
                sprite.left = 24
            if sprite.top > vc.SCREEN_HEIGHT:
                sprite.top = vc.SCREEN_HEIGHT
            elif sprite.bottom < 32:
                sprite.bottom = 32

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
