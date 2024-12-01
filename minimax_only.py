import math


def evaluate(board, captures, turn):
    score = 0
    for row in range(19):
        for col in range(19):
            if board[row][col] == turn:
                score += 1
            elif board[row][col] == 3 - turn:
                score -= 1
    score += captures[turn - 1] * 10
    score -= captures[2 - turn] * 10
    return score


def is_terminal(board, captures):
    return any(capture >= 10 for capture in captures) or not any(0 in row for row in board)


def get_possible_moves(board):
    moves = []
    for row in range(19):
        for col in range(19):
            if board[row][col] == 0:
                moves.append((row, col))
    return moves


def minimax(board, depth, maximizing_player, captures, turn, alpha=-math.inf, beta=math.inf):
    if depth == 0 or is_terminal(board, captures):
        return evaluate(board, captures, turn), None

    possible_moves = get_possible_moves(board)
    best_move = None

    if maximizing_player:
        max_eval = -math.inf
        for move in possible_moves:
            row, col = move
            board[row][col] = turn
            new_captures = list(captures)
            eval_score, _ = minimax(board, depth - 1, False, new_captures, 3 - turn, alpha, beta)
            board[row][col] = 0
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in possible_moves:
            row, col = move
            board[row][col] = 3 - turn
            new_captures = list(captures)
            eval_score, _ = minimax(board, depth - 1, True, new_captures, turn, alpha, beta)

            board[row][col] = 0

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move



def do_ai(last_move, board, captures, turn, num_moves):
    try:
        depth = 2
        _, best_move = minimax(board, depth, True, captures, turn)
        if best_move and 0 <= best_move[0] < 19 and 0 <= best_move[1] < 19:
            return best_move
        else:
            print("Fallback: AI move invalid, defaulting to center.")
            return (9, 9)
    except Exception as e:
        print(f"AI Error: {e}")
        return (19, 19)
