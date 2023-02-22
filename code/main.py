"""
driver file
"""

import new_screens
import arcade
import visualConstants as vc


def main():
    window = arcade.Window(vc.SCREEN_WIDTH, vc.SCREEN_HEIGHT, vc.SCREEN_TITLE)
    start_view = new_screens.TitleView()
    window.show_view(start_view)
    # start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
