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
                self.cells[row][column].button.bind('<Button-1>', pushCell(self, row, column))
                self.cells[row][column].button.bind('<Button-3>', rightClick(self, row, column))
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
            
def setBoard(self):
    """Sets the values of the cells with a mine nearby"""
    for row in range(self.rows):
        for column in range(self.columns):
            if self.cells[row][column].value == 9:
                if row - 1 in range(self.rows) and column - 1 in range(self.columns):
                    self.cells[row - 1][column - 1].value += 1
                if row - 1 in range(self.rows):
                    self.cells[row - 1][column].value += 1
                if row - 1 in range(self.rows) and column + 1 in range(self.columns):
                    self.cells[row - 1][column + 1].value += 1
                if column - 1 in range(self.columns):
                    self.cells[row][column - 1].value += 1
                if column + 1 in range(self.columns):
                    self.cells[row][column + 1].value += 1
                if row + 1 in range(self.rows) and column - 1 in range(self.columns):
                    self.cells[row + 1][column - 1].value += 1
                if row + 1 in range(self.rows):
                    self.cells[row + 1][column].value += 1
                if row + 1 in range(self.rows) and column + 1 in range(self.columns):
                    self.cells[row + 1][column + 1].value += 1
    return self

def pushCell(self, row, column):
    if row in range(self.rows) and column in range(self.columns):
        self.cells[row][column].button = tkinter.Label(window, text=str(self.cells[row][column].value))
        if self.cells[row][column].value == 9:
            youLose()
        else:
            if self.cells[row][column].value == 0:
                if row - 1 in range(self.rows) and column - 1 in range(self.columns):
                    pushCell(self, row - 1, column - 1)
                if row - 1 in range(self.rows):
                    pushCell(self, row - 1, column)
                if row - 1 in range(self.rows) and column + 1 in range(self.columns):
                    pushCell(self, row - 1, column + 1)
                if column - 1 in range(self.columns):
                    pushCell(self, row, column - 1)
                if column + 1 in range(self.columns):
                    pushCell(self, row, column + 1)
                if row + 1 in range(self.rows) and column - 1 in range(self.columns):
                    pushCell(self, row + 1, column - 1)
                if row + 1 in range(self.rows):
                    pushCell(self, row + 1, column)
                if row + 1 in range(self.rows) and column + 1 in range(self.columns):
                    pushCell(self, row + 1, column + 1)
            
def rightClick(self, row, column):
    self[row][column].button = tkinter.Button(window,fg='red')
    self[row][column].button.bind('<Button-1>')
    #self[row][column].button.bind('<Button-3>', )
def youLose():
    pass
def youWin(self):
    pass
if __name__ == "__main__":
    
    window = tkinter.Tk()
    Board = setBoard(Board_t(14, 18, 40))
    
    #button11 = tkinter.Label(window, text="1")
    window.mainloop()
    