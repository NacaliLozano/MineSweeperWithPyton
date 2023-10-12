
import tkinter
from tkinter import messagebox
from random import randint
import time
import pickle

class Cell:
    def __init__(self):
        """Creates a Cell"""
        self.value = 0
        self.isFlipped = False
        return self
    
    def setValue(self, value):
        """Sets the value of a Cell"""
        try:
            self.value = value
            return True
        except:
            return False
        
    def getValue(self):
        return self.value
    
    def setFlipped(self):
        """Sets a Cell to flipped state"""
        try:
            self.isFlipped = True
            return True
        except:
            return False
    
    def isFlipped(self):
        return self.isFlipped
    
    
class Board:
    def __init__(self, rows, columns, mines):
        """Initializes an empty board and sets the mines"""
        if mines >= rows * columns:
            return
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.remainingCoveredCells = rows * columns
        self.cells = []
        for row in range(rows):
            self.cells.append([])
            for column in range(columns):
                self.cells[row].append(Cell(row, column))
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
        return self
            
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
        self.remainingCoveredCells -= 1
        if self.remainingCoveredCells == self.mines:
            self.youWin()
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
        self.showAllCells()
        tkinter.messagebox.showinfo("Game over","You Win!!!")
        
class Player:
    def __init__(self, name):
        self.name = name
        self.fileName = self.name + ".msg" #MineSweeper Game
        self.record = None
        
    def getName(self):
        return self.name
    
    def getRecord(self):
        return self.record
    
    def getFileName(self):
        return self.fileName

class Game:
    def __init_(self, name):
        self.player = Player(name)
        self.board = Board(14, 18, 40)
        self.board.setBoard()
        self.startTimer = time.time()
    
    def save(self):
        game = {"Board": self.board, "Time": self.getTime()}
        try:
            with open(self.player.getFileName(), "w") as f:
                f.pickle.dump(game)
            return True
        except:
            return False
    
    def load(self):
        try:
            with open(self.player.getFileName(), "r") as f:
                game = pickle.load(f)
                self.board = game["Board"]
                self.startTimer = time.time() - game["Time"]
            return True
        except:
            return False
    
    def getPlayer(self):
        return self.player
    
    def getTime(self):
        return time.time() - self.startTimer
    
    def getBoard(self):
        return self.board
    
    def doMove(self, row, column):
        pass
    
    def reset(self):
        try:
            self.board = Board(self.board.rows, self.board.columns, self.board.mines)
            self.startTimer = time.time()
            return True
        except:
            return False
    def end(self):
        try:
            self.board.showAllCells()
            return True
        except:
            return False
        
if __name__ == "__main__":
    window = tkinter.Tk()
    game = Game()
    window.mainloop()
    