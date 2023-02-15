"""
Platformer Game
"""
<<<<<<< HEAD

import arcade
import pathlib
=======
import arcade
>>>>>>> 0f2197176e605c978a6dd45b272471ff120d9821

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "PORTaLAND"

<<<<<<< HEAD
ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"
=======
>>>>>>> 0f2197176e605c978a6dd45b272471ff120d9821

class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__()
        self.window.set_mouse_visible(False)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        self.clear()
        self.texture.draw_sized(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)


<<<<<<< HEAD
class TitleView(arcade.View):
=======
class InstructionView(arcade.View):
>>>>>>> 0f2197176e605c978a6dd45b272471ff120d9821

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color_from_hex_string("27a7d8"))
<<<<<<< HEAD
        title_path = ASSETS_PATH/"images"/"portaland.png"
        self.texture = arcade.load_texture(title_path)
=======
        self.texture = arcade.load_texture("portaland.png")
>>>>>>> 0f2197176e605c978a6dd45b272471ff120d9821

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color_from_hex_string("27a7d8"))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.texture.draw_scaled(self.window.width / 2, self.window.height / 2, 1)

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
<<<<<<< HEAD
        inst_view = InstructionView()
        self.window.show_view(inst_view)

class InstructionView(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color_from_hex_string("cccc00"))
        instructions_path = ASSETS_PATH/"images"/"instructions.png"
        self.texture = arcade.load_texture(instructions_path)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color_from_hex_string("cccc00"))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.texture.draw_scaled(self.window.width / 2, self.window.height / 2, 1)

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
        game_over_view = GameOverView()
        #game_over_view.setup()
        self.window.show_view(game_over_view)

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.selected: bool = False
        gameover_image_path = ASSETS_PATH/"images"/"gameover_image.png"
        self.gameover_image = arcade.load_texture(gameover_image_path)
        lying_cake_path = ASSETS_PATH/"images"/"theCakeIsALie.png"
        self.lying_cake_image = arcade.load_texture(lying_cake_path)

    def on_draw(self) -> None:
        arcade.start_render()
        if self.selected:
            self.draw_image(self.lying_cake_image)
        else:
            self.draw_image(self.gameover_image)

    def draw_image(self, screen_image: str):
        arcade.draw_texture_rectangle(
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT / 2,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            texture=screen_image,
        )

    def on_mouse_enter(self, x: float, y: float):
        self.selected = True

    def on_mouse_leave(self, x: float, y: float):
        self.selected = False

    # TODO: test functionality once GameView class is implemented
    # def on_mouse_press(self, _x, _y, _button, _modifiers):
    #    game_view = GameView()
    #    self.window.show_view(game_view)
=======
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

>>>>>>> 0f2197176e605c978a6dd45b272471ff120d9821

def main():
    """Main function"""

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
<<<<<<< HEAD
    start_view = TitleView()
=======
    start_view = InstructionView()
>>>>>>> 0f2197176e605c978a6dd45b272471ff120d9821
    window.show_view(start_view)
    # start_view.setup()
    # window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
