"""
Screen Classes

written by the Firm (trying out creepy anonymous corporation names)
"""

import arcade
import pathlib

WIDTH = 800
HEIGHT = 600

ASSETS_PATH = pathlib.Path(__file__).resolve().parent / "assets"

class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        instructions_path = ASSETS_PATH/"images"/"instructions.png"
        self.instructions_image = arcade.load_texture(instructions_path)

    def on_draw(self) -> None:
        self.clear()
        instructions_path = ASSETS_PATH/"images"/"instructions.png"
        self.texture = arcade.load_texture(instructions_path)

        arcade.set_viewport(0, WIDTH - 1, 0, HEIGHT - 1)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = InstructionView()
        self.window.show_view(game_view)

def main():
    window = arcade.Window(WIDTH, HEIGHT, "Instructions")
    start_view = InstructionView()
    window.show_view(start_view)
#    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
