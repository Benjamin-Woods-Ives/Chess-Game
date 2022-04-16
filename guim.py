import tkinter as tk
BROWN = "#4a4b4d"
CREAM = "#d1d1d1"
WHITE = "W"
BLACK = "B"
# "#F5DEB3" cream
# "#8B4513" brown


class Tile(tk.Canvas):
    """this class creates 1 of the tiles displayed on the chess board"""
    def __init__(self, parent, row, column, background, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.original_background = background
        self.parent = parent
        self.row = row
        self.column = column
        self.image = None
        self.bind("<Button-1>", self.user_input)

    def user_input(self, event):
        """called when a user clicks on one of the tiles"""
        if event is event:
            self.parent.update_turn()
            self.parent.store_position(self.row, self.column)

    def update_image(self, image):
        """updates the image displayed within the tile"""
        self.delete("all")
        self.image = image
        self.create_image(35, 35, image=self.image)

    def delete_image(self):
        """deletes the image within the tile"""
        self.delete("all")

    def image_check(self):
        """checks if there is a image within the tile.used for testing purposes"""
        if self.image is None:
            return True
        else:
            return False

    def background_update(self, colour):
        """updates the background of the tile object"""
        self.configure(bg=colour)


class TileBoard(tk.Frame):
    """this is a tkinter frame that contains all the tiles and displayes them in a 8x8 chess grid"""
    def __init__(self, parent, board, piece_board, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.board = board
        self.turn = 0
        self.input_location = [None, None]
        self.piece_board = piece_board
        self.create_tiles()
        self.grid_tiles()

    def update_turn(self):
        """this method is called within user_input method with tile class"""
        if self.turn == 2:
            self.turn = 0
        else:
            self.turn += 1

    def reset_turn(self):
        """sets the background of all tiles back to there default colour"""
        self.turn = 0
        self.reset_tiles()

    def set_turn(self, state):
        """directly sets  the turn"""
        self.turn = state

    def store_position(self, row, column):
        """assigns the loctaion that the user input was to the input_location tribute"""
        self.input_location = [row, column]

    def create_tile(self, row, column, colour):
        """creates a inilises a tile object and stoles it within the board tribute of board"""
        self.board.board[row][column] = Tile(self, row, column, colour, width=70, height=70, bg=colour,
                                             highlightthickness=0.5, highlightbackground="black")

    def create_tiles(self):
        """creates the 8x8 grid of tiles. each tile has its own location and colour."""
        colour = BROWN
        for row in range(8):
            for column in range(8):
                if colour == BROWN:
                    self.create_tile(row, column, colour)
                    colour = CREAM
                elif colour == CREAM:
                    self.create_tile(row, column, colour)
                    colour = BROWN
            if colour == BROWN:
                colour = CREAM
            elif colour == CREAM:
                colour = BROWN

    def grid_tiles(self):
        """grids all the tiles within the board to a 8x8 grid"""
        for row in range(8):
            for column in range(8):
                self.board.board[row][column].grid(row=row, column=column)

    def update_tiles(self, place, moves):
        """update all the tiles that have the same location as moves """
        self.board.board[place[0]][place[1]].background_update("#fc9403")
        for update in moves:
            self.board.board[update[0]][update[1]].background_update("#34ebe5")

    def reset_tiles(self):
        """resets all the tiles back to original background"""
        for row in self.board.board:
            for column in row:
                column.background_update(column.original_background)


class Images:
    """ dictionary class used to store the tkinter photo images """
    def __init__(self):

        self.images = {"W": {"WPawn.png": tk.PhotoImage(file="WPawn.png"),
                             "WRook.png": tk.PhotoImage(file="WRook.png"),
                             "WKnight.png": tk.PhotoImage(file="WKnight.png"),
                             "WBishop.png": tk.PhotoImage(file="WBishop.png"),
                             "WKing.png": tk.PhotoImage(file="WKing.png"),
                             "WQueen.png": tk.PhotoImage(file="WQueen.png")},
                       "B": {"BPawn.png": tk.PhotoImage(file="BPawn.png"),
                             "BRook.png": tk.PhotoImage(file="BRook.png"),
                             "BKnight.png": tk.PhotoImage(file="BKnight.png"),
                             "BBishop.png": tk.PhotoImage(file="BBishop.png"),
                             "BKing.png": tk.PhotoImage(file="BKing.png"),
                             "BQueen.png": tk.PhotoImage(file="BQueen.png")}
                       }

    def get_image(self, colour, image_name):
        """returns the tkinter photoimage with the corosponding colour and name"""
        colour_type = self.images[colour]
        tk_image = colour_type[image_name]
        return tk_image


class CheckMateFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.spacer1 = tk.Button(self, bg="#404040", width=26, relief="flat", state="disabled")
        self.spacer2 = tk.Button(self, bg="#404040", width=26, relief="flat", state="disabled")
        self.test = tk.Label(self, text="Load as", bg="#4a4b4d", fg="#ffffff", font="arial")
        self.spacer1.pack()
        self.test.pack()
        self.spacer2.pack()

    def update_label(self, text):
        self.test.configure(text=text)
        self.update()

    def to_grid(self):
        self.grid(row=0, column=0)


class MainWindow(tk.Tk):
    """the main window that the 8x8 chess board is displayed in"""
    def __init__(self, board, piece_board, height):
        super().__init__()
        self.geometry("+"+str(int(height)+290)+"+300")
        self.title("Benji's Chess")
        self.iconbitmap("icon.ico")
        self.resizable(0, 0)
        self.tile_board = TileBoard(self, board, piece_board)
        self.winner = CheckMateFrame(self, bg="#4a4b4d", highlightthickness=0.5, highlightcolor="black")
        self.grid_all()

    def grid_all(self):
        """grids all nessaserry tkinter objects to the menu"""
        self.tile_board.grid(row=0, column=0)

    def grid_winner(self, winner):
        self.winner.update_label(winner)
        self.winner.to_grid()


if __name__ == '__main__':
    pass
