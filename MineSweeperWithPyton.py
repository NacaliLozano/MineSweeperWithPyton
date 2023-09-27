import tkinter
from random import randint

class Cell_t:
    def __init__(self, row, column):
        self.value = 0
        self.visible = False
        self.row = row
        self.column = column
        self.button = tkinter.Button(window)
        self.button.grid(row = row, column = column)
 
class Board_t:
    def __init__(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.cells = []
        for row in range(rows):
            self.cells.append([])
            for column in range(columns):
                self.cells[row].append(Cell_t(row, column))
        #Set mines
        for mine in range(mines):
            row = randint(0, rows -1)
            column = randint(0, columns - 1)
            while self.cells[row][column].value == 9:
                row = randint(0, rows -1)
                column = randint(0, columns - 1)
            self.cells[row][column].value = 9
    def __len__(self):
        return len(self.cells)
            
def setBoard(Board):
    """Sets the values of the cells with a mine nearby"""
    for row in range(Board.rows):
        for column in range(Board.columns):
            if Board.cells[row][column].value == 9:
                if row - 1 in range(Board.rows) and column - 1 in range(Board.columns):
                    Board.cells[row - 1][column - 1].value += 1
                if row - 1 in range(Board.rows):
                    Board.cells[row - 1][column].value += 1
                if row - 1 in range(Board.rows) and column + 1 in range(Board.columns):
                    Board.cells[row - 1][column + 1].value += 1
                if column - 1 in range(Board.columns):
                    Board.cells[row][column - 1].value += 1
                if column + 1 in range(Board.columns):
                    Board.cells[row][column + 1].value += 1
                if row + 1 in range(Board.rows) and column - 1 in range(Board.columns):
                    Board.cells[row + 1][column - 1].value += 1
                if row + 1 in range(Board.rows):
                    Board.cells[row + 1][column].value += 1
                if row + 1 in range(Board.rows) and column + 1 in range(Board.columns):
                    Board.cells[row + 1][column + 1].value += 1
    return Board
def pushCell(self):
    pass
def youLose():
    pass
def youWin(self):
    pass
if __name__ == "__main__":
    
    window = tkinter.Tk()
    Board = setBoard(Board_t(14, 18, 40))
    
    #button11 = tkinter.Label(window, text="1")
    window.mainloop()
    