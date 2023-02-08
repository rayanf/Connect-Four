import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# MinMax class that contains the MinMax algorithm and the evaluation function
class MinMax:
    def __init__(self,peace,peaceEnemy,mode='MinMax'):
        self.alpha = np.NINF
        self.beta = np.Inf
        self.Peace = peace
        self.PeaceEnemy = peaceEnemy
        self.mode = mode
        
    # function that start the algorithm
    def move(self,state):
        ch = self.minMax(state,4,self.alpha,self.beta,self.Peace)[0]
        return ch

    # main recursive function that implements the MinMax algorithm
    def minMax(self,state,depth,alpha,beta,turn):
        # check if the game is over or the depth is 0
        if depth == 0 or self.checkTerminal(state):
            if self.checkTerminal(state):
                if self.checkWin(state):
                    return (None,np.Inf)
                elif self.checkLose(state):
                    return (None,np.NINF)
                else:
                    return (None,0)
            else:
                if self.mode != 'MinMax':
                    return (None,self.stateScoreEvalGenetic(state))

                return (None,self.stateScoreEval(state))
        # if its the max player
        if turn == self.Peace:
            value = np.NINF
            column = np.random.choice(self.getChoices(state))
            # check all the possible moves
            for col in self.getChoices(state):
                row = self.getEmptyRow(state,col)
                b_copy = state.copy()
                self.dropPeace(b_copy,row,col,self.Peace)
                newScore = self.minMax(b_copy,depth-1,alpha,beta,self.PeaceEnemy)[1]
                if newScore > value:
                    value = newScore
                    column = col
                alpha = max(alpha,value)
                # alpha beta pruning
                if alpha >= beta:
                    break
            return column,value

        # if its the min player
        else:
            value = np.Inf
            column = np.random.choice(self.getChoices(state))
            # check all the possible moves
            for col in self.getChoices(state):
                row = self.getEmptyRow(state,col)
                b_copy = state.copy()
                self.dropPeace(b_copy,row,col,self.PeaceEnemy)
                newScore = self.minMax(b_copy,depth-1,alpha,beta,self.Peace)[1]
                if newScore < value:
                    value = newScore
                    column = col
                beta = min(beta,value)
                # alpha beta pruning
                if alpha >= beta:
                    break
            return column,value
    # get sequence's score if we called minimax with genetic algorithm
    def getScoreGenetic(self,sequence):
        score = 0
        sequence = list(sequence)
        if sequence.count(self.Peace) == 4:
            score += np.inf
        elif sequence.count(self.PeaceEnemy) == 4:
            score -= np.inf
        elif sequence.count(self.Peace) == 3 and (sequence[0] == 0 or sequence[-1] == 0):
            score += self.mode[1]
        elif sequence.count(self.PeaceEnemy) == 3 and (sequence[0] == 0 or sequence[-1] == 0):
            score -= self.mode[1]
        elif sequence.count(self.Peace) == 3 and sequence.count(0) == 1:
            self.mode[0]
        elif sequence.count(self.PeaceEnemy) == 3 and sequence.count(0) == 1:
            self.mode[0]
        elif sequence.count(self.Peace) == 2 and sequence.count(0) == 2:
            if sequence[0] == sequence[-1] == 0:
                score += self.mode[2]
            else:
                score += self.mode[3]
        elif sequence.count(self.PeaceEnemy) == 2 and sequence.count(0) == 2:
            if sequence[0] == sequence[-1] == 0:
                score -= self.mode[2]
            else:
                score -= self.mode[3]
        elif sequence.count(self.Peace) == 2 and sequence.count(0) == 1:
            if sequence[0] == self.PeaceEnemy or sequence[-1] == self.PeaceEnemy:
                score += self.mode[4]

        elif sequence.count(self.PeaceEnemy) == 2 and sequence.count(0) == 1:
            if sequence[0] == self.Peace or sequence[-1] == self.Peace:
                score -= self.mode[4]
        return score
    
    # get score of the state if we called minimax with genetic algorithm
    def stateScoreEvalGenetic(self,state):
        score = 0
        # horizontal
        for i in range(len(state)):
            for j in range(len(state[0]-3)):
                sequence = state[i][j:j+4]
                score += self.getScoreGenetic(sequence)
        # vertical
        for i in range(len(state)-3):
            for j in range(len(state[0])):
                sequence = state[i:i+4,j]
                score += self.getScoreGenetic(sequence)
        # diagonal 
        for i in range(len(state)-3):
            for j in range(len(state[0])-3):
                sequence = [state[i+k][j+k] for k in range(4)]
                score += self.getScoreGenetic(sequence)
        for i in range(len(state)-3):
            for j in range(len(state[0])-3):
                sequence = [state[i+3-k][j+k] for k in range(4)]
                score += self.getScoreGenetic(sequence)


        # check if there is 7 shape in the board
        for i in range(len(state)-3):
            for j in range(len(state[0])-3):
                if state[i][j:j+3].all() == self.Peace:
                    if state[i+1][j+1] == self.Peace:
                        if state[i+2][j] == self.Peace or state[i+2][j+2] == self.Peace:
                            score += self.mode[5]
                elif state[i][j:j+3].all() == self.PeaceEnemy:
                    if state[i+1][j+1] == self.PeaceEnemy:
                        if state[i+2][j] == self.PeaceEnemy or state[i+2][j+2] == self.PeaceEnemy:
                            score -= self.mode[5]
           
        # calculate dictance from center
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == self.Peace:
                    score += abs(j - (len(state[0])-1)/2) * self.mode[6]
                elif state[i][j] == self.PeaceEnemy:
                    score -= abs(j - (len(state[0])-1)/2) * self.mode[6]
        
        return score
    # get state score if we called minimax with the main function and not genetic algorithm
    def stateScoreEval(self,state):
        score = 0

        for i in range(len(state)):
            for j in range(len(state[0]-3)):
                sequence = state[i][j:j+4]
                score += self.getScore(sequence)

        for i in range(len(state)-3):
            for j in range(len(state[0])):
                sequence = state[i:i+4,j]
                score += self.getScore(sequence)

        for i in range(len(state)-3):
            for j in range(len(state[0])-3):
                sequence = [state[i+k][j+k] for k in range(4)]
                score += self.getScore(sequence)
        
        for i in range(len(state)-3):
            for j in range(len(state[0])-3):
                sequence = [state[i+3-k][j+k] for k in range(4)]
                score += self.getScore(sequence)

        return score
    # get sequence's score if we called minimax with the main function and not genetic algorithm
    def getScore(self,sequence):
        score = 0
        unique, counts = np.unique(sequence, return_counts=True)
        counting = dict(zip(unique, counts))
        try:
            counting[0] = counting[0]
        except:
            counting[0] = 0
        try:
            counting[self.Peace] = counting[self.Peace]
        except:
            counting[self.Peace] = 0
        try:
            counting[self.PeaceEnemy] = counting[self.PeaceEnemy]
        except:
            counting[self.PeaceEnemy] = 0

        if counting[self.Peace] == 4:
            score += np.Inf

        elif counting[self.Peace] == 3 and counting[0] == 1:
            score += 10

        elif counting[self.Peace] == 2 and counting[0] == 2:
            score += 3

        if counting[self.PeaceEnemy] == 3 and counting[0] == 1:
            score -= 10

        return score

    # get lowest row that is empty for drop peace
    def getEmptyRow(self,state,col):
        for i in range(len(state)-1,-1,-1):
            if state[i][col] == 0:
                return i

    # drop peace in the column
    def dropPeace(self,state,row,col,peace):
        state[row][col] = peace

    # get all drop's possible choices for the current state
    def getChoices(self,state):
        choices = []
        for i in range(len(state[0])):
            if state[0][i] == 0:
                choices.append((i))
        return choices

    # check if the state is terminal or not. to check if there is a winner or tie
    def checkTerminal(self,state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] != 0:
                    if j < len(state[0])-3:
                        if state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3]:
                            return True
                    if i < len(state)-3:
                        if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j]:
                            return True
                    if i < len(state)-3 and j < len(state[0])-3:
                        if state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                            return True
                    if i < len(state)-3 and j > 2:
                        if state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                            return True
    
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    return False
        return True

    # check if player if winner or not
    def checkWin(self,state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] != 0:
                    if j < len(state[0])-3:
                        if state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3]==self.Peace:
                            return True
                    if i < len(state)-3:
                        if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j]==self.Peace:
                            return True
                    if i < len(state)-3 and j < len(state[0])-3:
                        if state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]==self.Peace:
                            return True
                    if i < len(state)-3 and j > 2:
                        if state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]==self.Peace:
                            return True
        return False

    # check if player if loser or not
    def checkLose(self,state):
         for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] != 0:
                    if j < len(state[0])-3:
                        if state[i][j] == state[i][j+1] == state[i][j+2] == state[i][j+3]==self.PeaceEnemy:
                            return True
                    if i < len(state)-3:
                        if state[i][j] == state[i+1][j] == state[i+2][j] == state[i+3][j]==self.PeaceEnemy:
                            return True
                    if i < len(state)-3 and j < len(state[0])-3:
                        if state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]==self.PeaceEnemy:
                            return True
                    if i < len(state)-3 and j > 2:
                        if state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]==self.PeaceEnemy:
                            return True

    # check if tie or not
    def checkDraw(self,state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if self.board[i][j] == 0:
                    return False
        return True



    


    