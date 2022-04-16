class Piece:
    """this is the base class for all the pieces"""
    WHITE = "W"
    BLACK = "B"

    def __init__(self, colour, row, column, board):
        """each piece contains these attributes"""
        self.colour = colour
        self.row = row
        self.column = column
        self.moves = []
        self.board = board
        self.board.update_board(self, self.row, self.column)

    def update_row_column(self, row, column):
        """updates the attributes row and column"""
        self.row = row
        self.column = column

    @staticmethod
    def out_range_check(row, column):
        """checks that a given row and column is within the specified range"""
        if row > 8 or column > 8 or row < 0 or column < 0:
            return True
        else:
            return False

    def collision_check(self, element):
        """checks that the element given isnt the fill fo the board object"""
        if element != self.board.fill:
            return True
        else:
            return False

    def collision_colour_check(self, row, column):
        """Checks that for a collision that the pieces are of the same colour"""
        obj = self.board.direct_access(row, column)
        if obj.colour is self.colour:
            return True
        return False

    def check_decision(self, row, column):
        """this summerises all the checks and adds a turn or not"""
        try:
            element = self.board.return_board()[row][column]
            range_check = self.out_range_check(row, column)
            collision = self.collision_check(element)
            if range_check is True:
                return True
            else:
                if collision is True:
                    colour_check = self.collision_colour_check(row, column)
                    if colour_check is True:
                        return True
                    elif colour_check is False:
                        self.moves.append([row, column])
                        return True
                elif collision is False:
                    self.moves.append([row, column])
        except IndexError:
            return True

    def clear_moves(self):
        """clears the array moves"""
        self.moves = []


class Rook(Piece):
    """this class defines the rules for the moves of a Rook piece. inherits from piece class"""
    def __init__(self, colour, row, column, board):
        super().__init__(colour, row, column, board)
        self.type = "Rook.png"
        self.type_colour = colour + self.type
        self.get_moves()

    def get_moves(self):
        """gets all of the moves availale this piece"""
        self.moves_horizontal(1)
        self.moves_horizontal(-1)
        self.moves_vertical(1)
        self.moves_vertical(-1)

    def moves_horizontal(self, direction):
        """go horizontaly though the board"""
        for a in range(1, 8):
            if self.check_decision(self.row, self.column + (a * direction)) is True:
                break
            else:
                pass

    def moves_vertical(self, direction):
        """goes vertically through the board"""
        for a in range(1, 8):
            if self.check_decision(self.row + (a * direction), self.column) is True:
                break
            else:
                pass


class Bishop(Piece):
    """this class defines the rules for the moves of a bishop piece. inherits from piece class"""
    def __init__(self, colour, row, column, board):
        super().__init__(colour, row, column, board)
        self.type = "Bishop.png"
        self.type_colour = colour + self.type
        self.get_moves()

    def moves_diagonal(self, row_direction, column_direction):
        for a in range(1, 8):
            if self.check_decision(self.row + (a * row_direction), self.column + (a * column_direction)) is True:
                break

    def get_moves(self):
        """gets all of the moves availale this piece"""
        self.moves_diagonal(1, 1)
        self.moves_diagonal(1, -1)
        self.moves_diagonal(-1, -1)
        self.moves_diagonal(-1, 1)


class Queen(Bishop, Rook):
    """this class defines the rules for the moves of a queen piece. inherits from bishop and rook and piece"""
    def __init__(self, colour, row, column, board):
        super().__init__(colour, row, column, board)
        self.type = "Queen.png"
        self.type_colour = colour + self.type
        self.get_moves()

    def get_moves(self):
        """gets all of the moves availale this piece"""
        Rook.get_moves(self)
        Bishop.get_moves(self)


class Knight(Piece):
    """this class defines the rules for the moves of a knight piece. inherits from piece class"""
    def __init__(self, colour, row, column, board):
        super().__init__(colour, row, column, board)
        self.type = "Knight.png"
        self.type_colour = colour + self.type
        self.get_moves()

    def knight_moves(self, row_move, column_move):
        """checks if the loaction passed is valid"""
        self.check_decision(self.row + row_move, self.column + column_move)

    def get_moves(self):
        """gets all of the moves availale this piece"""
        self.knight_moves(2, 1)
        self.knight_moves(2, -1)
        self.knight_moves(-2, 1)
        self.knight_moves(-2, -1)
        self.knight_moves(1, 2)
        self.knight_moves(1, -2)
        self.knight_moves(-1, - 2)
        self.knight_moves(-1, 2)


class Pawn(Piece):
    """this class defines the rules for the moves of a Pawn piece. inherits from piece class"""
    def __init__(self, colour, row, column, board):
        super().__init__(colour, row, column, board)
        self.moved = 0
        self.x = row
        self.y = column
        self.type = "Pawn.png"
        self.type_colour = colour + self.type
        self.get_moves()

    def first_move(self):
        """defines how the pawn moves on its first go"""
        if self.colour == self.WHITE:
            for a in range(2):
                if self.collision_check(self.board.return_board()[self.row - (a + 1)][self.column]) is True:
                    break
                else:
                    self.check_decision(self.row - (a + 1), self.column)
        if self.colour == self.BLACK:
            for a in range(2):
                if self.collision_check(self.board.return_board()[self.row + (a + 1)][self.column]) is True:
                    break
                else:
                    self.check_decision(self.row + (a + 1), self.column)
        self.moved = 1

    def after_first(self):
        """defines how the pawn can move after its first move"""
        if self.colour == self.WHITE:
            try:
                if self.collision_check(self.board.return_board()[self.row - 1][self.column]) is False:
                    self.check_decision(self.row - 1, self.column)
            except IndexError:
                pass
        elif self.colour == self.BLACK:
            try:
                if self.collision_check(self.board.return_board()[self.row + 1][self.column]) is False:
                    self.check_decision(self.row + 1, self.column)
            except IndexError:
                pass

    def pawn_moves(self):
        """this sums up all the moves the pawn can make encluding taking diagonal pieces"""
        if self.y == self.column and self.x == self.row:
            self.first_move()
        else:
            self.after_first()

        if self.colour == self.WHITE:
            try:
                if self.collision_check(self.board.return_board()[self.row - 1][self.column - 1]) is True:
                    self.check_decision(self.row - 1, self.column - 1)
            except IndexError:
                pass
            try:
                if self.collision_check(self.board.return_board()[self.row - 1][self.column + 1]) is True:
                    self.check_decision(self.row - 1, self.column + 1)
            except IndexError:
                pass

        elif self.colour == self.BLACK:
            try:
                if self.collision_check(self.board.return_board()[self.row + 1][self.column - 1]) is True:
                    self.check_decision(self.row + 1, self.column - 1)
            except IndexError:
                pass
            try:
                if self.collision_check(self.board.return_board()[self.row + 1][self.column + 1]) is True:
                    self.check_decision(self.row + 1, self.column + 1)
            except IndexError:
                pass

    def get_moves(self):
        """gets all of the moves availale this piece"""
        self.promote()
        self.pawn_moves()

    def promote(self):
        if self.colour == self.WHITE and self.row == 0:
            Queen(self.WHITE, self.row, self.column, self.board)
        if self.colour == self.BLACK and self.row == 7:
            Queen(self.BLACK, self.row, self.column, self.board)


class King(Piece):
    """this class defines the rules for the moves of a king piece. inherits from piece class"""

    def __init__(self, colour, row, column, board):
        super().__init__(colour, row, column, board)
        self.check = False
        self.type = "King.png"
        self.type_colour = colour + self.type
        self.get_moves()

    def in_check(self):
        """changes the tribute check to true"""
        self.check = True

    def not_in_check(self):
        """changes the tribute check to false"""
        self.check = False

    def king_moves(self):
        """checks if the king moves are valid"""
        self.check_decision(self.row - 1, self.column)
        self.check_decision(self.row - 1, self.column + 1)
        self.check_decision(self.row, self.column + 1)
        self.check_decision(self.row + 1, self.column + 1)
        self.check_decision(self.row + 1, self.column)
        self.check_decision(self.row + 1, self.column - 1)
        self.check_decision(self.row, self.column - 1)
        self.check_decision(self.row - 1, self.column - 1)

    def get_moves(self):
        """gets all of the moves availale this piece"""
        self.king_moves()


if __name__ == '__main__':
    pass
