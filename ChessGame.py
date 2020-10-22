from ChessBoard import initClassic
import tkinter as tk


root = tk.Tk()

root.grid_rowconfigure((0, 1), weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)


# Variables
BOARD = initClassic()
outString = tk.StringVar()

# Main Frames
boardCanv = tk.Canvas(root, width=500, height=500, bg="Black", highlightthickness=0)
historyCanv = tk.Frame(root, width=200, height=250, bg="GREEN", highlightthicknes=0)
evalCanv = tk.Frame(root, width=200, height=250, bg="BLUE", highlightthickness=0)

boardCanv.grid(row=0, rowspan=2, column=0, sticky="NSEW")
historyCanv.grid(row=0, column=1, sticky="NSEW")
historyCanv.grid_propagate(0)
evalCanv.grid(row=1, column=1, sticky="NSEW")
evalCanv.grid_propagate(0)

# Draw chess in canvas


outLabel = tk.Label(historyCanv, textvariable=outString)

outLabel.grid()

def drawBoard(canvW, canvH, **highlights):

    rankH = int(canvW / BOARD.rows)
    fileH = int(canvH / BOARD.cols)
    squareH = (rankH, fileH)[rankH > fileH]
    extraX = int((canvW - (BOARD.rows * squareH)) / 2)
    extraY = int((canvH - (BOARD.cols * squareH)) / 2)

    boardCanv.delete("all")

    for row in range(BOARD.rows):

        for col in range(int(BOARD.cols)):
            try:
                color = highlights[]
            color = ("WHITE", "SADDLE BROWN")[(col + (row%2)) %2]

            boardCanv.create_rectangle(
                extraX + (col * squareH),
                extraY + (row * squareH),
                extraX + ((col + 1) * squareH),
                extraY + ((row + 1) * squareH),
                fill=color, outline="BLACK")


def resize(event):

    drawBoard(event.width, event.height)

    outString.set(" . ".join(map(str, [event.width, event.height])))


boardCanv.bind("<Configure>", resize)
root.mainloop()
