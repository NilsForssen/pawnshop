def unpackIndexSlices(idx):
    try:
        r, c = idx
    except (TypeError, ValueError):
        raise ValueError("Index position must be 2-dimensional.") from None

    if type(r) is not slice:
        r = slice(r, r + 1)
    if type(c) is not slice:
        c = slice(c, c + 1)

    return r, c


from ChessVector import ChessVector

vecList = [
    ChessVector((1, 0)),
    ChessVector((2, 0)),
    ChessVector((3, 0))
]

thisSlice = slice(1, 3, 1)
thisPos = (thisSlice, slice(1, 5, 2))
print(unpackIndexSlices(thisPos))
