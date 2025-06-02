import tkinter as tk
from components.board import Board 
from components.globals import H1, LEGAL_CHARS

class PasteBoard:
    """ Lets users graphically view a Sokoban warehouse from pasting as string. """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("SKBN - Visualizer Tool")
        tk.Label(self.root, text="Build From Paste", font=H1).pack(side=tk.TOP, pady=(10,0), padx=50)
        self.set_content()
        self.root.mainloop()

    def set_content(self) -> None:
        """ Setup the content section of the pasteboard. """
        self.content = tk.Frame(self.root)
        self.status = tk.StringVar(); self.status.set("")
        self.paste_var = tk.StringVar()
        tk.Label(self.content, text="", textvariable=self.status, fg="red").pack(side=tk.TOP, fill=tk.X)
        tk.Entry(self.content, textvariable=self.paste_var).pack(side=tk.TOP, fill=tk.X)
        tk.Button(self.content, text="Click to load board.", command=self.set_board).pack(side=tk.TOP, fill=tk.X)
        self.boardview = tk.Frame(self.root); self.boardview.pack(side=tk.TOP)
        self.content.pack(side=tk.TOP, fill=tk.X) 

    def set_board(self) -> None:
        """ On click to load board, reads the textbar and attempts to visualize a warehouse. """
        # Make sure that the warehouse is > 1 tile or char
        if len(self.paste_var.get()) <= 1: 
            self.status.set(f"Invalid board.")
            self.content.update()
            return
        
        # Iterate over ever char, and make sure there are only parsable chars
        as_array = self.paste_var.get().replace('\'', '').replace('"', '').split('\\n')
        for char in "".join(as_array):
            if char not in LEGAL_CHARS:
                self.status.set(f"Illegal char '{char}' given.")
                self.content.update()
                return
            
        # Clear the existing board, and add the visualization
        self.status.set(f""); self.content.update()
        self.boardview.destroy(); self.boardview = tk.Frame(self.root); self.boardview.pack(side=tk.TOP)
        board = Board(self.boardview, None, build_warehouse_from_array=as_array)
        self.root.mainloop()