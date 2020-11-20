# ChessGame.py

import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.font import Font
from PIL import ImageTk
from ChessBoard import initClassic
from Pieces import Piece, Empty, Disabled
from Utils import getResourcePath, fetchImage
from ChessVector import ChessVector
from Exceptions import PromotionError, Illegal
from formatPGN import *


IMAGEDIR = getResourcePath(__file__, "Sprites\\")
COLORS = {
    "black": (75, 75, 75),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 00)
}


class ScrollableLabel(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, *args, **kwargs)
        self.label = tk.Label(self)
        self.scroll = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.canvas.create_window(0, 0, anchor="nw", window=self.label)
        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.canvas.grid(row=0, column=0, sticky="NSEW")
        self.scroll.grid(row=0, column=1, sticky="NSEW")

        self.label.bind("<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")))


class ChessFrame(tk.Frame):
    def __init__(self, master, board, **kwargs):
        super().__init__(master, **kwargs, bg="red")

        # Geometry managment
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

        self.boardCanv = tk.Canvas(self, width=400, height=400, bg="black", highlightthickness=0)
        self.historyFrame = tk.Frame(self, width=200, height=200, bg="green", highlightbackground="black", highlightthickness=1)
        self.evalFrame = tk.Frame(self, width=200, height=200, bg="blue", highlightbackground="black", highlightthickness=1)

        self.historyFrame.grid_rowconfigure(1, weight=1)
        self.historyFrame.grid_columnconfigure(0, weight=1)
        self.evalFrame.grid_rowconfigure(1, weight=1)
        self.evalFrame.grid_columnconfigure(0, weight=1)

        self.boardCanv.grid(row=0, rowspan=2, column=0, sticky="NSEW")
        self.historyFrame.grid(row=0, column=1, sticky="NSEW")
        self.evalFrame.grid(row=1, column=1, sticky="NSEW")

        self.historyFrame.grid_propagate(0)
        self.evalFrame.grid_propagate(0)

        # Chesscanvas related
        self.board = board
        self.turnorder = self.board.turnorder
        self.currentTurn = self.turnorder[0]
        self.selected = None

        self.square = 64
        self.blackbarTop, self.blackbarBottom, self.blackbarLeft, self.blackbarRight = 0, 0, 0, 0

        # Generate board and pieceimages
        self.squares = {}
        self.images = {}

        for i, piece in enumerate(self.board):
            color = ("saddle brown", "white")[(i + int((i) / self.board.cols)) % 2 == 0]
            if not isinstance(piece, Disabled):
                pos = piece.vector
                self.squares[pos.tuple()] = (self.boardCanv.create_rectangle(
                    self.blackbarLeft + (pos.col * self.square),
                    self.blackbarTop + (pos.row * self.square),
                    self.blackbarLeft + ((pos.col + 1) * self.square),
                    self.blackbarTop + ((pos.row + 1) * self.square),
                    fill=color,
                    outline="black"))

                if not isinstance(piece, Empty):
                    self.getImage(piece)

        # Variables
        self.historyString = tk.StringVar(self)
        self.evalString = tk.StringVar(self)

        # Fonts
        self.headingFont = Font(family="Curier", size=20, weight="bold")
        self.labelFont = Font(family="Curier", size=20, weight="bold")

        # Labels
        self.historyHeading = tk.Label(self.historyFrame, text="HISTORY", font=self.headingFont)
        self.evalHeading = tk.Label(self.evalFrame, text="EVALUATION", font=self.headingFont)
        self.historyLabel = ScrollableLabel(self.historyFrame)
        self.evalLabel = ScrollableLabel(self.evalFrame)

        self.historyHeading.grid(row=0, column=0, sticky="NSEW")
        self.evalHeading.grid(row=0, column=0, sticky="NSEW")
        self.historyLabel.grid(row=1, column=0, sticky="NSEW")
        self.evalLabel.grid(row=1, column=0, sticky="NSEW")

        # Chesscanvas actions
        self.boardCanv.bind("<Configure>", self.resize)
        self.boardCanv.bind("<Button-1>", self.chessInteract)

    def getImage(self, piece):
        """Get image of given piece"""
        try:
            return self.images[piece.color + piece.__class__.__name__]
        except KeyError:
            return self.createImage(piece)

    def createImage(self, piece):
        """Create and return image of given piece"""
        img = fetchImage(COLORS[piece.color], IMAGEDIR + piece.__class__.__name__ + ".png")
        self.images[piece.color + piece.__class__.__name__] = img
        return img

    def chessInteract(self, event, *args):
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

        except Illegal as e:
            messagebox.showerror(title="Illegal", message=e)

    def select(self, vec):
        self.clearHighlights()
        piece = self.board[vec]
        if isinstance(piece, Piece) and piece.color == self.currentTurn:
            self.selected = piece
            self.boardCanv.itemconfigure(self.squares[piece.vector.tuple()], fill="light goldenrod")
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
                if self.boardCanv.itemcget(square, "fill") != color:
                    self.boardCanv.itemconfig(square, fill=color)
        self.selected = None

    def highlight(self, vecs):
        for vec in vecs:
            self.boardCanv.itemconfigure(self.squares[vec.tuple()], fill="sky blue")

    def resize(self, *args):
        rankH = int(self.boardCanv.winfo_width() / self.board.rows)
        fileH = int(self.boardCanv.winfo_height() / self.board.cols)
        self.square = (rankH, fileH)[rankH > fileH]
        self.blackbarLeft = int((self.boardCanv.winfo_width() - (self.board.rows * self.square)) / 2)
        self.blackbarRight = self.boardCanv.winfo_width() - self.blackbarLeft - (self.board.rows * self.square)
        self.blackbarTop = int((self.boardCanv.winfo_height() - (self.board.cols * self.square)) / 2)
        self.blackbarBottom = self.boardCanv.winfo_height() - self.blackbarTop - (self.board.rows * self.square)

        self.update()

    def update(self, *args):
        """Update all widgets of frame"""
        self.historyString.set(readable(self.board.history, 2))
        print(readable(self.board.history, 2))
        self.photos = []

        for (row, col), square in self.squares.items():
            self.boardCanv.coords(square,
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

                    self.boardCanv.create_image(
                        self.blackbarLeft + (pos.col * self.square) + int(self.square / 2),
                        self.blackbarTop + (pos.row * self.square) + int(self.square / 2),
                        image=photoImg)


root = tk.Tk()

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

chessFrame = ChessFrame(root, board=initClassic(), height=400, width=400)
chessFrame.grid(row=0, column=0, sticky="NSEW")

root.minsize(400, 240)
root.mainloop()
