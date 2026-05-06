import customtkinter as ctk
from database.db_manager import DnDDatabase
from utils.helpers import CollapsibleSection

class MonstersTab:
    def __init__(self, parent):
        self.db = DnDDatabase()

        self.left_frame = ctk.CTkScrollableFrame(parent)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.right_frame = ctk.CTkFrame(parent)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.detail_box = ctk.CTkTextbox(self.right_frame, font=("Arial", 14))
        self.detail_box.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_monsters_list()

    def build_monsters_list(self):
        title_names = ["CR 0","CR 1/8","CR 1/4","CR 1/2","CR 1","CR 2","CR 3","CR 4",
                       "CR 5",
                       "CR 6",
                       "CR 7",
                       "CR 8",
                       "CR 9",
                       "CR 10",
                       "CR 11",
                       "CR 12",
                       "CR 13",
                       "CR 14",
                       "CR 15",
                       "CR 16",
                       "CR 17",
                       "CR 18",
                       "CR 19",
                       "CR 20",
                       "CR 21",
                       "CR 22",
                       "CR 23",
                       "CR 24",
                       "CR 30",
                       ]
        self.monster_sections = {}

        for i, title in enumerate(title_names):
            section = CollapsibleSection(self.left_frame, title)
            self.monster_sections[i] = section

        # TODO: Search bar above the spell sections
        """
        ctk.CTkLabel(self.left_frame, text="Spell Overview").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(self.left_frame, text="Search Name").grid(row=1, column=0, padx=10, pady=10)
        """

        for challenge_rating, section in self.monster_sections.items():
            monsters = self.db.get_monster_by_cr(challenge_rating)
            for monster in monsters:
                btn = ctk.CTkButton(
                    section.content,
                    text=monster["monster_name"],
                    command=lambda m=monster: self.show_monster_details(m)
                )
                btn.pack(fill="x", pady=1)

    def show_monster_details(self, monster):
        self.detail_box.configure(state="normal")
        self.detail_box.delete("1.0", "end")
        self.detail_box.insert("1.0",
                               f"{monster['monster_name']}\nChallenge Rating {monster['challenge_rating']} {monster['monster_size']}"
                               f"\n{monster['max_hp']} {monster['monster_type']} {monster['armor_class']}")
        self.detail_box.configure(state="disabled")


        max_hp


        monster_type

        armor_class

