import customtkinter as ctk
from database.db_manager import DnDDatabase
from utils.helpers import CollapsibleSection

class SpellsTab:
    def __init__(self, parent):
        self.db = DnDDatabase()

        self.left_frame = ctk.CTkScrollableFrame(parent)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.right_frame = ctk.CTkFrame(parent)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.detail_box = ctk.CTkTextbox(self.right_frame, font=("Arial", 14))
        self.detail_box.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_spells_list()

    def build_spells_list(self):
        title_names = ["Cantrips",
                       "1st Level",
                       "2nd Level",
                       "3rd Level",
                       "4th Level",
                       "5th Level",
                       "6th Level",
                       "7th Level",
                       "8th Level",
                       "9th Level"
                       ]
        self.spell_sections = {}

        for i, title in enumerate(title_names):
            section = CollapsibleSection(self.left_frame, title)
            self.spell_sections[i] = section

        # TODO: Search bar above the spell sections
        """
        ctk.CTkLabel(self.left_frame, text="Spell Overview").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(self.left_frame, text="Search Name").grid(row=1, column=0, padx=10, pady=10)
        """

        for level, section in self.spell_sections.items():
            spells = self.db.get_spells_by_level(level)
            for spell in spells:
                btn = ctk.CTkButton(
                    section.content,
                    text=spell["spell_name"],
                    command=lambda s=spell: self.show_spell_details(s)
                )
                btn.pack(fill="x", pady=1)

    def show_spell_details(self, spell):
        self.detail_box.configure(state="normal")
        self.detail_box.delete("1.0", "end")
        self.detail_box.insert("1.0",
                               f"{spell['spell_name']}\nLevel {spell['spell_level']} {spell['spell_school']}\n\n{spell['description']}")
        self.detail_box.configure(state="disabled")

