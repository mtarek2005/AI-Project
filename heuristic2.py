# last move: previous player's last move position
# board: 19x19 array in the form board[row(from 0 to 18)][column(from 0 to 18)] where 0=no stone, 1=player 1's white stone, 2=player 2's black stone
# captures: number of peices captured, captures[0] is white stones(p1) captured by black(p2), captures[1] is black stones(p2) captured by white(p1)
# turn: 1 if player 1's turn(white) or 2 if player 2's turn(black)
# num_moves: number of moves since game started
#defensive heuristic
import math

def do_ai(last_move: tuple[int, int], board: list[list[int]], captures: tuple[int, int], turn: int, num_moves: int) -> tuple[int, int]:
  
    
    opponent_color = 2 if turn == 1 else 1 
    best_score = -math.inf
    best_move = None
    
    
    opponent_captures = captures[0] if opponent_color == 2 else captures[1]
    ai_captures = captures[1] if opponent_color == 2 else captures[0]
    
  
    capture_advantage = ai_captures - opponent_captures
    
    
    for row in range(0, 19):  
        for col in range(0, 19): 
            if board[row][col] == 0:  
                score = evaluate_defensive_move(row, col, board, opponent_color, last_move)
                
           
                if capture_advantage < 0:
                    score += 5  

                
                if num_moves > 10:
                    score += 3  
                
             
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    
    return best_move
def evaluate_defensive_move(row, col, board, opponent_color, last_move):

    dirs = [
        (1, 0), (-1, 0),  # Vertical directions
        (0, 1), (0, -1),  # Horizontal directions
        (1, 1), (1, -1),  # Diagonal directions
        (-1, 1), (-1, -1) # Reverse diagonal directions
    ]
    
    threat_score = 0
    
    # Weight factors for directions
    vertical_weight = 1.5 
    horizontal_weight = 1.5  
    diagonal_weight = 1  

    for dir in dirs:
        aligned_count = 1  
        
        for i in range(1, 5):  
            r, c = row + dir[0] * i, col + dir[1] * i
            if 0 <= r < 19 and 0 <= c < 19:
                if board[r][c] == opponent_color:
                    aligned_count += 1
                elif board[r][c] == 0:
                    break  
                else:
                    break 
            else:
                break 
        
        
        if dir in [(1, 0), (-1, 0)]:  
            weight = vertical_weight
        elif dir in [(0, 1), (0, -1)]:  
            weight = horizontal_weight
        else: 
            weight = diagonal_weight
        
        
        if aligned_count == 4:  
            threat_score += 10 * weight 
        elif aligned_count == 3: 
            threat_score += 5 * weight  
    
    
    last_row, last_col = last_move
    distance_to_last_move = math.sqrt((row - last_row)**2 + (col - last_col)**2)
    
    
    proximity_score = max(0, 10 - distance_to_last_move) 

    return threat_score + proximity_score
    
