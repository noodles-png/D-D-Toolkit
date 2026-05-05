import customtkinter as ctk
from database.db_manager import DnDDatabase


class SpellsTab:
    def __init__(self, parent):
        self.db = DnDDatabase()

        self.left_frame = ctk.CTkFrame(parent)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.right_frame = ctk.CTkFrame(parent)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.editor_tabs = ctk.CTkTabview(self.right_frame)
        self.editor_tabs.pack(fill="both", expand=True)

