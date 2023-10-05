
import tkinter
from tkinter import messagebox
from random import randint

class Cell_t:
    def __init__(self, row, column):
        self.value = 0
        self.visible = False
        self.row = row
        self.column = column
        self.button = tkinter.Button(window, height= 1, width=1)
        self.button.grid(row = row, column = column)
        self.label = None
 
class Board_t:
    def __init__(self, rows, columns, mines):
        """Initializes an empty board and sets the mines"""
        if mines >= rows * columns:
            return
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.cells = []
        for row in range(rows):
            self.cells.append([])
            for column in range(columns):
                self.cells[row].append(Cell_t(row, column))
                self.cells[row][column].button.bind('<Button-1>', lambda event, row = row, column = column: self.pushCell(row, column))
                self.cells[row][column].button.bind('<Button-3>', lambda event, row = row, column = column: self.rightClick(row, column))
        #Set mines
        for mine in range(mines):
            row = randint(0, rows -1)
            column = randint(0, columns - 1)
            while self.cells[row][column].value == 9:
                row = randint(0, rows -1)
                column = randint(0, columns - 1)
            self.cells[row][column].value = 9
            
    def setBoard(self):
        """Sets the values of the cells with a mine nearby"""
        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].value >= 9:
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
        """Reveals the cell and neighbour cells"""
        #Return early if the cell is already visible
        if self.cells[row][column].visible:
            return
        #Return early if stepped on a mine
        if self.cells[row][column].value >= 9:
            self.youLose()
            return
        self.cells[row][column].visible = True
        #Return early if player won
        if self.youWin():
            self.showAllCells()
            tkinter.messagebox.showinfo("Game over","You Win!!!")
            return
        #Turn the button into a label
        self.cells[row][column].button.destroy()
        self.cells[row][column].button = None
        self.cells[row][column].label = tkinter.Label(window, text=str(self.cells[row][column].value))
        self.cells[row][column].label.grid(row = row, column = column)
        #Trigger neighbour cells
        if self.cells[row][column].value == 0:
            if row - 1 in range(self.rows) and column - 1 in range(self.columns):
                self.pushCell(row - 1, column - 1)
            if row - 1 in range(self.rows):
                self.pushCell(row - 1, column)
            if row - 1 in range(self.rows) and column + 1 in range(self.columns):
                self.pushCell(row - 1, column + 1)
            if column - 1 in range(self.columns):
                self.pushCell(row, column - 1)
            if column + 1 in range(self.columns):
                self.pushCell(row, column + 1)
            if row + 1 in range(self.rows) and column - 1 in range(self.columns):
                self.pushCell(row + 1, column - 1)
            if row + 1 in range(self.rows):
                self.pushCell(row + 1, column)
            if row + 1 in range(self.rows) and column + 1 in range(self.columns):
                self.pushCell(row + 1, column + 1)
                
    def rightClick(self, row, column):
        self.cells[row][column].button.configure(bg="red")
        self.cells[row][column].button.unbind('<Button-1>')
        self.cells[row][column].button.bind('<Button-3>', lambda event, row = row, column = column: self.secondRightClick(row, column))
    
    def secondRightClick(self, row, column):
        self.cells[row][column].button.bind('<Button-1>', lambda event, row = row, column = column: self.pushCell(row, column))
        self.cells[row][column].button.bind('<Button-3>', lambda event, row = row, column = column: self.rightClick(row, column))
        self.cells[row][column].button.configure(bg="SystemButtonFace")

    def showAllCells(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].button == None:
                    continue
                self.cells[row][column].button.destroy()
                self.cells[row][column].button = None
                self.cells[row][column].label = tkinter.Label(window, text=str(self.cells[row][column].value))
                self.cells[row][column].label.grid(row = row, column = column)

    def youLose(self):
        self.showAllCells()
        messagebox.showinfo("Game over","You lost!!!")
        
    def youWin(self):
        notVisible = 0
        for row in range(self.rows):
            for column in range(self.columns):
                if not self.cells[row][column].visible:
                    notVisible += 1
        print(notVisible)
        if notVisible == self.mines:
            return True
        else:
            return False

if __name__ == "__main__":
    window = tkinter.Tk()
    Board = Board_t(14, 18, 40)
    Board.setBoard()
    #button11 = tkinter.Label(window, text="1")
    window.mainloop()
    