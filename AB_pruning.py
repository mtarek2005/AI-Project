import math


def evaluate(board, captures, turn, move, last_move):
    score = 0
    matches=get_matches(board,move,turn)
    inv_matches=get_matches(board,last_move,3-turn)
    max_match=max(matches)
    max_inv_match=max(inv_matches)
    winner=turn if max_match >= 5 else (1 if captures[0]>=10 else 2 if captures[1]>=10 else 0)
    # for row in range(19):
    #     for col in range(19):
    #         if board[row][col] == turn:
    #             score += 1
    #         elif board[row][col] == 3 - turn:
    #             score -= 1
    score = 100 if winner==turn else 0
    score -= max_match*20
    score += max_inv_match*20
    score -= captures[turn - 1] * 10
    score += captures[2 - turn] * 10
    return score


def is_terminal(board, captures, color, move):
    return any(capture >= 10 for capture in captures) or not any(0 in row for row in board) or max(get_matches(board,move,color))>=5


def get_possible_moves(board):
    moves = []
    for row in range(19):
        for col in range(19):
            if board[row][col] == 0:
                moves.append((row, col))
    return moves


def minimax(board, depth, maximizing_player, captures, turn, last_move:tuple[int,int], before_last_move:tuple[int,int], alpha=-math.inf, beta=math.inf):
    count=1
    #print(f"last move: {last_move}, bef last: {before_last_move}, depth: {depth}")
    if depth == 0 or is_terminal(board, captures, 3-turn, last_move):
        if depth!=0:
            print("terminal")
        return evaluate(board, captures, 3-turn, last_move, before_last_move), last_move, count
    possible_moves = get_possible_moves(board)
    best_move = None
    inv_color=3-turn
    color=turn
    if maximizing_player:
        max_eval = -math.inf
        for move in possible_moves:
            row, col = move
            board[row][col] = turn
            positions_captured,new_captures = get_new_captures(board,color,captures,row,col)
            eval_score, _, new_count = minimax(board, depth - 1, False, new_captures, 3 - turn, move, last_move, alpha, beta)
            count+=new_count
            board[row][col] = 0
            for pos in positions_captured:
                board[pos[0]][pos[1]]=inv_color
            if eval_score > max_eval:
                # print(f"max:{eval_score}>{max_eval} as {turn}")
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move, count
    else:
        min_eval = math.inf
        for move in possible_moves:
            row, col = move
            board[row][col] = 3 - turn
            positions_captured,new_captures = get_new_captures(board,color,captures,row,col)
            eval_score, _, new_count = minimax(board, depth - 1, True, new_captures, turn, move, last_move, alpha, beta)
            count+=new_count
            board[row][col] = 0
            for pos in positions_captured:
                board[pos[0]][pos[1]]=inv_color
            if eval_score < min_eval:
                # print(f"min:{eval_score}<{min_eval} as {turn}")
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move, count

def get_new_captures(board,color,captures,row,col):
    positions_captured=[]
    new_captures=list(captures)
    inv_color=3-color
    dirs=[
        (1,0),
        (-1,0),
        (0,1),
        (0,-1),
        (1,1),
        (1,-1),
        (-1,1),
        (-1,-1)
    ]
    for dir in dirs:
        if(min(row+dir[0]*3,col+dir[1]*3)>=0 and max(row+dir[0]*3,col+dir[1]*3)<19):
            if(board[row+dir[0]*1][col+dir[1]*1]==inv_color and board[row+dir[0]*2][col+dir[1]*2]==inv_color and board[row+dir[0]*3][col+dir[1]*3]==color):
                board[row+dir[0]*1][col+dir[1]*1]=0
                board[row+dir[0]*2][col+dir[1]*2]=0
                positions_captured+=[(row+dir[0]*1,col+dir[1]*1),(row+dir[0]*2,col+dir[1]*2)]
                new_captures[inv_color-1]+=2
    return positions_captured,new_captures

def get_matches(board,move,color):
    row=move[0]
    col=move[1]
    inv_color=3-color
    horizontal_match=1
    vertical_match=1
    rising_diagonal_match=1
    falling_diagonal_match=1

    search_row=row
    search_col=col
    search_row+=1
    while (min(search_row,search_col)>=0 and max(search_row,search_col)<19) and board[search_row][search_col]==color:
        horizontal_match+=1
        search_row+=1

    search_row=row
    search_col=col
    search_row-=1
    while (min(search_row,search_col)>=0 and max(search_row,search_col)<19) and board[search_row][search_col]==color:
        horizontal_match+=1
        search_row-=1

    search_row=row
    search_col=col
    search_col+=1
    while (min(search_row,search_col)>=0 and max(search_row,search_col)<19) and board[search_row][search_col]==color:
        vertical_match+=1
        search_col+=1

    search_row=row
    search_col=col
    search_col-=1
    while (min(search_row,search_col)>=0 and max(search_row,search_col)<19) and board[search_row][search_col]==color:
        vertical_match+=1
        search_col-=1

    search_row=row
    search_col=col
    search_row+=1
    search_col+=1
    while (min(search_row,search_col)>=0 and max(search_row,search_col)<19) and board[search_row][search_col]==color:
        rising_diagonal_match+=1
        search_row+=1
        search_col+=1

    search_row=row
    search_col=col
    search_row-=1
    search_col-=1
    while (min(search_row,search_col)>=0 and max(search_row,search_col)<19) and board[search_row][search_col]==color:
        rising_diagonal_match+=1
        search_row-=1
        search_col-=1

    search_row=row
    search_col=col
    search_row+=1
    search_col-=1
    while (min(search_row,search_col)>=0 and max(search_row,search_col)<19) and board[search_row][search_col]==color:
        falling_diagonal_match+=1
        search_row+=1
        search_col-=1

    search_row=row
    search_col=col
    search_row-=1
    search_col+=1
    while (min(search_row,search_col)>=0 and max(search_row,search_col)<19) and board[search_row][search_col]==color:
        falling_diagonal_match+=1
        search_row-=1
        search_col+=1

    return (horizontal_match,vertical_match,rising_diagonal_match,falling_diagonal_match)


#last move: previous player's last move position
# board: 19x19 array in the form board[row(from 0 to 18)][column(from 0 to 18)] where 0=no stone, 1=player 1's white stone, 2=player 2's black stone
# captures: number of peices captured, captures[0] is white stones(p1) captured by black(p2), captures[1] is black stones(p2) captured by white(p1)
# turn: 1 if player 1's turn(white) or 2 if player 2's turn(black)
# num_moves: number of moves since game started
def do_ai(last_move:tuple[int,int],before_last_move:tuple[int,int],board:list[list[int]],captures:tuple[int,int],turn:int,num_moves:int)->tuple[int,int]:
    try:
        depth = 2
        print(f"playing at {last_move}")
        score, best_move, count = minimax(board, depth, True, captures, turn, last_move, before_last_move)
        print(count)
        print(score)
        print(best_move)
        if best_move and 0 <= best_move[0] < 19 and 0 <= best_move[1] < 19:
            return best_move
        else:
            print("Fallback: AI move invalid, defaulting to center.")
            return (9, 9)
    except Exception as e:
        print(f"AI Error: {e}")
        return (19, 19)
