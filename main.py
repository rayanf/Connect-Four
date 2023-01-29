import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from game import game

def main():
    mode = int(input("Choose mode -> 1.Player vs Player    2.Player vs AI    3.AI vs AI: "))
    # n,m = input("Enter board size: ").split()
    # n = int(n)
    # m = int(m)
    if mode == 1:
        g = game(6,7)
        g.playerVsPlayer()

    elif mode == 2:
        g = game(6,7)
        g.playerVsAI()
    
    elif mode == 3:
        g = game(6,7)
        g.AIvsAI()



if __name__ == "__main__":
    main()