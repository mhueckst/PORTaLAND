"""
Gameview Class

written by the Firm (trying out creepy anonymous corporation names)
"""
import arcade
import player
import visualConstants as vc
import physicsConstants as pc
import new_screens
from paths import ASSETS_PATH
from typing import Optional


class GameView(arcade.View):

    def __init__(self) -> None:
        super().__init__()

        # Sprite lists
        self.background = None
        self.background2 = None
        self.ground = None
        self.ladders = None
        self.buildings = None
        self.exit = None
        self.portal_walls = None

        # Container to hold sprite lists
        self.sprite_list = None

        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

        self.level = 1

        # Variables to track if WASD keys are pressed
        self.A_pressed: bool = False
        self.D_pressed: bool = False
        self.W_pressed: bool = False
        self.S_pressed: bool = False

    def setup(self):

        # Set default background color
        background_color = arcade.color.FRESH_AIR
        arcade.set_background_color(background_color)

        self.map_setup()
        self.sprite_setup()
        self.physics_engine_setup()
        self.add_sprites_to_physics_engine()

    def map_setup(self):
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

    def sprite_setup(self):
        # Initialize sprite list
        self.sprite_list = arcade.SpriteList()

        # Create player sprite
        # NOTE: Another parameter could be added to this class to
        #       handle portal_wall collisions, see player.py
        self.player_sprite = player.Player(self.ladders)

        # Set player starting location
        self.player_sprite.center_x = vc.STARTING_X
        self.player_sprite.center_y = vc.STARTING_Y

        # Add to player sprite list
        self.sprite_list.append(self.player_sprite)

    def physics_engine_setup(self):
        # Set damping and gravity
        damping = pc.DEF_DAMPING
        gravity = (0, -(pc.GRAVITY))

        # Create physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=damping, gravity=gravity)

    def add_sprites_to_physics_engine(self):
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

        # Add exit to physics engine
        self.physics_engine.add_sprite_list(self.exit,
                                            friction=pc.GROUND_FRICTION,
                                            collision_type="exit",
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
            # Player jumps on W press iff on ground and not on ladder
            if self.physics_engine.is_on_ground(self.player_sprite) \
                    and not self.player_sprite.is_on_ladder:
                strength = (0, pc.PLAYER_JUMP_STRENGTH)
                self.physics_engine.apply_impulse(self.player_sprite, strength)
        elif key == arcade.key.S:
            self.S_pressed = True
            # Player goes down ladder on S press iff on ladder
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
            # Player stays on ladder when S is released
            if self.player_sprite.is_on_ladder:
                self.player_sprite.change_y = 0
            self.S_pressed = False

    def on_update(self, delta: float):

        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)

        # Update player movement based on keys pressed
        if self.A_pressed and not self.D_pressed:
            self.apply_player_movement('A', is_on_ground, 0)
        elif self.D_pressed and not self.A_pressed:
            self.apply_player_movement('D', is_on_ground, 0)
        elif self.W_pressed and not self.S_pressed:
            if self.player_sprite.is_on_ladder:
                self.apply_player_movement('W', is_on_ground, 0)
        elif self.S_pressed and not self.W_pressed:
            if self.player_sprite.is_on_ladder:
                self.apply_player_movement('S', is_on_ground, 0)

        else:
            self.set_player_friction(1.0)

        # Update movement in physics engine
        self.physics_engine.step(delta)

        # Update sprites to stay in screen bounds
        self.keep_sprites_within_bounds()

        # Check if player encountered exit tile
        self.check_exit_tile_collision()

        self.player_portal_collision_handler()

    def apply_player_movement(self, key, is_on_ground, friction):
        force = self.get_force(key, is_on_ground)
        self.apply_player_force(force)
        self.set_player_friction(friction)

    def get_force(self, key, is_on_ground) -> int:
        match key:
            case 'A':
                if is_on_ground or self.player_sprite.is_on_ladder:
                    return (-(pc.PLAYER_MOVE_FORCE_ON_GROUND), 0)
                else:
                    return (-(pc.PLAYER_MOVE_FORCE_IN_AIR), 0)
            case 'D':
                if is_on_ground or self.player_sprite.is_on_ladder:
                    return (pc.PLAYER_MOVE_FORCE_ON_GROUND, 0)
                else:
                    return (pc.PLAYER_MOVE_FORCE_IN_AIR, 0)
            case 'W':
                if self.player_sprite.is_on_ladder:
                    return (0, pc.PLAYER_MOVE_FORCE_ON_GROUND)
            case 'S':
                if self.player_sprite.is_on_ladder:
                    return (0, -(pc.PLAYER_MOVE_FORCE_ON_GROUND))
            case _:
                return

    def apply_player_force(self, force):
        self.physics_engine.apply_force(self.player_sprite, force)

    def set_player_friction(self, friction):
        self.physics_engine.set_friction(self.player_sprite, friction)

    def keep_sprites_within_bounds(self):
        for sprite in self.sprite_list:
            if sprite.right > vc.SCREEN_WIDTH:
                sprite.right = vc.SCREEN_WIDTH - 24
            elif sprite.left < 0:
                sprite.left = 24
            if sprite.top > vc.SCREEN_HEIGHT:
                sprite.top = vc.SCREEN_HEIGHT
            elif sprite.bottom < 32:
                sprite.bottom = 32

    def check_exit_tile_collision(self):
        if arcade.check_for_collision_with_list(self.player_sprite, self.exit):
            gameover_view = new_screens.GameOverView()
            self.window.show_view(gameover_view)

    def player_portal_collision_handler(self):
        collision_portal_list = arcade.check_for_collision_with_list(self.player_sprite, self.portal_walls) #CHANGE BACK TO PORTAL SPRITES
        exit_portal = None
        if len(collision_portal_list) == 0:
            return 
        entry_portal = collision_portal_list[0]
        ct = 0
        for p in self.portal_walls:  #CHANGE BACK TO PORTAL SPRITES
            if p is not entry_portal:
                exit_portal = p
                #break
            ct += 1
            if ct > 2:
                break

        if exit_portal is None:
           return

        exit_port_left = exit_portal.left
        exit_port_right = exit_portal.right
        entry_port_left = entry_portal.left
        entry_port_right = entry_portal.right

        (x_exit_port, y_exit_port) = exit_portal.position
        y_bottom_exit_port = exit_portal.bottom
        self.player_sprite.set_position(x_exit_port, y_exit_port)
        self.player_sprite.bottom = y_bottom_exit_port
        #self.player_sprite.bottom = y_bottom_exit_port

        (x_entry_port, y_entry_port) = entry_portal.position

        velocity_update = [pc.PLAYER_MAX_SPEED_HORIZ, pc.PLAYER_MAX_SPEED_VERT]
        [vel_x, vel_y] = velocity_update


            #check where collision is, apply dx, dy accordingly
            #new fxn?

        exit_width_check = abs(exit_port_right - exit_port_left)
        entry_width_check = abs(entry_port_right - entry_port_left)

        if entry_width_check <= vc.TILE_SIZE*2:
            if exit_width_check <= vc.TILE_SIZE*2:
                opposing_wall_check = abs(entry_port_right - exit_port_right)
                if opposing_wall_check > 0:
                    velocity_update[0] = -vel_x
            elif y_exit_port <= vc.TILE_SIZE*2:
                if x_entry_port >= (vc.SCREEN_WIDTH - vc.TILE_SIZE*5):
                    velocity_update = [vel_y, -vel_x]
                else:
                    velocity_update = [vel_y, vel_x]
            else:
                if x_entry_port >= (vc.SCREEN_WIDTH - vc.TILE_SIZE*5):
                    velocity_update = [vel_y, vel_x]
                else:
                    velocity_update = [vel_y, -vel_x]
        else:
            if exit_width_check <= vc.TILE_SIZE*2:
                if x_exit_port >= (vc.SCREEN_WIDTH - vc.TILE_SIZE*5):
                    velocity_update = [vel_y, vel_x]
                else:
                    velocity_update = [vel_y, -vel_x]
            elif y_exit_port <= vc.TILE_SIZE*2:
                velocity_update[1] = -vel_y

        self.player_sprite.velocity = velocity_update
        self.player_sprite.pymunk.gravity = (0, -pc.GRAVITY)
        self.player_sprite.pymunk.damping = pc.PLAYER_DAMPING





            



    def on_draw(self):
        self.clear()
        self.background.draw()
        self.background2.draw()
        self.ground.draw()
        self.buildings.draw()
        self.portal_walls.draw()
        self.ladders.draw()
        self.exit.draw()
        self.sprite_list.draw()
