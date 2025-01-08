from constants import *

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def check_empty(self):
        for row in self.grid:
            for cell in row:
                if cell != None:
                    return False

    def print_grid(self):
        for row in self.grid:
            print(row)
