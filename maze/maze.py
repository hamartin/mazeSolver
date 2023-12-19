

import io

from random import randint

import pygame

from .cell import Cell
from .food import Food
from .player import Player
from .utils import findIndex


class Maze():

    COLORS = {
            "darkslategray": pygame.Color("darkslategray"),
            "forestgreen": pygame.Color("forestgreen"),
            }
    THICKNESS = 2

    def __init__(self, args):
        self.args = args
        self.tileWidth = self.args.width//self.args.tiles
        self.tileHeight = self.args.height//self.args.tiles

        # Cell variables
        self.gridCells = []
        self.foodCells = []
        self.player = None

        # Game numbers
        self.score = 0
        self.highscore = 0
        self.lives = 3

        self._pygameinit()

    def _pygameInit(self):
        # TODO: We need to get rid of the current cell as the player replaces it
        # in the game. However in the maze generation, the current cell needs to
        # be aware of.
        self.currentCell = None
        self.nextCell = None

        self.running = False

        pygame.init()
        # Some fonts used in the application.
        self.font = pygame.font.SysFont('Impact', 150)
        self.text_font = pygame.font.SysFont('Impact', 80)
        # Adding THICKNESS here so that the outer most right lines and lower
        # lines does not get drawn outside the window.
        self.mazeSurface = pygame.Surface((self.args.width+self.THICKNESS,
                                           self.args.height+self.THICKNESS))
        self.scoreSurface = pygame.Surface((300,
                                            self.args.height+self.THICKNESS))
        # The menu on the right is 300 wide.
        self.screen = pygame.display.set_mode(
                (self.args.width+300,
                 self.args.height+self.THICKNESS))
        self.clock = pygame.time.Clock()

    def drawMazeSurface(self):
        self.mazeSurface.fill(self.COLORS["darkslategray"])
        for cell in self.gridCells:
            cell.draw()
        for foodCell in self.foodCells:
            foodCell.drawFood()
        self.currentCell.drawCurrentCell()

    def drawScoreSurface(self):
        dh = self.args.height/3
        margin = 5

        self.scoreSurface.fill(self.COLORS["darkslategray"])

        # Lives score
        self.livesText = self.text_font.render("Lives:", True,
                                               self.COLORS["forestgreen"])
        self.scoreSurface.blit(self.livesText, (50, margin))
        self.livesPoints = self.font.render(f"{self.lives}", True,
                                            self.COLORS["forestgreen"])
        self.scoreSurface.blit(
                self.livesPoints,
                (70, self.livesText.get_height()+margin))

        # Score
        self.scoreText = self.text_font.render("Score:", True,
                                               self.COLORS["forestgreen"])
        self.scoreSurface.blit(self.scoreText, (50, dh+margin))
        self.scoret = self.font.render(f"{self.score}", True,
                                      self.COLORS["forestgreen"])
        self.scoreSurface.blit(
                self.scoret,
                (70, dh+self.scoreText.get_height()+margin))

        # High score
        self.highScoreText = self.text_font.render("High Score:", True,
                                                   self.COLORS["forestgreen"])
        self.scoreSurface.blit(self.highScoreText, (50, 2*dh+margin))
        self.highScorePoints = self.font.render(f"{self.highscore}", True,
                                                self.COLORS["forestgreen"])
        self.scoreSurface.blit(
                self.highScorePoints,
                (70, 2*dh+self.highScoreText.get_height()+margin))

    def drawScreen(self):
        self.screen.fill(self.COLORS["darkslategray"])
        self.drawMazeSurface()
        self.drawScoreSurface()
        self.screen.blit(self.mazeSurface, (0, 0))
        self.screen.blit(self.scoreSurface, (self.args.width+1, 0))

        pygame.display.flip()
        self.clock.tick(self.args.fps)

    def eatFood(self, foodCell):
        self.score += self.args.foodpoint
        if self.args.debug:
            print(f"I ate food: +{self.args.foodpoint} points -> Points: {self.score}")
        self.foodCells.remove(foodCell)
        self.foodCells.append(Food(self.args, (self.tileWidth, self.tileHeight), self.mazeSurface))

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
        if (self.currentCell.collide(nextCell) or
                self.currentCell.wallCollide(direction)):
            self.lives -= 1
            if self.args.debug:
                print(f"Lives: {self.lives}")
        else:
            nindex = nextCell.getIndex()
            for food in self.foodCells:
                findex = food.getIndex()
                if findex[0] == nindex[0] and findex[1] == nindex[1]:
                    self.eatFood(food)
            self.currentCell = nextCell

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
        self.gridCells = [Cell(self.args,
                               {"column": col, "row": row},
                               (self.tileWidth, self.tileHeight),
                               self.mazeSurface)
                          for col in range(self.args.tiles)
                          for row in range(self.args.tiles)]
        for cell in self.gridCells:
            cell.addGridCellsRef(self.gridCells)
        self.foodCells = [Food(self.args,
                               (self.tileWidth, self.tileHeight),
                               self.mazeSurface)
                          for _ in range(self.args.food)]
        self.currentCell = self.gridCells[0]
        self.nextCell = None
        self.score = 0
        self.lives = 3

    def run(self):
        self.generateMaze()

        self.running = True
        while self.running:
            self.drawScreen()
            self.updateGame()
            self.getInput()

    def updateGame(self):
        if self.score > self.highscore:
            self.highscore = self.score
        if self.lives < 1:
            self.generateMaze()
