"""This module contains helper functions."""


import argparse


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--height", type=int, required=False, default=800,
                        help="Height of the application in pixels.")
    parser.add_argument("--tiles", type=int, required=False, default=10,
                        help="How many tiles each side should be divided into.")
    parser.add_argument("--width", type=int, required=False, default=1200,
                        help="Width of the application in pixels.")
    parser.add_argument("--fps", type=int, required=False, default=60,
                        help="The max framerate of the game.")

    return parser.parse_args()

def findIndex(col, row, tiles):
    assert isinstance(col, int)
    assert isinstance(row, int)
    assert isinstance(tiles, int)
    return row+col*tiles
