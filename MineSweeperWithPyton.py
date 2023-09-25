import tkinter
from random import randint

class Cell_t:
    def __init__(self):
        value = 0
        visible = False
 
class Board_t:
    def __init__(self, rows, columns, mines):
        self = []
        for row in range(rows):
            self.append
            for column in range(columns):
                self[row][column] = Cell_t()
        #Set mines
        for mine in range(mines):
            row = randint() % rows
            column = randint() % columns
            while self[row][column].value == 9:
                row = randint() % rows
                column = randint() % columns
            self[row][column].value = 9
            
def setBoard():
    Board = Board_t(14, 18, 40)
    print(Board)
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
    