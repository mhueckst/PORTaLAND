import paths
import unittest
import pathlib

class pathTests(unittest.TestCase):

    # Tests that the paths are correct
    def test_paths(self):
        self.assertEqual(paths.ASSETS_PATH, pathlib.Path(__file__).resolve().parent.parent / "assets")

        ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"

        self.assertEqual(paths.GAMEVIEW_MUSIC_PATH, ASSETS_PATH/"music"/"TwilightForest.wav")

        self.assertEqual(paths.PLAYER_PATH, ASSETS_PATH/"images"/"SPRITES"/"player")


# run the test
unittest.main()