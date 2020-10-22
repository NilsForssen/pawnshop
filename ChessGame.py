from ChessBoard import initClassic
from ChessVector import ChessVector
import tkinter as tk


root = tk.Tk()

root.grid_rowconfigure((0, 1), weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)


# Variables
BOARD = initClassic()
outString = tk.StringVar()


class ChessCanvas(tk.Canvas):
    def __init__(self, master, board=board, **kwargs):
        super().__init__(master, **kwargs)
        self.board = board
        self.master = master

        self.draw()

    def _fitBoard(self):
        rankH = int(self.winfo_width / self.board.rows)
        fileH = int(self.winfo_height / self.board.cols)
        self.square = (rankH, fileH)[rankH > fileH]
        self.blackbarX = int((self.winfo_width - (self.board.rows * self.square)) / 2)
        self.blackbarY = int((self.winfo_height - (self.board.cols * self.square)) / 2)

    def coordInBoard(self, x, y):
        if isinstance(self.master.winfo_containing(x, y), type(self)):
            if x <

    def draw(self, highlights=dict()):
        self._fitBoard()
        self.delete("all")
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                try:
                    color = highlights[ChessVector((row, col)).getStr(self.board)]
                except Exception:
                    color = ("WHITE", "SADDLE BROWN")[(col + (row % 2)) % 2]

                self.create_rectangle(
                    extraX + (col * squareH),
                    extraY + (row * squareH),
                    extraX + ((col + 1) * squareH),
                    extraY + ((row + 1) * squareH),
                    fill=color, outline="BLACK")


# Main Frames
boardCanv = ChessCanvas(root, width=500, height=500, bg="Black", highlightthickness=0)
historyCanv = tk.Frame(root, width=200, height=250, bg="GREEN", highlightthicknes=0)
evalCanv = tk.Frame(root, width=200, height=250, bg="BLUE", highlightthickness=0)

boardCanv.grid(row=0, rowspan=2, column=0, sticky="NSEW")
historyCanv.grid(row=0, column=1, sticky="NSEW")
historyCanv.grid_propagate(0)
evalCanv.grid(row=1, column=1, sticky="NSEW")
evalCanv.grid_propagate(0)

outLabel = tk.Label(historyCanv, textvariable=outString)
outLabel.grid()


def resize(event):
    # drawBoard(event.width, event.height, {"e3": "RED"})
    boardCanv.draw(event.width, event.height)
    outString.set(" . ".join(map(str, [event.width, event.height])))


def onClick(event):
    if boardCanv.coordInBoard(event.x, event.y):
        print("yes")
    print(event)
    # Buttonclick on canvas


boardCanv.bind("<Button-1>", onClick)
boardCanv.bind("<Configure>", resize)
root.mainloop()
