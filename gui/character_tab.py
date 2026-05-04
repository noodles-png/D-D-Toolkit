import customtkinter as ctk
from database.db_manager import DnDDatabase

class CharacterTab:
    STATS = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    STAT_VALUES = [str(i) for i in range(1, 21)]

    def __init__(self, parent):
        self.db = DnDDatabase()
        
        self.left_frame = ctk.CTkFrame(parent)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.right_frame = ctk.CTkFrame(parent)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.editor_tabs = ctk.CTkTabview(self.right_frame)
        self.editor_tabs.pack(fill="both", expand=True)

        self.editor_tabs.add("Overview")
        self.editor_tabs.add("Combat")
        self.editor_tabs.add("Skills")
        self.editor_tabs.add("Spells")
        self.editor_tabs.add("Inventory")

        self.build_basics_tab()
        self.build_combat_tab()
        self.build_character_list()


    def build_character_list(self):
        self.char_list = ctk.CTkScrollableFrame(self.left_frame, width=200)
        self.char_list.pack(fill="both", expand=True)

        for char in self.db.get_all_characters():
            btn = ctk.CTkButton(
                self.char_list,
                text=char["char_name"],
                command=lambda c=char: self.load_character(c)
            )
            btn.pack(fill="x", pady=2)

    def build_basics_tab(self):
        self.tab = self.editor_tabs.tab("Overview")
        self.tab.grid_columnconfigure(1, weight=1)
        self.tab.grid_columnconfigure(3, weight=1)
        levels = [str(i) for i in range(1, 21)]

        # Row 1: Name
        ctk.CTkLabel(self.tab, text="Character").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ctk.CTkEntry(self.tab, width=20)
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky="nsew")

        # Row 2: Class & Level
        ctk.CTkLabel(self.tab, text="Class").grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        classes = [c["class_name"] for c in self.db.get_all_classes()]
        self.class_entry = ctk.CTkComboBox(self.tab, values=classes, width=20)
        self.class_entry.grid(row=1, column=1, sticky="nsew")
        ctk.CTkLabel(self.tab, text="Level").grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.level_entry = ctk.CTkComboBox(self.tab, values=levels, width=10)
        self.level_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        # Row 3: Race
        ctk.CTkLabel(self.tab, text="Race").grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        races = [r["race_name"] for r in self.db.get_all_races()]
        self.race_entry = ctk.CTkComboBox(self.tab, values=races, width=20)
        self.race_entry.grid(row=2, column=1, columnspan=2, sticky="nsew")

        # Row 4-9: Ability Scores
        self.stats_frame = ctk.CTkFrame(self.tab)
        self.stats_frame.grid(row=4, column=0, columnspan=4, pady=10, sticky="w")

        stats_left = self.STATS[:3]
        stats_right = self.STATS[3:]
        self.stat_entries = {}

        for i, stat in enumerate(stats_left):
            ctk.CTkLabel(self.stats_frame, text=stat).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ctk.CTkComboBox(self.stats_frame, values=self.STAT_VALUES, width=70)
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.stat_entries[stat.lower()] = entry

        for i, stat in enumerate(stats_right):
            ctk.CTkLabel(self.stats_frame, text=stat).grid(row=i, column=2, padx=5, pady=5, sticky="w")
            entry = ctk.CTkComboBox(self.stats_frame, values=self.STAT_VALUES, width=70)
            entry.grid(row=i, column=3, padx=5, pady=3)
            self.stat_entries[stat.lower()] = entry

    def build_combat_tab(self):
        self.tab = self.editor_tabs.tab("Combat")

        ctk.CTkLabel(self.tab, text="Max HP").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        maxhp_entry = ctk.CTkEntry(self.tab, width=20)
        maxhp_entry.grid(row=0, column=1, sticky="ew")

        ctk.CTkLabel(self.tab, text="Temp HP").grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        temphp_entry = ctk.CTkEntry(self.tab, width=20)
        temphp_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # AC
        ctk.CTkLabel(self.tab, text="AC").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ac_entry = ctk.CTkEntry(self.tab, width=20)
        ac_entry.grid(row=1, column=1, padx=20, sticky="ew")

        # Proficiency bonus
        ctk.CTkLabel(self.tab, text="Proficiency bonus").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        profbonus_entry = ctk.CTkEntry(self.tab, width=20)
        profbonus_entry.grid(row=2, column=1, padx=20, sticky="ew")

        # Speed
        ctk.CTkLabel(self.tab, text="Speed").grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        speed_entry = ctk.CTkEntry(self.tab, width=20)
        speed_entry.grid(row=3, column=1, padx=20, sticky="ew")

        # Saves
        ctk.CTkLabel(self.tab, text="Saving Throws").grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        for i, stat in enumerate(self.STATS):
            ctk.CTkLabel(self.tab, text=stat).grid(row=5+i, column=0, padx=5, pady=5, sticky="ew")
            stat_entry = ctk.CTkEntry(self.tab, width=20).grid(row=5+i, column=1, padx=5, sticky="ew")
            stat_prof = ctk.CTkCheckBox(self.tab, text="")
            stat_prof.grid(row=5+i, column=2, padx=5, pady=5, sticky="ew")


    def build_skills_tab(self): # TODO Skills mit Prof bonus checkboxen
        pass

    def build_spells_tab(self): # TODO learned spells, spell slots
        pass

    def build_inv_tab(self):    # TODO Inventory & Quantity
        pass


    def load_character(self):
        print(f"Chosen: {char['char_name']}")  # Placeholder

