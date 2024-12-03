# last move: previous player's last move position
# board: 19x19 array in the form board[row(from 0 to 18)][column(from 0 to 18)] where 0=no stone, 1=player 1's white stone, 2=player 2's black stone
# captures: number of peices captured, captures[0] is white stones(p1) captured by black(p2), captures[1] is black stones(p2) captured by white(p1)
# turn: 1 if player 1's turn(white) or 2 if player 2's turn(black)
# num_moves: number of moves since game started
#aggressive heuristic
import math

def do_ai(last_move: tuple[int, int], board: list[list[int]], captures: tuple[int, int], turn: int, num_moves: int) -> tuple[int, int]:
    ai_color = turn
    opponent_color = 2 if ai_color == 1 else 1
    best_score = -math.inf
    best_move = None

    for row in range(19):
        for col in range(19):
            if board[row][col] == 0:
                if is_immediate_win(row, col, board, ai_color):
                    return (row, col)

                if is_immediate_win(row, col, board, opponent_color):
                    return (row, col)

                score = evaluate_move(row, col, board, ai_color, opponent_color, captures, num_moves)

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move


def is_immediate_win(row, col, board, color):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for dr, dc in directions:
        aligned_count = 1

        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < 19 and 0 <= c < 19 and board[r][c] == color:
                aligned_count += 1
            else:
                break

        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < 19 and 0 <= c < 19 and board[r][c] == color:
                aligned_count += 1
            else:
                break

        if aligned_count >= 5:
            return True

    return False


def evaluate_move(row, col, board, ai_color, opponent_color, captures, num_moves):
    score = 0
    score += evaluate_alignment(row, col, board, ai_color) * 5
    score += evaluate_alignment(row, col, board, opponent_color) * 3
    score += evaluate_capture_potential(row, col, board, ai_color, opponent_color) * 3
    center_bonus = max(0, 10 - (abs(row - 9) + abs(col - 9)))
    score += center_bonus
    return score


def evaluate_alignment(row, col, board, color):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    score = 0

    for dr, dc in directions:
        aligned_count = 1

        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < 19 and 0 <= c < 19 and board[r][c] == color:
                aligned_count += 1
            else:
                break

        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < 19 and 0 <= c < 19 and board[r][c] == color:
                aligned_count += 1
            else:
                break

        if aligned_count >= 5:
            score += 10000
        elif aligned_count == 4:
            score += 500
        elif aligned_count == 3:
            score += 100
        elif aligned_count == 2:
            score += 20

    return score


def evaluate_capture_potential(row, col, board, ai_color, opponent_color):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    capture_score = 0

    for dr, dc in directions:
        r1, c1 = row + dr, col + dc
        r2, c2 = row + 2 * dr, col + 2 * dc
        r3, c3 = row + 3 * dr, col + 3 * dc

        if (
            0 <= r1 < 19 and 0 <= c1 < 19 and board[r1][c1] == opponent_color and
            0 <= r2 < 19 and 0 <= c2 < 19 and board[r2][c2] == opponent_color and
            0 <= r3 < 19 and 0 <= c3 < 19 and board[r3][c3] == 0
        ):
            capture_score += 200

    return capture_score
