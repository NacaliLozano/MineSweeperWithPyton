import tkinter

class Cell_t:
    def __init__(self):
        value = 0
        visible = False
 
class Board_t:
    def __init__(self, rows, columns, mines):
        for row in rows:
            for column in columns:
                self[row][column] = Cell_t()
            
def SetBoard(self):
    pass
def pushCell(self):
    pass
def youLose():
    pass
def youWin(self):
    pass
if __name__ == "__main__":
    window = tkinter.Tk()
    
    
    button00 = tkinter.Button(window)
    button01 = tkinter.Button(window)
    button10 = tkinter.Button(window)
    button11 = tkinter.Button(window)
    
    button00.grid(row = 0, column = 0)
    button01.grid(row = 0, column = 1)
    button10.grid(row = 1, column = 0)
    button11.grid(row = 1, column = 1)
    
    window.mainloop()