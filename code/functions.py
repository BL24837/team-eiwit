from constants import *

class Board:
    def __init__(self):
        self.grid = []

    def check_empty(self):
        if self.squares == 0:
            return True
        else:
            return False

    def print_grid(self):
        rows = WIDTH
        cols = HEIGHT
        for i in range(rows):
            row = [0] * WIDTH
            self.grid.append(row)
        for row in grid:
            print(row)
