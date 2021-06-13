from pieces.Piece_class import *
from src.piece_move import *
class Rook(Piece):
    def __init__(self, player, position, name = 'ROOK'):
        super().__init__(player, position)
        self.name = name
        self.piece_flag = 'R'

    def __call__(self, board):
        rook_move(board, self)
