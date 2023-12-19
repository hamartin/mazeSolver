

import io

from random import randint

import pygame

from .cell import Cell
from .food import Food
from .player import Player
from .utils import findIndex


class Crashed(Exception):
    pass
class EatenFood(Exception):
    pass
class NoLivesLeft(Exception):
    pass


class MazeSurface(pygame.Surface):

    COLORS = {
            "darkslategray": pygame.Color("darkslategray")
            }

    def __init__(self, gargs, *args, **kwargs):
        super(MazeSurface, self).__init__(*args, **kwargs)
        self.args = gargs
        self.tileHeight = self.args.height//self.args.tiles
        self.tileWidth = self.args.width//self.args.tiles

        self.foodCells = []
        self.gridCells = []
        self.currentCell = None
        self.nextCell = None

    def _eatFood(self, foodCell):
        if self.args.debug:
            print(f"I ate food: +{self.args.foodpoint} points -> Points: {self.score}")
        self.foodCells.remove(foodCell)
        self.foodCells.append(Food(self.args, (self.tileWidth, self.tileHeight), self))

    def _generateMaze(self):
        breakCount = 1
        stack = []

        while breakCount != len(self.gridCells):
            self.currentCell.visited()
            self.nextCell = self.currentCell.checkNeighbours()
            if self.nextCell:
                self.nextCell.visited()
                breakCount += 1
                stack.append(self.currentCell)
                self._removeWalls(self.currentCell, self.nextCell)
                self.currentCell = self.nextCell
            elif stack:
                self.currentCell = stack.pop()

        self.currentCell = self.gridCells[0]

    def _removeWalls(self, currentCell, nextCell):
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

    def draw(self):
        self.fill(self.COLORS["darkslategray"])
        for cell in self.gridCells:
            cell.draw()
        for cell in self.foodCells:
            cell.draw()
        self.currentCell.drawCurrentCell()

    def move(self, direction):
        assert direction in ["left", "up", "right", "down"]
        col, row = self.currentCell.getIndex()
        ret = "moved"

        if direction == "left":
            if col > 0:
                col -= 1
        elif direction == "right":
            if col < self.args.tiles-1:
                col += 1
        elif direction == "up":
            if row > 0:
                row -= 1
        elif direction == "down":
            if row < self.args.tiles-1:
                row += 1

        # The cell to move to if we are not colliding with anything.
        nextCell = self.gridCells[findIndex(col, row, self.args.tiles)]
        if (self.currentCell.collide(nextCell)
                or self.currentCell.wallCollide(direction)):
            ret = "crashed"
        else:
            nindex = nextCell.getIndex()
            for food in self.foodCells:
                findex = food.getIndex()
                if findex[0] == nindex[0] and findex[1] == nindex[1]:
                    self._eatFood(food)
                    ret = "eaten"
            self.currentCell = nextCell

        return ret

    def reset(self):
        self.gridCells = [
                Cell(self.args,
                     {"column": col, "row": row},
                     (self.tileWidth, self.tileHeight),
                     self)
                for col in range(self.args.tiles)
                for row in range(self.args.tiles)]
        for cell in self.gridCells:
            cell.addGridCellsRef(self.gridCells)

        self.foodCells = [
                Food(self.args,
                     (self.tileWidth, self.tileHeight),
                     self)
                for _ in range(self.args.food)]

        self.currentCell = self.gridCells[0]
        self.nextCell = None
        self._generateMaze()


class ScoreSurface(pygame.Surface):

    COLORS = {
            "darkslategray": pygame.Color("darkslategray"),
            "forestgreen": pygame.Color("forestgreen")
            }
    MARGIN = 5

    def __init__(self, gargs, *args, **kwargs):
        super(ScoreSurface, self).__init__(*args, **kwargs)
        self.args = gargs
        self.font = pygame.font.SysFont('Impact', 150)
        self.text_font = pygame.font.SysFont('Impact', 80)

        self.livesText = self.text_font.render("Lives:", True,
                                               self.COLORS["forestgreen"])
        self.scoreText = self.text_font.render("Score:", True,
                                               self.COLORS["forestgreen"])
        self.highScoreText = self.text_font.render("High Score:", True,
                                                   self.COLORS["forestgreen"])

        # Game numbers
        self.score = 0
        self.highscore = 0
        self.lives = 3

    def addScore(self, points):
        assert isinstance(points, int)
        self.score += points
        if self.score > self.highscore:
            self.highscore = self.score

    def crashed(self):
        self.lives -= 1
        if self.lives < 1:
            return "dead"

    def draw(self):
        dh = self.args.height/3

        self.fill(self.COLORS["darkslategray"])

        # Lives score
        self.blit(self.livesText, (50, self.MARGIN))
        self.livesPoints = self.font.render(f"{self.lives}", True,
                                            self.COLORS["forestgreen"])
        self.blit(self.livesPoints, (70,
                                     self.livesText.get_height()+self.MARGIN))

        # Score
        self.blit(self.scoreText, (50, dh+self.MARGIN))
        self.scorePoints = self.font.render(f"{self.score}", True,
                                           self.COLORS["forestgreen"])
        self.blit(self.scorePoints, (70,
                                     dh+self.scoreText.get_height()+self.MARGIN))

        # High score
        self.blit(self.highScoreText, (50, 2*dh+self.MARGIN))
        self.highScorePoints = self.font.render(f"{self.highscore}", True,
                                                self.COLORS["forestgreen"])
        self.blit(self.highScorePoints, (70,
                                         2*dh+self.highScoreText.get_height()+self.MARGIN))

    def reset(self):
        self.score = 0
        self.lives = 3


class Maze():

    COLORS = {
            "darkslategray": pygame.Color("darkslategray")
            }
    EATENPOINTS = 10
    SCORESURFACEWIDTH = 300
    THICKNESS = 2

    def __init__(self, args):
        self.args = args
        self.running = False

        pygame.init()
        self.mazeSurface = MazeSurface(self.args,
                                       (self.args.width+self.THICKNESS,
                                        self.args.height+self.THICKNESS))
        self.scoreSurface = ScoreSurface(self.args, (self.SCORESURFACEWIDTH,
                                                     self.args.height+self.THICKNESS))
        self.screen = pygame.display.set_mode(
                (self.args.width+self.SCORESURFACEWIDTH+self.THICKNESS,
                 self.args.height+self.THICKNESS))
        self.clock = pygame.time.Clock()
        self.reset()

    def draw(self):
        self.screen.fill(self.COLORS["darkslategray"])
        self.mazeSurface.draw()
        self.scoreSurface.draw()
        self.screen.blit(self.mazeSurface, (0, 0))
        self.screen.blit(self.scoreSurface, (self.args.width+1, 0))

        pygame.display.flip()
        self.clock.tick(self.args.fps)

    def getInput(self):
        """The try except stuff below is bloody ugly. It needs to be fixed!"""
        ret = None
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
                elif event.key == pygame.K_LEFT:
                        ret = self.mazeSurface.move("left")
                elif event.key == pygame.K_RIGHT:
                        ret = self.mazeSurface.move("right")
                elif event.key == pygame.K_UP:
                        ret = self.mazeSurface.move("up")
                elif event.key == pygame.K_DOWN:
                        ret = self.mazeSurface.move("down")

        if ret == "crashed":
            if self.scoreSurface.crashed() == "dead":
                self.reset()
            elif ret == "eaten":
                self.scoreSurface.addScore(self.EATENPOINTS)

    def reset(self):
        self.mazeSurface.reset()
        self.scoreSurface.reset()

    def run(self):
        self.reset()

        self.running = True
        while self.running:
            self.draw()
            self.getInput()
