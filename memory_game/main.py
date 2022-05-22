from random import shuffle
from tkinter import *
from tkinter.font import Font
import time

root = Tk()

levels = [(4,4),(6,6),(8,6),(8,8)]  # even number of tile
a_button_active = False
grid_frame = None

running = True

class BtnItem(Button):
    def __init__(self, i: int, *args, **kwargs):
        super().__init__(*args, **kwargs, relief="flat", bd=0)  # command=self.click
        self.i = i
        self.bind("<Button-1>", self.click, add=True)

    def click(self, event=None):
        global running
        if not running:
            return
        global a_button_active , first_guess, numberof_tile, numberof_duo, number_of_guess, grid_frame
        print(f"{self} clicked")
        self.config(image=f"pyimage{self.i}")
        number_of_guess += 1
        if a_button_active == False :
            first_guess = self
            numberof_tile -= 1
            tile_to_discover_lbl.config(text=f"Number of tile \n to discover : {numberof_tile}")
            number_of_guess_lbl.config(text=f"Number of guess : {number_of_guess}")
        elif first_guess == self:
            return
        elif first_guess.i == self.i: # good guess
            numberof_tile -= 1
            tile_to_discover_lbl.config(text=f"Number of tile \n to discover : {numberof_tile}")
            number_of_guess_lbl.config(text=f"Number of guess : {number_of_guess}")
            print("oui")
            print(f"{numberof_tile},{numberof_duo}")
            advancement_lbl.config(text="Advancement : {:.1f} %".format(100-(numberof_tile/2)/numberof_duo*100))
            if numberof_tile == 0 :
                Label(grid_frame, text="Win !", font=winfont, fg='green', bg='#FFFFFF').place(relx=0.5, rely=0.5, anchor=CENTER)
                pass
        else : # bad guess
            running = False
            numberof_tile += 1
            print("non")
            root.update()
            time.sleep(0.5)
            first_guess.config(image=hidden_img)
            self.config(image=hidden_img)
            tile_to_discover_lbl.config(text=f"Number of tile \n to discover : {numberof_tile}")
            number_of_guess_lbl.config(text=f"Number of guess : {number_of_guess}")
            running = True
        a_button_active = not a_button_active


max_numberof_duo = int(levels[-1][0]*levels[-1][1]/2)
tileimg_var_holder = {}
for i in range(max_numberof_duo):
    tileimg_var_holder[f'tileimg_{i+1}'] = PhotoImage(file=f"tiles/{i+1}.png")
globals().update(tileimg_var_holder)

hidden_img = PhotoImage(file="tiles/hidden.png")

titlefont = Font(family='Bahnschrift SemiBold SemiConden', size=16, weight="bold")
winfont = Font(family='Bahnschrift SemiBold SemiConden', size=52, weight="bold")

title = Label(root, text="MEMORY GAME", font=titlefont)
title.grid(row=0, columnspan=2)

side_frame = Frame(root, width=200)
side_frame.grid(row=1, column=0)

level_frame = Frame(side_frame)
level_frame.grid(row=0, column=0, pady=15)

Label(level_frame, text="Levels :", font=titlefont).grid(row=0, column=0)

game_stats_frame = Frame(side_frame)
game_stats_frame.grid(row=1, column=0)

advancement_lbl = Label(game_stats_frame, text="Advancement : 0 % ", justify='left', font=titlefont)
advancement_lbl.grid(row=0, column=0, pady=5)

tile_to_discover_lbl = Label(game_stats_frame, text="Number of tile \n to discover : ", justify='left', font=titlefont)
tile_to_discover_lbl.grid(row=1, column=0, pady=5)

number_of_guess_lbl = Label(game_stats_frame, text="Number of guess : ", justify='left', font=titlefont)
number_of_guess_lbl.grid(row=2, column=0, pady=5)

rb = [["Easy", 0], ["Medium", 1], ["Hard", 2], ["Big Head", 3]]
levelvar = StringVar()

for x in range(len(rb)):
    r = Radiobutton(level_frame, text=rb[x][0], font=(12), variable=levelvar, value=rb[x][1])
    r.grid(row=x+1, column=0, sticky='w')
    if x == 0 :
        r.invoke()

def play():
    global numberof_tile, numberof_duo, number_of_guess, grid_frame
    if grid_frame is None:
        grid_frame = Frame(root)
        grid_frame.grid(row=1, column=1)
    for widgets in grid_frame.winfo_children():
        widgets.destroy()

    numberof_duo = int(levels[int(levelvar.get())][0]*levels[int(levelvar.get())][1]/2)
    numberof_tile = int(levels[int(levelvar.get())][0]*levels[int(levelvar.get())][1])

    tile_list = []
    for x in range(numberof_duo) :
        tile_list.append(x+1)
        tile_list.append(x+1)
    shuffle(tile_list)
    print(tile_list)

    grid = []
    for x in range(levels[int(levelvar.get())][1]) :
        grid_0 = []
        for y in range(levels[int(levelvar.get())][0]):
            grid_0.append(BtnItem(tile_list[0], grid_frame, image=hidden_img))
            tile_list.pop(0)
        grid.append(grid_0)
    print(grid)

    advancement_lbl.config(text=f"Advancement : 0 %")

    tile_to_discover_lbl.config(text=f"Number of tile \n to discover : {numberof_tile}")

    number_of_guess = 0
    number_of_guess_lbl.config(text=f"Number of guess : {number_of_guess}")

    for i, x in enumerate(grid) :
        for j, y in enumerate(x) :
            y.grid(row=i, column=j)

Button(side_frame, text="Play", font=(14), width=10, command=play).grid(row=2, column=0, sticky='s', pady=5)





root.mainloop()