import Tkinter as tk
from os import system, getpid
import platform
from random import choice
from collections import Counter

class AppWin(tk.Tk):
    WIDTH = 360
    HEIGHT = 720
    TITLE = 'this is the title'
    MENU_FONTS = 'TkDefaultFont 12'
    def __init__(self):
        tk.Tk.__init__(self)
        # self.geometry('{}x{}'.format(WIDTH, HEIGHT))
        self.title(AppWin.TITLE)
        self.resizable(width=False, height=False)
        self.protocol('WM_DELETE_WINDOW', self.onExit)

        # Create a menubar and associate it with the window
        self.menubar = tk.Menu()
        self.config(menu=self.menubar)
        self.menubar.config(font=AppWin.MENU_FONTS)

        # Create File menu and add it to the menubar
        self.fileMenu = tk.Menu(self.menubar, font=AppWin.MENU_FONTS,
                                tearoff=False)
        self.menubar.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Exit', command=self.onExit)
        self.fileMenu.add_command(label='New Game', command=self.onNewGame)

        # Create Game Style menu and add it to the menubar
        self.styleMenu = tk.Menu(self.menubar, font=AppWin.MENU_FONTS,
                                 tearoff=False)
        self.menubar.add_cascade(label='Choose Style', menu=self.styleMenu)
        self.styleMenu.add_command(label='Normal', command=self.onNormalStyle)
        self.styleMenu.add_command(label='Paused', command=self.onPausedStyle)
        self.styleMenu.add_command(label='Change speed',
                                   command=self.onChangeSpeedStyle)

        self.mainFrame = tk.Frame(self, borderwidth=5)
        self.mainFrame.pack()
        self.canvas = tk.Canvas(self.mainFrame, height=AppWin.HEIGHT,
                                width=AppWin.WIDTH, relief='ridge',
                                borderwidth=3)
        self.canvas.pack()
        self.scoreLabel = tk.Label(self.mainFrame,
                                   text='This is the score bar',
                                   font=AppWin.MENU_FONTS)
        # self.scoreLabel.pack(anchor='w')
        self.scoreLabel.pack(side='left')
        self.modeLabel = tk.Label(self.mainFrame, text='', relief='ridge',
                                  borderwidth=2, justify='center',
                                  anchor='center')
        self.modeLabel.pack(side='right')

    # Exit function
    def onExit(self):
        id = getpid()
        os = platform.system()
        if os == 'Linux':
            command = 'kill ' + str(id)
            system(command)
        else:
            command = 'taskkill /pid ' + str(id)
            system(command)

    # FUNCTIONS FOR THE MENU BUTTONS
    def onNewGame(self):
        pass

    def onNormalStyle(self):
        pass

    def onPausedStyle(self):
        pass

    def onChangeSpeedStyle(self):
        pass

    def is_game_over(self):
        for box in self.current_shape.boxes:
            if not self.current_shape.can_move_box(box, 0, 1):
                return True
        return False

    def remove_complete_lines(self):
        shape_boxes_coords = [self.canvas.coords(box)[3] for box
                in self.current_shape.boxes]
        all_boxes = self.canvas.find_all()
        all_boxes_coords = {k : v for k, v in
                zip(all_boxes, [self.canvas.coords(box)[3]
                    for box in all_boxes])}
        lines_to_check = set(shape_boxes_coords)
        boxes_to_check = dict((k, v) for k, v in all_boxes_coords.iteritems()
                if any(v == line for line in lines_to_check))
        counter = Counter()
        for box in boxes_to_check.values(): counter[box] += 1
        complete_lines = [k for k, v in counter.iteritems()
                if v == (AppWin.WIDTH/Shape.BOX_SIZE)]

        if not complete_lines: return False

        for k, v in boxes_to_check.iteritems():
            if v in complete_lines:
                self.canvas.delete(k)
                del all_boxes_coords[k]

        for (box, coords) in all_boxes_coords.iteritems():
            for line in complete_lines:
                if coords < line:
                    self.canvas.move(box, 0, Shape.BOX_SIZE)
        return len(complete_lines)


class Shape:
    '''Defines a tetris shape.'''
    # BOX_SIZE = 20
    BOX_SIZE = 20
    # START_POINT relies on screwy integer arithmetic to approximate the middle
    # of the canvas while remaining correctly on the grid.
    START_POINT = AppWin.WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE
    SHAPES = (
        ("yellow", (0, 0), (1, 0), (0, 1), (1, 1)),     # square
        ("lightblue", (0, 0), (1, 0), (2, 0), (3, 0)),  # line
        ("orange", (2, 0), (0, 1), (1, 1), (2, 1)),     # right el
        ("blue", (0, 0), (0, 1), (1, 1), (2, 1)),       # left el
        ("green", (0, 1), (1, 1), (1, 0), (2, 0)),      # right wedge
        ("red", (0, 0), (1, 0), (1, 1), (2, 1)),        # left wedge
        ("purple", (1, 0), (0, 1), (1, 1), (2, 1)),     # symmetrical wedge
    )

    def __init__(self, canvas):
        '''Create a shape.

        Select a random shape from the SHAPES tuple. Then, for each point
        in the shape definition given in the SHAPES tuple, create a
        rectangle of size BOX_SIZE. Save the integer references to these
        rectangles in the self.boxes list.

        Args:
        canvas - the parent canvas on which the shape appears

        '''
        self.boxes = [] # the squares drawn by canvas.create_rectangle()
        self.shape = choice(Shape.SHAPES) # a random shape
        self.color = self.shape[0]
        self.canvas = canvas

        for point in self.shape[1:]:
            box = canvas.create_rectangle(
                point[0] * Shape.BOX_SIZE + Shape.START_POINT,
                point[1] * Shape.BOX_SIZE,
                point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + Shape.START_POINT,
                point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE,
                fill=self.color)
            self.boxes.append(box)


    def move(self, x, y):
        '''Moves this shape (x, y) boxes.'''
        if not self.can_move_shape(x, y):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, x * Shape.BOX_SIZE, y * Shape.BOX_SIZE)
            return True

    def fall(self):
        '''Moves this shape one box-length down.'''
        if not self.can_move_shape(0, 1):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, 0 * Shape.BOX_SIZE, 1 * Shape.BOX_SIZE)
            return True

    def rotate(self):
        '''Rotates the shape clockwise.'''
        boxes = self.boxes[:]
        pivot = boxes.pop(2)

        def get_move_coords(box):
            '''Return (x, y) boxes needed to rotate a box around the pivot.'''
            box_coords = self.canvas.coords(box)
            pivot_coords = self.canvas.coords(pivot)
            x_diff = box_coords[0] - pivot_coords[0]
            y_diff = box_coords[1] - pivot_coords[1]
            x_move = (- x_diff - y_diff) / self.BOX_SIZE
            y_move = (x_diff - y_diff) / self.BOX_SIZE
            return x_move, y_move

        # Check if shape can legally move
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            if not self.can_move_box(box, x_move, y_move):
                return False

        # Move shape
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            self.canvas.move(box,
                             x_move * self.BOX_SIZE,
                             y_move * self.BOX_SIZE)

        return True

    def can_move_box(self, box, x, y):
        '''Check if box can move (x, y) boxes.'''
        x *= Shape.BOX_SIZE
        y *= Shape.BOX_SIZE
        coords = self.canvas.coords(box)

        # Returns False if moving the box would overrun the screen
        if coords[3] + y > AppWin.HEIGHT: return False
        if coords[0] + x < 0: return False
        if coords[2] + x > AppWin.WIDTH: return False

        # Returns False if moving box (x, y) would overlap another box
        overlap = set(self.canvas.find_overlapping(
            (coords[0] + coords[2]) / 2 + x,
            (coords[1] + coords[3]) / 2 + y,
            (coords[0] + coords[2]) / 2 + x,
            (coords[1] + coords[3]) / 2 + y
        ))
        other_items = set(self.canvas.find_all()) - set(self.boxes)
        if overlap & other_items: return False

        return True


    def can_move_shape(self, x, y):
        '''Check if the shape can move (x, y) boxes.'''
        for box in self.boxes:
            if not self.can_move_box(box, x, y): return False
        return True


if __name__ == '__main__':
    app = AppWin()
    app.mainloop()