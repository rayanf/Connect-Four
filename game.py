import numpy as np
import pygame
import math
import sys
from MinMax import MinMax


# main class for the game that contains the board and the game logic
class game:
    def __init__(self, n, m,mode='MinMax'):
        self.board = np.zeros((n,m))
        self.n = n
        self.m = m
        self.mode = mode


        pygame.init()
        self.screen = pygame.display.set_mode((m*90,n*90))
        self.fps = 60
        self.clock = pygame.time.Clock()


    # function that players should call to drop a piece in a column
    def drop(self,col,myTurn):
        if myTurn:
            piece = 1
        else:
            piece = 2

        for i in range(self.n-1,-1,-1):
            if self.board[i][col] == 0:
                self.board[i][col] = piece
                break 
    
    # update the screen after each move
    def updateScreen(self):
        self.screen = pygame.display.set_mode((self.m*90,self.n*90))
        self.screen.fill((112, 146, 190))
        self.drawPieces()
        self.drawLines()

        pygame.display.update()
        # pygame.image.save(self.screen, "screenshot.jpeg")

    # draw the pieces on the board
    def drawPieces(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == 1:
                    pygame.draw.circle(self.screen, (100,160,60), (j*90+45, i*90+45), 40)
                elif self.board[i][j] == 2:
                    pygame.draw.circle(self.screen, (161,35,96), (j*90+45, i*90+45), 40)

    # draw the lines on the board
    def drawLines(self):
        for i in range(self.n):
            pygame.draw.line(self.screen, (0,0,0), (0, i*90), (self.m*90, i*90), 3)
        for i in range(self.m):
            pygame.draw.line(self.screen, (0,0,0), (i*90, 0), (i*90, self.n*90), 3)


    # check if there is a winner
    # check vertically, horizontally and diagonally
    def checkWin(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] != 0:
                    if j < self.m-3:
                        if self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3]:
                            return True
                    if i < self.n-3:
                        if self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j]:
                            return True
                    if i < self.n-3 and j < self.m-3:
                        if self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3]:
                            return True
                    if i < self.n-3 and j > 2:
                        if self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == self.board[i+3][j-3]:
                            return True

    # check if no more empty spaces on the board and it's a tie
    def checkTie(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == 0:
                    return False
        return True
    
    # reset the board to empty
    def reset(self):
        self.board = np.zeros((self.n,self.m))
        if self.mode == 'MinMax':
            self.updateScreen()
    
    # play the game in player vs AI mode
    def playerVsAI(self,mode,modeGame = 'MinMax'):
        if modeGame == 'MinMax':
            self.reset()
            if mode == 'MinMax':
                AI = MinMax(1,2)

            turn = True
            # main loop of the game
            while True:
                self.updateScreen()

                # check if there is a winner or a tie
                win = self.checkWin()
                tie = self.checkTie()
                if win:
                    if turn:
                        print("lose")
                    else:
                        print("win")
                    pygame.quit()
                    sys.exit()
                elif tie:
                    print("tie")
                    pygame.quit()
                    sys.exit()
                # get the mouse position and drop a piece in the corresponding column if it's the player's turn
                if turn:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            posx = event.pos[0]
                            col = int(math.floor(posx/90))

                            self.drop(col,turn)
                            turn = not turn
                # get the best move from the AI and drop a piece in the corresponding column
                else:
                    col = AI.move(self.board)
                    self.drop(col,turn)
                    turn = not turn

    # play the game in player vs player mode
    def playerVsPlayer(self):
        self.reset()
        turn = True
        while True:
            self.updateScreen()


            win = self.checkWin()
            tie = self.checkTie()
            if win:
                if turn:
                    print("lose")
                else:
                    print("win")

                pygame.quit()
                sys.exit()
            elif tie:
                print("tie")
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx/90))



                    self.drop(col,turn)
                    turn = not turn

    # play the game in AI vs AI mode
    def AIvsAI(self,mode1,mode2,mode='MinMax'):
        # if its the minMax mode 
        if mode == 'MinMax':
            self.reset()
            if mode1 == 'MinMax':
                AI1 = MinMax(1,2,)
            if mode2 == 'MinMax':
                AI2 = MinMax(2,1)

            turn = True
            while True:
                self.updateScreen()


                win = self.checkWin()
                tie = self.checkTie()

                if win:
                    if turn:
                        print("lose")
                    else:
                        print("win")
                    pygame.quit()
                    sys.exit()
                elif tie:
                    print("tie")
                    pygame.quit()
                    sys.exit()

                if turn:
                    col = AI1.move(self.board)
                    self.drop(col,turn)
                    turn = not turn

                else:
                    col = AI2.move(self.board)
                    self.drop(col,turn)
                    turn = not turn
        # else if the genetic algorithm called the function
        else:
            self.reset()
            AI1 = MinMax(1,2,mode1)
            AI2 = MinMax(2,1,mode2)

            turn = True
            while True:

                win = self.checkWin()
                tie = self.checkTie()

                if win:
                    if turn:
                        return 2
                    else:
                        return 1
                elif tie:
                    return 3


                if turn:
                    col = AI1.move(self.board)
                    self.drop(col,turn)
                    turn = not turn

                else:
                    col = AI2.move(self.board)
                    self.drop(col,turn)
                    turn = not turn

if __name__ == "__main__":
    g = game(6,7)
    g.playerVsAI()
    # g.AIvsAI()