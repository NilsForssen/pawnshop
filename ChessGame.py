# ChessGame.py

import tkinter as tk
import _thread
import pickle
import socket
import webbrowser
from tkinter import simpledialog, filedialog, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
from ChessBoard import initClassic, init4P, initEmpty, Board
from Pieces import Piece, Empty, Disabled
from Utils import getResourcePath, fetchImage
from ChessVector import ChessVector
from Exceptions import PromotionError, DisabledError, Illegal
from GameNotations import *
from Network import Network
from socket import gaierror


class LoadingDialog(tk.Toplevel):
    def __init__(self, master, txt, GIFPath=getResourcePath("Sprites/LoadingGIF.gif")):
        super().__init__(master, bg="white")
        self._master = master
        self._txt = txt
        self.update_idletasks()
        self.geometry(f"+{master.winfo_x() + 100}+{master.winfo_y() + 100}")
        self.minsize(300, 200)
        self.resizable(False, False)

        gif = Image.open(GIFPath)
        self._frames = []
        for i in range(0, gif.n_frames):
            gif.seek(i)
            self._frames.append(ImageTk.PhotoImage(gif.resize((100, 100), Image.ANTIALIAS)))

        self.txtLabel = tk.Label(self, text=self._txt, bg="white", font=("Segoe", 13))
        self.imgLabel = tk.Label(self, image=self._frames[0], bg="white")
        self.cancelButton = tk.Button(self, text="Cancel", font=("Segoe", 13), command=self.close)
        self.cancelButton.focus()
        self.txtLabel.pack(padx=10, pady=10)
        self.imgLabel.pack(padx=10)
        self.cancelButton.pack(padx=10, pady=10)

        self.title("loading")

        self.protocol("WM_DELETE_WINDOW", self.close)

    @property
    def text(self):
        return self._txt

    @text.setter
    def text(self, text):
        self._txt = text
        self.txtLabel.configure(text=self._txt)

    def start(self):
        self.grab_set()
        self.startLoad()
        self._master.wait_window(self)

    def startLoad(self, i=0):
        if i == len(self._frames):
            i = 0
        self.imgLabel.configure(image=self._frames[i])
        self._ID = self.after(50, lambda: self.startLoad(i + 1))

    def stopLoad(self):
        self.after_cancel(self._ID)

    def close(self):
        self.stopLoad()
        self.destroy()


IMAGEDIR = getResourcePath("Sprites\\")
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
            "Empty": initEmpty,
            "Classic": initClassic,
            "4P": init4P
        }
        self.currentBoard = "Empty"
        self.board = self.boardInits[self.currentBoard]()
        self.kingsInCheck = []
        self.mated = False
        self.selected = None

        self.square = 64
        self.blackbarTop, self.blackbarBottom, self.blackbarLeft, self.blackbarRight = 0, 0, 0, 0
        # Online
        self.inConnections = []
        self.connection = None
        self.clientColor = None
        self.loadDialog = None
        self.pollingRate = 500

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

        self.onlineMenu.add_command(label="Host game", command=self.hostGame)
        self.onlineMenu.add_command(label="Join game", command=self.joinGame)
        self.onlineMenu.add_command(label="Disconnect", command=self.disconnect, state="disabled")

        self.menuBar.add_cascade(label="Game", menu=self.gameMenu)
        self.menuBar.add_cascade(label="Online", menu=self.onlineMenu)
        self.menuBar.add_command(label="Help", command=lambda: webbrowser.open("https://www.bible.com/sv"))

        self.config(menu=self.menuBar)

        # Chesscanvas actions
        self.boardCanv.bind("<Configure>", self.resize)
        self.boardCanv.bind("<Button-1>", self.chessInteract)

        # Generate board and pieceimages
        self.drawBoard()

        # Set icon
        self.iconphoto(True, ImageTk.PhotoImage(Image.open(IMAGEDIR + "\\King.ico")))

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

    def _waitForConn(self):
        self._waitID = self.after(self.pollingRate, self._waitForConn)

    def _client(self, conn, addr, color):
        MANDATORYFLAGS = {
            "ignoreOrder": False,
            "ignoreMate": False,
            "ignoreCheck": False,
            "checkForCheck": True,
            "checkForMate": True,
            "checkMove": True,
            "printOut": False
        }
        conn.send(pickle.dumps(color))
        while True:
            try:
                data = pickle.loads(conn.recv(1024))
            except EOFError as e:
                print(e)
                conn.close()
                self.disconnect()
                simpledialog.messagebox.showinfo("Lost connection", "Opponent disconnected from game server!")
                break
            except ConnectionAbortedError as e:
                print(e)
                break

            if data == "break":
                conn.close()
                self.disconnect()
                break
            elif data != "get":
                # Data is of format (args, kwargs)
                args, kwargs = data

                if color == self.board.currentTurn == color:
                    try:
                        self.board.movePiece(*args, **{**kwargs, **MANDATORYFLAGS})
                    except PromotionError:
                        conn.send(pickle.dumps("promote"))
                        continue
                    except Illegal:
                        conn.send(pickle.dumps("illegal"))
                        continue

            conn.send(pickle.dumps(self.board))

        print("Disconnected from ", addr)

    def _server(self):
        server = "0.0.0.0"
        port = 10000
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.bind((server, port))
        self.mySocket.listen()
        print("Waiting for opponent...")

        try:
            conn, addr = self.mySocket.accept()
        except OSError:
            print("Stopped waiting for opponents")
        else:
            self.inConnections.append(conn)
            self.reInitBoard("Classic")
            self.loadDialog.close()
            self.after_cancel(self._waitID)
            self._updateID = self.after(self.pollingRate, self._updateVisuals)
            self.onlineMenu.entryconfig("Disconnect", state="normal")
            self.clientColor = "white"
            self._client(conn, addr, "black")

    def hostGame(self):
        if self.connection is not None:
            self.disconnect()

        _thread.start_new_thread(self._server, ())

        self.reInitBoard("Empty")
        self.loadDialog = LoadingDialog(self, txt=f"Waiting for other player to connect, \n your global IP-addres is 127.0.0.1")
        self.loadDialog.start()
        self._waitID = self.after(self.pollingRate, lambda: self._checkLoading(loop=True))

    def _updateVisuals(self):
        self.updateGraphics()
        self._updateID = self.after(self.pollingRate, self._updateVisuals)

    def _checkLoading(self, loop=False):
        if self.loadDialog.winfo_exists():
            if loop:
                self.after(self.pollingRate, lambda: self._checkLoading(loop=True))
            return True
        else:
            self.disconnect()
            del self.loadDialog
            return False

    def joinGame(self):
        if self.connection is not None:
            self.disconnect()
        ip = simpledialog.askstring("IP-adress", "IP-adress of host?")
        if not ip:
            return
        self.connection = Network()
        try:
            self.clientColor = self.connection.connect(ip)
        except (gaierror, ConnectionRefusedError):
            simpledialog.messagebox.showinfo("Could not Connect", f"Could not connect to \"{ip}\"!")
            return
        if not self._waitForGame():
            self.reInitBoard("Empty")
            self.loadDialog = LoadingDialog(self, txt="Waiting for opponent\n to connect!")
            self.loadDialog.start()

    def _waitForGame(self):
        echo = self.connection.send("get")

        if isinstance(echo, Board):
            try:
                self.loadDialog.close()
                del self.loadDialog
            except AttributeError:
                pass

            self.onlineMenu.entryconfig("Disconnect", state="normal")
            self.board = echo
            self.drawBoard()
            self._updateID = self.after(self.pollingRate, self._updateBoard)
            return True
        else:
            try:
                if not self._checkLoading():
                    return False
            except AttributeError:
                pass
            self._waitID = self.after(self.pollingRate, self._waitForGame)
            return False

    def _updateBoard(self):
        try:
            newBoard = self.connection.send("get")
        except ConnectionResetError:
            self.disconnect()
            simpledialog.messagebox.showinfo("Lost connection", "Lost connection to server!")
            return
        if newBoard is None:
            self.disconnect()
            simpledialog.messagebox.showinfo("Lost connection", "Opponent disconnected from game server!")
        else:
            if newBoard != self.board:
                self.board = newBoard
                self.clearHighlights()
                self.updateGraphics()

            self._updateID = self.after(self.pollingRate, self._updateBoard)

    def disconnect(self):
        try:
            self.after_cancel(self._waitID)
        except Exception:
            pass
        try:
            self.after_cancel(self._updateID)
        except Exception:
            pass

        self.onlineMenu.entryconfig("Disconnect", state="disabled")
        for conn in self.inConnections:
            conn.close()
        try:
            self.connection.close()
        except AttributeError:
            pass
        try:
            self.mySocket.close()
        except AttributeError:
            pass
        self.connection = None
        self.clientColor = None
        self.reInitBoard("Empty")

    def importPGN(self):
        file = filedialog.askopenfile(title="Open PGN file", filetypes=[("PGN file", ".pgn"), ("Text file", ".txt")])
        if file is None:
            return
        self.board = PGN2Board(file.read())
        self.drawBoard()

    def exportPGN(self):
        file = filedialog.asksaveasfile(title="Save PGN file", defaultextension=".pgn", filetypes=[("PGN file", ".pgn")])
        if file is None:
            return
        file.write(board2PGN(self.board, players=2))

    def exportFEN(self):
        self.clipboard_append(board2FEN(self.board))
        simpledialog.messagebox.showinfo("FEN Copied!", "FEN-string has been copied to clipboard!")

    def importFEN(self):
        FEN = StringDialog.askstring("Load FEN!", "Enter a FEN string to load into the board.")
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
        if not self.mated and self.board.ready:
            if event.x + self.blackbarRight < self.boardCanv.winfo_width() and event.x - self.blackbarLeft > 0 and event.y + self.blackbarBottom < self.boardCanv.winfo_height() and event.y - self.blackbarTop > 0:
                vec = ChessVector((int((event.y - self.blackbarTop) / self.square), int((event.x - self.blackbarRight) / self.square)))

                try:
                    piece = self.board[vec]
                except DisabledError:
                    pass
                else:
                    if self.selected is not None and vec.matches(self.selected.getMoves(self.board)):
                        self.moveSelected(vec)

                        self.clearHighlights()

                    elif isinstance(piece, Piece) and piece.color == self.board.currentTurn and (self.clientColor is None or self.clientColor == piece.color):
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

    def moveSelected(self, vector, *args, **kwargs):
        try:
            if self.connection is not None:
                echo = self.connection.send(((self.selected.vector, vector, *args), kwargs))
                if isinstance(echo, Board):
                    self.board = echo
                elif echo == "promote":
                    raise PromotionError
                else:
                    print("something went wrong")
            else:
                self.board.movePiece(self.selected.vector, vector, *args, checkMove=False, **kwargs)
        except PromotionError:
            msg = "What do you want the pawn to promote to?"
            while True:
                prompt = StringDialog.askstring("Promote!", msg)
                if prompt is None:
                    break
                try:
                    pType = {pType.__name__: pType for pType in self.board.promoteTo[self.selected.color]}[prompt.lower().capitalize()]
                except KeyError:
                    msg = prompt + "is Not a valid piece, must be any of \n" + "\n".join([pType.__name__ for pType in self.board.promoteTo[self.selected.color]])
                    continue
                else:
                    self.moveSelected(vector, promote=pType)
                    break

        self.updateGraphics()

    def select(self, piece, highlights=None):
        self.clearHighlights()
        self.selected = piece
        self.boardCanv.itemconfigure(self.squares[piece.vector.tuple()], fill="light goldenrod")
        self.highlight(highlights)

    def highlightKings(self):
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

        for king in self.kingsInCheck:
            self.boardCanv.itemconfigure(self.squares[king.vector.tuple()], fill="red")

    def clearHighlights(self):
        self.selected = None
        for i, piece in enumerate(self.board):
            color = ("saddle brown", "white")[(i + int((i) / self.board.cols)) % 2 == 0]
            if not isinstance(piece, Disabled):
                square = self.squares[piece.vector.tuple()]
                if self.boardCanv.itemcget(square, "fill") != color:
                    self.boardCanv.itemconfig(square, fill=color)

        self.highlightKings()

    def highlight(self, vecs):
        for vec in vecs:
            self.boardCanv.itemconfigure(self.squares[vec.tuple()], fill="sky blue")

    def resize(self, *args):
        self.update_idletasks()
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
