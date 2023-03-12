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
        arcade.set_background_color(arcade.color_from_hex_string("cccc00"))
        self.texture = arcade.load_texture(path.INSTRUCTIONS_PATH)
        self.music_player = music_player

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color_from_hex_string("cccc00"))

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

        # commented out code for reference of how to add text or position things
        # def draw_scaled(self, center_x: float, center_y: float,
        #                 scale: float = 1.0,
        #                 angle: float = 0,
        #                 alpha: int = 255):
        # arcade.draw_text("Instructions Screen", self.window.width / 2, self.window.height / 2,
        #                  arcade.color.WHITE, font_size=50, anchor_x="center")
        # arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
        #                  arcade.color.WHITE, font_size=20, anchor_x="center")

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

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        title_view = TitleView()
        self.window.show_view(title_view)
