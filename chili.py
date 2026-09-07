# . empty | K outline | R red | L highlight | G green | D dark green
CHILI = [
    "......................................................GGD...",
    "....................................................GGD.....",
    ".................................................GGGDD......",
    "..........................................GGGGGGGGGGGDDDD...",
    ".............................................KKKKKKKKKK.....",
    ".........................................KKKKLLRRLLRRRRKK...",
    "......................................KKKLLRRRRRRRRRRRRKK...",
    "....................................KKKLLRRRRRRRRRRRRRRRK...",
    ".................................KKKLLRRRRRRRRRRRRRRRRRKK...",
    "...............................KKKLLRRRRRRRRRRRRRRRRRRKK....",
    ".............................KKLLRRRRRRRRRRRRRRRRRRRRKK.....",
    "...........................KKLLRRRRRRRRRRRRRRRRRRRRKK.......",
    "........................KKKLLRRRRRRRRRRRRRRRRRRRRKK.........",
    "......................KKKLLRRRRRRRRRRRRRRRRRRRKKK...........",
    "....................KKLLRRRRRRRRRRRRRRRRRRRKKK..............",
    ".................KKKLLRRRRRRRRRRRRRRRRRRKKK.................",
    "...............KKKLLRRRRRRRRRRRRRRRRKKKK....................",
    "............KKKLLRRRRRRRRRRRRRRRKKKK........................",
    "..........KKLLRRRRRRRRRRRRRRKKKK............................",
    ".......KKKLLRRRRRRRRRRRKKKKK................................",
    "......KKLLRRRRRRRKKKKKK.....................................",
    ".......KKKKKKKKK............................................",
    "............................................................",
    "............................................................",
]

PALETTE = {
    "R": "#e8402a",
    "L": "#f79b8a",
    "G": "#4fa32a",
    "D": "#2f6b1c",
}
OUTLINE = {"dark": "#8f3227", "light": "#2b2b2b"}

# character texture per pixel class, sampled deterministically
GLYPHS = {
    "K": "#8%@",
    "R": "8%@&09",
    "L": "0oO*3",
    "G": "%8$#",
    "D": "#&8%",
}

def glyph(ch, r, c):
    pool = GLYPHS.get(ch)
    if not pool:
        return " "
    return pool[(r * 37 + c * 17 + len(pool)) % len(pool)]

def widen(grid, factor=2):
    """Character cells are ~2x taller than wide; duplicate columns to fix aspect."""
    return ["".join(ch * factor for ch in row) for row in grid]

CHILI_WIDE = CHILI  # already generated at the right aspect
