from ChessBoard import initClassic
import tkinter as tk

root = tk.Tk()

root.grid_rowconfigure((0, 1), weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)


# Variables
board = initClassic()
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


def resize(event):

    rankH = int(event.width / board.rows)
    fileH = int(event.height / board.cols)
    squareH = (rankH, fileH)[rankH > fileH]
    extraX = int((event.width - (board.rows * squareH)) / 2)
    extraY = int((event.height - (board.cols * squareH)) / 2)

    boardCanv.delete("all")
    boardCanv.create_rectangle(
        extraX,
        extraY,
        extraX + (squareH * board.cols),
        extraY + (squareH * board.rows),
        fill="SADDLE BROWN", outline="BLACK")

    for row in range(board.rows):

        for col in range(int(board.cols / 2)):
            startX = extraX + (squareH * (row % 2))

            boardCanv.create_rectangle(
                startX + (2 * col) * squareH,
                extraY + (row * squareH),
                startX + ((2 * col) + 1) * squareH,
                extraY + ((row + 1) * squareH),
                fill="WHITE", outline="BLACK")

    outString.set(" . ".join(map(str, [extraX, extraY, rankH, fileH, event.width, event.height])))


boardCanv.bind("<Configure>", resize)
root.mainloop()
