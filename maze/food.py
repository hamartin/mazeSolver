

import pygame

from .cell import Cell
from .utils import getRandomIndex


class Food(Cell):

    def __init__(self, args, tileSize, screen):
        index = getRandomIndex(args.tiles)
        super(Food, self).__init__(args, index, tileSize, screen)

    def draw(self):
        super().drawColoredCell(color="red")
