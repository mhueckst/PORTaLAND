"""
Screen Classes

written by the Firm (trying out creepy anonymous corporation names)
"""

import arcade
import pathlib

WIDTH = 800
HEIGHT = 600

ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"


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
            center_x=WIDTH / 2,
            center_y=HEIGHT / 2,
            width=WIDTH,
            height=HEIGHT,
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


def main():
    window = arcade.Window(WIDTH, HEIGHT, "PORTaLAND")
    gameover_view = GameOverView()
    window.show_view(gameover_view)
    arcade.run()


if __name__ == "__main__":
    main()
