import tkinter as tk
from tkinter import simpledialog
import time
import threading
from components.board import Board 
from components.globals import H1, BUTTONS, TABOO, DIRECTIONS

class Sequence:
    """ 
        Lets users graphically view a Sokoban warehouse,
        and either play the game, or watch a sequence of moves
        provided by text in a list.
    """
    def __init__(self, root: tk.Tk, path: str):
        self.path = path
        self.root = root
        self.root.focus_force()
        self.root.title("SKBN - Sequence Player Tool")
        wh_name = (path.split('/')[-1]).split('.txt')[0]
        tk.Label(self.root, text=f"Sequencer for {wh_name}", font=H1).pack(side=tk.TOP, pady=(10, 0))
        self.moves = []
        self.moves_index = 0
        self.player_status = tk.StringVar(); self.player_status.set("Play")
        self.sleep = tk.DoubleVar(); self.sleep.set(50)
        self.set_content()
        self.set_keybinds(True)
        self.root.mainloop()

    def set_sleep_speed(self) -> None:
        """ Ask user to enter speed value for animation. """
        prior = self.sleep
        self.sleep = simpledialog.askfloat("Change Speed", "Enter sleep time (ms): ", minvalue=0, maxvalue=3)
        self.sleep = self.sleep if self.sleep != None else prior

    def set_content(self) -> None:
        """ 
            Adds the board to view (in button form), 
            and the text visualizer on the right hand side.
        """
        self.impossible_status = tk.StringVar(); self.impossible_status.set("")
        self.impossible_alert = tk.Label(self.root, fg="red", 
                                         textvariable=self.impossible_status).pack(side=tk.TOP)
        
        # Add options to either manually move the player, or by sequence
        self.mode = tk.IntVar(); self.mode.set(0)

        self.playView = tk.Frame(self.root)
        self.manualMode = tk.Radiobutton(
            self.playView, text="Manual (WASD)", variable=self.mode, 
            value=0, command=self.change_mode).pack(side=tk.LEFT)
        self.sequenceMode = tk.Radiobutton(
            self.playView, text="Sequence", variable=self.mode, 
            value=1, command=self.change_mode).pack(side=tk.LEFT)
        self.toEndButton = tk.Button(
            self.playView, text=">>", state=tk.DISABLED, 
            command=self.animate_directions); self.toEndButton.pack(side=tk.RIGHT)
        self.nextButton = tk.Button(
            self.playView, text=">", state=tk.DISABLED, 
            command=self.perform_next_direction); self.nextButton.pack(side=tk.RIGHT)
        self.playButton = tk.Button(
            self.playView, text=f"{self.player_status.get()} ⏯️", state=tk.DISABLED, width=7, 
            command=self.play_pause); self.playButton.pack(side=tk.RIGHT)
        self.beginButton = tk.Button(
            self.playView, text="Click to load", state=tk.DISABLED, 
            command=self.load_directions); self.beginButton.pack(side=tk.RIGHT)
        self.playView.pack(side=tk.TOP, expand=True, fill=tk.X)
        
        # Add the board and copy result functionalities
        self.text_field = tk.Text(self.root)
        self.text_field.insert(tk.END, 
                "Manual mode is enabled.\n\n" + \
                "This means that you can use your arrow keys, " + \
                "or your WASD keys to move the player around.")
        self.board = Board(self.root, self.path, side=tk.LEFT, text_field=self.text_field)
        self.text_field.config(width=self.board.wh.ncols + 5, height=10, state=tk.DISABLED)
        self.text_field.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.status = tk.StringVar(); self.status.set("")
        tk.Label(self.root, text="", textvariable=self.status, bg="white").pack(fill=tk.X)
        tk.Button(self.root, text="Copy Moves", 
                  command=lambda:self.to_clipboard(text=repr(self.moves))).pack(fill=tk.X)
        tk.Button(self.root, text="Copy Result", 
                  command=lambda:self.to_clipboard(
                      text=self.impossible_status.get() 
                      if self.impossible_status.get() != "" 
                      else self.board.__repr__())).pack(fill=tk.X)
        
    def change_mode(self) -> None:
        # Sequence mode is #1 or True
        sequence_mode = bool(self.mode.get())
        self.beginButton.config(state=tk.NORMAL if sequence_mode else tk.DISABLED)
        for tkobj in [self.toEndButton, self.nextButton, self.playButton]:
            tkobj.config(state=tk.DISABLED)

        # Pre-add a slider to change speed of animation
        if sequence_mode: 
            self.slider = tk.Scale(self.root, variable=self.sleep, from_=1, to=100, orient=tk.HORIZONTAL)
            self.slider.place(x=0, y=self.root.winfo_height(), anchor=tk.SW)
        else: self.slider.destroy()
        
        # Enable or disable keybinds
        self.set_keybinds(not sequence_mode)

        # Clear prior variables
        self.moves = []
        self.impossible_status.set("")
        self.player_status.set("Play")

        # Clear textbox and put tutorial text
        text = ("Paste in your moves here, and click \"Click to load\".\n\n" + \
                "Click play or next to start animation.\n" + \
                "You can click ⏯️¸ to play/pause whenever, " + \
                "> to go next when paused, " + \
                "or >> to skip to the very end." 
                if sequence_mode else
                "Manual mode is enabled.\n\n" + \
                "This means that you can use your arrow keys, " + \
                "or your WASD keys to move the player around.")
        self.text_field.config(state=tk.NORMAL)
        self.text_field.delete('1.0', tk.END)
        self.text_field.insert(tk.END, text)
        if not sequence_mode: self.text_field.config(state=tk.DISABLED)

    def set_keybinds(self, on: bool) -> None:
        """ Adds or removes keybinds for manual player movement. """
        bindings = {
            "w": "Up", "s": "Down", "a": "Left", "d": "Right", # wasd direction keys
            "<Up>": "Up", "<Down>": "Down", "<Left>": "Left", "<Right>": "Right" # arrow keys
        } 
        for key in bindings: 
            if on: self.root.bind(key, lambda e, d=bindings[key]: self.key_event(d))
            else: self.root.unbind(key)

    def key_event(self, d) -> None:
        """ Handle request to move the player by a direction. """
        map = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0),
        }
        result = self.board.try_tile_shift(map[d])
        if not result: self.impossible_status.set("Impossible!")
        if self.mode.get() == 0: 
            self.moves.append(d)
            self.board.update_text_field(repr(self.moves))

    def load_directions(self) -> None:
        """ 
            Takes the string value from the textbox and attempts
            to store it as a list of moves in self.moves.
            If valid, animation buttons are made usable to the user.
            Otherwise, if an invalid move/direction is found, the
            user is given a red error message with an invalid direction. 
        """
        text = self.text_field.get("1.0", tk.END)
        
        # First strip unwanted characters from the raw text
        for char in ["\n", " ", "[", "]", "\"", "\'"]:
            text = text.replace(char, "")

        # Check for any invalid directions
        self.moves = text.split(",")
        self.moves_index = 0
        for direction in self.moves: 
            if direction not in DIRECTIONS.keys():
                prior_status = self.impossible_status.get()
                self.impossible_status.set(f"Invalid action -> {direction}"); 
                self.root.update(); time.sleep(0.5)
                self.impossible_status.set(prior_status)
                return        
            
        # Permit user to use the animation buttons now & choose animation speed
        for tkobj in [self.toEndButton, self.nextButton, self.playButton]:
            tkobj.config(state=tk.NORMAL)

    def perform_next_direction(self) -> None:
        """ 
            Moves the player tile (and any other effected tile)
            according to the direction found by indexing the moves list
            by the moves index.
            Moves index is then updated to the next index.
        """
        self.key_event(self.moves[self.moves_index])
        self.moves_index += 1

    def play_pause(self) -> None:
        """ 
            Handle toggling of the play animation. Toggles between 'Pause' and 'Play'. 
            If the animation is in a state of 'Play', user can toggle the play button
            to interrupt or pause the animation.

            Use threading to play the animation and allow state of the animation player
            to interupt the animation loop.
        """
        status = self.player_status.get()
        if status == "Play": 
            t = threading.Thread(
                target=lambda: self.animate_directions(sleep=True, conditional=True), daemon=True
            ).start()
        self.player_status.set("Pause" if status == "Play" else "Play")
        self.playButton.config(text=f"{self.player_status.get()} ⏯️")

    def animate_directions(self, sleep=False, conditional=False) -> None:
        """
            Iterates over the list of moves until finished or interrupted.
            A sleep parameter can be provided for the amount of time to rest in
            between moves. A conditional parameter can be provided as an option
            to break out of the animation if the play button is set to pause.

            By default, the sleep is set False, and there is no interruption clause.
            This means that by default, this function graphically appears to skip to 
            the end after all moves have been taken by the player.
        """
        while (self.moves_index < len(self.moves)):
            if sleep: time.sleep(self.sleep.get()/50)
            if (conditional and self.player_status.get() != "Pause"): break
            self.perform_next_direction()

    def to_clipboard(self, text: str) -> None:
        """ Clear user clipboard and replace with requested text. """
        self.status.set("Copied!")
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        time.sleep(0.5)
        self.status.set("")