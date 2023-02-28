import tkinter
from random import shuffle


class MyButton(tkinter.Button):
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0

    def __repr__(self):
        return f'MyButton {self.x}{self.y}{self.number}{self.is_mine}'


class Minesweeper:
    window = tkinter.Tk()
    row = 7
    column = 10
    mines = 20

    def __init__(self):
        self.buttons = []
        for i in range(Minesweeper.row + 2):
            temp = []
            for j in range(Minesweeper.column + 2):
                btn = MyButton(Minesweeper.window, x=i, y=j, width=3)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
        else:
            clicked_button.config(text=clicked_button.number)
        clicked_button.config(state='disabled')

    def start(self):
        self.create_widgets()
        self.insert_mines()
        self.count_mines_in_buttons()
        self.print_button()
        self.open_all_buttons()
        Minesweeper.window.mainloop()

    def create_widgets(self):
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def open_all_buttons(self):
        for i in range(Minesweeper.row + 2):
            for j in range(Minesweeper.column + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                else:
                    btn.config(text=btn.count_bomb, disabledforeground='black')

    def print_button(self):
        for row_btn in self.buttons:
            print(row_btn)

    def insert_mines(self):
        index_mines = self.get_mines_places(self)
        print(index_mines)
        count = 1
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                btn.number = count
                if btn.number in index_mines:
                    btn.is_mine = True
                count += 1

    def count_mines_in_buttons(self):
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

    @staticmethod
    def get_mines_places(self):
        indexes = list(range(1, Minesweeper.column * Minesweeper.row + 1))
        shuffle(indexes)
        return indexes[:Minesweeper.mines]


game = Minesweeper()
game.start()
