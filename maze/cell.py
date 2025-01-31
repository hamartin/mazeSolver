

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

    def __init__(self, args, index, tileSize, screen):
        self.args = args
        # self.index = {"column": val, "row": val}
        self.index = index
        # self.tileSize = (width, height)
        self.tileSize = tileSize
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
        return f"Cell(index={self.index}, tiles={self.args.tiles})"

    def __repr__(self):
        return self.__str__()

    def addGridCellsRef(self, gridCells):
        self.gridCells = gridCells

    def beenVisited(self):
        return self.visitedBool

    def checkCell(self, col, row):
        if (col < 0
             or col > self.args.tiles-1
             or row < 0
             or row > self.args.tiles-1):
            return None
        return self.gridCells[findIndex(col, row, self.args.tiles)]

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
        col = self.index["column"]*self.tileSize[0]
        row = self.index["row"]*self.tileSize[1]
        colDest = self.tileSize[0]+self.THICKNESS
        rowDest = self.tileSize[1]+self.THICKNESS
        if self.visitedBool:
            pygame.draw.rect(
                    self.screen, self.COLORS["black"],
                    (col, row, colDest, rowDest))
        if self.walls["top"]:
            pygame.draw.line(
                    self.screen, self.COLORS["darkorange"],
                    (col, row),
                    (col+self.tileSize[0], row),
                    self.THICKNESS)
        if self.walls["right"]:
            pygame.draw.line(
                    self.screen, self.COLORS["darkorange"],
                    (col+self.tileSize[0], row),
                    (col+self.tileSize[0], row+self.tileSize[1]),
                    self.THICKNESS)
        if self.walls["bottom"]:
            pygame.draw.line(
                    self.screen, self.COLORS["darkorange"],
                    (col, row+self.tileSize[1]),
                    (col+self.tileSize[0], row+self.tileSize[1]),
                    self.THICKNESS)
        if self.walls["left"]:
            pygame.draw.line(
                    self.screen, self.COLORS["darkorange"],
                    (col, row),
                    (col, row+self.tileSize[1]),
                    self.THICKNESS)

    def drawColoredCell(self, color):
        assert isinstance(color, str) and color in self.COLORS
        col = self.index["column"]*self.tileSize[0]+self.THICKNESS
        row = self.index["row"]*self.tileSize[1]+self.THICKNESS
        colDest = self.tileSize[0]-self.THICKNESS
        rowDest = self.tileSize[1]-self.THICKNESS
        pygame.draw.rect(self.screen, self.COLORS[color],
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
        elif direction == "right" and col == self.args.tiles-1:
            ret = True
        elif direction == "up" and row == 0:
            ret = True
        elif direction == "down" and row == self.args.tiles-1:
            ret = True

        return ret
