from pieces.Piece_class import *
from src.piece_move import check_oo, king_move
class King(Piece):
    def __init__(self, player, position, name = 'KING'):
        super().__init__(player, position)
        self.name = name
        self.piece_flag = 'K'


    def __call__(self, board) :
        king_move(board, self)
        check_oo(board, self)
