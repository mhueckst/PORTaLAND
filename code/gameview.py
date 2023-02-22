"""
Gameview Class

written by the Firm (trying out creepy anonymous corporation names)
"""
import new_screens
import arcade
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

        self.player = None

        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

        self.level = 1

    def setup(self):

        map_name = f"level_{self.level:02}.tmx"
        map_path = ASSETS_PATH / "maps" / map_name

        portal_wall_layer = "portal walls"
        ground_layer = "ground"
        building_layer = "buildings"
        exit_layer = "exit"
        background_layer = "background"
        background_layer2 = "background2"
        ladders_layer = "ladders"

        tile_map = arcade.load_tilemap(str(map_path), vc.TILE_SCALING)

        self.scene = arcade.Scene.from_tilemap(tile_map)

        self.background = tile_map.sprite_lists["background"]
        self.background2 = tile_map.sprite_lists["background2"]
        self.ground = tile_map.sprite_lists["ground"]
        self.buildings = tile_map.sprite_lists["building"]
        self.ladders = tile_map.sprite_lists["ladders"]
        self.exit = tile_map.sprite_lists["exit"]
        self.portal_walls = tile_map.sprite_lists["portal walls"]

        background_color = arcade.color.FRESH_AIR
        arcade.set_background_color(background_color)

        self.player = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(
            ASSETS_PATH /
            "images" /
            "SPRITES" /
            "player" /
            "idle" /
            "idle-1.png",
            vc.TILE_SCALING)

        self.player_sprite.center_x = vc.STARTING_X
        self.player_sprite.center_y = vc.STARTING_Y

        self.player.append(self.player_sprite)

        damping = pc.DEF_DAMPING
        gravity = (0, -(pc.GRAVITY))

        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=damping, gravity=gravity)

        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=pc.PLAYER_FRICTION,
                                       mass=pc.PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=pc.PLAYER_MAX_SPEED_HORIZ,
                                       max_vertical_velocity=pc.PLAYER_MAX_SPEED_VERT)

        self.physics_engine.add_sprite_list(self.ground,
                                            friction=pc.GROUND_FRICTION,
                                            collision_type="ground",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

    def on_mouse_press(self, x, y, button, modifiers):
        # for testing screen switching functionality before adding gameplay elements
        game_over = new_screens.GameOverView()
        self.window.show_view(game_over)

    def on_key_press(self, key, modifiers):
        pass

    def on_update(self, delta: float) -> None:
        self.physics_engine.step()
        pass

    def on_draw(self):
        self.clear()
        self.background.draw()
        self.background2.draw()
        self.ground.draw()
        self.buildings.draw()
        self.portal_walls.draw()
        self.ladders.draw()
        self.exit.draw()
        self.player.draw()
