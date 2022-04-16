import tkinter as tk
import pickle

WHITE = "W"
BLACK = "B"

#this class sets up the gui and proforms the primary controls of the game
class Game(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.W_King = tk.PhotoImage(file="WKing.png")
        self.W_Pawn = tk.PhotoImage(file="WPawn.png")
        self.W_Queen = tk.PhotoImage(file="WQueen.png")
        self.W_Bishop = tk.PhotoImage(file="WBishop.png")
        self.W_Knight = tk.PhotoImage(file="WKnight.png")
        self.W_Rook =  tk.PhotoImage(file="WRook.png")
        self.White = ["WPawn.png", self.W_Pawn], ["WRook.png", self.W_Rook], ["WKnight.png", self.W_Knight], ["WBishop.png", self.W_Bishop],["WKing.png", self.W_King], ["WQueen.png", self.W_Queen]
        #
        self.B_Bishop = tk.PhotoImage(file="BBishop.png")
        self.B_King = tk.PhotoImage(file="BKing.png")
        self.B_Pawn = tk.PhotoImage(file="BPawn.png")
        self.B_Queen = tk.PhotoImage(file="BQueen.png")
        self.B_Knight = tk.PhotoImage(file="BKnight.png")
        self.B_Rook = tk.PhotoImage(file="BRook.png")
        self.Black = ["BPawn.png", self.B_Pawn], ["BRook.png", self.B_Rook], ["BKnight.png", self.B_Knight], ["BBishop.png", self.B_Bishop], ["BKing.png", self.B_King], ["BQueen.png", self.B_Queen]
        #
        self.black_white = [self.Black, self.White]
        self.brown = "#8B4513"
        self.cream = "#F5DEB3"
        self.canvas_grid = []
        self.grid_update = []
        self.background_grid = []
        self.background_row = []
        self.image_row = []
        self.image_grid = []
        self.image_name_grid = []
        self.image_name_row = []
        self.white_king = False
        self.black_king = False
        self.white_check_mate = False
        self.black_check_mate = False
        self.piece1 = None
        self.piece2 = None
        self.counter = 0
        self.image1 = None
        self.image_object1 = None
        self.image_object2 = None
        self.row = None
        self.column = None
        self.place_on_board = None
        self.current_moves = []
        self.turn = "W"
        self.temp_color = None
        self.piece_move_board = []
        self.create_board()
        self.insert_images()

    #this method returns the color of the image
    def get_color(self, location):
        temp = self.image_name_grid[location[0]][location[1]]
        for a in self.White:
            if temp is a:
                return WHITE
        for a in self.Black:
            if temp is a:
                return BLACK
        else:
            return None
    
    #this method resets the move progress and allows the first input method below to run
    def reset(self):
        self.undo_background()
        self.row = None
        self.column = None
        self.current_moves = None
        self.piece1 = None
        self.image1 = None
        self.image_object1 = None
        self.image_object2 = None
        self.image_object1 = None
        self.piece1 = None
        self.piece2 = None
        self.image1 = None
        self.counter = 0
    
    #this method stores the position of the first click on a piece
    def first_input(self, selected, place):
        if piece_board.return_board()[place[0]][place[1]] is not None:
            temp = piece_board.direct_access(place[0], place[1])
            if (temp.color == WHITE and self.turn == "W") or (
                    temp.color == BLACK and self.turn == "B"):
                self.row = place[0]
                self.column = place[1]
                self.piece1 = piece_board.direct_access(self.row, self.column)
                self.image_object1 = selected
                self.image1 = self.image_name_grid[self.row][self.column]
                self.current_moves = self.piece1.moves
                self.update_background(self.current_moves)
                self.counter = 1
                
                
    #this method moves the piece to the new position
    def second_input(self, selected, place):
        for_undoing.update_moves_made(place, [self.row, self.column], self.piece1, piece_board.direct_access(place[0], place[1]), self.image1, self.image_name_grid[place[0]][place[1]])
        self.image_object2 = selected
        self.image_object2.delete("all")
        self.image_object2.create_image(35, 35, image=self.image1)
        self.image_object1.delete("all")
        self.image_object1.create_image(35, 35, image=None)
        self.image_name_grid[place[0]][place[1]] = self.image1
        self.image_name_grid[self.row][self.column] = None
        piece_board.board[place[0]][place[1]] = piece_board.board[self.row][self.column]
        piece_board.board[self.row][self.column] = None
        piece_board.board[place[0]][place[1]].row = place[0]
        piece_board.board[place[0]][place[1]].column = place[1]
        update_all_moves()
        self.white_king = king_check()[0].check
        self.black_king = king_check()[1].check
        if self.turn == "W":
            self.turn = "B"
        elif self.turn == "B":
            self.turn = "W"
    
    #this method checks the current move to see if is putting either side in check
    def pre_move_check(self, row, column, place):
        temp_piece = piece_board.board[place[0]][place[1]]
        piece_board.board[place[0]][place[1]] = piece_board.board[row][column]
        piece_board.board[row][column] = None
        piece_board.board[place[0]][place[1]].row = place[0]
        piece_board.board[place[0]][place[1]].column = place[1]
        update_all_moves()
        white_temp = king_check()[0].check
        black_temp = king_check()[1].check
        piece_board.board[row][column] = piece_board.board[place[0]][place[1]]
        piece_board.board[place[0]][place[1]] = temp_piece
        piece_board.board[row][column].row = row
        piece_board.board[row][column].column = column
        update_all_moves()
        return [white_temp, black_temp]
    
    #this method checks for a checkmate
    def check_mate_check(self):
        white_check_mate = True
        black_check_mate = True
        for a in piece_board.board:
            for b in a:
                if b is not None:
                    if b.color == WHITE:
                        for c in b.moves:
                            temp_white = self.pre_move_check(b.row, b.column, c)
                            if temp_white[0] is False:
                                white_check_mate = False
                                break
                    elif b.color == BLACK:
                        for c in b.moves:
                            temp_black = self.pre_move_check(b.row, b.column, c)
                            if temp_black[1] is False:
                                black_check_mate = False
                                break
        return [white_check_mate, black_check_mate]
    
    #this method checks if the move that is being made is valid
    def piece_move(self, selected, place):
        if self.counter == 0:
            if self.white_king is False and self.black_king is False:
                self.first_input(selected, place)
            else:
                checkmate = self.check_mate_check()
                if (self.row == place[0] and self.column == place[1]) is False:
                    if checkmate[0] is True:
                        print("Black team wins")
                    else:
                        if self.white_king is True and self.turn == "W":
                            if checkmate[0] is True:
                                print("Black team wins")
                            else:
                                after_check = self.pre_move_check(self.row, self.column, place)
                                if after_check[0] is True:
                                    self.reset()
                                elif after_check[0] is False:
                                    for a in self.current_moves:
                                        if a[0] == place[0] and a[1] == place[1]:
                                            self.second_input(selected, place)
                                            break
                                    self.reset()
                        elif self.black_king is True and self.turn == "B":
                            if checkmate[1] is True:
                                print("White team wins")
                            else:
                                after_check = self.pre_move_check(self.row, self.column, place)
                                if after_check[1] is True:
                                    self.reset()
                                elif after_check[1] is False:
                                    for a in self.current_moves:
                                        if a[0] == place[0] and a[1] == place[1]:
                                            self.second_input(selected, place)
                                            break
                                    self.reset()
        elif self.counter == 1:
            if piece_board.direct_access(place[0], place[1]) is not None:
                if (self.row == place[0] and self.column == place[1]) is False:
                    if piece_board.direct_access(place[0], place[1]).color is self.piece1.color:
                        self.reset()
                        self.first_input(selected, place)
                    else:
                        for a in self.current_moves:
                            if a[0] == place[0] and a[1] == place[1]:
                                after_check = self.pre_move_check(self.row, self.column, place)
                                if (after_check[0] is False and self.turn == "W") or (after_check[1] is False and self.turn == "B"):
                                    self.second_input(selected, place)
                                    break
                        self.reset()
                else:
                    self.reset()

            else:
                for a in self.current_moves:
                    if a[0] is place[0] and a[1] is place[1]:
                        after_check = self.pre_move_check(self.row, self.column, place)
                        if (after_check[0] is False and self.turn == "W") or (after_check[1] is False and self.turn == "B"):
                            self.second_input(selected, place)
                            break
                self.reset()
        else:
            self.reset()
    
    #updates gui so the moves are shown
    def update_background(self, moves):
        self.canvas_grid[self.row][self.column].configure(bg="#fc9403")
        for a in moves:
            temp = self.canvas_grid[a[0]][a[1]]
            temp.configure(bg="#34ebe5")

   #sets the updateed background back to the original 
    def undo_background(self):
        pass
        for a in range(8):
            for b in range(8):
                self.canvas_grid[a][b].configure(bg=self.background_grid[a][b])
    
    #creats a canvas whitch represents part of the 8x8 grid
    def create_canvas(self, r, c, color, img):
        def update(event):
            update_all_moves()
            selected = event.widget
            place_on_board = self.indexer(event.widget)
            self.place_on_board = place_on_board
            self.position = place_on_board
            self.piece_move(selected, place_on_board)

        temp_canvas = tk.Canvas(self, width=70, height=70, bg=color, highlightthickness=0.5, highlightbackground="black")
        self.image_row.append(temp_canvas.create_image(35, 35, image=img))
        self.image_name_row.append(img)
        self.background_row.append(color)
        if len(self.image_row) == 8:
            self.background_grid.append(self.background_row)
            self.image_name_grid.append(self.image_name_row)
            self.background_row = []
            self.image_name_row = []
            self.image_grid.append(self.image_row)
            self.image_row = []
        temp_canvas.bind("<Button-1>", update)
        temp_canvas.grid(row=r, column=c)
        return temp_canvas

    # creates the entire board using the create_canvas method
    def create_board(self):
        row_temp = []
        temp = True
        for a in range(8):
            for b in range(8):
                if temp is True:
                    row_temp.append(self.create_canvas(a + 2, b, self.brown, None))
                    temp = False
                elif temp is False:
                    row_temp.append(self.create_canvas(a + 2, b, self.cream, None))
                    temp = True
            if temp is True:
                temp = False
            elif temp is False:
                temp = True
            self.canvas_grid.append(row_temp)
            row_temp = []
    
    #this method places the piece images onto the canvas grid in the correct spaces. this is used for startig the game and loading the game
    def insert_images(self):
        for a in self.image_name_grid:
            for b in a:
                b = None
        for a in range(8):
            for b in range(8):
                self.canvas_grid[a][b].delete("all")
                if piece_board.board[a][b] is not None:
                    if piece_board.board[a][b].color == WHITE:
                        for c in self.White:
                            if c[0] == piece_board.board[a][b].type_color:
                                image_name = c[1]
                                self.image_name_grid[a][b] = image_name
                                self.canvas_grid[a][b].create_image(35, 35, image=image_name)
                                break
                    elif piece_board.board[a][b].color == BLACK:
                        for c in self.Black:
                            if c[0] == piece_board.board[a][b].type_color:
                                image_name = c[1]
                                self.image_name_grid[a][b] = image_name
                                self.canvas_grid[a][b].create_image(35, 35, image=image_name)
                                break
                    image_name = None

    #searches through the canvas_grid attribute for a certain element
    def indexer(self, element):
        for a in self.canvas_grid:
            for b in a:
                if b is element:
                    return [self.canvas_grid.index(a), a.index(b)]
                else:
                    pass


#this class sets a board for the pieces to go on
class Board:
    def __init__(self, fill):
        self.board = []  # 2d Array
        self.fill = fill
        self.create_board()
    
    #creates a 2d array
    def create_board(self):
        for y in range(8):
            temp = []
            for x in range(8):
                temp.append(self.fill)
            self.board.append(temp)
    
    def print_board(self):
        for a in self.board:
            pass
            print(a)
    
    #updates the a element from the board tribute
    def update_board(self, piece, row, column):
        self.board[row][column] = piece
    
    #updates the entire board woth a new board. this is used when loading a game
    def update_entire_board(self, new):
        self.board = new
    
    #returns the entire board tribute to the main program
    def return_board(self):
        return_board = self.board
        return return_board

    #accesses a element from board directly
    def direct_access(self, row, column):
        element = self.board[row][column]
        return element

#this class is a base class for all pieces eg queen, king, pawn
class Piece:
    board = Board(None)

    def __init__(self, color, row, column):
        self.color = color
        self.row = row
        self.column = column
        self.moves = []
        piece_board.update_board(self, self.row, self.column)

    
    #this static method is used to know if a move is out of range of the bpard
    @staticmethod
    def out_range_check(row, column):
        if row >= 8 or column >= 8 or row <= -1 or column <= -1:
            return True
        else:
            return False

    #this checks to see if a a move is obstructed by another piece
    @staticmethod
    def collision_check(element):
        if element is not piece_board.fill:
            return True
        if element is piece_board.fill:
            return False
    
    #this method checks to see what colour the piece is that is obstructing the move
    def collision_color_check(self, row, column):
        obj = piece_board.direct_access(row, column)
        if obj.color is self.color:
            return True
        if obj.color is not self.color:
            return False

    #this method is used to check if the move is valid or not
    def check_decision(self, row, column):
        try:
            element = piece_board.return_board()[row][column]
            range_check = self.out_range_check(row, column)
            collision = self.collision_check(element)
            if range_check is True:
                return True
            else:
                if collision is True:
                    color_check = self.collision_color_check(row, column)
                    if color_check is True:
                        return True
                    elif color_check is False:
                        self.moves.append([row, column])
                        return True
                elif collision is False:
                    self.moves.append([row, column])
        except IndexError:
            return True

#this is the rook class witch gets valid moves for the rook objects
class Rook(Piece):
    def __init__(self, color, row, column):
        super().__init__(color, row, column)
        self.type = "Rook.png"
        self.type_color = color + self.type

    def get_moves(self):
        self.moves_horizontal(1)
        self.moves_horizontal(-1)
        self.moves_vertical(1)
        self.moves_vertical(-1)
    #this method gets all the horizontal moves
    def moves_horizontal(self, direction):
        for a in range(1, 8):
            if self.check_decision(self.row, self.column + (a * direction)) is True:
                break
            else:
                pass
    #this method gets all the vertical moves
    def moves_vertical(self, direction):
        for a in range(1, 8):
            if self.check_decision(self.row + (a * direction), self.column) is True:
                break
            else:
                pass

#this is the rook class witch gets valid moves for the bishop objects
class Bishop(Piece):
    def __init__(self, color, row, column):
        super().__init__(color, row, column)
        self.type = "Bishop.png"
        self.type_color = color + self.type
    #this methods get all the diagonal moves
    def moves_diagonal(self, row_direction, column_direction):
        for a in range(1, 8):
            if self.check_decision(self.row + (a * row_direction), self.column + (a * column_direction)) is True:
                break
            else:
                pass

    def get_moves(self):
        self.moves_diagonal(1, 1)
        self.moves_diagonal(1, -1)
        self.moves_diagonal(-1, -1)
        self.moves_diagonal(-1, 1)

#this class inherites from rook and bishop this allows for the vertical, horizonatal and diagonal moves to be used to get all moves fro the queen
class Queen(Bishop, Rook):
    def __init__(self, color, row, column):
        super().__init__(color, row, column)
        self.type = "Queen.png"
        self.type_color = color + self.type
    
    def get_moves(self):
        Rook.get_moves(self)
        Bishop.get_moves(self)


class Knight(Piece):
    def __init__(self, color, row, column):
        super().__init__(color, row, column)
        self.type = "Knight.png"
        self.type_color = color + self.type

    def knight_moves(self, row_move, column_move):
        self.check_decision(self.row + row_move, self.column + column_move)

    def get_moves(self):
        self.knight_moves(2, 1)
        self.knight_moves(2, -1)
        self.knight_moves(-2, 1)
        self.knight_moves(-2, -1)
        self.knight_moves(1, 2)
        self.knight_moves(1, -2)
        self.knight_moves(-1, - 2)
        self.knight_moves(-1, 2)


class Pawn(Piece):
    def __init__(self, color, row, column, ):
        super().__init__(color, row, column, )
        self.moved = 0
        self.x = row
        self.y = column
        self.type = "Pawn.png"
        self.type_color = color + self.type
    #this is the move of the first move of the pawn
    def first_move(self):
        if self.color == WHITE:
            for a in range(2):
                if self.collision_check(piece_board.return_board()[self.row - (a + 1)][self.column]) is True:
                    break
                else:
                    self.check_decision(self.row - (a + 1), self.column)
        if self.color == BLACK:
            for a in range(2):
                if self.collision_check(piece_board.return_board()[self.row + (a + 1)][self.column]) is True:
                    break
                else:
                    self.check_decision(self.row + (a + 1), self.column)
        self.moved = 1
    #this is the moves of the pawn after the first move
    def after_first(self):
        if self.color == WHITE:
            if self.collision_check(piece_board.return_board()[self.row - 1][self.column]) is True:
                pass
            else:
                self.check_decision(self.row - 1, self.column)
        elif self.color == BLACK:
            try:
                if self.collision_check(piece_board.return_board()[self.row + 1][self.column]) is True:
                    pass
                else:
                    self.check_decision(self.row + 1, self.column)
            except IndexError:
                self.promote()
    #this method gets all the pawn moves 
    def pawn_moves(self):
        if self.y is self.column and self.x is self.row:
            self.first_move()
        else:
            self.after_first()

        if self.color == WHITE:
            try:
                if self.collision_check(piece_board.return_board()[self.row - 1][self.column - 1]) is True:
                    self.check_decision(self.row - 1, self.column - 1)
            except IndexError:
                pass
            try:
                if self.collision_check(piece_board.return_board()[self.row - 1][self.column + 1]) is True:
                    self.check_decision(self.row - 1, self.column + 1)
            except IndexError:
                pass

        elif self.color == BLACK:
            try:
                if self.collision_check(piece_board.return_board()[self.row + 1][self.column - 1]) is True:
                    self.check_decision(self.row + 1, self.column - 1)
            except IndexError:
                pass
            try:
                if self.collision_check(piece_board.return_board()[self.row + 1][self.column + 1]) is True:
                    self.check_decision(self.row + 1, self.column + 1)
            except IndexError:
                pass

    def get_moves(self):
        self.pawn_moves()
    
    def promote(self):
        Queen(self.color, self.row, self.column)
        print(piece_board.board[self.row][self.column].type_color)
        left.board.insert_images()
        print("ok")

class King(Piece):
    def __init__(self, color, row, column, ):
        super().__init__(color, row, column, )
        self.check = False
        self.type = "King.png"
        self.type_color = color + self.type

    def in_check(self):
        self.check = True

    def not_in_check(self):
        self.check = False

    def king_moves(self):
        self.check_decision(self.row - 1, self.column)
        self.check_decision(self.row - 1, self.column + 1)
        self.check_decision(self.row, self.column + 1)
        self.check_decision(self.row + 1, self.column + 1)
        self.check_decision(self.row + 1, self.column)
        self.check_decision(self.row + 1, self.column - 1)
        self.check_decision(self.row, self.column - 1)
        self.check_decision(self.row - 1, self.column - 1)

    def get_moves(self):
        self.king_moves()
        

def place_board():
    Rook(BLACK, 0, 0)
    Knight(BLACK, 0, 1)
    Bishop(BLACK, 0, 2)
    Queen(BLACK, 0, 3)
    King(BLACK, 0, 4)
    Bishop(BLACK, 0, 5)
    Knight(BLACK, 0, 6)
    Rook(BLACK, 0, 7)
    for a in range(8):
        Pawn(BLACK, 1, a)
    for a in range(8):
        Pawn(WHITE, 6, a)
    Pawn(WHITE, 6, 1)
    Rook(WHITE, 7, 0)
    Knight(WHITE, 7, 1)
    Bishop(WHITE, 7, 2)
    Queen(WHITE, 7, 3)
    King(WHITE, 7, 4)
    Bishop(WHITE, 7, 5)
    Knight(WHITE, 7, 6)
    Rook(WHITE, 7, 7)

#this global function updates all moves avalible from all the pices on the board
def update_all_moves():
    for a in piece_board.return_board():
        for b in a:
            if b is not None:
                b.moves = []
                b.get_moves()
            else:
                pass
    king_check()

#this global function returns all moves possible by white and all moves possible by black and this is stoered in a 3 dimentinal array. this is used when calculating for check and checkmate
def board_all_moves():
    all_moves_white = []
    all_moves_black = []
    for a in piece_board.return_board():
        for c in a:
            try:
                if c.color == WHITE:
                    for b in c.moves:
                        all_moves_white.append(b)
                elif c.color == BLACK:
                    for b in c.moves:
                        all_moves_black.append(b)
            except AttributeError:
                pass
    return [all_moves_white, all_moves_black]

#this global function iterates through the board and finds the elements that have a check tribute and returns the objects and there location within the board
def return_king_objects():
    all_moves = board_all_moves()
    white_moves = all_moves[0]
    black_moves = all_moves[1]
    black_row = None
    black_column = None
    white_row = None
    white_column = None
    for a in piece_board.return_board():
        for b in a:
            try:
                if b.color == BLACK:
                    try:
                        b.check 
                        black_row = b.row
                        black_column = b.column
                    except AttributeError:
                        pass
                elif b.color == WHITE:
                    try:
                        b.check
                        white_row = b.row
                        white_column = b.column
                    except AttributeError:
                        pass
            except AttributeError:
                pass
    return [white_row, white_column, white_moves, black_row, black_column, black_moves]

#this global fuction checks if either of the king are in check and updates the kings check tribute and also returns king pieces loaction
def king_check():
    all_check_needs = return_king_objects()
    white_row = all_check_needs[0]
    white_column = all_check_needs[1]
    white_moves = all_check_needs[2]
    black_row = all_check_needs[3]
    black_column = all_check_needs[4]
    black_moves = all_check_needs[5]
    for a in white_moves:
        if a[0] is black_row and a[1] is black_column:
            piece_board.board[black_row][black_column].in_check()
            break
        else:
            piece_board.board[black_row][black_column].not_in_check()
    for a in black_moves:
        if a[0] is white_row and a[1] is white_column:
            piece_board.board[white_row][white_column].in_check()
            break
        else:
            piece_board.board[white_row][white_column].not_in_check()
    return [piece_board.board[white_row][white_column], piece_board.board[black_row][black_column]]

#this class saves the games progress using pickle and also creates a tkframe with a lable, entry box and button to enter the name of the save they want
class Save(tk.Frame):
    def __init__(self, parent, *args, **kwargs): 
        super().__init__(parent, *args, **kwargs)
        self.save_name = ""
        self.save_in_progress = False
        
        #this method saves the games progress to a pickle file with a name entered by the uses and updates a pickle file that contains a list of the saved names for later use when loading the game
        def save_game():
            self.save_in_progress = True
            self.save_name = self.b.get()
            if self.save_name != "":
                to_pickle = [piece_board.board, for_undoing.all_moves_made]
                pickling = open(self.save_name + ".pickle","wb")
                saves.add_name(self.save_name)
                pickling2 = open("123123123saves123123123.pickle", "wb")
                pickle.dump(saves.save_name, pickling2)
                pickling2.close()
                saves.update_save_name()
                pickle.dump(to_pickle, pickling)
                pickling.close()
                self.grid_forget()
                self.b.delete(0, "end")
                self.save_in_progress = False
        
        self.a = tk.Label(self, text="Save as", font=("arial", 12))
        self.b = tk.Entry(self, justify="center")
        self.c = tk.Button(self, text="Save", command=save_game)
        self.a.pack()
        self.b.pack()
        self.c.pack()

#this class creates a tkframe where you can type the name of the save and load it
class Load(tk.Frame):
    def __init__(self, parent, *args, **kwargs): 
        super().__init__(parent, *args, **kwargs)
        self.load_name = ""
        self.load_name_list = []
        self.load_in_progress = False
        
        #this method loads the picle file and updates the board and gui to the configuration of the saved state
        def load_game():
            self.load_in_progress = True
            self.load_name = self.b.get()
            try:
                unpickleing = open(self.load_name + ".pickle","rb")
                unpickled = pickle.load(unpickleing)
                piece_board.update_entire_board(unpickled[0])
                for_undoing.update_all_moves_made(unpickled[1])
                try:
                    left.board.insert_images()
                except AttributeError:
                    left.start_game(0)
                    left.board.insert_images()
                self.grid_forget()
                window.right.j.place_forget()
                self.b.delete(0, "end")
                self.load_in_progress = False
            except FileNotFoundError:
                pass
        
        def key_input(key):
            load_string_name = ""
            self.b.delete(0, "end")
            self.b.insert(0, load_string_name.join(self.load_name_list))
            if ord(key.char) == 8:
                try:
                    self.load_name_list.pop()
                except IndexError:
                    pass
            elif (ord(key.char) >= 48 and ord(key.char) <= 122) and (ord(key.char)>= 97 or ord(key.char)<= 90):
                self.load_name_list.append(key.char)
            else:
                self.b.delete(0, "end")
                self.b.insert(0, load_string_name.join(self.load_name_list))
            window.right.j.labels(saves.search_name(load_string_name.join(self.load_name_list)))
        self.a = tk.Label(self, text="Load as", font=("arial", 12))
        self.b = tk.Entry(self, justify="center")
        self.b.bind("<Key>", key_input)
        self.c = tk.Button(self, text="Load", command=load_game)
        self.a.pack()
        self.b.pack()
        self.c.pack()

class LoadNames():
    def __init__(self):
        try:
            unpickleing = open("123123123saves123123123.pickle","rb")
            self.save_name = pickle.load(unpickleing)
            unpickleing.close()
        except (FileNotFoundError, EOFError):
            self.save_name = []
        
    def add_name(self, name):
        self.save_name.append(name)
    
    def remove_name(self, name):
        for a in self.save_name:
            if a == name:
                self.save_name.remove(a)
    
    def update_save_name(self):
        unpickleing = open("123123123saves123123123.pickle","rb")
        self.save_name = pickle.load(unpickleing)
        unpickleing.close()
    
    def search_name(self, name):#uses a linear search
        return_name = []
        name.split()
        name_lenth = len(name)
        for a in self.save_name:
            list_name = a
            list_name.split()
            name_in_search = False
            for b in range(len(list_name)):
                for c in range(name_lenth):
                    try:
                        if name[c] != list_name[b+c]:
                            name_in_search = False
                            break
                        else:
                            name_in_search = True
                    except IndexError:
                        name_in_search = False
                        break
                if name_in_search is True:
                    return_name.append(a)
                    name_in_search = False
        return return_name

                    
#this class is a tkinter scrolable frame where its used for searching through the name of saves whitch can selected to load
class ScrollFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        def update(event):
            w=self.canvas.winfo_width()
            h=self.canvas.winfo_height()
            self.canvas.configure(scrollregion=(0,0, w,h))
        
        self.label_objects = []
        self.text = ""
        
        self.canvas = tk.Canvas(self, width=150, height=200)
        self.canvas.grid(row=0, column=0)
        
        self.scrollbar= tk.Scrollbar(self,command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set, scrollregion=(0,0, 150, 200))
        self.scrollbar.grid(row=0, column=1,sticky='ns')
        
        self.interior = tk.Frame(self.canvas)
        self.interior.bind('<Configure>',update)
        self.canvas.create_window((0,0),window=self.interior ,anchor='nw')
        
    def labels(self,array):
        def update(event):
            self.text = event.widget.cget("text")
            window.right.i.b.delete(0, "end")
            window.right.i.b.insert("end",self.text)
        
        for b in self.label_objects:
            b.grid_forget()
        for a in array:
            index = array.index(a)
            try:
               self.label_objects[index].config(text=a)
               self.label_objects[index].grid(row=index, column=2)
            except IndexError:   
                temp = tk.Label(self.interior, text=a, anchor="w", justify="left", relief="raised", width=15)
                temp.bind("<Button-1>", update)
                temp.grid(row=index, column=2)
                self.label_objects.append(temp)
                
# this class is the right side of my gui where all the buttons are eg load, save, newgame
class RightSide(tk.Frame):
    def __init__(self, parent, *args, **kwargs): 
        super().__init__(parent, *args, **kwargs)
        def reset_game():
            left.reset_game()
        
        def start_game():
            left.start_game(1)
                
        def end_process():
            exit()
        
        def undo():
            try:
                for_undoing.undo_move()
            except IndexError:
                pass
        
        def save_game():
            if left.game_in_progress is True:
                if h.save_in_progress is False:
                    h.place(x=190, y=69)
    
        def load_game():
            if self.i.load_in_progress is False:
                self.i.grid(row= 2, column= 1)
                self.j.place(x=320, y=140)
        
        self.grid_propagate(0)
        a = tk.Button(self, height=1, width=9, text="New game",font=("arial", 26), borderwidth= 2, relief="groove", command=start_game)
        a.grid(row=0, column=0)
        b = tk.Button(self, height=1, width=9, text="Save game",font=("arial", 26), borderwidth= 2, relief="groove", command=save_game)
        b.grid(row=1, column=0)
        c = tk.Button(self, height=1, width=9, text="Load game",font=("arial", 26), borderwidth= 2, relief="groove", command=load_game)
        c.grid(row=2, column=0)
        d = tk.Button(self, height=1, width=9, text="Reset game",font=("arial", 26), borderwidth= 2, relief="groove", command=reset_game)
        d.grid(row=3, column=0)
        e = tk.Button(self, height=1, width=9, text="Undo",font=("arial", 26), borderwidth= 2, relief="groove", command=undo)
        e.grid(row=4, column=0)
        g = tk.Button(self, height=1, width=9, text="Quit",font=("arial", 26), borderwidth= 2, relief="groove", command=end_process)
        g.grid(row=5, column=0)
        h = Save(self, height=1, width=9, borderwidth= 2, relief="groove")
        self.i = Load(self, height=1, width=9, borderwidth= 2, relief="groove")
        self.j = ScrollFrame(self,height=1, width=1, borderwidth= 2, relief="groove")

#this is the area where the game is displayed
class LeftSide(tk.Frame):
    def __init__(self, parent, *args, **kwargs): 
        super().__init__(parent, *args, **kwargs)
        self.game_in_progress = False
        self.board = None
        
    def start_game(self, check):
        if self.game_in_progress is False:
            self.game_in_progress = True
            if check == 1:
                place_board()
            self.board = Game(self, highlightthickness=1, highlightbackground="black")
            self.board.grid(row=0, column=0)
        
    def reset_game(self):
        if self.game_in_progress is True:
            while True:
                try:
                    for_undoing.undo_move()
                except IndexError:
                    break
            left.board.turn="W"

#this class is tha main window where all over tkinter frames are located
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Benji's Chess")
        self.iconbitmap("icon.ico")
        self.resizable(0, 0)
        self.right = RightSide(self,height=578, width=547, highlightthickness=2, highlightbackground="black", bg="white")
    
    def grid(self, temp):
        temp.grid(row=0, column = 0)
        self.right.grid(row=0, column=1)

#this class saves all moves made in the game 
class Undo():
    def __init__(self):
        self.all_moves_made = [] #this is being used as a stack
        self.row = None
        self.column = None
        
    #this method is used for inserting into the stack
    def update_moves_made(self, original, new, original_object, new_object, image_original, image_new):
        print(original)
        print(new)
        one_move = [original, new, original_object, new_object]
        self.all_moves_made.append(one_move)
    
    #this method pops from the stack and does what is nessasary to undo the move on the board
    def undo_move(self):
        undo_moves = self.all_moves_made.pop()
        self.row = undo_moves[0][0]
        self.column = undo_moves[0][1]
        place = undo_moves[1]
        object_one = undo_moves[2]
        object_two = undo_moves[3]
        image1 = None
        image2 = None
        if object_one is not None:
            temp1 = object_one.type_color
            image1 = self.get_image(temp1)
        if object_two is not None:
            temp2 = object_two.type_color
            image2 = self.get_image(temp2)
        self.undo_move_on_board(place, object_one, object_two, image1, image2)
    
    def get_image(self, image):
        for a in left.board.black_white:
            for b in a:
                if b[0] == image:
                    image = b[1]
                    break
        return image
    #this method updates the entire stack. this is used when loading a game
    def update_all_moves_made(self, new):
        self.all_moves_made = new
                    
    def undo_move_on_board(self, place, orginal_object, new_object, image1, image2):
        left.board.undo_background()
        image_one = left.board.canvas_grid[self.row][self.column]
        image_two = left.board.canvas_grid[place[0]][place[1]]
        image_two.delete("all")
        image_two.create_image(35, 35, image=image1)
        image_one.delete("all")
        image_one.create_image(35, 35, image=image2)
        left.board.image_name_grid[place[0]][place[1]] = image1
        left.board.image_name_grid[self.row][self.column] = image2
        piece_board.board[place[0]][place[1]] = orginal_object
        piece_board.board[self.row][self.column] = new_object
        piece_board.board[place[0]][place[1]].row = place[0]
        piece_board.board[place[0]][place[1]].column = place[1]
        update_all_moves()
        left.board.white_king = king_check()[0].check
        left.board.black_king = king_check()[1].check
        if left.board.turn == "W":
            left.board.turn = "B"
        elif left.board.turn == "B":
            left.board.turn = "W"

saves = LoadNames()
for_undoing = Undo()
piece_board = Board(None)
window = Window()
left = LeftSide(window)
window.grid(left)
window.mainloop()
