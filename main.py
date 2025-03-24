import sys
import pygame
import numpy as np

pygame.init()

# Colours
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)

#Sizes

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE= WIDTH//BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE//3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen= pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK)

board= np.zeros((BOARD_ROWS,BOARD_COLS))


def draw_lines(colour):
    for i in range(1,BOARD_ROWS):
        pygame.draw.line(screen,colour,(0,SQUARE_SIZE*i),(WIDTH,SQUARE_SIZE*i), LINE_WIDTH )
        pygame.draw.line(screen,colour,(SQUARE_SIZE*i,0), (SQUARE_SIZE*i,HEIGHT), LINE_WIDTH )
    
def draw_figures(colour):
    for row in range (BOARD_ROWS):
        for col in range (BOARD_COLS):
            if board[row][col]==1:
                pygame.draw.circle(screen,colour, (col*SQUARE_SIZE+ SQUARE_SIZE//2,row*SQUARE_SIZE + SQUARE_SIZE//2) ,CIRCLE_RADIUS,CIRCLE_WIDTH)
            elif board[row][col]==2:
                pygame.draw.line(screen,colour,
                                (col*SQUARE_SIZE + SQUARE_SIZE//4,row*SQUARE_SIZE +SQUARE_SIZE//4),( (col+1)*SQUARE_SIZE-SQUARE_SIZE//4,(row+1)*SQUARE_SIZE- SQUARE_SIZE//4 ),
                                ((col+1)*SQUARE_SIZE - SQUARE_SIZE//4,row*SQUARE_SIZE +SQUARE_SIZE//4),( col*SQUARE_SIZE+SQUARE_SIZE//4,(row+1)*SQUARE_SIZE- SQUARE_SIZE//4 )                                             
                                )


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col]==0:
                return False
    return True

def check_win(player,check_board):
    for col in range (BOARD_COLS):
        if check_board[0][col]==player and check_board[1][col]==player and check_board[2][col]==player:
            return True
    for row in range (BOARD_ROWS):  
        if check_board[row][0]==player and check_board[row][1]==player and check_board[row][2]==player:
            return True
    if check_board[0][0]==player and check_board[1][1]==player and check_board[2][2]==player:
        return True
    if check_board[0][2]==player and check_board[1][1]==player and check_board[2][0]==player:
        return True
    
    return False


def minimax(minimax_board,is_maximizing):
    if check_win(2,minimax_board):
        return float('inf')
    
    elif check_win(1,minimax_board):
        return float('-inf')
    elif is_board_full():
        return 0
    
    if is_maximizing:
        best_score= float('-inf')

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col]==0:
                    minimax_board[row][col]=2
                    score=minimax(minimax_board,False)
                    minimax_board[row][col]=0
                    best_score=max(score,best_score)
        return best_score

    else:
        best_score=float('inf')

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col]==0:
                    minimax_board[row][col]=1
                    score=minimax(minimax_board,True)
                    minimax_board[row][col]=0
                    best_score=min(score,best_score)
        return best_score
    

def best_move():
    best_score=float('-inf')
    move=(-1,-1)

    for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col]==0:
                    board[row][col]=2
                    score=minimax(board,False)
                    if score>best_score:
                        best_score=score
                        move=(row,col)
                    board[row][col]=0
    if move!=(-1,-1):
        board[move[0]][move[1]]=2
        return True
    return False


def restart():
    screen.fill(BLACK)
    draw_lines(WHITE)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col]=0


draw_lines(WHITE)


game_over=False


while(True):
    
    for event in pygame.event.get():

        if event.type== pygame.QUIT:
            sys.exit()

        if event.type== pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX=event.pos[0] // SQUARE_SIZE
            mouseY=event.pos[1] // SQUARE_SIZE

            if(board[mouseX][mouseY]==0):
                board[mouseX][mouseY]=1

                if check_win(1,board):
                    game_over=True
                # else:
                #     player=player%2 +1
                
                if not game_over:

                   if best_move():
                       if check_win(2,board) :
                           game_over=True
                
                if(is_board_full()):
                    game_over=True  
        
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_r:
                restart()
                game_over=False    

    if not game_over:
        draw_figures(WHITE)
    
    if game_over:
        if check_win(1,board):
            draw_lines(GREEN)
            draw_figures(GREEN)
        elif check_win(2,board):
            draw_lines(RED)
            draw_figures(RED)
        else:
            draw_lines(GREY)    
            draw_figures(GREY)
    
    pygame.display.update()