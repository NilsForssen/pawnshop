from ChessBoard import initClassic, init4P
from Pieces import Piece, Queen
from Pieces import Empty, Disabled
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from Utils import getResourcePath
from ChessVector import ChessVector
from Exceptions import PromotionError

root = tk.Tk()

COLORS = {
    "black": (50, 50, 50),      # Not pure black for visual purposes
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 00)
}


def getImage(color, imgpath):
    img = Image.open(imgpath)
    pixels = img.load()
    fullGreen = 255
    r, g, b = color
    for x in range(img.height):
        for y in range(img.width):
            _, greenVal, _, alpha = pixels[x, y]
            if greenVal:
                ratio = greenVal / fullGreen
                pixels[x, y] = (round(r * ratio), round(g * ratio), round(b * ratio), alpha)
    return img


BOARD = initClassic()
IMAGEDIR = getResourcePath(__file__, "Sprites\\")

outString = tk.StringVar()

root.grid_rowconfigure((0, 1), weight=1)
root.grid_columnconfigure(0, weight=4)
root.grid_columnconfigure(1, weight=1)

# Variables


class ChessCanvas(tk.Canvas):
    def __init__(self, master, board, **kwargs):
        super().__init__(master, **kwargs)

        self.board = board
        self.turnorder = self.board.turnorder
        self.currentTurn = self.turnorder[0]
        self.selected = None

        self.square = 64
        self.blackbarTop, self.blackbarBottom, self.blackbarLeft, self.blackbarRight = 0, 0, 0, 0

        self.squares = {}
        self.images = {}

        for i, piece in enumerate(self.board):
            color = ("saddle brown", "white")[(i + int((i) / self.board.cols)) % 2 == 0]
            if not isinstance(piece, Disabled):
                pos = piece.vector
                self.squares[pos.tuple()] = (self.create_rectangle(
                    self.blackbarLeft + (pos.col * self.square),
                    self.blackbarTop + (pos.row * self.square),
                    self.blackbarLeft + ((pos.col + 1) * self.square),
                    self.blackbarTop + ((pos.row + 1) * self.square),
                    fill=color,
                    outline="black"))

                if not isinstance(piece, Empty):
                    self.getImage(piece)

    def getImage(self, piece):
        pColor = piece.color
        pClass = piece.__class__.__name__
        try:
            return self.images[pColor + pClass]
        except KeyError:
            return self.createImage(pColor, pClass)

    def createImage(self, pColor, pClass):
        img = getImage(COLORS[pColor], IMAGEDIR + pClass + ".png")
        self.images[pColor + pClass] = img
        return img

    def interact(self, event, *args):
        if event.x + self.blackbarRight < self.winfo_width() and event.x - self.blackbarLeft > 0 and event.y + self.blackbarBottom < self.winfo_height() and event.y - self.blackbarTop > 0:
            vec = ChessVector((int((event.y - self.blackbarTop) / self.square), int((event.x - self.blackbarRight) / self.square)))
            if self.selected is None:
                self.select(vec)
            else:
                if vec in self.selected.getMoves(self.board):
                    self.moveSelected(vec)
                else:
                    self.select(vec)

    def moveSelected(self, vector):
        try:
            print(self.board.movePiece(self.selected.vector, vector))
        except PromotionError:
            msg = "What do you want the pawn to promote to?"
            while True:
                prompt = simpledialog.askstring("Promote!", msg)
                if prompt is None:
                    break
                try:
                    pType = {pType.__name__: pType for pType in self.board.promoteTo[self.selected.color]}[prompt.lower().capitalize()]
                    print(self.board.movePiece(self.selected.vector, vector, promote=pType))
                    break
                except KeyError:
                    msg = prompt + "is Not a valid piece, must be any of \n" + "\n".join([pType.__name__ for pType in self.board.promoteTo[self.selected.color]])
                    continue
        self.clearHighlights()
        self.advanceTurn()
        self.update()

    def select(self, vec):
        self.clearHighlights()
        piece = self.board[vec]
        if isinstance(piece, Piece) and piece.color == self.currentTurn:
            self.selected = piece
            self.itemconfigure(self.squares[piece.vector.tuple()], fill="light goldenrod")
            self.highlight(piece.getMoves(self.board))
        else:
            self.selected = None

    def advanceTurn(self):
        idx = self.turnorder.index(self.currentTurn)
        try:
            self.currentTurn = self.turnorder[idx + 1]
        except IndexError:
            self.currentTurn = self.turnorder[0]

    def clearHighlights(self):
        for i, piece in enumerate(self.board):
            color = ("saddle brown", "white")[(i + int((i) / self.board.cols)) % 2 == 0]
            if not isinstance(piece, Disabled):
                square = self.squares[piece.vector.tuple()]
                if self.itemcget(square, "fill") != color:
                    self.itemconfig(square, fill=color)
        self.selected = None

    def highlight(self, vecs):
        for vec in vecs:
            self.itemconfigure(self.squares[vec.tuple()], fill="sky blue")

    def resize(self, *args):
        rankH = int(self.winfo_width() / self.board.rows)
        fileH = int(self.winfo_height() / self.board.cols)
        self.square = (rankH, fileH)[rankH > fileH]
        self.blackbarLeft = int((self.winfo_width() - (self.board.rows * self.square)) / 2)
        self.blackbarRight = self.winfo_width() - self.blackbarLeft - (self.board.rows * self.square)
        self.blackbarTop = int((self.winfo_height() - (self.board.cols * self.square)) / 2)
        self.blackbarBottom = self.winfo_height() - self.blackbarTop - (self.board.rows * self.square)

        self.update()

    def update(self):
        self.photos = []

        for (row, col), square in self.squares.items():
            self.coords(square,
                self.blackbarLeft + (col * self.square),
                self.blackbarTop + (row * self.square),
                self.blackbarLeft + ((col + 1) * self.square),
                self.blackbarTop + ((row + 1) * self.square))

        for piece in self.board:
            if not isinstance(piece, Disabled):
                pos = piece.vector

                if not isinstance(piece, Empty):
                    img = self.getImage(piece).copy().resize((self.square, self.square))
                    photoImg = ImageTk.PhotoImage(img)

                    # To keep an image on the canvas, a reference to the ImageTk.PhotoImage
                    # object needs to be stored. I have no idea why this is, but oh well,
                    # I will store the reference in the photos list.
                    self.photos.append(photoImg)

                    self.create_image(
                        self.blackbarLeft + (pos.col * self.square) + int(self.square / 2),
                        self.blackbarTop + (pos.row * self.square) + int(self.square / 2),
                        image=photoImg)


boardCanv = ChessCanvas(root, board=BOARD, width=400, height=400, bg="black", highlightthickness=0)
historyCanv = tk.Frame(root, width=200, height=200, bg="green", highlightthickness=0)
evalCanv = tk.Frame(root, width=200, height=200, bg="blue", highlightthickness=0)

boardCanv.grid(row=0, rowspan=2, column=0, sticky="NSEW")
historyCanv.grid(row=0, column=1, sticky="NSEW")
historyCanv.grid_propagate(0)
evalCanv.grid(row=1, column=1, sticky="NSEW")
evalCanv.grid_propagate(0)

outLabel = tk.Label(historyCanv, textvariable=outString)
outLabel.grid()


def resize(event):
    boardCanv.update()


boardCanv.bind("<Button-1>", boardCanv.interact)
boardCanv.bind("<Configure>", boardCanv.resize)

root.minsize(400, 240)
root.mainloop()
