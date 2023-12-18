

from random import choice

import pygame

from .utils import findIndex


COLORS = {
        "black": pygame.Color("black"), # (0, 0, 0)
        "darkorange": pygame.Color("darkorange"), # (255, 140, 0)
        "darkslategray": pygame.Color("darkslategray"), # (47, 79, 79)
        "saddlebrown": pygame.Color("saddlebrown") # (139, 69, 19)
        }


class Cell():

    THICKNESS = 2

    def __init__(self, index, tiles, screen):
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

    def draw(self):
        col = self.index["column"]*self.tiles["tileWidth"]
        row = self.index["row"]*self.tiles["tileHeight"]
        colDest = self.tiles["tileWidth"]+self.THICKNESS
        rowDest = self.tiles["tileHeight"]+self.THICKNESS
        if self.visitedBool:
            pygame.draw.rect(
                    self.screen, COLORS["black"],
                    (col, row, colDest, rowDest))
        if self.walls["top"]:
            pygame.draw.line(
                    self.screen, COLORS["darkorange"],
                    (col, row),
                    (col+self.tiles["tileWidth"], row),
                    self.THICKNESS)
        if self.walls["right"]:
            pygame.draw.line(
                    self.screen, COLORS["darkorange"],
                    (col+self.tiles["tileWidth"], row),
                    (col+self.tiles["tileWidth"], row+self.tiles["tileHeight"]),
                    self.THICKNESS)
        if self.walls["bottom"]:
            pygame.draw.line(
                    self.screen, COLORS["darkorange"],
                    (col, row+self.tiles["tileHeight"]),
                    (col+self.tiles["tileWidth"], row+self.tiles["tileHeight"]),
                    self.THICKNESS)
        if self.walls["left"]:
            pygame.draw.line(
                    self.screen, COLORS["darkorange"],
                    (col, row),
                    (col, row+self.tiles["tileHeight"]),
                    self.THICKNESS)

    def drawCurrentCell(self):
        col = self.index["column"]*self.tiles["tileWidth"]+self.THICKNESS
        row = self.index["row"]*self.tiles["tileHeight"]+self.THICKNESS
        colDest = self.tiles["tileWidth"]-self.THICKNESS
        rowDest = self.tiles["tileHeight"]-self.THICKNESS
        pygame.draw.rect(self.screen, COLORS["saddlebrown"],
                         (col, row, colDest, rowDest))

    def getIndex(self, colrow=None):
        assert colrow is None or colrow in ["column", "row"]
        if not colrow:
            return self.index["column"], self.index["row"]
        return self.index[colrow]

    def removeWall(self, wall):
        assert wall in ["left", "top", "right", "bottom"]
        self.walls[wall] = False

    def visited(self):
        self.visitedBool = True


class Maze():

    THICKNESS = 2

    def __init__(self, args):
        self.args = args
        self.size = {
                "width": self.args.width,
                "height": self.args.height
                }
        self.tiles = {
                "numbTiles": self.args.tiles,
                "tileWidth": self.size["width"]//self.args.tiles,
                "tileHeight": self.size["height"]//self.args.tiles
                }
        self.fps = self.args.fps

        self.gridCells = ()
        self.currentCell = None
        self.nextCell = None
        self.running = False

        pygame.init()
        # Adding THICKNESS here so that the outer most right lines and lower
        # lines does not get drawn outside the window.
        self.mazeSurface = pygame.Surface((self.size["width"]+self.THICKNESS,
                                           self.size["height"]+self.THICKNESS))
        # The menu on the right is 300 wide.
        self.screen = pygame.display.set_mode(
                (self.size["width"]+300,
                 self.size["height"]+self.THICKNESS))
        self.clock = pygame.time.Clock()

    def drawMazeSurface(self):
        self.mazeSurface.fill(COLORS["darkslategray"])
        for cell in self.gridCells:
            cell.draw()
        self.currentCell.drawCurrentCell()

    def drawScreen(self):
        self.screen.fill(COLORS["darkslategray"])
        self.drawMazeSurface()
        self.screen.blit(self.mazeSurface, (0, 0))

        pygame.display.flip()
        self.clock.tick(self.fps)

    def generateMaze(self):
        self.reset()
        breakCount = 1
        stack = []

        while breakCount != len(self.gridCells):
            self.currentCell.visited()
            self.nextCell = self.currentCell.checkNeighbours()
            if self.nextCell:
                self.nextCell.visited()
                breakCount += 1
                stack.append(self.currentCell)
                self.removeWalls(self.currentCell, self.nextCell)
                self.currentCell = self.nextCell
            elif stack:
                self.currentCell = stack.pop()

        self.currentCell = self.gridCells[0]

    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_g:
                    self.generateMaze()
                elif event.key == pygame.K_LEFT:
                    self.move("left")
                elif event.key == pygame.K_RIGHT:
                    self.move("right")
                elif event.key == pygame.K_UP:
                    self.move("up")
                elif event.key == pygame.K_DOWN:
                    self.move("down")

    def move(self, direction):
        assert direction in ["left", "up", "right", "down"]
        col, row = self.currentCell.getIndex()
        if direction == "left":
            if col > 0:
                col -= 1
        elif direction == "right":
            if col < self.tiles["numbTiles"]-1:
                col += 1
        elif direction == "up":
            if row > 0:
                row -= 1
        elif direction == "down":
            if row < self.tiles["numbTiles"]-1:
                row += 1
        self.currentCell = self.gridCells[findIndex(col, row, self.tiles["numbTiles"])]

    def removeWalls(self, currentCell, nextCell):
        dcol = currentCell.getIndex("column")-nextCell.getIndex("column")
        if dcol == 1:
            currentCell.removeWall("left")
            nextCell.removeWall("right")
        elif dcol == -1:
            currentCell.removeWall("right")
            nextCell.removeWall("left")
        drow = currentCell.getIndex("row")-nextCell.getIndex("row")
        if drow == 1:
            currentCell.removeWall("top")
            nextCell.removeWall("bottom")
        elif drow == -1:
            currentCell.removeWall("bottom")
            nextCell.removeWall("top")

    def reset(self):
        self.gridCells = [Cell({"column": col, "row": row}, self.tiles,
                               self.mazeSurface)
                          for col in range(self.tiles["numbTiles"])
                          for row in range(self.tiles["numbTiles"])]
        for cell in self.gridCells:
            cell.addGridCellsRef(self.gridCells)
        self.currentCell = self.gridCells[0]
        self.nextCell = None

    def run(self):
        self.reset()

        self.running = True
        while self.running:
            #self.updateScreen()
            self.drawScreen()
            self.getInput()
