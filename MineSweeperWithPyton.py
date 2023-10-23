
import tkinter
import tkinter.simpledialog
import random
import time
import pickle
import os


class Cell:
    def __init__(self, row, column):
        """Creates a Cell"""
        self.value = 0
        self.visible = False
        self.button = None
        self.label = None
        self.row = row
        self.column = column
        
    def setValue(self, value):
        """Sets the value of a Cell"""
        try:
            self.value = value
            return True
        except:
            return False
        
    def getValue(self):
        return self.value
    
    def setVisible(self):
        """Sets a Cell to visible state"""
        if self.visible:
            return False
        try:
            self.button.destroy()
            cellValue = self.getValue()
            if cellValue >= 9:
                self.label = tkinter.Label(text = "X")
            elif cellValue > 0:
                self.label = tkinter.Label(text = str(cellValue))
            else:
                self.label = tkinter.Label(text = "")
            self.label.grid(row = self.row, column = self.column)
            self.visible = True
            return True
        except:
            return False
    
    def isVisible(self):
        return self.visible
    
    def swapVisible(self):
        """Swaps the value of visible"""
        try:
            self.visible = not self.visible
            return True
        except:
            return False
        
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
        #Set mines
        for mine in range(mines):
            row = random.randint(0, rows -1)
            column = random.randint(0, columns - 1)
            while self.cells[row][column].value >= 9:
                row = random.randint(0, rows -1)
                column = random.randint(0, columns - 1)
            self.cells[row][column].value = 9
            
    def setBoard(self):
        """Sets the values of the cells with a mine nearby"""
        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].getValue() >= 9:
                    for incrementRows in [-1, 0, 1]:
                        for incrementColumns in [-1, 0, 1]:
                            if row + incrementRows in range(self.rows) and column + incrementColumns in range(self.columns):
                                if incrementRows == 0 and incrementColumns == 0:
                                    continue
                                self.cells[row + incrementRows][column + incrementColumns].setValue(self.cells[row + incrementRows][column + incrementColumns].getValue() + 1)
        return self
    
    def getCell(self, row, column):
        return self.cells[row][column]
    
    def getRows(self):
        return self.rows
    
    def getColumns(self):
        return self.columns
    
    def getMines(self):
        return self.mines
    
    def getRemainingCoveredCells(self):
        return self.remainingCoveredCells
    
    def setRemainingCoveredCells(self, value):
        try:
            self.remainingCoveredCells = value
            return True
        except:
            return False

    def showAllCells(self):
        try:
            for row in range(self.rows):
                for column in range(self.columns):
                    if self.cells[row][column].isVisible():
                        continue
                    self.cells[row][column].setVisible()
            return True
        except:
            return False

        
class Player:
    def __init__(self, name):
        self.name = name
        self.fileName = self.name + ".msg" #MineSweeper Game
        self.record = None
        
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
    
    def getRecord(self):
        return self.record
    
    def setRecord(self, record):
        self.record = record
        
    def getFileName(self):
        return self.fileName

class Game:
    def __init__(self):
        self.player = None
        self.board = None
        self.startTimer = None
    
    def requestName(self):
        return tkinter.simpledialog.askstring("Minesweeper", "Enter your name:")
    
    def save(self):
        game = {"Board": self.board, "Time": self.getTime(), "Player": self.player}
        try:
            with open(self.player.getFileName(), "wb") as f:
                f.pickle.dump(game, f)
            return True
        except:
            return False

    def newGame(self):
        try:
            self.board = Board(14, 18, 1)
            self.board.setBoard()
            self.startTimer = time.time()
            return True
        except:
            return False

    
    def load(self, fileName):
        try:
            with open(fileName, "rb") as f:
                game = pickle.load(f)
                if game["Board"] == None:
                    self.player = game["Player"]
                    self.newGame()
                else:
                    self.board = game["Board"]
                    self.startTimer = time.time() - game["Time"]
                    self.player = game["Player"]
            return True
        except:
            return False
        #TODO corregir
    
    def getPlayer(self):
        return self.player
    
    def getTime(self):
        return time.time() - self.startTimer
    
    def getBoard(self):
        return self.board
    
    def doMove(self, row, column):
        """Flips a Cell and neighbour cells"""
        #Return early if the cell is already visible
        if self.board.getCell(row, column).isVisible():
            return
        #Return early if stepped on a mine
        if self.board.getCell(row, column).getValue() >= 9:
            self.youLoose()
            return
        #Set Cell to visible
        self.board.getCell(row, column).setVisible()
        #Decrement RemainingCoveredCells
        self.board.setRemainingCoveredCells(self.board.getRemainingCoveredCells() - 1)
        #Return if player won
        if self.board.getRemainingCoveredCells() == self.board.getMines():
            self.youWin()
            return
        #Trigger neighbour cells
        if self.board.getCell(row, column).getValue() == 0:
            for incrementRows in [-1, 0, 1]:
                for incrementColumns in [-1, 0, 1]:
                    if row + incrementRows in range(self.board.getRows()) and column + incrementColumns in range(self.board.getColumns()):
                        if incrementRows == 0 and incrementColumns == 0:
                            continue
                        self.doMove(row + incrementRows, column + incrementColumns)
        self.save()
    
    def reset(self):
        try:
            self.board = Board(self.board.getRows(), self.board.getColumns(), self.board.getMines())
            self.startTimer = time.time()
            return True
        except:
            return False
        
    def end(self):
        try:
            self.board.showAllCells()
            self.board = None
            self.save()
            return True
        except:
            return False
        
    def youLoose(self):
        self.end()
        tkinter.messagebox.showinfo("Game over","You lost!!!")
        
    def youWin(self):
        if self.getTime() - self.startTimer < self.player.getRecord() or self.player.getRecord() is None:
            self.player.setRecord(self.getTime())
        self.end()
        tkinter.messagebox.showinfo("Game over","You Win!!!")
        
    def rightClick(self, row, column):
        self.board.getCell(row, column).button.unbind('<Button-1>')
        self.board.getCell(row, column).button.configure(bg="red")
        self.board.getCell(row, column).button.bind('<Button-3>', lambda event, row=row, column=column: self.secondRightClick(row, column))
        
    def secondRightClick(self, row, column):
        self.board.getCell(row, column).button.bind('<Button-1>', lambda event, row=row, column=column: self.doMove(row, column))
        self.board.getCell(row, column).button.bind('<Button-3>', lambda event, row=row, column=column: self.rightClick(row, column))
        
    def gameLoop(self):
        window = tkinter.Tk()
        playerName = self.requestName()
    
        if os.path.exists(playerName + ".msg"):
            self.load(playerName + ".msg")
        else:
            self.player = self.Player(playerName)
        if self.board is None:
            self.newGame()
        for row in range(self.board.getRows()):
            for column in range(self.board.getColumns()):
                self.board.getCell(row, column).button = tkinter.Button(window, height = 1, width = 1)
                self.board.getCell(row, column).button.grid(row=row, column=column)
                self.board.getCell(row, column).button.bind('<Button-1>', lambda event, row=row, column=column: self.doMove(row, column))
                self.board.getCell(row, column).button.bind('<Button-3>', lambda event, row=row, column=column: self.rightClick(row, column))
        window.mainloop()
        
if __name__ == "__main__":
    #window = tkinter.Tk()
    game = Game()
    game.gameLoop()
    
    #window.mainloop()
    