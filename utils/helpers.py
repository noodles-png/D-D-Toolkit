import os

def get_asset(filename):
    return os.path.join(os.path.dirname(__file__), "..", "assets", filename)

def get_modifier(value):
    """ Returns the calculated modifier based on the ability score """
    value = int(value)
    modifier = round((value - 10) // 2)
    return modifier