

from random import randint

import pygame

from .cell import Cell


class Food(Cell):

    COLORS = {
            "red": pygame.Color("red")
            }

    def __init__(self, args, tileSize, screen):
        index = self.getRandomIndex(args.tiles)
        super(Food, self).__init__(args, index, tileSize, screen)

    def drawFood(self):
        col = self.index["column"]*self.tileSize[0]+self.THICKNESS
        row = self.index["row"]*self.tileSize[1]+self.THICKNESS
        colDest = self.tileSize[0]-self.THICKNESS
        rowDest = self.tileSize[1]-self.THICKNESS
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


