import tkinter
from random import shuffle


class MyButton(tkinter.Button):
    def __init__(self, master, x, y, number, *args, **kwargs):
        super(MyButton, self).__init__(master, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False

    def __repr__(self):
        return f'MyButton {self.x}{self.y}{self.number}{self.is_mine}'


class Minesweeper:
    window = tkinter.Tk()
    row = 10
    column = 7
    mines = 15

    def __init__(self):
        count = 1
        self.buttons = []
        for i in range(Minesweeper.row):
            temp = []
            for j in range(Minesweeper.column):
                btn = MyButton(Minesweeper.window, x=i, y=j, width=3, number=count)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
                count += 1
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
        else:
            clicked_button.config(text=clicked_button.number)
        clicked_button.config(state='disabled')

    def create_widgets(self):
        for i in range(Minesweeper.row):
            for j in range(Minesweeper.column):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def start(self):
        self.create_widgets()
        self.insert_mines()
        self.print_button()
        Minesweeper.window.mainloop()

    def print_button(self):
        for row_btn in self.buttons:
            print(row_btn)

    def insert_mines(self):
        index_mines = self.get_mines_places(self)
        print(index_mines)
        for row_btn in self.buttons:
            for btn in row_btn:
                if btn.number in index_mines:
                    btn.is_mine = True

    @staticmethod
    def get_mines_places(self):
        indexes = list(range(1, Minesweeper.column * Minesweeper.row + 1))
        shuffle(indexes)
        return indexes[:Minesweeper.mines]


game = Minesweeper()
game.start()
