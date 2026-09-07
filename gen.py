import math

COLS, ROWS = 60, 24
CW = 0.5  # a character cell is ~2x taller than wide

def centerline(t):
    x = 5.0 + 48.0 * t
    y = 20.5 - 15.0 * (t ** 1.35)
    return x, y

def halfwidth(t):
    w = 0.9 + 4.6 * (t ** 0.75)
    cap = math.sqrt(max(0.0, 1.0 - t ** 8))      # round off the head
    tip = min(1.0, 0.35 + t * 6)                  # taper the tail
    return w * cap * tip

def build():
    pts = []
    N = 900
    for i in range(N + 1):
        t = i / N
        cx, cy = centerline(t)
        pts.append((cx, cy, halfwidth(t)))

    grid = [["." for _ in range(COLS)] for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            X, Y = c * CW, r
            best = None
            for cx, cy, w in pts:
                d = math.hypot((X - cx * CW), Y - cy)
                s = d - w
                if best is None or s < best[0]:
                    best = (s, w)
            s, w = best
            if s <= 0:
                grid[r][c] = "K" if s > -0.85 else "R"
    # highlight: inner upper-left edge
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] != "R":
                continue
            up = grid[r - 1][c] if r > 0 else "."
            left = grid[r][c - 2] if c > 1 else "."
            if up in (".", "K") and left in ("R", "K") and grid[r][c + 2 if c + 2 < COLS else c] == "R":
                grid[r][c] = "L"
    return ["".join(row) for row in grid]

def add_stem(grid):
    g = [list(r) for r in grid]
    top_r = next(r for r in range(ROWS) if any(ch in "KRL" for ch in grid[r]))
    cols = [c for c, ch in enumerate(grid[top_r]) if ch in "KRL"]
    cx = (min(cols) + max(cols)) // 2

    # calyx: a solid cap sitting on the shoulder
    for d in range(-7, 8):
        c = cx + d
        if 0 <= c < COLS and top_r - 1 >= 0:
            g[top_r - 1][c] = "D" if d > 3 else "G"

    # stalk: rises diagonally up and to the right
    for i, (dr, dc, half) in enumerate([(2, 2, 2), (3, 4, 1), (4, 6, 1)]):
        r = top_r - dr
        if r < 0:
            continue
        for d in range(-half, half + 1):
            c = cx + dc + d
            if 0 <= c < COLS:
                g[r][c] = "D" if d > 0 else "G"
    return ["".join(r) for r in g]

if __name__ == "__main__":
    g = add_stem(build())
    for row in g:
        print(row)
    open("grid.txt", "w").write("\n".join(g))
