

def findIndex(col, row, tiles):
    assert isinstance(col, int)
    assert isinstance(row, int)
    assert isinstance(tiles, int)
    return row+col*tiles
