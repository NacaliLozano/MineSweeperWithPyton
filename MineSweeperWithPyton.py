import tkinter
from random import randint

class Cell_t:
    def __init__(self):
        self.value = 0
        self.visible = False
 
class Board_t:
    def __init__(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.board = []
        for row in range(rows):
            self.board.append([])
            for column in range(columns):
                self.board[row].append(Cell_t())
        #Set mines
        for mine in range(mines):
            row = randint(0, rows -1)
            column = randint(0, columns - 1)
            while self.board[row][column].value == 9:
                row = randint(0, rows -1)
                column = randint(0, columns - 1)
            self.board[row][column].value = 9
    def __len__(self):
        return len(self.board)
            
def setBoard():
    Board = Board_t(14, 18, 40)
    for row in range(Board.rows):
        for column in range(Board.columns):
            if Board.board[row][column].value == 9:
                if row - 1 in range(Board.rows) and column -1 in range(Board.columns):
                    Board.board[row - 1][column - 1].value += 1
def pushCell(self):
    pass
def youLose():
    pass
def youWin(self):
    pass
if __name__ == "__main__":
    setBoard()
    window = tkinter.Tk()
    
    
    button00 = tkinter.Button(window)
    button01 = tkinter.Button(window)
    button10 = tkinter.Button(window)
    button11 = tkinter.Label(window, text="1")
    
    button00.grid(row = 0, column = 0)
    button01.grid(row = 0, column = 1)
    button10.grid(row = 1, column = 0)
    button11.grid(row = 1, column = 1)
    
    window.mainloop()
    