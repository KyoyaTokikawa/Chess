from pieces.Rook_class import Rook
import sys
from pieces.Piece_class import Piece
from src.piece_move import *
class Queen(Piece):
    def __init__(self, player, position, name = 'QUEEN'):
        super().__init__(player, position)
        self.name = name
        self.piece_flag = 'Q'

    def __call__(self, board):
        bishop_move(board, self)
        rook_move(board, self)