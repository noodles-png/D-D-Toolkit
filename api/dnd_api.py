import requests



def get_all_spells():
    response = requests.get(f"https://www.dnd5eapi.co/api/2014/spells")
    data = response.json()
    return [item["index"] for item in data["results"]]


def get_spell(spell_choice):
    response = requests.get(f"https://www.dnd5eapi.co/api/2014/spells/{spell_choice}")
    return response.json()








if __name__ == '__main__':
    indices = get_all_spells()
    print(f"Gefunden: {len(indices)} Zauber")
    print(indices[:5])