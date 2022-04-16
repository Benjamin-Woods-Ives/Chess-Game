from boardm import *
import piecesm
import guim
import menum as menu
import databasem as database
WHITE = "W"
BLACK = "B"
HEIGHT = "600"


class Chess:
    def __init__(self):
        self.piece_board = Board(None)
        self.tile_board = Board(None)
        self.game_end = False
        self.undo = Undo(self.piece_board)
        self.saves = database.GameSaves()
        self.gui = guim.MainWindow(self.tile_board, self.piece_board, HEIGHT)
        self.gui.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.gui.withdraw()
        self.image_dict = guim.Images()
        self.turn = WHITE
        self.white_checkmate = False
        self.black_checkmate = False
        self.black_stalemate = False
        self.white_stalemate = False
        self.create_pieces()
        self.tiles_update()
        self.moves_update()
        self.turn_state = TurnState()
        self.menu = menu.MainMenu(self, HEIGHT)

    def on_exit(self):
        self.end_game()
        self.gui.destroy()

    def create_pieces(self):
        """creates all of the pieces needed for a chess game and puts them into there correct space within pieceboard"""
        piecesm.Rook(BLACK, 0, 0, self.piece_board)
        piecesm.Knight(BLACK, 0, 1, self.piece_board)
        piecesm.Bishop(BLACK, 0, 2, self.piece_board)
        piecesm.Queen(BLACK, 0, 3, self.piece_board)
        piecesm.King(BLACK, 0, 4, self.piece_board)
        piecesm.Bishop(BLACK, 0, 5, self.piece_board)
        piecesm.Knight(BLACK, 0, 6, self.piece_board)
        piecesm.Rook(BLACK, 0, 7, self.piece_board)
        for column in range(8):
            piecesm.Pawn(BLACK, 1, column, self.piece_board)
            piecesm.Pawn(WHITE, 6, column, self.piece_board)
        piecesm.Rook(WHITE, 7, 0, self.piece_board)
        piecesm.Knight(WHITE, 7, 1, self.piece_board)
        piecesm.Bishop(WHITE, 7, 2, self.piece_board)
        piecesm.Queen(WHITE, 7, 3, self.piece_board)
        piecesm.King(WHITE, 7, 4, self.piece_board)
        piecesm.Bishop(WHITE, 7, 5, self.piece_board)
        piecesm.Knight(WHITE, 7, 6, self.piece_board)
        piecesm.Rook(WHITE, 7, 7, self.piece_board)

    def moves_update(self):
        """updates all moves every piece can take"""
        for row in self.piece_board.board:
            for column in row:
                if column is not self.piece_board.fill:
                    column.clear_moves()
                    column.get_moves()

    def tiles_update(self):
        """updates the gui based of the piece_board """
        for row in range(8):
            for column in range(8):
                if self.piece_board.board[row][column] != self.piece_board.fill:
                    self.tile_board.board[row][column].delete_image()
                    piece_colour = self.piece_board.board[row][column].colour
                    piece_image = self.piece_board.board[row][column].type_colour
                    image_object = self.image_dict.get_image(piece_colour, piece_image)
                    self.tile_board.board[row][column].update_image(image_object)
                else:
                    self.tile_board.board[row][column].delete_image()

    def get_move_type(self):
        """returns the turn tribute withing tile_board"""
        return self.gui.tile_board.turn()

    def reset_turn_state(self):
        """calls the reset_turn method within the tile_board object"""
        self.gui.tile_board.reset_turn()

    def next_turn(self):
        """changes to the next turn"""
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def set_turn(self, turn):
        self.turn = turn

    def state_1(self):
        """handles what happens when there is the firs click and the tile_board tribute turn = 1 """
        row = self.gui.tile_board.input_location[0]
        column = self.gui.tile_board.input_location[1]
        if self.piece_board.board[row][column] is not None:
            if self.turn == self.piece_board.board[row][column].colour:
                self.turn_state.update_1(row, column)
                self.gui.tile_board.update_tiles([row, column], self.piece_board.board[row][column].moves)
            else:
                self.reset_turn_state()
        else:
            self.reset_turn_state()

    def pre_move_check(self, row, column, turn, row_1, column_1):
        """checks that the next move is valid to make(eg not putting yourself into check)"""
        piece_1 = self.piece_board.board[row_1][column_1]
        piece_2 = self.piece_board.board[row][column]
        self.move_piece(piece_2, row, column, False, row_1, column_1)
        if piece_1 is not None:
            piece_1.update_row_column(row, column)
        if piece_2 is not None:
            piece_2.update_row_column(row_1, column_1)
        self.moves_update()
        white_check, black_check = self.in_check_checker()
        self.piece_board.update_board(piece_1, row_1, column_1)
        self.piece_board.update_board(piece_2, row, column)
        if piece_1 is not None:
            piece_1.update_row_column(row_1, column_1)
        if piece_2 is not None:
            piece_2.update_row_column(row, column)
        self.moves_update()
        temp = {"W": black_check, "B": white_check}
        return temp[turn]

    def state_2(self):
        """handles what happens when there is the second click and the tile_board tribute turn = 2 """
        row = self.gui.tile_board.input_location[0]
        column = self.gui.tile_board.input_location[1]
        into_check = self.pre_move_check(row, column, self.turn,
                                         self.turn_state.location_1[0], self.turn_state.location_1[1])
        if into_check is False:
            if self.piece_board.board[row][column] is None:
                self.make_move(row, column)
            elif self.turn == self.piece_board.board[row][column].colour:
                self.reset_turn_state()
                self.gui.tile_board.set_turn(1)
                self.state_1()
                self.gui.update()
            elif self.turn != self.piece_board.board[row][column].colour:
                self.make_move(row, column)
        else:
            self.reset_turn_state()

    def get_all_moves(self, colour):
        """returns all the moves of a given colour piece"""
        moves = []
        for row in self.piece_board.board:
            for column in row:
                if column is not None:
                    if column.colour == colour:
                        moves.append(column.moves)
        return moves

    def get_king_location(self, colour):
        """returns the row and column of the given colour king object"""
        for row in self.piece_board.board:
            for column in row:
                if column is not None:
                    if column.colour == colour:
                        if hasattr(column, "check"):
                            return [column.row, column.column]

    @staticmethod
    def in_moves_check(moves, location):
        """checks the a location is within the moves"""
        in_moves = False
        for all_moves in moves:
            for individual_move in all_moves:
                if location == individual_move:
                    in_moves = True
                    break
        return in_moves

    def get_pieces(self, colour):
        pieces = []
        for row in self.piece_board.board:
            for column in row:
                if column is not None:
                    if column.colour == colour and not hasattr(column, "check"):
                        pieces.append(column)
        return pieces

    def stalemate_checker(self):
        black_stalemate = False
        white_stale_mate = False
        black_pieces = self.get_pieces(BLACK)
        white_pieces = self.get_pieces(WHITE)
        can_move_black = self.moves_available(black_pieces)
        can_move_white = self.moves_available(white_pieces)
        white_king_move = self.can_king_move(WHITE)
        black_king_move = self.can_king_move(BLACK)
        if white_king_move and not can_move_white:
            white_stale_mate = True
        if black_king_move and not can_move_black:
            black_stalemate = True
        return black_stalemate, white_stale_mate

    def update_stalemate(self):
        self.black_stalemate, self.white_stalemate = self.stalemate_checker()

    @staticmethod
    def moves_available(pieces):
        for piece in pieces:
            if len(piece.moves) > 0:
                return True

    def can_king_move(self, king_colour):
        king_location = self.get_king_location(king_colour)
        king_piece = self.piece_board.board[king_location[0]][king_location[1]]
        king_can_move = True
        for moves in king_piece.moves:
            if self.pre_move_check(moves[0], moves[1], king_colour, king_location[0], king_location[1]) is False:
                king_can_move = False
        return king_can_move

    def in_check_checker(self):
        """checks to see what state the king is in. true for being in check and false for not being in check"""
        black_moves = self.get_all_moves(BLACK)
        white_moves = self.get_all_moves(WHITE)
        black_king_location = self.get_king_location(BLACK)
        white_king_location = self.get_king_location(WHITE)
        in_check_black = self.in_moves_check(white_moves, black_king_location)
        in_check_white = self.in_moves_check(black_moves, white_king_location)
        return in_check_black, in_check_white

    def move_piece(self, piece_2, row_2, column_2, add_to_undo, row_1, column_1):
        """moves a given piece to a new location and also saves that move to the undo stack"""
        piece_1 = self.piece_board.board[row_1][column_1]
        if add_to_undo is True:
            self.undo.update_moves_made([row_1, column_1], [row_2, column_2],
                                        piece_1, self.piece_board.board[row_2][column_2],
                                        self.turn)
        self.piece_board.board[row_1][column_1].update_row_column(row_2, column_2)
        self.piece_board.update_board(piece_1, row_2, column_2)
        self.piece_board.update_board(piece_2, row_1, column_1)

    def make_move(self, row, column):
        """handles moving a piece and checking that the move is possible"""
        self.turn_state.update_2(row, column)
        if self.move_check(row, column) is True:
            self.move_piece(None, row, column, True, self.turn_state.location_1[0], self.turn_state.location_1[1])
            self.reset_turn_state()
            self.next_turn()
        else:
            self.gui.tile_board.reset_turn()
        self.turn_state.reset()

    def move_check(self, row, column):
        """checks that the move the piece is going to make is within the moves it can make"""
        returning = False
        row_1 = self.turn_state.location_1[0]
        column_1 = self.turn_state.location_1[1]
        for move_check in self.piece_board.board[row_1][column_1].moves:
            if move_check == [row, column]:
                returning = True
        return returning

    def game_start(self):
        """starts the game"""
        while self.game_end is False:
            self.gui.update()
            self.tiles_update()
            self.moves_update()
            self.update_stalemate()
            self.gui.update()
            if (self.black_checkmate is False) or (self.white_checkmate is False):
                pass
            if (self.black_stalemate is True) or (self.white_stalemate is True):
                self.gui.grid_winner("Draw")
                self.end_game()
            else:
                if self.gui.tile_board.turn == 1:
                    self.state_1()
                if self.gui.tile_board.turn == 2:
                    self.state_2()
                    self.update_stalemate()
                    white_check, black_check = self.in_check_checker()
                    print("white check: ", black_check)
                    print("black check: ", white_check)
                    self.turn_state.update_check(white_check, black_check)
                    self.turn_state.update_king_location(self.get_king_location(BLACK), self.get_king_location(WHITE))

    def end_game(self):
        """ends the game if needed."""
        self.game_end = True


class TurnState:
    """stores the kings location and also where the pieces location  that was first selected is stored """
    def __init__(self):
        self.location_1 = []
        self.location_2 = []
        self.check = {"W": False, "B": False}
        self.white_king_location = []
        self.black_king_location = []

    def reset(self):
        """resets all the tributes back to there inilised state"""
        self.__init__()

    def reset_1(self):
        """resetes the location_1 tribute"""
        self.location_1 = None

    def reset_2(self):
        """resets the location_2 tribute"""
        self.location_2 = []

    def update_1(self, row, column):
        """updates location_1 tribute"""
        self.location_1 = [row, column]

    def update_2(self, row, column):
        """updates location_tribute"""
        self.location_2 = [row, column]

    def update_check(self, white_check, black_check):
        """updates the check dictioanry"""
        self.check["W"] = white_check
        self.check["B"] = black_check

    def update_king_location(self, white_location, black_location):
        """updates the kings locations"""
        self.white_king_location = white_location
        self.black_king_location = black_location

    def return_king_location(self, colour):
        """returns the location of the given colour king"""
        temp = {"W": self.white_king_location, "B": self.black_king_location}
        return temp[colour]


class Undo:
    def __init__(self, board):
        self.all_moves_made = []
        self.board = board

    def update_moves_made(self, original, new, original_object, new_object, turn):
        """adds a move made to state to the undo stack"""
        one_move = [original, new, original_object, new_object, turn]
        self.all_moves_made.append(one_move)

    def undo_move(self):
        """undoes a move last move was made"""
        if len(self.all_moves_made) != 0:
            undoing = self.all_moves_made.pop()
            self.board.update_board(undoing[2], undoing[0][0], undoing[0][1])
            self.board.update_board(undoing[3], undoing[1][0], undoing[1][1])
            undoing[2].update_row_column(undoing[0][0], undoing[0][1])

    def update_move_stack(self, moves):
        """updates the entire stack this is used when loading a game"""
        self.all_moves_made = moves


if __name__ == '__main__':
    Chess()

