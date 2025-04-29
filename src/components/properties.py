from tkinter import messagebox
from typing import Dict
from components.globals import SRC_PATH
import os
import json

class Properties:
    """
        Holds app properties, namely the path of the directory where
        all Sokoban warehouse .txt files are currently stored.
        Saves the current directory for future use.
    """
    def __init__(self):
        self.properties_json = SRC_PATH + "\\properties.json"
        print(self.properties_json)
        self.dir_path = None
        self.read_json() 
        
    def read_json(self) -> None:
        """
            Attempts to get the directory path from the properties.json file.
            If there is no properties file, or existing properties path is invalid,
            force user to select a directory.
        """
        if os.path.exists(self.properties_json): 
            with open(self.properties_json) as f:
                content = json.load(f)
            if self.validate_path(content["dir_path"]): 
                self.dir_path = content["dir_path"]
                return
        self.gui_select_directory(new=True) # dir is invalid or properties.json doesn't exist

    def update_json(self, data: Dict[str, str]) -> None:
        """
            Overwrites all json contents with provided dictionary.
        """
        with open(self.properties_json, 'w') as f:
            json.dump(data, f, indent=4)

    def validate_path(self, dir_path: str) -> bool:
        """
            Returns true if a path is valid, otherwise false.
            A path is invalid if it contains no .txt file, or does not exist.
        """
        if not os.path.isdir(dir_path): return False
        for path in os.listdir(dir_path): 
            if path.split('.')[-1] == "txt": return True
        return False

    def gui_select_directory(self, new=False) -> None:
        """
            Triggers tkinter filedialog, which prompts user to choose a directory
            using native os file explorer. If there is no txt file present, error
            and re-force filedialog. Otherwise, update the properties.json file. 
        """
        from tkinter.filedialog import askdirectory
        if new: messagebox.showinfo("Select Directory",
                    "Please select a directory which contains your Sokoban warehouses.")
        while True:
            dir_path = askdirectory() 
            if dir_path == "" and self.dir_path != None: return
            elif not self.validate_path(dir_path):
                messagebox.showerror("Directory error", 
                    "Unable to find a .txt file in this directory. Please select a different directory.")
            else:
                self.dir_path = dir_path
                self.update_json({"dir_path": dir_path})
                return
