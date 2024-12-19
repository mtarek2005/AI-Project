# import the pygame module, so you can use it
# install with `pip install pygame`
import pygame
import time
import minimax_only
import AB_pruning
import heuristic1_minimax
import heuristic2_minimax

w = 800
h = 800
# ai type: None for 2 player game
ai_type = None
AIs: dict = {"mnmx":minimax_only.do_ai,"ABp":AB_pruning.do_ai,"h1":heuristic1_minimax.do_ai,"h2":heuristic2_minimax.do_ai}
ai_choice_menu = [("No AI",None), ("Minimax","mnmx"), ("Alpha - Beta pruning","ABp"), ("Heuristic Function 1: \"Aggressive\"","h1"), ("Heuristic Function 2: \"Defensive\"","h2")]

#positions: 0 empty, 1 white, 2 black
board = [[0] * 19 for i in range(19)]
turn = 0
num_moves = 0
winner = 0
captures = [0, 0]
game_started = False
last_move: tuple[int, int] = (9, 9)

# define a main function
def main():
    global num_moves, turn, board
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Pente - AI Project")
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((w, h))

    
    # load font, prepare values
    font = pygame.font.Font(None, 128)

    draw_menu(screen, pygame.font.Font(None, 64))
    turn = 1

    # define a variable to control the main loop
    running = True
    # main loop(which currently does nothing other than keep the window open)
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    menu_on_click(screen, font)
                else:
                    ingame_on_click(screen, font)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

def menu_on_click(screen: pygame.Surface, font: pygame.font.Font):
    global ai_type, game_started, turn, last_move
    u = h / len(ai_choice_menu)
    loc = pygame.mouse.get_pos()
    choice = int(loc[1] // u)
    print(choice)
    ai_type = ai_choice_menu[choice][1]
    print(ai_type)
    player_color = (loc[0] // (w / 2)) + 1
    game_started = True
    if player_color>1 and ai_type != None:
        do_move((9, 9))
        last_move = (9, 9)
    draw(screen, font)

def ingame_on_click(screen: pygame.Surface, font: pygame.font.Font):
    global num_moves, turn, board, last_move
    u = min(w, h) / (19)
    loc = pygame.mouse.get_pos()
    int_loc = (int(loc[0] // u), int(loc[1] // u))
    print(loc)
    print(int_loc)
    if(board[int_loc[0]][int_loc[1]] == 0 and (int_loc == (9, 9) or num_moves != 0) and winner == 0):
        do_move(int_loc)
        if(ai_type != None and winner == 0):
            draw(screen, font)
            ai_move = do_ai(int_loc, last_move, board, tuple(captures), turn = turn, num_moves = num_moves)
            if(not (min(ai_move[0], ai_move[1]) >= 0 and max(ai_move[0], ai_move[1])<19)):
                raise Exception(f"\033[0;31mAI Error: invalid move \033[0;33m({ai_move[0]},{ai_move[1]})\033[0;31m out of bounds\033[0m")
            if(board[ai_move[0]][ai_move[1]] != 0):
                raise Exception(f"\033[0;31mAI Error: invalid move \033[0;33m({ai_move[0]},{ai_move[1]})\033[0;31m already occupied\033[0m")
            do_move(ai_move)
            last_move = ai_move
        else:
            last_move = int_loc
    draw(screen, font)

def draw_menu(screen: pygame.Surface, font: pygame.font.Font, w: int = w, h: int = h, lw: int = 3, bgC: pygame.Color = (161, 102, 47), rectC: pygame.Color = (73.5, 105, 145), rectLightC: pygame.Color = (140, 150, 200), rectDarkC: pygame.Color = (7, 60, 90), fontC: pygame.Color = (255, 255, 255), wpC: pygame.Color = (220, 220, 220), bpC: pygame.Color = (40, 40, 40)):
    u = h / len(ai_choice_menu)
    screen.fill(bgC)
    for i in range(len(ai_choice_menu)):
        pygame.draw.rect(screen, rectLightC if ai_choice_menu[i][1] else rectC, (u * 0.05, (i + 0.05) * u, (w - u * 0.1) / 2, u * 0.9))
        pygame.draw.rect(screen, rectDarkC if ai_choice_menu[i][1] else rectC, (w / 2, (i + 0.05) * u, (w - u * 0.1) / 2, u * 0.9))
        ren = font.render(ai_choice_menu[i][0], 1, fontC)
        screen.blit(ren, (w / 2 - ren.get_width() / 2, (i * u) + u / (4 if ai_choice_menu[i][1] else 2) - ren.get_rect().height / 2))
        if ai_choice_menu[i][1]:
            ren = font.render("White", 1, fontC)
            screen.blit(ren, (w / 4 - ren.get_width() / 2, (i * u) + u / (4 / 3) - ren.get_rect().height / 2))
            ren = font.render("Black", 1, fontC)
            screen.blit(ren, (w / (4 / 3) - ren.get_width() / 2, (i * u) + u / (4 / 3) - ren.get_rect().height / 2))
    pygame.display.flip()

def draw(screen: pygame.Surface, font: pygame.font.Font, w: int = w, h: int = h, lw: int = 3, bgC: pygame.Color = (161, 102, 47), lnC: pygame.Color = (10, 20, 10), fontC: pygame.Color = (10, 70, 10), wpC: pygame.Color = (220, 220, 220), bpC: pygame.Color = (40, 40, 40)):
    u = min(w, h) / (19)
    # fill background
    screen.fill(bgC)
    for i in range(19):
        pygame.draw.line(screen, lnC, (u / 2, (i + 0.5) * u), (w - u / 2, (i + 0.5) * u), lw)
        pygame.draw.line(screen, lnC, ((i + 0.5) * u, u / 2), ((i + 0.5) * u, h - u / 2), lw)
    pygame.draw.circle(screen, lnC, (w / 2, h / 2), u * 0.3, lw)

    pygame.draw.circle(screen, lnC, (u * 6.5, u * 6.5), u * 0.3, lw)
    pygame.draw.circle(screen, lnC, (u * 12.5, u * 12.5), u * 0.3, lw)
    pygame.draw.circle(screen, lnC, (u * 6.5, u * 12.5), u * 0.3, lw)
    pygame.draw.circle(screen, lnC, (u * 12.5, u * 6.5), u * 0.3, lw)

    # draw stones
    for row in range(19):
        for col in range(19):
            if board[row][col] == 1:
                pygame.draw.circle(screen, wpC, (u * (row + 0.5), u * (col + 0.5)), u * 0.4)
            if board[row][col] == 2:
                pygame.draw.circle(screen, bpC, (u * (row + 0.5), u * (col + 0.5)), u * 0.4)
    if winner != 0:
        ren = font.render(f"Player {winner} wins!", 1, fontC)
        screen.blit(ren, (w / 2 - ren.get_width() / 2, h / 2 - ren.get_rect().height / 2))
    # display stuff
    pygame.display.flip()

def inv_col(color: int):
    return 0 if color == 0 else (1 if color == 2 else 2)

def do_move(loc: tuple[int, int]):
    global board, winner, captures, turn, num_moves
    row = loc[0]
    col = loc[1]
    board[row][col] = turn
    color = turn
    turn = (1 if turn == 2 else 2)
    num_moves += 1
    inv_color = inv_col(color)
    if(color == 0):
        raise Exception(f"\033[0;31mError: invalid board state 0 at \033[0;33m({row},{col})\033[0m")
    
    # search for 5 matching
    dirs={(0, 1): 1, (1, 0): 1, (1, 1):1, (1, -1): 1}
    for dir in dirs.keys():
        search_row = row
        search_col = col
        search_row += dir[0]
        search_col += dir[1]
        while (min(search_row, search_col) >= 0 and max(search_row, search_col)<19) and board[search_row][search_col] == color:
            dirs[dir] += 1
            search_row += dir[0]
            search_col += dir[1]
        search_row = row
        search_col = col
        search_row -= dir[0]
        search_col -= dir[1]
        while (min(search_row, search_col) >= 0 and max(search_row, search_col)<19) and board[search_row][search_col] == color:
            dirs[dir] += 1
            search_row -= dir[0]
            search_col -= dir[1]

    # check for winning
    if(max(dirs.values()) >= 5):
        winner = color
        print(winner)
    
    dirs = [
        (1, 0),
        ( - 1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        ( - 1, 1),
        ( - 1, -1)
    ]
    for dir in dirs:
        if(min(row + dir[0] * 3, col + dir[1] * 3) >= 0 and max(row + dir[0] * 3, col + dir[1] * 3)<19):
            if(board[row + dir[0] * 1][col + dir[1] * 1] == inv_color and board[row + dir[0] * 2][col + dir[1] * 2] == inv_color and board[row + dir[0] * 3][col + dir[1] * 3] == color):
                board[row + dir[0] * 1][col + dir[1] * 1] = 0
                board[row + dir[0] * 2][col + dir[1] * 2] = 0
                captures[inv_color - 1] += 2
                print(f"Capture! white stones captured:{captures[0]}, black stones captured:{captures[1]}")
    if(captures[0] >= 10):
        winner = 2
    if(captures[1] >= 10):
        winner = 1

def do_ai(last_move: tuple[int, int], before_last_move: tuple[int, int], board: list[list[int]], captures: tuple[int, int], turn: int = turn, num_moves: int = num_moves)->tuple[int, int]:
    start_time=time.time()
    move = AIs[ai_type](last_move, before_last_move, board, captures, turn, num_moves)
    end_time=time.time()
    print(f"took {end_time-start_time}s to move")
    return move

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
