import Tkinter as tk
import tkMessageBox

from gui import AppWin, Shape

NORMAL = 0
PAUSED = 1
CHANGE_SPEED = 2

class Tetris(AppWin):
    def __init__(self):
        AppWin.__init__(self)
        self.bind('<Key>', self.handleEvents)

        self.gameMode= NORMAL
        self.gameRunning = True
        self.level = 0
        self.speed = 500
        self.counter = 0
        self.score = 0
        self.output = 'Level: {} Score: {}'.format(self.level, self.score)
        self.create_new_game = True
        self.timer()


    def timer(self):
        '''Every self.speed ms, attempt to cause the current_shape to fall().

        If fall() returns False, create a new shape and check if it can fall.
        If it can't, then the game is over.

        '''
        if self.create_new_game:
            self.current_shape = Shape(self.canvas)
            self.create_new_game = False

        if not self.current_shape.fall():
            lines = self.remove_complete_lines()
            if lines:
                self.score += 10 * self.level**2 * lines**2
                # self.scoreLabel.update()

            self.current_shape = Shape(self.canvas)
            if self.is_game_over():
                tkMessageBox.showinfo(
                    "Game Over",
                    "You scored %d points." % self.score)
                self.onNewGame()
                return

            self.counter += 1
            if self.counter == 5:
                self.level += 1
                if self.gameMode == NORMAL:
                    self.speed -= 20
                self.counter = 0
        if (not self.gameMode == PAUSED) and (self.gameRunning == True):
            self.timeLoop = self.after(self.speed, self.timer)
        self.updateLabels()

    def handleEvents(self, event):
        if event.keysym == "p": self.changeState()
        if event.keysym == "Left": self.current_shape.move(-1, 0)
        if event.keysym == "Right": self.current_shape.move(1, 0)
        if event.keysym == "Up" and self.current_shape.color != 'yellow':
            self.current_shape.rotate()
        if self.gameMode == PAUSED:
            if event.keysym == "Down": self.timer()
        else:
            if event.keysym == "Down": self.current_shape.move(0, 1)
        if self.gameMode == CHANGE_SPEED:
            if self.speed < 100: self.speed = 100
            elif self.speed > 2000: self.speed = 2000
            else:
                if event.keysym == 'KP_Add':
                    self.speed -= 20
                if event.keysym == 'KP_Subtract':
                    self.speed += 20

    # Functions inherited from AppWin class
    def onNewGame(self):
        self.after_cancel(self.timeLoop)
        self.create_new_game = True
        self.canvas.delete(tk.ALL)
        self.level = 0
        self.counter = 0
        self.score = 0
        self.speed = 500
        self.updateLabels()
        self.timer()

    def onNormalStyle(self):
        self.gameMode = NORMAL
        self.onNewGame()

    def onPausedStyle(self):
        self.gameMode = PAUSED
        self.onNewGame()

    def onChangeSpeedStyle(self):
        self.gameMode = CHANGE_SPEED
        self.onNewGame()

    def updateLabels(self):
        self.scoreLabel.config(text='Level: %d  Score: %d' %
                                    (self.level, self.score))
        modes = ['N', 'P', 'CS']
        self.modeLabel.config(text='%s' % modes[self.gameMode])
        self.pauseLabel.update()

    def changeState(self):
        if self.gameMode != PAUSED:
            if self.gameRunning:
                self.gameRunning = False
                self.pauseLabel.config(text='paused')
            else:
                self.gameRunning = True
                self.pauseLabel.config(text='')
                self.timer()

if __name__ == '__main__':
    game = Tetris()
    game.mainloop()
