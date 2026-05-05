from dice.roller import roll_dice
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from utils.helpers import get_asset
from gui.character_tab import CharacterTab
from gui.spells_tab import SpellsTab
from gui.MonstersTab import MonstersTab


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("Logo-darkbg.ico")
        self.title("D&D Toolkit")
        self.geometry("900x600")

        # Logo
        logo = CTkImage(
            light_image=Image.open("Logo-darkbg.png"),
            dark_image=Image.open("Logo-transparent.png"),
            size=(40,40)
        )

        # Tab Navigation
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        # Added Tabs
        self.tabs.add("Characters")
        self.tabs.add("Spells")
        self.tabs.add("Monsters")
        self.tabs.add("Dice Roller")

        CharacterTab(self.tabs.tab("Characters"))
        DiceTab(self.tabs.tab("Dice Roller"))
        SpellsTab(self.tabs.tab("Spells"))
        MonstersTab(self.tabs.tab("Monsters"))

class DiceTab:
    def __init__(self, parent):
        """ Defines the structure of the dice roller tab """
        self.selected_die = 20
        self.count = 1
        self.modifier = 0

        # Tab division in left and right
        self.left_frame = ctk.CTkFrame(parent)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.right_frame = ctk.CTkFrame(parent)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Display of dice buttons
        dice_types = [2, 4, 6, 8, 10, 12, 20, 100]
        self.dice_buttons = {}
        for i, die in enumerate(dice_types):
            icon = ctk.CTkImage(light_image=Image.open(get_asset(f"d{die}.png")), size=(60,60))
            btn = ctk.CTkButton(
                self.left_frame, text="", image=icon,
                width=70, height=70, fg_color="transparent",
                command=lambda d=die: self.select_die(d)
            )
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.dice_buttons[die] = btn

        # Amount of dice setting
        ctk.CTkLabel(self.left_frame, text="Amount").grid(row=3, column=0, pady=10)
        self.count_entry = ctk.CTkEntry(self.left_frame, width=50, justify="center")
        self.count_entry.insert(0, "1")
        self.count_entry.grid(row=3, column=2)
        ctk.CTkButton(self.left_frame, text="-", width=40, command=self.decrease_amount).grid(row=3, column=1, sticky="ew")
        ctk.CTkButton(self.left_frame, text="+", width=40, command=self.increase_amount).grid(row=3, column=3, sticky="ew")

        # Modifier setting
        ctk.CTkLabel(self.left_frame, text="Modifier").grid(row=4, column=0, pady=10)
        ctk.CTkButton(self.left_frame, text="-", width=40, command=self.decrease_mod).grid(row=4, column=1, sticky="ew")
        self.mod_entry = ctk.CTkEntry(self.left_frame, width=50, justify="center")
        self.mod_entry.insert(0, "0")
        self.mod_entry.grid(row=4, column=2)
        ctk.CTkButton(self.left_frame, text="+", width=40, command=self.increase_mod).grid(row=4, column=3, sticky="ew")

        # Result history on the right side of the tab
        self.history_box = ctk.CTkTextbox(self.right_frame, width=300, font=("Arial", 16))
        self.history_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.history_box.configure(state="disabled")    # Read only Toggle

        # Roll the dice button
        self.left_frame.grid_rowconfigure(5, weight=1)
        self.left_frame.grid_rowconfigure(6, weight=1)
        roll_button = ctk.CTkButton(
            self.left_frame,
            text="🎲 Roll",
            font=("Arial", 20),
            command=self.roll_click
        )
        roll_button.grid(row=5, column=1, columnspan=4, rowspan=2, padx=10, pady=20, sticky="nsew")

        # Clear Text Box
        clear_button = ctk.CTkButton(
            self.left_frame,
            text="Clear",
            command=self.clear_click
        )
        clear_button.grid(row=7, column=1, columnspan=4, padx=10, pady=20, sticky="nsew")

        self.select_die(20) # Default option

    def decrease_amount(self):
        try:
            current = int(self.count_entry.get())
        except ValueError:
            current = 1
        if current > 1:
            current -= 1
        self.count_entry.delete(0, "end")
        self.count_entry.insert(0, str(current))

    def increase_amount(self):
        try:
            current = int(self.count_entry.get())
        except ValueError:
            current = 1
        current += 1
        self.count_entry.delete(0, "end")
        self.count_entry.insert(0, str(current))

    def decrease_mod(self):
        try:
            mod_current = int(self.mod_entry.get())
        except ValueError:
            mod_current = 0
        mod_current -= 1
        self.mod_entry.delete(0, "end")
        self.mod_entry.insert(0, str(mod_current))

    def increase_mod(self):
        try:
            mod_current = int(self.mod_entry.get())
        except ValueError:
            mod_current = 0
        mod_current += 1
        self.mod_entry.delete(0, "end")
        self.mod_entry.insert(0, str(mod_current))

    def select_die(self, die):
        self.selected_die = die
        for d, btn in self.dice_buttons.items():
            if d == die:
                btn.configure(fg_color="#1f6aa5") # 1f6aa5 (Blue)
            else:
                btn.configure(fg_color="transparent")

    def add_to_history(self, text):
        self.history_box.configure(state="normal")
        self.history_box.tag_remove("latest", "1.0", "end")
        self.history_box.insert("0.0", text + "\n\n") #0.0 for Top of history, end for bottom
        lines = text.count("\n") + 1
        self.history_box.tag_add("latest", "1.0", f"{lines +1}.0")
        self.history_box.tag_config("latest", foreground="#1f6aa5")

        self.history_box.configure(state="disabled")

    def roll_click(self):
        try:
            dice_amount = int(self.count_entry.get())
            roll_modifier = int(self.mod_entry.get())
        except ValueError:
            self.add_to_history("Invalid input!")
            return
        dice_type = self.selected_die
        notation = f"{dice_amount}d{dice_type}"
        if roll_modifier > 0:
            notation += f"+{roll_modifier}"
        elif roll_modifier < 0:
            notation += str(roll_modifier)
        result = roll_dice(notation)
        self.add_to_history(f"{notation}\nRolls: {result['rolls']}\nTotal: {result['total']}")

    def clear_click(self):
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        self.history_box.configure(state="disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()