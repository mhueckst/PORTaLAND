"""
Non-gameplay screen classes
"""
import gameview
import arcade
import visual_constants as vc
import paths as path

MUSIC_VOLUME = 0.5


class TitleView(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color_from_hex_string("27a7d8"))
        self.texture = arcade.load_texture(path.TITLE_PATH)
        self.background_music = arcade.load_sound(path.NEW_SCREENS_MUSIC_PATH)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color_from_hex_string("27a7d8"))
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.music_player = self.background_music.play(MUSIC_VOLUME, loop=True)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.texture.draw_scaled(
            self.window.width / 2, self.window.height / 2, 1)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        inst_view = InstructionView(self.music_player)
        self.window.show_view(inst_view)


class InstructionView(arcade.View):

    def __init__(self, music_player):
        super().__init__()
        arcade.set_background_color(arcade.color_from_hex_string("fceab8"))
        self.texture = arcade.load_texture(path.INSTRUCTIONS_PATH)
        self.music_player = music_player

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color_from_hex_string("fceab8"))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_hide_view(self):
        self.music_player.pause()

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.texture.draw_scaled(
            self.window.width / 2, self.window.height / 2, 1)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = gameview.GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.selected: bool = False
        self.game_over_image = arcade.load_texture(path.GAMEOVER_IMAGE_PATH)
        self.lying_cake_image = arcade.load_texture(path.LYING_CAKE_PATH)
        self.background_music = arcade.load_sound(path.NEW_SCREENS_MUSIC_PATH)

    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("000000"))
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.music_player = self.background_music.play(MUSIC_VOLUME, loop=True)

    def on_hide_view(self):
        self.music_player.pause()

    def on_draw(self) -> None:
        arcade.start_render()
        if self.selected:
            self.draw_image(self.lying_cake_image)
        else:
            self.draw_image(self.game_over_image)

    def draw_image(self, screen_image: str):
        arcade.draw_texture_rectangle(
            center_x=vc.SCREEN_WIDTH / 2,
            center_y=vc.SCREEN_HEIGHT / 2,
            width=vc.SCREEN_WIDTH,
            height=vc.SCREEN_HEIGHT,
            texture=screen_image,
        )

    def on_mouse_enter(self, x: float, y: float):
        self.selected = True

    def on_mouse_leave(self, x: float, y: float):
        self.selected = False

# TODO: add option to quit?
#     def on_mouse_press(self, _x, _y, _button, _modifiers):
#         title_view = TitleView()
#         self.window.show_view(title_view)


class PauseView(arcade.View):
    def __init__(self, game_view: arcade.View):
        super().__init__()
        self.game_view = game_view
        self.fill_color = arcade.make_transparent_color(
            arcade.color.WHITE, transparency=150)

    def on_draw(self):
        self.game_view.on_draw()

        arcade.draw_lrtb_rectangle_filled(
            left=0,
            right=vc.SCREEN_WIDTH,
            top=vc.SCREEN_HEIGHT,
            bottom=0,
            color=self.fill_color
        )

        self.draw_pause_screen_text()

    def draw_pause_screen_text(self):
        arcade.draw_text(
            "PAUSED",
            vc.SCREEN_WIDTH // 2,
            vc.SCREEN_HEIGHT // 1.75,
            arcade.color.INDIGO,
            font_size=60,
            font_name="Kenney Future",
            anchor_x="center"
        )

        arcade.draw_text(
            "ESC to continue",
            vc.SCREEN_WIDTH // 2,
            vc.SCREEN_HEIGHT // 2.1,
            arcade.color.DARK_MAGENTA,
            font_size=30,
            font_name="Kenney Pixel",
            anchor_x="center",
            bold=True
        )

        arcade.draw_text(
            "ENTER to quit",
            vc.SCREEN_WIDTH // 2,
            vc.SCREEN_HEIGHT // 2.5,
            arcade.color.DARK_MAGENTA,
            font_size=30,
            font_name="Kenney Pixel",
            anchor_x="center",
            bold=True
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        title_view = TitleView()
        self.window.show_view(title_view)
