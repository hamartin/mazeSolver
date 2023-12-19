

from random import randint


def findIndex(col, row, tiles):
    assert isinstance(col, int)
    assert isinstance(row, int)
    assert isinstance(tiles, int)
    return row+col*tiles

def getRandomIndex(numbTiles):
    assert isinstance(numbTiles, int)
    col, row = 0, 0
    while col == 0 and row == 0:
        col = randint(0, numbTiles-1)
        row = randint(0, numbTiles-1)
    return {"column": col, "row": row}
