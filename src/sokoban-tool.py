import tkinter as tk
import os
from components.properties import Properties
from components.globals import VISUALIZE, TABOO, SEQUENCE, H1
from windows.visualize import Visualize
from windows.taboo import Taboo
from windows.sequence import Sequence
from windows.pasteboard import PasteBoard
from windows.buildboard import BuildBoard

class App:
    """
        The main page for the application. 
        From here, users can select a directory which houses their Sokoban games.
        After, the app loads all .txt files into a listbox which users can choose 
        from by double-clicking. 

        Users have the choice of picking a mode, which modify what happens when double-clicking.
        1. Visualize: users can view the Sokoban game in image form.
        2. Taboo: users can click on Sokoban tiles to identify them as taboo.
        3. Sequence: users can play a Sokoban game, or paste in a list of actions to watch.
        4. Paste Board: users can paste a string Sokoban, and visualize it.
        5. Build Board: users can create a new board to add to the list of warehouses.

        To create .exe: pyinstaller --onefile --windowed --add-data "assets;assets" sokoban-tool.py
        Please read the README.md for more general details.
    """
    def __init__(self) -> None:
        self.properties: Properties = Properties()
        self.root: tk.Tk = tk.Tk()
        self.root.title("SKBN")
        self.header = tk.Frame(self.root).pack(side=tk.TOP, fill=tk.X)
        self.body = tk.Frame(self.root).pack(side=tk.TOP, fill=tk.BOTH)
        tk.Label(self.header, text="Sokoban Tool", font=H1).pack(side=tk.TOP, pady=10)
        self.set_logo()
        self.set_searchbar()
        self.set_options()
        self.set_listbox()
        self.root.mainloop()

    def set_logo(self) -> None:
        """ Sets the tkinter window logo to icon.ico. """
        try: 
            path = "\\".join(os.path.realpath(__file__).split('\\')[:-1]) + "\\assets\\icon.ico"
            self.root.iconbitmap(path) # ^ handle path absolutely
        except: pass

    def set_searchbar(self) -> None:
        """ Creates a searchbar for users to seach Sokoban games by name. """
        search = tk.Frame(self.header)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_update_searchbar)
        tk.Label(search, text='Filter: ').pack(side=tk.LEFT)
        tk.Entry(search, textvariable=self.search_var).pack(side=tk.TOP, fill=tk.X)
        search.pack(side=tk.TOP, fill=tk.X)

    def on_update_searchbar(self, var, index, mode) -> None:
        """ 
            Updates listbox, when searchbar is modified, 
            to only show searched Sokoban games by their name. 
        """
        self.current_warehouses = [
            wh for wh in self.warehouses 
            if wh[:len(self.search_var.get())]==self.search_var.get()]
        self.update_listbox()

    def set_options(self) -> None:
        """ 
            Sets the different buttons for users to change the mode.
            When as user double-clicks on a warehouse in listbox,
            what happens next depends on what mode the app is in.
        """
        options = tk.Frame(self.header)
        self.options_var = tk.IntVar(value=1)
        tk.Radiobutton(options, text="Visualize", variable=self.options_var, value=VISUALIZE).pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=(10,0))
        tk.Radiobutton(options, text="Taboo", variable=self.options_var, value=TABOO).pack(side=tk.TOP, anchor=tk.NW, padx=10)
        tk.Radiobutton(options, text="Sequence", variable=self.options_var, value=SEQUENCE).pack(side=tk.TOP, anchor=tk.NW, padx=10)
        tk.Button(options, text="Paste Board", command=lambda: PasteBoard(tk.Toplevel(self.root))).pack(side=tk.BOTTOM, fill=tk.X)
        tk.Button(options, text="Build Board", command=lambda: BuildBoard(tk.Toplevel(self.root))).pack(side=tk.BOTTOM, fill=tk.X)
        options.pack(side=tk.LEFT, fill=tk.Y)

    def set_listbox(self) -> None:
        """
            Lists out all the .txt files found in the current
            directory by name (excluding .txt). 
            A change folder button can be clicked to change the directory.
        """
        listing = tk.Frame(self.header)
        self.listbox = tk.Listbox(listing) 
        self.listbox.bind("<Double-1>", self.click_event_listbox)
        self.update_warehouses()
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        tk.Button(self.header, text="Change Folder", 
                  command=lambda:self.update_warehouses(new_dir=True)
                  ).pack(side=tk.BOTTOM, fill=tk.X)
        listing.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<Button-3>", self.click_event_listbox_right_click)

    def update_warehouses(self, new_dir=False) -> None:
        """
            Loads in all the .txt files from the elected directory
            into the listbox for viewing.
            Can be used to update the chosen directory of .txt files.
        """
        if new_dir: self.properties.gui_select_directory()
        self.warehouses = self.current_warehouses = [
            wh for wh in os.listdir(self.properties.dir_path) 
            if wh.split('.')[-1] == "txt"]
        self.on_update_searchbar(None, None, None)
        self.update_listbox()

    def update_listbox(self) -> None:
        """
            Removes all the entries of .txt files from the listbox
            and repopulates it with the current list of .txt/warehouse files.
            The current list of warehouse files is modified when the searchbar is modified.
        """
        self.listbox.delete(0, tk.END)
        for i, filename in enumerate(self.current_warehouses):
            name = filename.split(".txt")[0]
            self.listbox.insert(i + 1, name)

    def click_event_listbox(self, e) -> None:
        """
            Adds an event listener to the listbox.
            If any row is double-clicked, perform action according to 
            radio option selected on the left-hand-side.
        """
        wh = self.current_warehouses[self.listbox.curselection()[0]]
        path = self.properties.dir_path + "/" + wh
        new_window = tk.Toplevel(self.root)
        if (VISUALIZE == self.options_var.get()): Visualize(new_window, path)
        elif (TABOO == self.options_var.get()): Taboo(new_window, path)
        elif (SEQUENCE == self.options_var.get()): Sequence(new_window, path)

    def click_event_listbox_right_click(self, e):
        """ 
            Adds a an event listener to the listbox.
            If the listbox is right-clicked, an option comes up to refresh it.
            If the user clicks refresh? the listbox refreshes.
        """
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Refresh?", command=self.update_warehouses)
        menu.tk_popup(e.x_root, e.y_root)

if __name__ == "__main__":
    app: App = App()