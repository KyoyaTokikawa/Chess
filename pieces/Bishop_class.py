from pieces.Piece_class import *
from src.piece_move import *
class Bishop(Piece):
    def __init__(self, player, position, name = 'BISHOP'):
        super().__init__(player, position)
        self.name = name
        self.piece_flag = 'B'

    def __call__(self, board):
        bishop_move(board, self)
