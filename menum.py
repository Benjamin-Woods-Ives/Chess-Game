import tkinter as tk
import pickle


class MainMenu(tk.Toplevel):
    """tkinter window used to display the menu of the game"""
    def __init__(self, parent, height):
        super().__init__()
        self.load_save_in_progress = False
        self.in_progress = False
        self.parent = parent
        self.load_save = tk.Toplevel(self)
        self.load_save.iconbitmap("icon.ico")
        self.load_save.configure(bg="#4a4b4d")
        self.spacer1 = tk.Button(self.load_save, bg="#404040", width=26, relief="flat", state="disabled")
        self.spacer2 = tk.Button(self.load_save, bg="#404040", width=26, relief="flat", state="disabled")
        self.save_frame = SaveFrame(self, self.load_save)
        self.load_frame = LoadFrame(self, self.load_save)
        self.scroll_frame = ScrollFrame(self.load_frame, self.load_save)
        self.load_save.withdraw()
        self.geometry("+"+height+"+300")
        self.load_save.geometry("+"+str(int(height)-200)+"-395")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.load_save.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.title("Benji's Chess")
        self.iconbitmap("icon.ico")
        self.resizable(0, 0)
        self.configure(bg="#4a4b4d")
        self.buttons = []
        self.width = 25
        self.height = 2
        self.font = "arial"

        self.spacer_header = tk.Button(self, width=self.width+10, height=self.height-1, bg="#404040",
                                       relief="flat", state="disabled")
        self.new_game_button = tk.Button(self, text="New", width=self.width, height=self.height, relief="groove",
                                         bg="#4a4b4d", fg="#ffffff", font=self.font, command=self.new_game)
        self.save_game_button = tk.Button(self, text="Save", width=self.width, height=self.height, relief="groove",
                                          bg="#4a4b4d", fg="#ffffff", font=self.font, command=self.save)
        self.load_game_button = tk.Button(self, text="Load", width=self.width, height=self.height, relief="groove",
                                          bg="#4a4b4d", fg="#ffffff", font=self.font, command=self.load)
        self.reset_game_button = tk.Button(self, text="Reset", width=self.width, height=self.height, relief="groove",
                                           bg="#4a4b4d", fg="#ffffff", font=self.font, command=self.reset)
        self.undo_button = tk.Button(self, text="Undo", width=self.width, height=self.height, relief="groove",
                                     bg="#4a4b4d", fg="#ffffff", font=self.font, command=self.undo)
        self.Quit_button = tk.Button(self, text="Quit", width=self.width, height=self.height, relief="groove",
                                     bg="#4a4b4d", fg="#ffffff", font=self.font, command=self.quit_game)
        self.space_footer = tk.Button(self, width=self.width+10, height=self.height-1, bg="#404040",
                                      relief="flat", state="disabled")
        self.grid()
        self.mainloop()

    def on_exit(self):
        self.parent.on_exit()

    def new_game(self):
        """creates a new game"""
        if self.in_progress is False:
            self.in_progress = True
            self.parent.gui.deiconify()
            self.parent.game_start()

    def quit_game(self):
        """quits the game"""
        self.parent.end_game()
        self.parent.gui.destroy()
        self.destroy()
        quit()

    def undo(self):
        """undos a move in the game"""
        if self.in_progress is True:
            if len(self.parent.undo.all_moves_made) != 0:
                self.parent.reset_turn_state()
                self.parent.undo.undo_move()
                self.parent.moves_update()
                self.parent.tiles_update()
                self.parent.next_turn()
                self.parent.gui.update()

    def reset(self):
        """resets the game by going through the entire undo stack"""
        if self.in_progress is True:
            while len(self.parent.undo.all_moves_made) != 0:
                self.undo()

    def save(self):
        """saves the game"""
        if self.in_progress is True:
            if self.load_save_in_progress is False:
                self.load_save_in_progress = "saving"
                self.spacer1.pack()
                self.save_frame.pack()
                self.spacer2.pack()
                self.load_save.update()
                self.load_save.deiconify()
            else:
                self.end_load()
                self.save()

    def end_load(self):
        self.load_frame.grid_forget()
        self.spacer1.grid_forget()
        self.spacer2.grid_forget()
        self.load_frame.menu.scroll_frame.grid_forget()
        self.load_save.withdraw()
        self.load_frame.reset_key()
        self.load_frame.update()
        self.load_save_in_progress = False

    def end_save(self):
        self.save_frame.pack_forget()
        self.spacer1.pack_forget()
        self.spacer2.pack_forget()
        self.load_save.withdraw()
        self.save_frame.reset_key()
        self.save_frame.update()
        self.load_save_in_progress = False

    def saving(self, save_name):
        if self.parent.saves.check_name(save_name) is True:
            to_save = self.parent.piece_board.board
            pickled = pickle.dumps(to_save)
            undo_pickled = pickle.dumps(self.parent.undo.all_moves_made)
            self.parent.saves.add_save(save_name, pickled, undo_pickled)
            return True

    def load(self):
        """loads the game"""
        if self.load_save_in_progress is False:
            self.load_save_in_progress = "loading"
            save_names = self.parent.saves.get_names()
            for name in range(len(save_names)):
                str_name = "".join(save_names[name])
                save_names[name] = str_name
            self.spacer1.grid(row=0, column=0)
            self.load_frame.grid(row=1, column=0)
            self.scroll_frame.grid(row=2, column=0)
            self.spacer2.grid(row=3, column=0)
            self.scroll_frame.labels(save_names)
            self.load_save.update()
            self.load_save.deiconify()
        else:
            self.end_save()
            self.load()

    def loading(self, load_name):
        if self.parent.saves.check_name(load_name) is False:
            to_load, to_load_undo = self.parent.saves.get_data(load_name)
            un_pickled = pickle.loads(to_load)
            un_pickled_undo = pickle.loads(to_load_undo)
            self.parent.piece_board.update_entire_board(un_pickled)
            self.parent.undo.update_move_stack(un_pickled_undo)
            return True

    def grid(self):
        """grids all the buttons objects onto the window"""
        self.spacer_header.grid(row=0)
        self.new_game_button.grid(row=1)
        self.save_game_button.grid(row=2)
        self.load_game_button.grid(row=3)
        self.reset_game_button.grid(row=4)
        self.undo_button.grid(row=5)
        self.Quit_button.grid(row=6)
        self.space_footer.grid(row=7)


class SaveFrame(tk.Frame):
    def __init__(self, menu, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg="#4a4b4d")
        self.menu = menu
        self.key = ""
        self.font = "arial"
        self.save_in_progress = False
        self.a = tk.Label(self, text="save as", bg="#4a4b4d", fg="#ffffff", font=self.font)
        self.b = tk.Entry(self, justify="center", borderwidth=0)
        self.b = tk.Entry(self, justify="center")
        self.b.bind("<Key>", self.key_input)
        self.c = tk.Button(self, text="Save", font=(self.font, 10), relief="groove",
                           bg="#4a4b4d", fg="#ffffff", command=self.save_game)
        self.a.pack()
        self.b.pack()
        self.c.pack()

    def save_game(self):
        if self.menu.saving(self.key) is True:
            self.menu.end_save()

    def key_input(self, event):
        self.b.delete(0, "end")
        self.b.insert("end", self.key)
        self.update()
        if (48 <= event.keycode <= 57) or event.keycode == 32:
            self.key = self.key + event.char
        elif 65 <= event.keycode <= 90:
            self.key = self.key + event.char
        elif 97 <= event.keycode <= 122:
            self.key = self.key + event.char
        elif event.keycode == 8:
            self.key = self.key[:-1]

    def reset_key(self):
        self.key = ""


class LoadFrame(tk.Frame):
    def __init__(self, menu, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.menu = menu
        self.key = ""
        self.font = "arial"
        self.configure(bg="#4a4b4d")
        self.a = tk.Label(self, text="Load as", bg="#4a4b4d", fg="#ffffff", font=self.font)
        self.b = tk.Entry(self, justify="center", borderwidth=0)
        self.b.bind("<Key>", self.key_input)
        self.c = tk.Button(self, text="Load", font=(self.font, 10), relief="groove",
                           bg="#4a4b4d", fg="#ffffff", command=self.on_button_press)
        self.a.pack()
        self.b.pack()
        self.c.pack()

    def on_button_press(self):
        if self.menu.loading(self.key) is True:
            if self.menu.in_progress is False:
                self.menu.new_game()
            self.grid_forget()
            self.menu.scroll_frame.grid_forget()
            self.menu.load_save.withdraw()
            self.reset_key()
            self.update()
            self.menu.load_save_in_progress = False

    def key_input(self, event):
        self.b.delete(0, "end")
        self.b.insert("end", self.key)
        self.update()
        if event.keycode == 13:
            self.on_button_press()
        elif (48 <= event.keycode <= 57) or event.keycode == 32:
            self.key = self.key + event.char
            self.update_search()
        elif 65 <= event.keycode <= 90:
            self.key = self.key + event.char
            self.update_search()
        elif 97 <= event.keycode <= 122:
            self.key = self.key + event.char
            self.update_search()
        elif event.keycode == 8:
            self.key = self.key[:-1]
            self.update_search()

    def reset_key(self):
        self.key = ""

    def update_search(self):
        save_names = self.menu.parent.saves.get_names()
        for name in range(len(save_names)):
            str_name = "".join(save_names[name])
            save_names[name] = str_name
        key_in_name = []
        for name in save_names:
            if self.key in name:
                key_in_name.append(name)
        self.menu.scroll_frame.labels(key_in_name)

    def update_key(self, name):
        self.key = name


class ScrollFrame(tk.Frame):
    def __init__(self, load_frame, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.load = load_frame
        self.label_objects = []
        self.text = ""
        self.configure(bg="#4a4b4d")
        self.canvas = tk.Canvas(self, width=150, height=200)
        self.canvas.configure(bg="#4a4b4d", highlightcolor="#4a4b4d", highlightbackground="#4a4b4d", borderwidth=10)
        self.canvas.grid(row=0, column=0)
        self.scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
        self.scrollbar.configure(bg="#4a4b4d", borderwidth=0)
        self.canvas.configure(yscrollcommand=self.scrollbar.set, scrollregion=(0, 0, 150, 200))
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.interior = tk.Frame(self.canvas)
        self.interior.configure(bg="#4a4b4d", highlightcolor="#4a4b4d", highlightbackground="#4a4b4d", borderwidth=0)
        self.interior.bind('<Configure>', self.update_scroll)
        self.canvas.create_window((0, 0), window=self.interior, anchor='nw')

    def labels(self, array):
        for b in self.label_objects:
            b.grid_forget()
        for a in array:
            index = array.index(a)
            try:
                self.label_objects[index].config(text=a)
                self.label_objects[index].grid(row=index, column=2)
            except IndexError:
                temp = tk.Label(self.interior, text=a, anchor="w", justify="left", width=17, relief="groove",
                                bg="#4a4b4d", fg="#ffffff", font="arial")
                temp.bind("<Button-1>", self.update_label)
                temp.grid(row=index, column=2)
                self.label_objects.append(temp)

    def update_scroll(self, event):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.configure(scrollregion=(0, 0, w, h))

    def update_label(self, event):
        self.text = event.widget.cget("text")
        self.load.update_key(self.text)
        self.load.b.delete(0, "end")
        self.load.b.insert("end", self.text)


if __name__ == '__main__':
    pass

