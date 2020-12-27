# ChessGame.py

import tkinter as tk
import webbrowser
from tkinter import simpledialog, filedialog, messagebox
from tkinter.font import Font
from PIL import ImageTk
from ChessBoard import initClassic, init4P
from Pieces import Piece, Empty, Disabled
from Utils import getResourcePath, fetchImage
from ChessVector import ChessVector
from Exceptions import PromotionError, DisabledError
from GameNotations import *


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
        self.canvas.bind("<Configure>", self.resize)

    def resize(self, event):
        self.label.configure(wraplength=event.width - 10)


class ChessGame(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()

        # Geometry managment
        self.minsize(600, 400)
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure(0, weight=10)
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
        self.boardInits = {
            "Classic": initClassic,
            "4P": init4P
        }
        self.currentBoard = "Classic"
        self.board = self.boardInits[self.currentBoard]()
        self.kingsInCheck = []
        self.mated = False
        self.selected = None

        self.square = 64
        self.blackbarTop, self.blackbarBottom, self.blackbarLeft, self.blackbarRight = 0, 0, 0, 0

        # Variables
        self.historyString = tk.StringVar(self)
        self.evalString = tk.StringVar(self)

        # Fonts
        self.headingFont = Font(family="Curier", size=18, weight="bold")
        self.labelFont = Font(family="Curier", size=12, weight="normal")

        # Labels
        self.historyHeading = tk.Label(self.historyFrame, text="HISTORY", font=self.headingFont)
        self.evalHeading = tk.Label(self.evalFrame, text="EVALUATION", font=self.headingFont)
        self.historyLabel = ScrollableLabel(self.historyFrame)
        self.evalLabel = ScrollableLabel(self.evalFrame)

        self.historyLabel.label.configure(textvariable=self.historyString, justify="left", font=self.labelFont)
        self.evalLabel.label.configure(justify="left", font=self.labelFont)

        self.historyHeading.grid(row=0, column=0, sticky="NSEW")
        self.evalHeading.grid(row=0, column=0, sticky="NSEW")
        self.historyLabel.grid(row=1, column=0, sticky="NSEW")
        self.evalLabel.grid(row=1, column=0, sticky="NSEW")

        # Menubar
        self.menuBar = tk.Menu(self, tearoff=0)

        self.gameMenu = tk.Menu(self.menuBar)
        self.newGameMenu = tk.Menu(self.menuBar)
        self.onlineMenu = tk.Menu(self.menuBar)

        self.newGameMenu.add_command(label="Classic", command=lambda: self.reInitBoard("Classic"))
        self.newGameMenu.add_command(label="Four Players", command=lambda: self.reInitBoard("4P"))

        self.gameMenu.add_command(label="Save PGN", command=self.exportPGN)
        self.gameMenu.add_command(label="Load PGN", command=self.importPGN)
        self.gameMenu.add_command(label="Copy FEN", command=self.exportFEN)
        self.gameMenu.add_command(label="Paste FEN", command=self.importFEN)
        self.gameMenu.add_separator()
        self.gameMenu.add_cascade(label="New Game", menu=self.newGameMenu)
        self.gameMenu.add_command(label="Reset", command=self.reInitBoard)
        self.gameMenu.add_separator()
        self.gameMenu.add_command(label="Exit", command=lambda: self.destroy())

        self.onlineMenu.add_command(label="Host game")
        self.onlineMenu.add_command(label="Join game")

        self.menuBar.add_cascade(label="Game", menu=self.gameMenu)
        self.menuBar.add_cascade(label="Online", menu=self.onlineMenu)
        self.menuBar.add_command(label="Help", command=lambda: webbrowser.open("https://www.bible.com/sv"))

        self.config(menu=self.menuBar)

        # Chesscanvas actions
        self.boardCanv.bind("<Configure>", self.resize)
        self.boardCanv.bind("<Button-1>", self.chessInteract)

        # Generate board and pieceimages
        self.drawBoard()

        # Mainloop
        self.mainloop()

    def drawBoard(self):
        self.selected = None
        self.boardCanv.delete("all")
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

        self.updateGraphics()

    def importPGN(self):
        with filedialog.askopenfile(title="Open PGN file", filetypes=[("PGN file", ".pgn"), ("Text file", ".txt")]) as file:
            self.board = PGN2Board(file.read())
            self.drawBoard()

    def exportPGN(self):
        with filedialog.asksaveasfile(title="Save PGN file", defaultextension=".pgn", filetypes=[("PGN file", ".pgn")]) as file:
            file.write(board2PGN(self.board, players=2))

    def exportFEN(self):
        self.clipboard_append(board2FEN(self.board))
        simpledialog.messagebox.showinfo("FEN Copied!", "FEN-string has been copied to clipboard!")

    def importFEN(self):
        FEN = simpledialog.askstring("Load FEN!", "Enter a FEN string to load into the board.")
        self.board = FEN2Board(FEN)
        self.drawBoard()

    def reInitBoard(self, boardType=None):
        if boardType is not None:
            self.currentBoard = boardType
        self.board = self.boardInits[self.currentBoard]()
        self.resize()
        self.drawBoard()

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
        print(self.mated)
        if not self.mated and self.board.ready:
            if event.x + self.blackbarRight < self.boardCanv.winfo_width() and event.x - self.blackbarLeft > 0 and event.y + self.blackbarBottom < self.boardCanv.winfo_height() and event.y - self.blackbarTop > 0:
                vec = ChessVector((int((event.y - self.blackbarTop) / self.square), int((event.x - self.blackbarRight) / self.square)))

                try:
                    piece = self.board[vec]
                except DisabledError:
                    pass
                else:
                    if self.selected is not None:
                        moves = self.selected.getMoves(self.board)
                        if vec.matches(moves):
                            self.moveSelected(vec)

                            if any(self.board.checks.values()):
                                for color in [col for col, value in self.board.checks.items() if value]:
                                    for king in self.board.kings[color]:
                                        if self.board.isThreatened(king.vector, color):
                                            if king not in self.kingsInCheck:
                                                self.kingsInCheck.append(king)
                                        else:
                                            if king in self.kingsInCheck:
                                                self.kingsInCheck.remove(king)
                            else:
                                self.kingsInCheck = []

                            self.clearHighlights()

                        elif vec == self.selected.vector:
                            self.clearHighlights()
                        else:
                            if isinstance(piece, Piece) and piece.color == self.board.currentTurn:
                                self.select(piece, highlights=piece.getMoves(self.board))
                            else:
                                self.clearHighlights()
                    else:
                        if isinstance(piece, Piece) and piece.color == self.board.currentTurn:
                            self.select(piece, highlights=piece.getMoves(self.board))
                        else:
                            self.clearHighlights()

                    if any(self.board.checkmates.values()):
                        while True:
                            if len(self.board.checkmates.keys()) > 2:
                                for color, value in self.board.checkmates.items():
                                    if value:
                                        self.board.removeColor(color)
                                        self.updateGraphics()
                                        break
                                else:
                                    break
                            else:
                                messagebox.showinfo("Checkmate!", f"{[color for color, value in self.board.checkmates.items() if value].pop()} has been checkmated!")
                                self.mated = True
                                break

        elif not self.board.ready:
            print("Board is not ready yet.")

    def moveSelected(self, vector):
        try:
            self.board.movePiece(self.selected.vector, vector, checkMove=False)
        except PromotionError:
            msg = "What do you want the pawn to promote to?"
            while True:
                prompt = simpledialog.askstring("Promote!", msg)
                if prompt is None:
                    break
                try:
                    pType = {pType.__name__: pType for pType in self.board.promoteTo[self.selected.color]}[prompt.lower().capitalize()]
                    self.board.movePiece(self.selected.vector, vector, promote=pType, checkMove=False)
                    break
                except KeyError:
                    msg = prompt + "is Not a valid piece, must be any of \n" + "\n".join([pType.__name__ for pType in self.board.promoteTo[self.selected.color]])
                    continue

        self.updateGraphics()

    def select(self, piece, highlights=None):
        self.clearHighlights()
        self.selected = piece
        self.boardCanv.itemconfigure(self.squares[piece.vector.tuple()], fill="light goldenrod")
        self.highlight(highlights)

    def clearHighlights(self):
        self.selected = None
        for i, piece in enumerate(self.board):
            color = ("saddle brown", "white")[(i + int((i) / self.board.cols)) % 2 == 0]
            if not isinstance(piece, Disabled):
                square = self.squares[piece.vector.tuple()]
                if self.boardCanv.itemcget(square, "fill") != color:
                    self.boardCanv.itemconfig(square, fill=color)

        for king in self.kingsInCheck:
            self.boardCanv.itemconfigure(self.squares[king.vector.tuple()], fill="red")

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

        self.updateGraphics()

    def updateGraphics(self):
        """Update all widgets of frame"""
        self.historyString.set(readable(self.board.history, len(self.board.turnorder)))
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


if __name__ == "__main__":
    ChessGame()
