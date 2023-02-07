"""
Platformer Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "PORTaLAND"


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


class InstructionView(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color_from_hex_string("27a7d8"))
        self.texture = arcade.load_texture("portaland.png")

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
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


def main():
    """Main function"""

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    # start_view.setup()
    # window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
