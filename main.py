import tkinter


class MyButton(tkinter.Button):
    def __init__(self, master, x, y, *args, **kwargs):
        super(MyButton, self).__init__(master, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.is_mine = False

    def __repr__(self):
        return 'MyButton'


class Minesweeper:
    window = tkinter.Tk()
    row = 5
    column = 7

    def __init__(self):
        self.buttons = []
        for i in range(Minesweeper.row):
            temp = []
            for j in range(Minesweeper.column):
                btn = MyButton(Minesweeper.window, x=i, y=j, width=3)
                temp.append(btn)
            self.buttons.append(temp)

    def create_widgets(self):
        for i in range(Minesweeper.row):
            for j in range(Minesweeper.column):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def start(self):
        self.create_widgets()
        Minesweeper.window.mainloop()


game = Minesweeper()
game.start()
