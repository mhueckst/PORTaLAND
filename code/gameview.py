"""
Gameview Class

written by the Firm (trying out creepy anonymous corporation names)
"""
import math
import arcade
import time
import player
import portal
import visual_constants as vc
import physics_constants as pc
import new_screens
from paths import ASSETS_PATH, GAMEVIEW_MUSIC_PATH
from typing import Optional

MUSIC_VOLUME = 0.5


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
        self.portal_sprite = None
        self.blue_portal_texture_list = []
        self.orange_portal_texture_list = []
        self.explosion_texture_list = []

        self.player_sprite = None


        # columns = 2
        # count = 4
        # sprite_width = 100
        # sprite_height = 100
        # filename_blue = ASSETS_PATH/"images/SPRITES/misc/portals/blue/blue_portal_spritesheet.png"
        # filename_orange = ASSETS_PATH/"images/SPRITES/misc/portals/orange/orange_portal_spritesheet.png"

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"
        self.explosion_texture_list = arcade.load_spritesheet(
            file_name, sprite_width, sprite_height, columns, count)

        # self.blue_portal_texture_list = arcade.load_spritesheet(
        #     filename_blue, sprite_width, sprite_height, columns, count)
        # self.orange_portal_texture_list = arcade.load_spritesheet(
        #     filename_orange, sprite_width, sprite_height, columns, count)

        # Container to hold sprite lists
        self.sprite_list = None
        self.bullet_list = None
        self.portal_list = []
        self.blue_portal_sprite = None
        self.orange_portal_sprite = None

        self.player_list = None

        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

        self.level = 1

        # Variables to track which keys are pressed
        self.A_pressed: bool = False
        self.D_pressed: bool = False
        self.W_pressed: bool = False
        self.S_pressed: bool = False

        # Load sounds:
        self.portal_gun_sound = arcade.sound.load_sound(ASSETS_PATH/"sounds/forceField_000.wav")
        self.hit_sound = arcade.sound.load_sound(ASSETS_PATH/"sounds/doorOpen_002.wav")
        self.miss_sound = arcade.sound.load_sound(ASSETS_PATH/"sounds/laserLarge_000.wav")
        self.portal_gun_sound = arcade.sound.load_sound(
            ":resources:sounds/lose2.wav")
        self.hit_sound = arcade.sound.load_sound(
            ":resources:sounds/upgrade1.wav")


        # Variables used to manage music
        self.music_list = []
        self.current_song_index = 0
        self.current_song_player = None
        self.music = None



    def setup(self):

        # Set default background color
        background_color = arcade.color.FRESH_AIR
        arcade.set_background_color(background_color)

        self.player_list = arcade.SpriteList()

        self.map_setup()
        self.sprite_setup()
        self.physics_engine_setup()
        self.create_screen_boundaries(vc.SCREEN_WIDTH, vc.SCREEN_HEIGHT)
        self.add_sprites_to_physics_engine()

        self.music_setup()
        self.bullet_list = arcade.SpriteList()
        self.blue_portal_list = arcade.SpriteList()
        self.orange_portal_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()


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
        ct = 5
        while ct > 0:
            self.portal_walls.pop()
            ct -= 1

    def sprite_setup(self):
        # Initialize sprite lists
        self.sprite_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.portal_list = arcade.SpriteList()
        # self.bullet_list = arcade.SpriteList()
        # self.blue_portal_list = arcade.SpriteList()
        # self.orange_portal_list = arcade.SpriteList()

        # Create player sprite
        # NOTE: Another parameter could be added to this class to
        #       handle portal_wall collisions, see player.py
        self.player_sprite = player.Player(self.ladders)

        # Set player starting location
        self.player_sprite.center_x = vc.STARTING_X
        self.player_sprite.center_y = vc.STARTING_Y

        # Add to player sprite list
        self.sprite_list.append(self.player_sprite)

        # Test that portal sprite can be loaded from path as sprite:
        self.blue_portal_sprite = arcade.Sprite(ASSETS_PATH/"images/SPRITES/portal_spritesheets/blue_portal.png", .3)
        self.orange_portal_sprite = arcade.Sprite(ASSETS_PATH/"images/SPRITES/portal_spritesheets/orange_portal.png", .3)

        # self.sprite_list.append(self.portal_sprite)

    def physics_engine_setup(self):
        # Set damping and gravity
        damping = pc.DEF_DAMPING
        gravity = (0, -(pc.GRAVITY))

        # Create physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=damping, gravity=gravity)

    def create_screen_boundaries(self, width, height):
        # Create left boundary
        left_boundary = arcade.SpriteSolidColor(1, height, arcade.color.BLACK)
        left_boundary.center_x = 0
        left_boundary.center_y = height / 2

        # Create right boundary
        right_boundary = arcade.SpriteSolidColor(1, height, arcade.color.BLACK)
        right_boundary.center_x = width
        right_boundary.center_y = height / 2

        # Create top boundary
        top_boundary = arcade.SpriteSolidColor(width, 1, arcade.color.BLACK)
        top_boundary.center_x = width / 2
        top_boundary.center_y = height

        # Create bottom boundary
        bottom_boundary = arcade.SpriteSolidColor(width, 1, arcade.color.BLACK)
        bottom_boundary.center_x = width / 2
        bottom_boundary.center_y = 0

        # Add boundaries to physics engine
        self.physics_engine.add_sprite(
            left_boundary, body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite(
            right_boundary, body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite(
            top_boundary, body_type=arcade.PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite(
            bottom_boundary, body_type=arcade.PymunkPhysicsEngine.STATIC)

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

        # self.physics_engine.add_sprite_list(self.blue_portal_list)

    def music_setup(self):
        self.music_list = [GAMEVIEW_MUSIC_PATH]
        self.current_song_index = 0
        self.play_song()

    def play_song(self):
        # Stop music currently playing
        if self.music:
            self.music.stop()

        # Play next song
        self.music = arcade.Sound(
            self.music_list[self.current_song_index], streaming=True)
        self.current_song_player = self.music.play(MUSIC_VOLUME)
        time.sleep(0.03)

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
        elif key == arcade.key.ESCAPE:
            pause = new_screens.PauseView(self)
            self.window.show_view(pause)

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
        self.bullet_list.update()
        self.portal_list.update()

        for bullet in self.bullet_list:
            portal_wall_hit = arcade.check_for_collision_with_list(
                bullet, self.portal_walls)
            normal_wall_hit = arcade.check_for_collision_with_list(
                bullet, self.ground)

            # Handle hitting portal walls
            if len(portal_wall_hit) > 0:
                blue_portal = self.blue_portal_sprite
                orange_portal = self.orange_portal_sprite

                # Portal cycling logic:
                if len(self.portal_list) == 0:
                    blue_portal.center_x = portal_wall_hit[0].center_x
                    blue_portal.center_y = portal_wall_hit[0].center_y
                    blue_portal.update()
                    self.portal_list.append(blue_portal)
                if (self.portal_list[0] == blue_portal) and (len(self.portal_list) == 1):
                    orange_portal.center_x = portal_wall_hit[0].center_x
                    orange_portal.center_y = portal_wall_hit[0].center_y
                    orange_portal.update()
                    self.portal_list.append(orange_portal)
                elif (self.portal_list[0] == blue_portal) and len(self.portal_list) == 2:
                    self.portal_list.pop(0)
                    self.portal_list.update()
                    # blue_portal.remove_from_sprite_lists()
                    blue_portal.center_x = portal_wall_hit[0].center_x
                    blue_portal.center_y = portal_wall_hit[0].center_y
                    blue_portal.update()
                    self.portal_list.append(blue_portal)
                elif self.portal_list[0] == orange_portal and len(self.portal_list) == 2:
                    self.portal_list.pop(0)
                    self.portal_list.update()
                    # orange_portal.remove_from_sprite_lists()
                    orange_portal.center_x = portal_wall_hit[0].center_x
                    orange_portal.center_y = portal_wall_hit[0].center_y
                    orange_portal.update()
                    self.portal_list.append(orange_portal)

                bullet.remove_from_sprite_lists()
                arcade.play_sound(self.hit_sound)

            if len(normal_wall_hit) > 0:
                arcade.play_sound(self.miss_sound)
                bullet.remove_from_sprite_lists()

            if bullet.bottom > vc.SCREEN_WIDTH or bullet.top < 0 or bullet.right < 0 or bullet.left > vc.SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

            # if len(hit_list) > 2:
            #     for portal in hit_list:
            #         portal.remove_from_sprite_lists()

        self.update_music()

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
            if sprite.center_x < sprite.width / 2:
                sprite.center_x = sprite.width / 2
            elif sprite.center_x > vc.SCREEN_WIDTH - sprite.width / 2:
                sprite.center_x = vc.SCREEN_WIDTH - sprite.width / 2
            if sprite.center_y < sprite.height / 2:
                sprite.center_y = sprite.height / 2
            elif sprite.center_y > vc.SCREEN_HEIGHT - sprite.height / 2:
                sprite.center_y = vc.SCREEN_HEIGHT - sprite.height / 2

    def check_exit_tile_collision(self):
        if arcade.check_for_collision_with_list(self.player_sprite, self.exit):
            game_over_view = new_screens.GameOverView()
            self.window.show_view(game_over_view)

    def player_portal_collision_handler(self):
        collision_portal_list = arcade.check_for_collision_with_list(self.player_sprite, self.portal_walls) #TODO: CHANGE BACK TO PORTAL SPRITES

        exit_portal = None
        if len(collision_portal_list) == 0:
            return
        entry_portal = collision_portal_list[0]
        exit_portal = self.find_exit_portal(entry_portal)
        self.player_sprite.remove_from_sprite_lists()
        self.player_sprite = player.Player(self.ladders)
        self.sprite_list.append(self.player_sprite)

        self.player_sprite.position = self.player_sprite.portal_physics_handler(entry_portal, exit_portal)
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=pc.PLAYER_FRICTION,
                                       mass=pc.PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=pc.PLAYER_MAX_SPEED_HORIZ,
                                       max_vertical_velocity=pc.PLAYER_MAX_SPEED_VERT)



    def update_music(self):
        stream_position = self.music.get_stream_position(
            self.current_song_player)
        if stream_position == 0.0:
            self.advance_song()
            self.play_song()

    def advance_song(self):
        self.current_song_index += 1
        if self.current_song_index >= len(self.music_list):
            self.current_song_index = 0

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
        self.bullet_list.draw()
        self.blue_portal_sprite.draw()
        self.orange_portal_sprite.draw()

    # Shoot portal to mouse location at mouse click
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # Create a 'bullet' laser w/ sound
        arcade.play_sound(self.portal_gun_sound)
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", vc.SCALING_LASER)

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        dest_x = x
        dest_y = y

        # This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)
        bullet.angle = math.degrees(angle)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        bullet.change_x = math.cos(angle) * pc.BULLET_SPEED
        bullet.change_y = math.sin(angle) * pc.BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def find_exit_portal(self, entry_portal):
        ct = 0
        exit_portal = None
        for p in self.portal_walls:  # CHANGE BACK TO PORTAL SPRITES
            if p is not entry_portal:
                exit_portal = p
                #break
            #ct += 1
            #if ct > 3:
               # break
        return exit_portal
