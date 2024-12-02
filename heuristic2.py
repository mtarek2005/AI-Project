# last move: previous player's last move position
# board: 19x19 array in the form board[row(from 0 to 18)][column(from 0 to 18)] where 0=no stone, 1=player 1's white stone, 2=player 2's black stone
# captures: number of peices captured, captures[0] is white stones(p1) captured by black(p2), captures[1] is black stones(p2) captured by white(p1)
# turn: 1 if player 1's turn(white) or 2 if player 2's turn(black)
# num_moves: number of moves since game started
def do_ai(last_move:tuple[int,int],before_last_move:tuple[int,int],board:list[list[int]],captures:tuple[int,int],turn:int,num_moves:int)->tuple[int,int]:
    move=(0,0)
    return move