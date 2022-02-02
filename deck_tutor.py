import tkinter as tk
import tkinter.font as font
import tutor
import os.path
from tkinter import ttk
import tkinter.filedialog
from tkinter import Menu


class MenuCustom(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        file_menu = Menu(self, tearoff=0)
        file_menu.add_command(label="Exit", underline=1, command=self.quit)
        self.add_cascade(label="File", underline=0, menu=file_menu)

        help_menu = Menu(self, tearoff=0)
        help_menu.add_command(label="About", underline=0, command=self.help)
        self.add_cascade(label="Help", underline=0, menu=help_menu)

    @staticmethod
    def help():
        print("test")


class FormatFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.checkbox_variables = [tk.IntVar(), tk.IntVar(
        ), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]

        self.label = ttk.Label(self, text="Formats")

        self.standard_checkbox = ttk.Checkbutton(self,
                                                 text="  Standard",
                                                 variable=self.checkbox_variables[0])
        self.modern_checkbox = ttk.Checkbutton(self,
                                               text="  Modern",
                                               variable=self.checkbox_variables[1])
        self.pioneer_checkbox = ttk.Checkbutton(self,
                                                text="  Pioneer",
                                                variable=self.checkbox_variables[2])
        self.pauper_checkbox = ttk.Checkbutton(self,
                                               text="  Pauper",
                                               variable=self.checkbox_variables[3]
                                               )
        self.legacy_checkbox = ttk.Checkbutton(self,
                                               text="  Legacy",
                                               variable=self.checkbox_variables[4])
        self.vintage_checkbox = ttk.Checkbutton(self,
                                                text="  Vintage",
                                                variable=self.checkbox_variables[5])

        self.path_label = ttk.Label(self, text="Download path")
        self.path_label.grid(column=0, row=0, sticky="w", pady=(0, 18))
        self.standard_checkbox.grid(column=0, row=1, sticky="w")
        self.modern_checkbox.grid(column=0, row=2,  sticky="w")
        self.pioneer_checkbox.grid(column=0, row=3, sticky="w")
        self.pauper_checkbox.grid(column=0, row=4,  sticky="w")
        self.legacy_checkbox.grid(column=0, row=5, sticky="w")
        self.vintage_checkbox.grid(column=0, row=6,  sticky="w")


class PathFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test = tk.StringVar()
        self.test.set(tutor.getPath())
        self.path_text = tk.Text(self, height=1)
        self.path_text.insert("1.0", self.test.get())
        self.path_text.config(state="disabled")
        self.path_button = ttk.Button(
            self, text="...", width=3, command=self.changeDir)

        self.path_text.grid(column=0, row=0, sticky="new")
        self.path_button.grid(column=1, row=0, sticky="e", padx=(10, 0))

    def changeDir(self):
        self.test.set(os.path.normpath(os.path.join(tk.filedialog.askdirectory(),
                                                    "Decks")))
        self.path_text.config(state="normal")
        self.path_text.replace("1.0", "end", self.test.get())
        self.path_text.config(state="disabled")
        self.update()


class OutputFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.output_entry = tk.Text(self)
        self.output_entry.config(state="disabled")
        self.control_scroll = ttk.Scrollbar(
            self, orient="vertical", command=self.output_entry.yview)

        self.output_entry["yscrollcommand"] = self.control_scroll.set

        self.output_entry.grid(column=0, row=0, sticky="news")
        self.control_scroll.grid(column=1, row=0, sticky="ns")

    def addText(self, output):
        self.output_entry.config(state="normal")
        self.output_entry.insert("end", output+"\n")
        self.output_entry.config(state="disabled")
        self.output_entry.see("end")
        self.update()


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Deck Tutor")
        self.geometry("800x280")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        font.nametofont("TkDefaultFont").configure(size=12)

        self.menu_bar = MenuCustom(self)
        self.config(menu=self.menu_bar)

        self.main_container = ttk.Frame(self)
        self.main_container.grid(column=0, row=0, sticky="news")
        self.main_container.columnconfigure(0, weight=0)
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(0, weight=1)

        self.container = ttk.Frame(self.main_container)
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=1)

        self.format_frame = FormatFrame(self.main_container)
        self.format_frame.columnconfigure(0, weight=1)

        self.path_frame = PathFrame(self.container)
        self.path_frame.columnconfigure(0, weight=1)

        self.output_frame = OutputFrame(self.container)
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)

        self.button_start = ttk.Button(
            self.main_container, text="Download", command=lambda: callDeckTutor(self))

        self.container.grid(column=1, row=0, sticky="news", padx=10, pady=10)
        self.format_frame.grid(column=0, row=0, sticky="nw",
                               rowspan=2, padx=(10, 0), pady=10)
        self.path_frame.grid(column=0, row=0, sticky="nwe", pady=(0, 10))
        self.output_frame.grid(column=0, row=1, sticky="nwes")
        self.button_start.grid(
            column=1, row=2, sticky="e", padx=10, pady=(0, 10))


def callDeckTutor(self):
    path_download = self.path_frame.test.get()
    wanted_formats = self.format_frame.checkbox_variables
    tutor.deckTutor(path_download, wanted_formats, self.output_frame)


def main():
    root = MainWindow()
    root.mainloop()


if __name__ == "__main__":
    main()