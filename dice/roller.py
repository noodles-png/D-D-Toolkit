import re
import random

def roll_dice(notation: str) -> dict:
    """ Rolls a dice

    Args: notation based on D&D notation like '2d6+2'
    Returns:
        dict with keys 'rolls' (list of individual rolls),
        'modifier'(int) and 'total' (int)
    """

    pattern = r"(\d+)?[dD](\d+)([+-]\d+)?"
    match = re.fullmatch(pattern, notation)

    if not match:
        raise ValueError(f"Invalid notation: {notation}")

    num_dice = int(match.group(1)) if match.group(1) else 1
    dice_type = int(match.group(2))
    dice_mod = int(match.group(3)) if match.group(3) else 0

    # TODO: compare with other randomizer (numpy e.g.)
    rolls = [random.randint(1, dice_type) for _ in range(num_dice)]
    total = sum(rolls) + dice_mod

    return dict(rolls=rolls, modifier=dice_mod, total=total)




