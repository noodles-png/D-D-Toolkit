import requests

class DnDApiClient:
    BASE_URL = "https://www.dnd5eapi.co/api/2014"


    def __init__(self):
        self.session = requests.Session()


    def get_all_spells(self):
        response = self.session.get(f"{self.BASE_URL}/spells")
        data = response.json()
        return [item["index"] for item in data["results"]]


    def get_spell(self, spell_choice):
        response = self.session.get(f"{self.BASE_URL}/spells/{spell_choice}")
        return response.json()


    def get_all_items(self):
        response = self.session.get(f"{self.BASE_URL}/equipment")
        data = response.json()
        return [item["index"] for item in data["results"]]


    def get_item(self, item_choice):
        response = self.session.get(f"{self.BASE_URL}/equipment/{item_choice}")
        return response.json()


    def get_monster(self, api_index):
        response = self.session.get(f"{self.BASE_URL}/monsters/{api_index}")
        return response.json()


    def get_all_monsters(self):
        response = self.session.get(f"{self.BASE_URL}/monsters")
        data = response.json()
        return [monster["index"] for monster in data["results"]]


    def get_all_classes(self):
        response = self.session.get(f"{self.BASE_URL}/classes")
        data = response.json()
        return [item["index"] for item in data["results"]]


    def get_class(self, api_index):
        response = self.session.get(f"{self.BASE_URL}/classes/{api_index}")
        return response.json()


    def get_all_races(self):
        response = self.session.get(f"{self.BASE_URL}/races")
        data = response.json()
        return [race["index"] for race in data["results"]]


    def get_race(self, race_index):
        response = self.session.get(f"{self.BASE_URL}/races/{race_index}")
        return response.json()


if __name__ == '__main__':
    pass