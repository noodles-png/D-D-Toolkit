import os
import customtkinter as ctk

def get_asset(filename):
    return os.path.join(os.path.dirname(__file__), "..", "assets", filename)

def get_modifier(value):
    """ Returns the calculated modifier based on the ability score """
    value = int(value)
    modifier = round((value - 10) // 2)
    return modifier

def get_prof_bonus(level):
    """ Returns the proficiency bonus based on character level """
    level = int(level)
    prof_bonus = (level // 4) + 1
    return prof_bonus

def get_spell_dc(prof_bonus, stat_modifier):
    """ Returns the spell difficulty check
     Args:
         prof_bonus: proficiency bonus calculated from get_prof_bonus
         stat_modifier: Ability score modifier calculated from get_modifier
     Returns:
         spell_dc: integer
     """
    spell_dc = 8 + prof_bonus + stat_modifier
    return spell_dc

def CollapsibleSection():
    """ Open/Closes Widget via Button CLick """
    pass

# TODO Adjust code!!!
# Code from https://github.com/TomSchimansky/CustomTkinter/blob/master/examples/scrollable_frame_example.py
class Overview_Frame(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):   # **kwargs for not yet defined var
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label = ctk.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = ctk.CTkButton(self, text="Command", width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return


