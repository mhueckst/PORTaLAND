"""
Gameview Class

written by the Firm (trying out creepy anonymous corporation names)
"""

import arcade
import pathlib
from typing import Optional

# visual constants
SCREEN_TITLE = "PORTaLAND"

TILE_SIZE = 32

SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 20

SCREEN_WIDTH = TILE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * SCREEN_GRID_HEIGHT

TILE_SCALING = 2.0

STARTING_X = TILE_SIZE * 7
STARTING_Y = TILE_SIZE * 3

# physics constants

GRAVITY = 1500

DEF_DAMPING = 1.0
PLAYER_DAMPING = 0.4

PLAYER_FRICTION = 1.0
GROUND_FRICTION = 0.7

PLAYER_MASS = 2.0

PLAYER_MAX_SPEED_HORIZ = 450
PLAYER_MAX_SPEED_VERT = 1600


ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"

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

        tile_map = arcade.load_tilemap(str(map_path),TILE_SCALING)

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

        self.player_sprite = arcade.Sprite(ASSETS_PATH / "images" / "SPRITES" / "player" / "idle" / "idle-1.png", TILE_SCALING)

        self.player_sprite.center_x = STARTING_X
        self.player_sprite.center_y = STARTING_Y

        self.player.append(self.player_sprite)

        damping = DEF_DAMPING
        gravity = (0, -GRAVITY)


        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,gravity=gravity)

        self.physics_engine.add_sprite(self.player_sprite, friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS, moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player", max_horizontal_velocity=PLAYER_MAX_SPEED_HORIZ,
                                       max_vertical_velocity=PLAYER_MAX_SPEED_VERT)
        
        self.physics_engine.add_sprite_list(self.ground, friction = GROUND_FRICTION,
                                            collision_type="ground", body_type=arcade.PymunkPhysicsEngine.STATIC)


    ''' 
    def on_mouse_press(self, x, y, button, modifiers):
        # for testing screen switching functionality before adding gameplay elements
        game_over = GameOverView()
        window.show_view(game_over)
    '''

    def on_key_press(self, key, modifiers):
        pass


    def on_update(self, delta: float) -> None:
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
        self.player.draw()


if __name__ == "__main__":

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()

