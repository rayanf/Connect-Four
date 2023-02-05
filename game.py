import numpy as np
import pygame
import math
import sys
from MinMax import MinMax
# 4 connected game
class game:
    def __init__(self, n, m):
        self.board = np.zeros((n,m))
        self.n = n
        self.m = m

        pygame.init()
        self.screen = pygame.display.set_mode((m*90,n*90))
        self.fps = 60
        self.clock = pygame.time.Clock()



    def drop(self,col,myTurn):
        if myTurn:
            piece = 1
        else:
            piece = 2

        for i in range(self.n-1,-1,-1):
            if self.board[i][col] == 0:
                self.board[i][col] = piece
                break 

    def updateScreen(self):
        self.screen = pygame.display.set_mode((self.m*90,self.n*90))
        self.screen.fill((112, 146, 190))
        self.drawPieces()
        self.drawLines()

        pygame.display.update()
        pygame.image.save(self.screen, "screenshot.jpeg")

    def drawPieces(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == 1:
                    pygame.draw.circle(self.screen, (100,160,60), (j*90+45, i*90+45), 40)
                elif self.board[i][j] == 2:
                    pygame.draw.circle(self.screen, (161,35,96), (j*90+45, i*90+45), 40)

    def drawLines(self):
        for i in range(self.n):
            pygame.draw.line(self.screen, (0,0,0), (0, i*90), (self.m*90, i*90), 3)
        for i in range(self.m):
            pygame.draw.line(self.screen, (0,0,0), (i*90, 0), (i*90, self.n*90), 3)



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

    def checkTie(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def reset(self):
        self.board = np.zeros((self.n,self.m))
        self.updateScreen()
    
    def playerVsAI(self,mode):
        self.reset()
        if mode == 'MinMax':
            AI = MinMax(1,2)

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
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        posx = event.pos[0]
                        col = int(math.floor(posx/90))

                        self.drop(col,turn)
                        turn = not turn
            else:
                col = AI.move(self.board)
                self.drop(col,turn)
                turn = not turn

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
    def AIvsAI(self,mode1,mode2):
        self.reset()
        if mode1 == 'MinMax':
            AI1 = MinMax(1,2)
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

if __name__ == "__main__":
    g = game(6,7)
    g.playerVsAI()
    # g.AIvsAI()