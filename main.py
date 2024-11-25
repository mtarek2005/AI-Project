# import the pygame module, so you can use it
# install with `pip install pygame`
import math
import pygame

w=800
h=800

#positions: 0 empty, 1 white, 2 black
board=[[0]*19 for i in range(19)]
turn=0

# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("OS Project")
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((w,h))
     
    # fill background
    screen.fill((161,102,47))
    
    # load font, prepare values
    font = pygame.font.Font(None, 16)

    # display stuff
    pygame.display.flip()

    draw(screen,w,h)
    turn=1

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
                u=min(w,h)/(19)
                loc=pygame.mouse.get_pos()
                int_loc=(int(loc[0]//u),int(loc[1]//u))
                print(loc)
                print(int_loc)
                if(board[int_loc[0]][int_loc[1]]==0):
                    board[int_loc[0]][int_loc[1]]=turn
                    turn=(1 if turn==2 else 2)
                    do_move(int_loc)
                draw(screen,w,h)

def draw(screen:pygame.Surface,w:int,h:int,lw:int=3,bgC:pygame.Color=(161,102,47),lnC:pygame.Color=(10,20,10),wpC:pygame.Color=(220,220,220),bpC:pygame.Color=(40,40,40)):
    u=min(w,h)/(19)
    # fill background
    screen.fill(bgC)
    for i in range(19):
        pygame.draw.line(screen,lnC,(u/2,(i+0.5)*u),(w-u/2,(i+0.5)*u),lw)
        pygame.draw.line(screen,lnC,((i+0.5)*u,u/2),((i+0.5)*u,h-u/2),lw)
    pygame.draw.circle(screen,lnC,(w/2,h/2),u*0.3,lw)

    pygame.draw.circle(screen,lnC,(u*6.5,u*6.5),u*0.3,lw)
    pygame.draw.circle(screen,lnC,(u*12.5,u*12.5),u*0.3,lw)
    pygame.draw.circle(screen,lnC,(u*6.5,u*12.5),u*0.3,lw)
    pygame.draw.circle(screen,lnC,(u*12.5,u*6.5),u*0.3,lw)

    for row in range(19):
        for col in range(19):
            if board[row][col]==1:
                pygame.draw.circle(screen,wpC,(u*(row+0.5),u*(col+0.5)),u*0.4)
            if board[row][col]==2:
                pygame.draw.circle(screen,bpC,(u*(row+0.5),u*(col+0.5)),u*0.4)
    # display stuff
    pygame.display.flip()

def inv_col(color:int):
    return 0 if color==0 else (1 if color==2 else 2)

def do_move(loc:tuple[int,int]):
    row=loc[0]
    col=loc[1]
    pass

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()