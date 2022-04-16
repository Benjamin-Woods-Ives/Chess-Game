class Board:
    """this class is basically a 8x8 2d array with other methods"""
    def __init__(self, fill):
        self.board = []  # 2d Array
        self.fill = fill
        for y in range(8):
            temp = []
            for x in range(8):
                temp.append(self.fill)
            self.board.append(temp)

    def print_board(self):
        """prints the board used whiles creating the game"""
        for a in self.board:
            pass
            print(a)

    def update_board(self, piece, row, column):
        """updates a element within the board tribute"""
        self.board[row][column] = piece

    def update_entire_board(self, board):
        """updates the entire board tribute this is used load the game"""
        self.board = board

    def return_board(self):
        """returns the board tribute to the main program"""
        return_board = self.board
        return return_board

    def direct_access(self, row, column):
        """returns a element within from the board tribute"""
        element = self.board[row][column]
        return element


if __name__ == '__main__':
    pass

