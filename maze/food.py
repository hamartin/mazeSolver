

from random import randint

import pygame

from .cell import Cell


class Food(Cell):

    COLORS = {
            "red": pygame.Color("red")
            }

    def __init__(self, args, tiles, screen):
        index = self.getRandomIndex(tiles["numbTiles"])
        super(Food, self).__init__(args, index, tiles, screen)

    def drawFood(self):
        col = self.index["column"]*self.tiles["tileWidth"]+self.THICKNESS
        row = self.index["row"]*self.tiles["tileHeight"]+self.THICKNESS
        colDest = self.tiles["tileWidth"]-self.THICKNESS
        rowDest = self.tiles["tileHeight"]-self.THICKNESS
        pygame.draw.rect(self.screen, self.COLORS["red"],
                         (col, row, colDest, rowDest))

    def getRandomIndex(self, numbTiles):
        assert isinstance(numbTiles, int)

        col = 0
        row = 0
        while col == 0 and row == 0:
            col = randint(0, numbTiles-1)
            row = randint(0, numbTiles-1)
        return {"column": col, "row": row}


