

import pygame

from .cell import Cell
from .utils import getRandomIndex


class Food(Cell):

    def __init__(self, args, tileSize, screen):
        index = getRandomIndex(args.tiles)
        super(Food, self).__init__(args, index, tileSize, screen)

    def draw(self):
        col = self.index["column"]*self.tileSize[0]+self.THICKNESS
        row = self.index["row"]*self.tileSize[1]+self.THICKNESS
        colDest = self.tileSize[0]-self.THICKNESS
        rowDest = self.tileSize[1]-self.THICKNESS
        pygame.draw.rect(self.screen, self.COLORS["red"],
                         (col, row, colDest, rowDest))
