from constants import *

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    def check_empty(self):
        for row in self.grid:
            for cell in row:
                if cell != 0:
                    return False

    def print_grid(self):
        for row in self.grid:
            print(row)
