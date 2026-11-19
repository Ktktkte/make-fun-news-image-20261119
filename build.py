#!/usr/bin/env python3
"""Compose v3 of the news-image-20261119 front page.

v3 keeps v2's story set and all six illustrated tiles, and fixes the one
verified factual error in v2's briefs (gold: the 18 Nov fall was 3.2% to
about $3,730, lowest since Sept 2025 — the 5% figure belonged to silver
that day). Briefs band set one point larger for legibility.

Deterministic: fixed seeds, no timestamps, JPEG q92, no EXIF. Run twice,
get identical bytes. Writes entry.png next to this script.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (16, 20, 36)
NAVY = (16, 28, 58)
NAVY2 = (24, 40, 84)
GOLD = (217, 164, 65)
GOLD_D = (176, 128, 42)
RED = (178, 34, 34)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def vgrad(img, box, top, bottom):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    base = Image.new("RGB", (1, h))
    px = base.load()
    for y in range(h):
        t = y / (h - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    img.paste(base.resize((x1 - x0, h)), (x0, y0))


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def skyline(d, box, rng, color, win_colors, min_h=18, max_h=70):
    x0, y0, x1, y1 = box
    x = x0
    while x < x1:
        bw = rng.randint(22, 46)
        bh = rng.randint(min_h, max_h)
        d.rectangle([x, y1 - bh, min(x + bw, x1), y1], fill=color)
        for _ in range(rng.randint(2, 7)):
            wx = rng.randint(x + 3, max(x + 4, min(x + bw - 5, x1 - 4)))
            wy = rng.randint(y1 - bh + 4, y1 - 8)
            d.rectangle([wx, wy, wx + 3, wy + 4], fill=rng.choice(win_colors))
        x += bw + rng.randint(2, 8)


def flag_us(d, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                    fill=(178, 34, 52) if i % 2 == 0 else (240, 240, 240))
    cw, ch = w * 0.4, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([x + 3 + c * (cw - 6) / 4 - 1, y + 3 + r * (ch - 6) / 3 - 1,
                       x + 3 + c * (cw - 6) / 4 + 1, y + 3 + r * (ch - 6) / 3 + 1],
                      fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon(star_points(x + w * 0.22, y + h * 0.28, h * 0.16, h * 0.07),
              fill=(255, 222, 0))
    for sx, sy in [(0.55, 0.12), (0.68, 0.25), (0.68, 0.45), (0.55, 0.58)]:
        d.polygon(star_points(x + w * sx, y + h * sy, h * 0.07, h * 0.03),
                  fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)


def hero_art(img, box, rng):
    x0, y0, x1, y1 = box
    vgrad(img, box, (36, 29, 79), (224, 123, 57))
    d = ImageDraw.Draw(img, "RGBA")
    # distant skyline
    skyline(d, (x0, y0 + 30, x1, y1 - 34), rng, (43, 36, 84),
            [(255, 214, 130), (255, 170, 90)], 20, 62)
    # near skyline
    skyline(d, (x0, y0 + 70, x1, y1 - 34), rng, (24, 22, 58),
            [(255, 220, 140), (255, 190, 110)], 12, 44)
    # three flag poles on the right
    pole_x = [x1 - 250, x1 - 165, x1 - 80]
    drawers = [flag_us, flag_cn, flag_ru]
    for px, fn in zip(pole_x, drawers):
        d.line([px, y0 + 26, px, y1 - 34], fill=(230, 230, 230), width=3)
        d.ellipse([px - 3, y0 + 22, px + 3, y0 + 28], fill=(217, 164, 65))
        fn(d, px + 4, y0 + 28, 62, 34)
    # summit table + three seated silhouettes, lower left/centre
    ty = y1 - 34
    d.rectangle([x0 + 60, ty - 16, x0 + 330, ty], fill=(18, 16, 44))
    d.rectangle([x0 + 60, ty - 20, x0 + 330, ty - 16], fill=(217, 164, 65))
    for i, cx in enumerate([x0 + 110, x0 + 195, x0 + 280]):
        d.ellipse([cx - 11, ty - 60, cx + 11, ty - 38], fill=(12, 12, 30))
        d.pieslice([cx - 30, ty - 42, cx + 30, ty - 8], 180, 360, fill=(12, 12, 30))
    # searchlight beams
    for bx, ang in [(x0 + 420, -32), (x0 + 560, -18)]:
        d.polygon([(bx, y1), (bx + 26, y1),
                   (bx + 150 + ang, y0 + 10), (bx + 90 + ang, y0 + 10)],
                  fill=(255, 240, 200, 46))
    # kicker chip
    d.rectangle([x0 + 10, y1 - 32, x0 + 268, y1 - 6], fill=NAVY)
    d.text((x0 + 20, y1 - 29), "APEC SUMMIT · SHENZHEN",
           font=font(SANS_B, 16), fill=GOLD)
    # top story tag
    d.rectangle([x1 - 118, y0 + 8, x1 - 10, y0 + 30], fill=GOLD)
    d.text((x1 - 108, y0 + 11), "TOP STORY", font=font(SANS_B, 14), fill=NAVY)


def gta_art(img, box, rng):
    x0, y0, x1, y1 = box
    vgrad(img, box, (26, 11, 46), (64, 17, 90))
    d = ImageDraw.Draw(img, "RGBA")
    skyline(d, (x0, y0 + 18, x1, y1), rng, (16, 8, 34),
            [(0, 229, 255), (255, 0, 153), (255, 214, 64), (120, 255, 120)],
            24, 78)
    # neon sign
    d.rounded_rectangle([x0 + 108, y0 + 26, x0 + 330, y0 + 62], radius=4,
                        outline=(255, 0, 153), width=3)
    d.text((x0 + 124, y0 + 30), "VICE CITY", font=font(SANS_B, 26),
           fill=(255, 92, 199))
    # palm silhouettes
    for px in [x0 + 26, x1 - 30]:
        d.line([px, y1, px + 8, y0 + 44], fill=(8, 4, 18), width=5)
        for a in range(-70, 71, 35):
            rad = math.radians(a - 90)
            ex, ey = px + 8 + 34 * math.cos(rad), y0 + 44 + 30 * math.sin(rad)
            d.line([px + 8, y0 + 44, ex, ey], fill=(8, 4, 18), width=4)
    d.rectangle([x0, y1 - 6, x1, y1], fill=(255, 0, 153))


def gulf_art(img, box, rng):
    x0, y0, x1, y1 = box
    vgrad(img, box, (11, 16, 48), (30, 34, 84))
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(46):
        sx = rng.randint(x0 + 4, x1 - 6)
        sy = rng.randint(y0 + 4, y0 + 44)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # searchlight beams
    for bx in [x0 + 320, x0 + 420]:
        d.polygon([(bx, y1 - 30), (bx + 14, y1 - 30),
                   (bx + 90, y0 + 6), (bx + 60, y0 + 6)],
                  fill=(255, 244, 200, 60))
    # explosion sun on the horizon
    d.pieslice([x0 + 60, y1 - 78, x0 + 170, y1 + 32], 180, 360, fill=(232, 126, 40))
    d.pieslice([x0 + 80, y1 - 58, x0 + 150, y1 + 12], 180, 360, fill=(245, 178, 66))
    # smoke
    for cx, cy, r in [(x0 + 110, y0 + 26, 16), (x0 + 140, y0 + 18, 20),
                      (x0 + 170, y0 + 30, 13)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 70, 90))
    # sea + debris streaks
    d.rectangle([x0, y1 - 30, x1, y1], fill=(10, 26, 51))
    for _ in range(14):
        sx = rng.randint(x0 + 8, x1 - 60)
        d.line([sx, y1 - rng.randint(4, 26), sx + rng.randint(18, 48),
                y1 - rng.randint(4, 26)], fill=(232, 126, 40), width=2)


def capitol_art(img, box, rng):
    x0, y0, x1, y1 = box
    vgrad(img, box, (28, 44, 92), (120, 140, 190))
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(24):
        sx = rng.randint(x0 + 4, x1 - 6)
        sy = rng.randint(y0 + 4, y0 + 30)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    cx = (x0 + x1) // 2
    # flag on dome
    d.line([cx, y0 + 2, cx, y0 + 10], fill=(60, 60, 60), width=2)
    d.rectangle([cx + 1, y0 + 3, cx + 14, y0 + 9], fill=(178, 34, 52))
    # dome (top half of ellipse: apex at bbox top, base at bbox centre)
    d.pieslice([cx - 38, y0 + 8, cx + 38, y0 + 54], 180, 360, fill=(240, 236, 224))
    d.rectangle([cx - 44, y0 + 28, cx + 44, y0 + 33], fill=(220, 214, 196))
    d.rectangle([cx - 42, y0 + 32, cx + 42, y1 - 12], fill=(240, 236, 224))
    for i in range(-2, 3):
        d.rectangle([cx + i * 17 - 3, y0 + 34, cx + i * 17 + 3, y1 - 12],
                    fill=(200, 192, 172))
    d.rectangle([cx - 48, y1 - 14, cx + 48, y1 - 8], fill=(220, 214, 196))
    d.rectangle([cx - 56, y1 - 8, cx + 56, y1 - 2], fill=(200, 192, 172))
    # wings
    d.rectangle([x0 + 6, y1 - 16, cx - 62, y1 - 2], fill=(210, 204, 186))
    d.rectangle([cx + 62, y1 - 16, x1 - 6, y1 - 2], fill=(210, 204, 186))


def cyclone_art(img, box, rng):
    x0, y0, x1, y1 = box
    vgrad(img, box, (16, 60, 80), (30, 110, 130))
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = (x0 + x1) // 2 - 30, (y0 + y1) // 2 + 2
    for r in range(30, 4, -5):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=r * 12 % 360,
              end=r * 12 % 360 + 250, fill=(235, 245, 245), width=4)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(217, 164, 65))
    # coastline on the right
    d.polygon([(x1 - 52, y0), (x1, y0), (x1, y1), (x1 - 74, y1),
               (x1 - 60, y0 + 34)], fill=(52, 84, 66))
    d.line([x1 - 52, y0, x1 - 60, y0 + 34, x1 - 74, y1], fill=(240, 240, 220),
           width=2)
    # rain streaks
    for _ in range(26):
        rx = rng.randint(x0 + 4, x1 - 8)
        ry = rng.randint(y0 + 4, y1 - 16)
        d.line([rx, ry, rx - 5, ry + 12], fill=(200, 225, 225), width=2)
    # red alert tag
    d.rectangle([x0 + 8, y0 + 6, x0 + 96, y0 + 24], fill=RED)
    d.text((x0 + 14, y0 + 8), "RED ALERT", font=font(SANS_B, 12), fill=(255, 255, 255))


def eu_art(img, box, rng):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1, y1], fill=(0, 51, 153))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 4
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = cx + 108 * math.cos(a), cy + 30 * math.sin(a)
        d.polygon(star_points(sx, sy, 9, 4), fill=(255, 209, 0))
    d.text((cx - 26, cy - 26), "€", font=font(SANS_B, 52), fill=(255, 209, 0))
    # Brussels slab silhouette
    d.rectangle([x0, y1 - 16, x1, y1], fill=(10, 24, 66))
    for wx in range(x0 + 12, x1 - 12, 22):
        d.rectangle([wx, y1 - 12, wx + 8, y1 - 5], fill=(255, 209, 0))


def grain(img, seed=7, alpha=10):
    rng = random.Random(seed)
    small = Image.new("L", (256, 256))
    px = small.load()
    for y in range(256):
        for x in range(256):
            px[x, y] = 118 + rng.randint(-18, 18)
    noise = small.resize((W, H)).convert("RGB")
    return Image.blend(img, noise, alpha / 255.0)


def main():
    rng = random.Random(20261119)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 76], fill=NAVY)
    d.text((W // 2, 2), "THE WORLD IN ONE DAY", font=font(SERIF_B, 46),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 52), "THURSDAY 19 NOVEMBER 2026", font=font(SANS_B, 20),
           fill=GOLD, anchor="ma")
    # gold rule under masthead
    d.rectangle([0, 76, W, 80], fill=GOLD)
    # FINAL EDITION chip, top-right (title at 46px ends well clear of it)
    d.rounded_rectangle([W - 196, 8, W - 12, 32], radius=4, fill=GOLD)
    d.text((W - 104, 12), "FINAL EDITION", font=font(SANS_B, 14),
           fill=NAVY, anchor="ma")

    # ---- hero art + headline ----
    hero_art(img, (24, 92, 1000, 242), rng)
    d = ImageDraw.Draw(img)
    d.text((24, 250), "TRUMP, XI AND PUTIN MEET IN", font=font(SERIF_B, 46), fill=INK)
    d.text((24, 298), "SHENZHEN", font=font(SERIF_B, 46), fill=INK)
    deck = ("The first three-way summit of the US, Chinese and Russian leaders, "
            "on the sidelines of APEC — with the Gulf war, Ukraine and world "
            "trade on the table.")
    y = 352
    for line in wrap(d, deck, font(SANS, 19), 976):
        d.text((24, y), line, font=font(SANS, 19), fill=(40, 40, 40))
        y += 23
    d.line([24, 402, 1000, 402], fill=(120, 100, 60), width=1)

    # ---- row 2: two tiles ----
    tiles2 = [
        ("CULTURE · GAMING", "GTA VI ROLLS OUT", "WORLDWIDE",
         "After 13 years, Rockstar's game unlocks at midnight market by "
         "market, starting in New Zealand. Pre-orders top $1.5 billion.", gta_art),
        ("MIDDLE EAST · WAR", "GULF WAR WIDENS", "TO KUWAIT",
         "Iran strikes a US base in Kuwait; Kuwait and Bahrain say they "
         "repelled overnight drone attacks. Diplomacy deadlocked.", gulf_art),
    ]
    for i, (kick, h1, h2, deck, art) in enumerate(tiles2):
        x0 = 24 + i * 494
        x1 = x0 + 470
        art(img, (x0, 414, x1, 514), rng)
        d = ImageDraw.Draw(img)
        d.text((x0, 520), kick, font=font(SANS_B, 14), fill=NAVY)
        d.text((x0, 538), h1, font=font(SERIF_B, 27), fill=INK)
        d.text((x0, 568), h2, font=font(SERIF_B, 27), fill=INK)
        y = 600
        for line in wrap(d, deck, font(SANS, 18), 470):
            d.text((x0, y), line, font=font(SANS, 18), fill=(40, 40, 40))
            y += 22
    d.line([24, 668, 1000, 668], fill=(120, 100, 60), width=1)

    # ---- row 3: three tiles, each with its own art strip ----
    tiles3 = [
        ("UNITED STATES · POLITICS", "JEFFRIES NOMINATED", "FOR SPEAKER",
         "House Democrats back Hakeem Jeffries 251–11; in line to be the "
         "first Black Speaker at the Jan 3 floor vote.", capitol_art),
        ("INDIA · WEATHER", "CYCLONE AKVAN", "NEARS THE COAST",
         "Severe storm in the Bay of Bengal; landfall due between Narsapur "
         "and Puri by noon Friday. Red alerts; schools shut.", cyclone_art),
        ("EUROPE · UKRAINE", "EU OFFERS €45BN", "UKRAINE LOAN",
         "Brussels proposes a €45bn loan for 2027, repaid only once Russia "
         "pays war reparations.", eu_art),
    ]
    for i, (kick, h1, h2, deck, art) in enumerate(tiles3):
        x0 = 24 + i * 326
        x1 = x0 + 310
        art(img, (x0, 680, x1, 754), rng)
        d = ImageDraw.Draw(img)
        d.rectangle([x0, 760, x0 + 52, 764], fill=GOLD)
        d.text((x0, 770), kick, font=font(SANS_B, 13), fill=NAVY)
        d.text((x0, 788), h1, font=font(SERIF_B, 24), fill=INK)
        d.text((x0, 814), h2, font=font(SERIF_B, 24), fill=INK)
        y = 842
        for line in wrap(d, deck, font(SANS, 17), 310):
            d.text((x0, y), line, font=font(SANS, 17), fill=(40, 40, 40))
            y += 21
    d.line([24, 918, 1000, 918], fill=(120, 100, 60), width=1)

    # ---- briefs band ----
    d.rectangle([0, 924, W, H], fill=NAVY)
    d.text((24, 930), "ALSO THURSDAY", font=font(SANS_B, 19), fill=GOLD)
    briefs = [
        "Nvidia halts H-chip shipments to China — $2.4bn walked away",
        "Voyager 1 is one light-day from Earth — NASA discusses it",
        "Anthropic debuts on Nasdaq as ANT, valued past $1.4tn",
        "Van Gogh sells for a record $190.4m after Nazi-history row",
        "Gold falls 3.2% to about $3,730 — lowest since Sept 2025",
        "South Florida floods: 15 inches of rain in Broward County",
        "Crimean Bridge attacked again, traffic suspended",
    ]
    for i, b in enumerate(briefs):
        col = 0 if i < 4 else 1
        row = i if i < 4 else i - 4
        d.text((24 + col * 500, 952 + row * 17), "•  " + b,
               font=font(SANS, 15), fill=(235, 235, 235))

    img = grain(img)
    img.save(HERE / "entry.png", "JPEG", quality=92)
    print("wrote", HERE / "entry.png")


if __name__ == "__main__":
    main()
