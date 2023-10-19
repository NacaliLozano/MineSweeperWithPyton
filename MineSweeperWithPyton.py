
import tkinter
import tkinter.simpledialog
import random
import time
import pickle
import os


class Cell:
    def __init__(self):
        """Creates a Cell"""
        self.value = 0
        self.flipped = False
    
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
            self.flipped = True
            return True
        except:
            return False
    
    def isFlipped(self):
        return self.flipped
    
    def swapFlipped(self):
        """Swaps the value of flipped"""
        try:
            self.flipped = not self.flipped
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
                self.cells[row].append(Cell())
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
                if self.cells[row][column].value >= 9:
                    for incrementRows in [-1, 0, 1]:
                        for incrementColumns in [-1, 0, 1]:
                            if row + incrementRows in range(self.rows) and column + incrementColumns in range(self.columns):
                                if incrementRows == 0 and incrementColumns == 0:
                                    continue
                                self.cells[row + incrementRows][column + incrementColumns].value += 1
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
                    if self.cells[row][column].isFlipped():
                        continue
                    self.cells[row][column].setFlipped()
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
    
    def getFileName(self):
        return self.fileName

class Game:
    def __init__(self):
        self.player = None
        self.board = None
        self.startTimer = None
    
    def requestName(self):
        return tkinter.simpledialog.askstring("Minesweeper", ">")
    
    def save(self):
        game = {"Board": self.board, "Time": self.getTime(), "Player": self.player}
        try:
            with open(self.player.getFileName(), "w") as f:
                f.pickle.dump(game)
            return True
        except:
            return False

    def newGame(self):
        try:
            self.board = Board(14, 18, 40)
            self.board.setBoard()
            self.startTimer = time.time()
            return True
        except:
            return False
    
    def load(self, fileName):
        try:
            with open(fileName, "r") as f:
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
    
    def getPlayer(self):
        return self.player
    
    def getTime(self):
        return time.time() - self.startTimer
    
    def getBoard(self):
        return self.board
    
    def doMove(self, row, column):
        """Flips a Cell and neighbour cells"""
        #Return early if the cell is already visible
        if self.board.getCell(row, column).isFlipped():
            return
        #Return early if stepped on a mine
        if self.board.getCell(row, column).getValue() >= 9:
            self.youLoose()
            return
        #Set Cell to visible
        self.board.getCell(row, column).setFlipped()
        self
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
        if self.getTime() - self.startTimer < self.player.getRecord():
            self.player.setRecord(self.getTime() - self.startTimer)
        self.end()
        tkinter.messagebox.showinfo("Game over","You Win!!!")
        
    def gameLoop(self):
        window = tkinter.Tk()
        playerName = self.requestName()
        if os.path.exists(playerName + ".msg"):
            self.load(playerName + ".msg")
        else:
            self.player = Player(playerName)
            self.newGame()
        buttons = []
        for row in range(self.board.getRows()):
            buttons.append([])
            for column in range(self.board.getColumns()):
                buttons[row].append(tkinter.Button(window, height = 1, width = 1))
                buttons[row][column].grid(row = row, column = column)
                buttons[row][column].bind('<Button-1>', lambda event, row = row, column = column: self.doMove(row, column), buttons[row][column].destroy())
                buttons[row][column].bind('<Button-3>', lambda event, row = row, column = column: self.rightClick(row, column))
        window.mainloop()
        
if __name__ == "__main__":
    #window = tkinter.Tk()
    game = Game()
    game.gameLoop()
    
    #window.mainloop()
    