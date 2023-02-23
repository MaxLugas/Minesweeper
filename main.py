import tkinter

class Minesweeper:
    window = tkinter.Tk()
    row = 5
    column = 7

    def __init__(self):
        self.buttons = []
        for i in range(Minesweeper.row):
            temp = []
            for j in range(Minesweeper.column):
                btn = tkinter.Button(Minesweeper.window, width=3, font='Calibri 15 bold')
                temp.append(btn)
            self.buttons.append(temp)

    def create_widgets(self):
        for i in range(Minesweeper.row):
            for j in range(Minesweeper.column):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def start(self):
        Minesweeper.window.mainloop()

game=Minesweeper()
game.create_widgets()
game.start()
