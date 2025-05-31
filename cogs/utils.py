import math
from .config import Emojis

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

def xpUntilNextLevel(xp: float) -> tuple[float, float, float]:
    level = 1
    cumulative_xp = 0

    while True:
        xp_for_next_level = 50 * (1.03 ** (level - 1))
        if xp < cumulative_xp + xp_for_next_level:
            xp_needed = (cumulative_xp + xp_for_next_level) - xp
            progress = (xp - cumulative_xp) / xp_for_next_level
            unRoundedProg=progress
            progress = round(progress, 1)
            return (xp_needed, progress, unRoundedProg)
        cumulative_xp += xp_for_next_level
        level += 1

def getProgressBar(progress: float) -> str:
    progress = round(progress, 1)
    full_segments = int(progress * 10)

    bar = []

    if full_segments >= 1:
        bar.append(Emojis["ProgressBar"]["LeftFull"])
    else:
        bar.append(Emojis["ProgressBar"]["LeftEmpty"])
    for i in range(1, 9):
        if i < full_segments:
            bar.append(Emojis["ProgressBar"]["MiddleFull"])
        else:
            bar.append(Emojis["ProgressBar"]["MiddleEmpty"])
    if full_segments == 10:
        bar.append(Emojis["ProgressBar"]["RightFull"])
    else:
        bar.append(Emojis["ProgressBar"]["RightEmpty"])

    return "".join(bar)