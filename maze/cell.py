

import pygame

from random import choice

from .utils import findIndex

class Cell():

    COLORS = {
            "black": pygame.Color("black"),
            "darkorange": pygame.Color("darkorange"),
            "darkslategray": pygame.Color("darkslategray"),
            "saddlebrown": pygame.Color("saddlebrown"),
            "forestgreen": pygame.Color("forestgreen"),
            "red": pygame.Color("red")
            }
    THICKNESS = 2

    def __init__(self, args, index, tiles, screen):
        self.args = args
        # self.index = {"column": val, "row": val}
        self.index = index
        # self.tiles = {"numbTiles": val, "tileWidth": val, "tileHeight": val}
        self.tiles = tiles
        self.screen = screen

        self.gridCells = []
        self.walls = {
                "top": True,
                "right": True,
                "bottom": True,
                "left": True
                }
        self.visitedBool = False

    def __str__(self):
        return f"Cell(index={self.index}, tiles={self.tiles})"

    def __repr__(self):
        return self.__str__()

    def addGridCellsRef(self, gridCells):
        self.gridCells = gridCells

    def beenVisited(self):
        return self.visitedBool

    def checkCell(self, col, row):
        if (col < 0
             or col > self.tiles["numbTiles"]-1
             or row < 0
             or row > self.tiles["numbTiles"]-1):
            return None
        return self.gridCells[findIndex(col, row, self.tiles["numbTiles"])]

    def checkNeighbours(self):
        neighbours = []
        top = self.checkCell(self.index["column"], self.index["row"]-1)
        right = self.checkCell(self.index["column"]+1, self.index["row"])
        bottom = self.checkCell(self.index["column"], self.index["row"]+1)
        left = self.checkCell(self.index["column"]-1, self.index["row"])
        if top and not top.beenVisited():
            neighbours.append(top)
        if right and not right.beenVisited():
            neighbours.append(right)
        if bottom and not bottom.beenVisited():
            neighbours.append(bottom)
        if left and not left.beenVisited():
            neighbours.append(left)
        return choice(neighbours) if neighbours else None

    def collide(self, cell):
        assert isinstance(cell, Cell)
        dcol = self.index["column"]-cell.getIndex("column")
        drow = self.index["row"]-cell.getIndex("row")

        if dcol == -1:
            wall = cell.getWall("left")
            if wall and self.args.debug:
                print("Collision with right cell.")
            return wall
        elif dcol == 1:
            wall = cell.getWall("right")
            if wall and self.args.debug:
                print("Collision with left cell.")
            return wall
        elif drow == -1:
            wall = cell.getWall("top")
            if wall and self.args.debug:
                print("Collision with cell below.")
            return wall
        elif drow == 1:
            wall = cell.getWall("bottom")
            if wall and self.args.debug:
                print("Collision with cell above.")
            return wall

    def draw(self):
        col = self.index["column"]*self.tiles["tileWidth"]
        row = self.index["row"]*self.tiles["tileHeight"]
        colDest = self.tiles["tileWidth"]+self.THICKNESS
        rowDest = self.tiles["tileHeight"]+self.THICKNESS
        if self.visitedBool:
            pygame.draw.rect(
                    self.screen, self.COLORS["black"],
                    (col, row, colDest, rowDest))
        if self.walls["top"]:
            pygame.draw.line(
                    self.screen, self.COLORS["darkorange"],
                    (col, row),
                    (col+self.tiles["tileWidth"], row),
                    self.THICKNESS)
        if self.walls["right"]:
            pygame.draw.line(
                    self.screen, self.COLORS["darkorange"],
                    (col+self.tiles["tileWidth"], row),
                    (col+self.tiles["tileWidth"], row+self.tiles["tileHeight"]),
                    self.THICKNESS)
        if self.walls["bottom"]:
            pygame.draw.line(
                    self.screen, self.COLORS["darkorange"],
                    (col, row+self.tiles["tileHeight"]),
                    (col+self.tiles["tileWidth"], row+self.tiles["tileHeight"]),
                    self.THICKNESS)
        if self.walls["left"]:
            pygame.draw.line(
                    self.screen, self.COLORS["darkorange"],
                    (col, row),
                    (col, row+self.tiles["tileHeight"]),
                    self.THICKNESS)

    def drawCurrentCell(self):
        col = self.index["column"]*self.tiles["tileWidth"]+self.THICKNESS
        row = self.index["row"]*self.tiles["tileHeight"]+self.THICKNESS
        colDest = self.tiles["tileWidth"]-self.THICKNESS
        rowDest = self.tiles["tileHeight"]-self.THICKNESS
        pygame.draw.rect(self.screen, self.COLORS["saddlebrown"],
                         (col, row, colDest, rowDest))

    def getIndex(self, colrow=None):
        assert colrow is None or colrow in ["column", "row"]
        if not colrow:
            return self.index["column"], self.index["row"]
        return self.index[colrow]

    def getWall(self, direction):
        assert direction in ["left", "right", "top", "bottom"]
        return self.walls[direction]

    def removeWall(self, wall):
        assert wall in ["left", "top", "right", "bottom"]
        self.walls[wall] = False

    def visited(self):
        self.visitedBool = True

    def wallCollide(self, direction):
        assert direction in ["left", "up", "right", "down"]
        col, row = self.getIndex()
        ret = False

        if direction == "left" and col == 0:
            ret = True
        elif direction == "right" and col == self.tiles["numbTiles"]-1:
            ret = True
        elif direction == "up" and row == 0:
            ret = True
        elif direction == "down" and row == self.tiles["numbTiles"]-1:
            ret = True

        return ret
