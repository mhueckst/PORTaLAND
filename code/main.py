"""
driver file
"""
SCREEN_TITLE = "PORTaLAND"

TILE_SIZE = 32

SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 20

SCREEN_WIDTH = TILE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * SCREEN_GRID_HEIGHT

import gameview
import new_screens
import arcade

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = new_screens.TitleView()
    window.show_view(start_view)
    #start_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()