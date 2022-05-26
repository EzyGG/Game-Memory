import sys
import time
from tkinter import *
from random import shuffle
from ezyapi.UUID import UUID
from threading import Thread
from tkinter.font import Font
import ezyapi.game_manager as manager
from ezyapi.sessions import UserNotFoundException
from ezyapi.mysql_connection import DatabaseConnexionError

GAME_UUID = UUID("4789f232-83b3-a61f-858b-641a1bef19a3")
GAME_VERSION = manager.GameVersion("v1.0")


class Error(Tk):
    def __init__(self, name: str, desc: str):
        super().__init__("err")
        self.app_bg = 'black'
        self.app_fg = 'white'
        self.app_circle_color = 'blue'
        self.app_cross_color = 'red'

        self.title("Erreur")
        # self.resizable(False, False)
        self.geometry("300x300")
        self.configure(background=self.app_bg)
        try:
            self.iconbitmap("icon.ico")
        except Exception:
            pass

        self.name, self.desc = name, desc

        self.name_label = Label(self, bg=self.app_bg, fg=self.app_fg, font=("", 16, "bold"), wraplengt=300, text=name)
        self.name_label.pack(side=TOP, pady=10)

        self.desc_label = Label(self, bg=self.app_bg, fg=self.app_fg, wraplengt=300, text=desc)
        self.desc_label.pack(side=TOP, pady=10)

        self.opt_frame = Frame(self, bg=self.app_bg)
        self.cont_frame = Frame(self.opt_frame, bg=self.app_circle_color)
        self.cont_btn = Button(self.cont_frame, activebackground=self.app_bg, bg=self.app_bg, bd=0, relief=SOLID,
                               width=12, activeforeground=self.app_circle_color, fg=self.app_circle_color,
                               highlightcolor=self.app_circle_color, font=("", 12, "bold"), text="Continuer !",
                               command=self.cont_cmd)
        self.cont_btn.pack(padx=1, pady=1)
        self.cont_frame.pack(side=LEFT, padx=5)
        self.quit_frame = Frame(self.opt_frame, bg=self.app_cross_color)
        self.quit_btn = Button(self.quit_frame, activebackground=self.app_bg, bg=self.app_bg, bd=0, relief=SOLID,
                               width=12, activeforeground=self.app_cross_color, fg=self.app_cross_color,
                               highlightcolor=self.app_cross_color, font=("", 12, "bold"), text="Quitter.",
                               command=self.quit_cmd)
        self.quit_btn.pack(padx=1, pady=1)
        self.quit_frame.pack(side=RIGHT, padx=5)
        self.opt_frame.pack(side=BOTTOM, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.quit_cmd)
        self.bind("<Configure>", self.event_handler)
        self.bind("<Return>", self.on_return)
        self.quit_btn.focus_set()

        self.mainloop()

    def on_return(self, event=None):
        if self.focus_get() == self.cont_btn:
            self.cont_cmd()
        elif self.focus_get() == self.quit_btn:
            self.quit_cmd()

    def cont_cmd(self, event=None):
        self.destroy()

    def quit_cmd(self, event=None):
        try:
            sys.exit(1)
        except NameError:
            quit(1)

    def event_handler(self, event=None):
        new_wrap = int(self.winfo_geometry().split("x")[0]) - 5
        self.name_label.config(wraplengt=new_wrap)
        self.desc_label.config(wraplengt=new_wrap)


class Update(Thread):
    def __init__(self, from_version: manager.GameVersion = manager.GameVersion(),
                 to_version: manager.GameVersion = manager.GameVersion()):
        super().__init__()
        self.running = True

        self.from_version, self.to_version = from_version, to_version
        self.tk: Tk = None

    def stop(self):
        self.running = False
        if self.tk:
            self.tk.destroy()
        raise Exception("Thread Ending.")

    def run(self):
        self.tk = Tk("update")
        self.app_bg = 'black'
        self.app_fg = 'white'

        self.tk.title("Mise-à-Jour")
        self.tk.geometry("375x320")
        self.tk.configure(background=self.app_bg)
        try:
            self.tk.iconbitmap("tic_tac_toe.ico")
        except Exception:
            pass

        self.magic_frame = Frame(self.tk)
        self.internal_frame = Frame(self.magic_frame, bg=self.app_bg)

        self.magic_frame.pack_propagate(0)
        self.internal_frame.pack_propagate(0)

        self.title_frame = Frame(self.internal_frame, bg=self.app_bg)
        self.name_label = Label(self.title_frame, bg=self.app_bg, fg=self.app_fg, font=("", 16, "bold"), text="Mise-à-Jour")
        self.name_label.pack(side=TOP)

        self.version_label = Label(self.title_frame, bg=self.app_bg, fg=self.app_fg, font=("", 12, "bold"), text=f"{self.from_version}  →  {self.to_version}")
        self.version_label.pack(side=TOP)
        self.title_frame.pack(side=TOP, fill=X, expand=True, pady=20, padx=20)

        self.desc_label = Label(self.internal_frame, bg=self.app_bg, fg=self.app_fg, text="Nous remettons à jour votre jeu pour vous assurer une experience sans égale. Actuellement, nous transferont et compilons les nouveaux fichiers depuis la base de donnée. Si le jeu est important ou que votre connexion est mauvaise, l'action peut durer plusieurs minutes... Revenez un peu plus tard. (Temps éstimé: 5sec)")
        self.desc_label.pack(side=BOTTOM, pady=20, padx=20)

        self.internal_frame.pack(fill=BOTH, expand=True, padx=7, pady=7)
        self.magic_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

        self.tk.protocol("WM_DELETE_WINDOW", self.quit)
        self.tk.bind("<Configure>", self.on_configure)

        while self.running:
            self.loop()
            self.tk.mainloop()

    def quit(self):
        if not self.running:
            self.stop()

    def on_configure(self, e=None):
        wrap = int(self.tk.winfo_geometry().split("x")[0]) - 114  # 114 -> padx: 2*30 + 2*7 + 2*20
        self.name_label.config(wraplengt=wrap)
        self.desc_label.config(wraplengt=wrap)

    def loop(self, infinite=True, random=True):
        path = ["000", "100", "110", "010", "011", "001", "101", "111"]
        color = [0, 0, 0]
        while self.running:
            temp_path = path[:]
            if random:
                shuffle(temp_path)
            for p in temp_path:
                run = True
                while run and self.running:
                    run = False
                    for i in range(len(color)):
                        if p[i] == "0" and color[i] != 0:
                            color[i] -= 2 if color[i] - 2 > 0 else 1
                            run = True
                        elif p[i] == "1" and color[i] != 255:
                            color[i] += 2 if color[i] + 2 < 256 else 1
                            run = True
                    str_color = "#{color[0]:0>2X}{color[1]:0>2X}{color[2]:0>2X}".format(color=color)
                    self.magic_frame.configure(bg=str_color)
                    self.tk.update()
                    time.sleep(0.0001)
            if not infinite:
                break


CONTINUE = "\n\nIf you Continue, you will not be able to get rewards and update the ranking."
try:
    try:
        try:
            manager.setup(GAME_UUID, GAME_VERSION, __update=False, __import_missing_resources=False)
            for r in manager.import_resources(GAME_UUID):
                if r.specification == "game" or r.specification == "thumbnail":
                    pass
                elif "tile" in r.specification:
                    r.save_if_doesnt_exists("tiles")
                else:
                    r.save_by_erasing()
        except manager.UserParameterExpected as e:
            Error("UserParameterExpected",
                  str(e) + "\nYou must run the game from the Launcher to avoid this error." + CONTINUE)
        except UserNotFoundException as e:
            Error("UserNotFoundException", str(e) + "\nThe user information given does not match with any user." + CONTINUE)
    except DatabaseConnexionError as e:
        Error("DatabaseConnexionError",
              str(e) + "\nThe SQL Serveur is potentially down for maintenance...\nWait and Retry Later." + CONTINUE)
except Exception as e:
    Error(f"Erreur !", str(e) + CONTINUE)


root = Tk()
root.title("Memory Game")
try:
    root.iconbitmap("icon.ico")
except Exception:
    pass

levels = [(4,4),(6,6),(8,6),(8,8)]  # even number of tile
a_button_active = False
grid_frame = None

# Format: (exp, gp)
score_winnable = [(10, 2), (13, 3), (17, 4), (20, 5)]
score_worth = [(0, 1), (0, 1), (0, 1), (0, 1)]
score_won = [0, 0]


def apply_score(won: bool, close: bool = False):
    if manager.get_user() and manager.get_user().connected() and score_won != [0, 0]:
        manager.start_new_game()
        manager.commit_new_set(GAME_UUID, won, score_won[0], score_won[1], other="advent={:.1f}".format(100-(numberof_tile/2)/numberof_duo*100))
    if close:
        root.destroy()
        sys.exit()


root.protocol("WM_DELETE_WINDOW", lambda: apply_score(False, True))
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
        elif first_guess.i == self.i:  # good guess
            score_won[0] += score_winnable[levelvar.get()][0]
            score_won[1] += score_winnable[levelvar.get()][1]
            numberof_tile -= 1
            tile_to_discover_lbl.config(text=f"Number of tile \n to discover : {numberof_tile}")
            number_of_guess_lbl.config(text=f"Number of guess : {number_of_guess}")
            print("oui")
            print(f"{numberof_tile},{numberof_duo}")
            advancement_lbl.config(text="Advancement : {:.1f} %".format(100-(numberof_tile/2)/numberof_duo*100))
            if numberof_tile == 0:
                Label(grid_frame, text="Win !", font=winfont, fg='green', bg='#FFFFFF').place(relx=0.5, rely=0.5, anchor=CENTER)
                apply_score(True)
        else:  # bad guess
            score_won[0] -= score_worth[levelvar.get()][0]
            score_won[1] -= score_worth[levelvar.get()][1]
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
levelvar = IntVar()

for x in range(len(rb)):
    r = Radiobutton(level_frame, text=rb[x][0], font=(12,), variable=levelvar, value=rb[x][1])
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
