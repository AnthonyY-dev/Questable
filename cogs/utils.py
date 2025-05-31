import math

def calculateLevel(xp: float) -> int:
    level = 1
    cumulative_xp = 0

    while True:
        xp_for_next_level = 50 * (1.03 ** (level - 1))
        if xp < cumulative_xp + xp_for_next_level:
            break
        cumulative_xp += xp_for_next_level
        level += 1

    return level