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


class CollapsibleSection:
    """ """
    def __init__(self, parent, title):
        self.title = title
        self.is_open = False

        self.header_btn = ctk.CTkButton(parent, text=f"▶ {title}", command=self.toggle_button, fg_color="#222222")
        self.header_btn.pack(fill="x", pady=2)

        self.content = ctk.CTkFrame(parent)

    def toggle_button(self):
        self.is_open = not self.is_open

        if self.is_open:
            self.content.pack(fill="x", after=self.header_btn)
            self.header_btn.configure(text=f"▼ {self.title}")
        else:
            self.content.pack_forget()
            self.header_btn.configure(text=f"▶ {self.title}")










