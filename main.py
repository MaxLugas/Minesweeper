import time
import tkinter
from random import shuffle
from tkinter.messagebox import showinfo, showerror

colors = {
    1: '#0000ff',
    2: '#018723',
    3: '#857701',
    4: '#e6020a',
    5: '#ad45a0',
    6: '#c45104',
    7: '#04c4ae',
    8: '#5a0c8a',
}


class MyButton(tkinter.Button):
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False


class Minesweeper:
    window = tkinter.Tk()
    window.title('Minesweeper')
    row = 7
    column = 10
    mines = 10
    is_game_over = False
    is_first_click = True

    def __init__(self):
        self.buttons = []
        for i in range(Minesweeper.row + 2):
            temp = []
            for j in range(Minesweeper.column + 2):
                btn = MyButton(Minesweeper.window, x=i, y=j, width=3)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
                btn.bind('<Button-3>', self.right_click)
            self.buttons.append(temp)

    def right_click(self, event):
        if Minesweeper.is_game_over:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
            cur_btn['disabledforeground'] = 'red'
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'

    def check_win(self):
        open_buttons = 0
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                if self.buttons[i][j].is_open:
                    open_buttons += 1
        if open_buttons == Minesweeper.row * Minesweeper.column - Minesweeper.mines:
            Minesweeper.is_game_over = True
            showinfo('Game Over', 'You Win!')

    def click(self, clicked_button: MyButton):
        if Minesweeper.is_game_over:
            return
        if clicked_button['text'] == '🚩':
            Minesweeper.mines += 1
            self.flags_label.config(text=f"Flags: {Minesweeper.mines}")
        elif clicked_button['state'] == 'disabled':
            Minesweeper.mines -= 1
            self.flags_label.config(text=f"Flags: {Minesweeper.mines}")
        if Minesweeper.is_first_click:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_button()
            Minesweeper.is_first_click = False
            self.start_time = time.time()
        self.update_time_label()
        color = colors.get(clicked_button.count_bomb, "black")
        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
            clicked_button.is_open = True
            Minesweeper.is_game_over = True
            showinfo('Game Over', 'You Lose!')
            for i in range(1, Minesweeper.row + 1):
                for j in range(1, Minesweeper.column + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        elif clicked_button.count_bomb:
            clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color, relief=tkinter.SUNKEN)
            clicked_button.is_open = True
        else:
            clicked_button.config(text='', relief=tkinter.SUNKEN)
            clicked_button.is_open = True
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    btn = self.buttons[clicked_button.x + i][clicked_button.y + j]
                    if not btn.is_open and btn.number != 0:
                        self.click(btn)
        clicked_button.config(state='disabled')

        self.check_win()

    def update_time_label(self):
        if not Minesweeper.is_game_over:
            elapsed_time = round(time.time() - self.start_time)
            self.time_label.config(text=f"Time: {elapsed_time}")
            Minesweeper.window.after(1000, self.update_time_label)
    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tkinter.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if abs(dx - dy) == 1:
                        #     continue

                        next_btn = self.buttons[x + dx][y + dy]
                        if next_btn.is_open and 1 <= next_btn.x <= Minesweeper.row \
                                and 1 <= next_btn.y <= Minesweeper.column and next_btn not in queue:
                            queue.append(next_btn)

    def start(self):
        self.create_widgets()
        Minesweeper.window.mainloop()

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        Minesweeper.is_first_click = True
        Minesweeper.is_game_over = False

    def create_setting_window(self):
        window_settings = tkinter.Toplevel(self.window)
        window_settings.wm_title('Settings')

        tkinter.Label(window_settings, text='Row count').grid(row=0, column=0)
        row_entry = tkinter.Entry(window_settings)
        row_entry.insert(0, Minesweeper.row)
        row_entry.grid(row=0, column=1, padx=20, pady=20)

        tkinter.Label(window_settings, text='Column count').grid(row=1, column=0)
        column_entry = tkinter.Entry(window_settings)
        column_entry.insert(0, Minesweeper.column)
        column_entry.grid(row=1, column=1, padx=20, pady=20)

        tkinter.Label(window_settings, text='Mines count').grid(row=2, column=0)
        mines_entry = tkinter.Entry(window_settings)
        mines_entry.insert(0, Minesweeper.mines)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        save_btn = tkinter.Button(window_settings, text='Submit',
                                  command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tkinter.Entry, column: tkinter.Entry, mines: tkinter.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Error', 'Enter the number')
            return
        Minesweeper.row = int(row.get())
        Minesweeper.column = int(column.get())
        Minesweeper.mines = int(mines.get())
        self.reload()

    def about(self):
        showinfo('Version', 'Game version 1.1')

    def author(self):
        showinfo('Author', 'Visit my website lugasm.beget.tech')

    def create_widgets(self):
        menubar = tkinter.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu_1 = tkinter.Menu(menubar, tearoff=0)
        settings_menu_1.add_command(label='Restart', command=self.reload)
        settings_menu_1.add_command(label='Settings', command=self.create_setting_window)
        settings_menu_1.add_command(label='Exit', command=self.window.destroy)
        menubar.add_cascade(label='File', menu=settings_menu_1)

        self.flags_label = tkinter.Label(Minesweeper.window, text=f"Flags: {Minesweeper.mines}")
        self.flags_label.grid(row=Minesweeper.row + 1, column=0, columnspan=Minesweeper.column // 2)


        self.time_label = tkinter.Label(Minesweeper.window, text="Time: 0")
        self.time_label.grid(row=Minesweeper.row + 1, column=Minesweeper.column // 2,
                             columnspan=Minesweeper.column // 2)

        settings_menu_2 = tkinter.Menu(menubar, tearoff=0)
        settings_menu_2.add_command(label='Version', command=self.about)
        settings_menu_2.add_command(label='Author', command=self.author)
        menubar.add_cascade(label='Information', menu=settings_menu_2)

        count = 1
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, sticky='NWES')
                count += 1

        for i in range(1, Minesweeper.row + 1):
            Minesweeper.window.rowconfigure(i, weight=1)
        for j in range(1, Minesweeper.column + 1):
            Minesweeper.window.columnconfigure(j, weight=1)

    def open_all_buttons(self):
        for i in range(Minesweeper.row + 2):
            for j in range(Minesweeper.column + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def print_button(self):
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]

    def insert_mines(self, number: int):
        index_mines = self.get_mines_places(number)
        for i in range(1, Minesweeper.row + 1):
            for j in range(1, Minesweeper.column + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True

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
    def get_mines_places(exclude_number: int):
        indexes = list(range(1, Minesweeper.column * Minesweeper.row + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:Minesweeper.mines]


game = Minesweeper()
game.start()
