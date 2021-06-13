def pown_move(board, piece):
    myfile = piece.file
    myrank = piece.rank
    player = piece.player
    uprank = myrank + player.player
    if uprank > -1 and uprank < 8:
        if board[myfile][myrank + player.player] == 0:
            if player.player == 1 and myrank == 6:
                player.add_move(piece, myfile, uprank, 'P')
            elif player.player == -1 and myrank == 1:
                player.add_move(piece, myfile, uprank, 'P')
            else:
                player.add_move(piece, myfile, uprank, '')

            if piece.move_count == 0:
                up2rank = myrank + (player.player * 2)
                if board[myfile][up2rank] == 0:
                    player.add_move(piece, myfile, up2rank, '')

    right_file = myfile + player.player
    if right_file > -1 and right_file < 8 and uprank > -1 and uprank < 8:
        if board[right_file][uprank] != 0 and board[right_file][uprank].player != player:
            if player.player == 1 and myrank == 6:
                player.add_move(piece, right_file, uprank, 'P')
            elif player.player == -1 and myrank == 1:
                player.add_move(piece, right_file, uprank, 'P')
            else:
                player.add_move(piece, right_file, uprank, '')
        else: 
            player.add_move(piece, right_file, uprank, 'C')

    left_file = myfile - player.player
    if left_file > -1 and left_file < 8 and uprank > -1 and uprank < 8:
        if board[left_file][uprank] != 0 and board[left_file][uprank].player != player:
            if player.player == 1 and myrank == 6:
                player.add_move(piece, left_file, uprank, 'P')
            elif player.player == -1 and myrank == 1:
                player.add_move(piece, left_file, uprank, 'P')
            else:            
                player.add_move(piece, left_file, uprank, '')
        else: 
            player.add_move(piece, left_file, uprank, 'C')
    if right_file > -1 and right_file < 8:
        if type(board[right_file][myrank]) == type(piece):
            if board[right_file][myrank].can_Enpassant == True:
                player.add_move(piece, right_file, uprank, '')
    if left_file > -1 and left_file < 8:
        if type(board[left_file][myrank]) == type(piece):
            if board[left_file][myrank].can_Enpassant == True:
                player.add_move(piece, left_file, uprank, '')

def add_piece(piece, file, rank, board):
    player = piece.player
    board_piece = board[file][rank]
    if board_piece != 0:
        if piece.player != board_piece.player:
            player.add_move(piece, file, rank, '')
        else:
            player.add_move(piece, file, rank, 'C')
        return False
    else:
        player.add_move(piece, file, rank, '')
    return True

def rook_move(board, piece):
    find_over = True
    find_under = True
    find_right = True
    find_left = True
    for num in range(1, 8):
        over_rank  = piece.rank + num
        under_rank = piece.rank - num
        right_file = piece.file + num
        left_file  = piece.file - num
        if find_over:
            if over_rank < 8:
                find_over = add_piece(piece, piece.file, over_rank, board)
        if find_under:
            if under_rank > -1:
                find_under = add_piece(piece, piece.file, under_rank, board)
        if find_right:
            if right_file < 8:
                find_right = add_piece(piece, right_file, piece.rank, board)
        if find_left:
            if left_file > -1:
                find_left = add_piece(piece, left_file, piece.rank, board)

def bishop_move(board, piece):
    find_right_over  = True
    find_right_under = True
    find_left_over   = True
    find_left_under  = True
    for num in range(1, 8):
        right_file  = piece.file + num
        left_file   = piece.file - num
        over_rank   = piece.rank + num
        under_rank  = piece.rank - num
        if find_left_under:
            if left_file > -1 and under_rank > -1:
                find_left_under = add_piece(piece, left_file, under_rank, board)
        if find_left_over:
            if left_file > -1 and over_rank  < 8:
                find_left_over = add_piece(piece, left_file, over_rank, board)
        if find_right_over:
            if right_file < 8 and over_rank  < 8:
                find_right_over = add_piece(piece, right_file, over_rank, board)
        if find_right_under:
            if right_file < 8 and under_rank > -1:
                find_right_under = add_piece(piece, right_file, under_rank, board)

def knight_move(board, piece):
    file_right1   = piece.file + 1
    file_right2   = piece.file + 2
    file_left1    = piece.file - 1
    file_left2    = piece.file - 2
    rank_up2      = piece.rank + 2
    rank_up1      = piece.rank + 1
    rank_down1    = piece.rank - 1
    rank_down2    = piece.rank - 2
    if file_right1 < 8 and rank_up2   < 8:# file + 1 rank + 2
        add_piece(piece, file_right1, rank_up2, board)
    
    if file_right2 < 8 and rank_up1 < 8:# file + 2 rank + 1
        add_piece(piece, file_right2, rank_up1, board)
    
    if file_right2 < 8 and rank_down1   > -1:# file + 2 rank - 1
        add_piece(piece, file_right2, rank_down1, board)
    
    if file_right1 < 8 and rank_down2 > -1:# file + 1 rank - 2
        add_piece(piece, file_right1, rank_down2, board)
    
    if file_left1 > -1 and rank_up2   < 8:# file - 1 rank + 2
        add_piece(piece, file_left1 , rank_up2, board)
    
    if file_left2 > -1 and rank_up1 < 8:# file - 2 rank + 1
        add_piece(piece, file_left2 , rank_up1, board)
    
    if file_left2 > -1 and rank_down1   > -1:# file - 2 rank - 1
        add_piece(piece, file_left2 , rank_down1, board)
    
    if file_left1 > -1 and rank_down2 > -1:# file -1 rank - 2
        add_piece(piece, file_left1 , rank_down2, board)

def king_move(board, piece):
    my_file = piece.file
    my_rnak = piece.rank
    right_file = my_file + 1
    left_file  = my_file - 1
    up_rank    = my_rnak + 1
    down_rank  = my_rnak - 1

    if left_file > -1:
        add_piece(piece, left_file, my_rnak, board)

    if left_file > -1 and up_rank < 8:
        add_piece(piece, left_file, up_rank, board)

    if up_rank < 8:
        add_piece(piece, my_file, up_rank, board)

    if up_rank < 8 and right_file < 8:
        add_piece(piece, right_file, up_rank, board)

    if right_file < 8:
        add_piece(piece, right_file, my_rnak, board)

    if right_file < 8 and down_rank > -1:
        add_piece(piece, right_file, down_rank, board)

    if down_rank > -1:
        add_piece(piece, my_file, down_rank, board)

    if down_rank > -1 and left_file > -1:
        add_piece(piece, left_file, down_rank, board)

def check_oo(board, piece):
    a, b, c, d, e, f, g, h = 0, 1, 2, 3, 4, 5, 6, 7
    if piece.player.flag == 'W':
        king_position   = (e, 0)
        bishop_position = (g, 0)
        knight_position = (f, 0)
        rook_position   = (h, 0)
    else:
        king_position   = (e, 7)
        bishop_position = (g, 7)
        knight_position = (f, 7)
        rook_position   = (h, 7)
    bishop = board[bishop_position]
    knight = board[knight_position]
    rook   = board[rook_position]
    player = piece.player
    enemy = player.enemy

    bol_king   = king_position in enemy.attack_list
    bol_bishop = bishop_position in enemy.attack_list
    bol_knight = knight_position in enemy.attack_list
    if bishop == 0 and knight == 0:
        if rook != 0:
            if rook.move_count == 0 and piece.move_count == 0:
                if bol_king == False and bol_bishop  == False and bol_knight == False :
                    piece.player.add_oo(piece.player, piece, rook)


def check_ooo(board, piece):
    a, b, c, d, e, f, g, h = 0, 1, 2, 3, 4, 5, 6, 7
    if piece.player.flag == 'W':
        king_position   = (e, 0)
        queen_position  = (d, 0)
        bishop_position = (c, 0)
        knight_position = (b, 0)
        rook_position   = (a, 0)
    else:
        king_position   = (e, 7)
        queen_position  = (d, 7)
        bishop_position = (g, 7)
        knight_position = (f, 7)
        rook_position   = (h, 7)
    queen  = board[queen_position]
    bishop = board[bishop_position]
    knight = board[knight_position]
    rook   = board[rook_position]
    player = piece.player
    enemy = player.enemy

    bol_king   = king_position in enemy.attack_list
    bol_bishop = bishop_position in enemy.attack_list
    bol_queen  = queen_position in enemy.attack_list
    if queen == 0 and bishop == 0 and knight == 0:
        if rook != 0:
            if rook.move_count == 0 and piece.move_count == 0:
                if bol_king == False and bol_bishop  == False and bol_queen == False :
                    piece.player.add_ooo(piece.player, piece, rook)
    

