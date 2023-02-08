import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from game import game


# main function that runs the game and gets the board size and game mode
def main():
    mode = int(input("Choose mode -> 1.Player vs Player    2.Player vs AI    3.AI vs AI: "))
    n,m = input("Enter board size: ").split()
    n = int(n)
    m = int(m)
    if mode == 1:
        g = game(n,m)
        g.playerVsPlayer()

    elif mode == 2:
        g = game(n,m)
        g.playerVsAI('MinMax')
    
    elif mode == 3:
        g = game(n,m)
        g.AIvsAI('MinMax','MinMax')



if __name__ == "__main__":
    main()