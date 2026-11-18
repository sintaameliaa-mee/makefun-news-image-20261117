#!/usr/bin/env python3
"""Draw the news-image-20261117 v2 entry: a dense newspaper front page
summing up Tuesday 17 November 2026 — 46 stories, 3 large, 10 cards,
a world map with numbered pins, and a numbered list.

Renders at 2x and downscales for crisp edges.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import math
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

PAPER = (248, 244, 231)
CARD = (255, 252, 245)
BORDER = (198, 188, 168)
INK = (18, 18, 18)
GREY = (96, 96, 96)
RED = (178, 34, 52)
BLUE = (30, 80, 150)
NAVY = (14, 42, 71)
SKY = (183, 216, 235)
SEA = (64, 120, 168)
MAPSEA = (202, 224, 236)
LAND = (224, 212, 182)
LAND_EDGE = (190, 175, 140)


def font(bold, size, serif=False):
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(FONT_DIR + name, size * S)


def R(x0, y0, x1, y1):
    return [x0 * S, y0 * S, x1 * S, y1 * S]


def P(x, y):
    return (x * S, y * S)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width (in 1024-space)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width * S:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for i, line in enumerate(lines):
        draw.text(P(x, y + i * leading), line, font=fnt, fill=fill)


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt) / S
    draw.text(P(cx - w / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- scenes

def bridge_scene(d, x0, y0, x1, y1):
    """Kerch Bridge: deck with a collapsed middle span, smoke, fallen span."""
    d.rectangle(R(x0, y0, x1, y1), fill=SKY)
    d.ellipse(R(x1 - 74, y0 + 10, x1 - 26, y0 + 58), fill=(255, 238, 175))
    sea_y = y0 + int((y1 - y0) * 0.66)
    d.rectangle(R(x0, sea_y, x1, y1), fill=SEA)
    for i, wy in enumerate(range(sea_y + 12, y1 - 6, 18)):
        off = 14 if i % 2 else 0
        for wx in range(x0 + off, x1 - 36, 52):
            d.arc(R(wx, wy, wx + 30, wy + 12), 200, 340,
                  fill=(255, 255, 255), width=2 * S)
    deck_y = y0 + int((y1 - y0) * 0.46)
    gap_l = x0 + int((x1 - x0) * 0.52)
    gap_r = x0 + int((x1 - x0) * 0.68)
    deck = (66, 70, 76)
    d.rectangle(R(x0, deck_y, gap_l, deck_y + 12), fill=deck)
    d.rectangle(R(gap_r, deck_y, x1, deck_y + 12), fill=deck)
    for px in (x0 + 44, x0 + 128, x1 - 116, x1 - 44):
        d.rectangle(R(px, deck_y - 58, px + 10, deck_y), fill=deck)
        d.line([P(px + 5, deck_y - 58), P(px - 34, deck_y)],
               fill=(125, 129, 135), width=2 * S)
        d.line([P(px + 5, deck_y - 58), P(px + 44, deck_y)],
               fill=(125, 129, 135), width=2 * S)
    # jagged broken ends at the gap
    d.polygon([P(gap_l, deck_y), P(gap_l + 20, deck_y - 28), P(gap_l + 10, deck_y)],
              fill=deck)
    d.polygon([P(gap_r, deck_y), P(gap_r - 20, deck_y - 28), P(gap_r - 10, deck_y)],
              fill=deck)
    # fallen span in the water
    d.polygon([P(gap_l - 4, sea_y + 22), P(gap_r + 8, sea_y + 8),
               P(gap_r, sea_y + 26), P(gap_l + 4, sea_y + 38)], fill=(48, 52, 58))
    for sx in (gap_l + 2, (gap_l + gap_r) // 2, gap_r - 16):
        d.arc(R(sx, sea_y + 2, sx + 24, sea_y + 20), 180, 360,
              fill=(255, 255, 255), width=3 * S)
    # smoke + flash at the break
    cx, cy = (gap_l + gap_r) // 2, deck_y - 34
    for dx, dy, r in ((-24, 6, 18), (2, -4, 24), (24, 8, 17), (-6, -22, 15)):
        d.ellipse(R(cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r),
                  fill=(122, 122, 122))
    ex, ey = cx, deck_y - 4
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([P(ex + int(8 * math.cos(a)), ey + int(8 * math.sin(a))),
                P(ex + int(22 * math.cos(a)), ey + int(22 * math.sin(a)))],
               fill=(255, 140, 0), width=4 * S)
    d.ellipse(R(ex - 8, ey - 8, ex + 8, ey + 8), fill=(255, 200, 40))
    f = font(True, 11)
    d.rectangle(R(x0, y1 - 22, x0 + 118, y1), fill=(30, 60, 90))
    d.text(P(x0 + 10, y1 - 19), "KERCH STRAIT", font=f, fill=(255, 255, 255))


def gulf_scene(d, x0, y0, x1, y1):
    """Strait of Hormuz at dusk: burning tankers, island missile site, jets."""
    d.rectangle(R(x0, y0, x1, y1), fill=(52, 68, 96))
    d.ellipse(R(x1 - 84, y0 + 12, x1 - 36, y0 + 60), fill=(255, 214, 130))
    sea_y = y0 + int((y1 - y0) * 0.62)
    d.rectangle(R(x0, sea_y, x1, y1), fill=(24, 48, 84))
    for i, wy in enumerate(range(sea_y + 10, y1 - 6, 16)):
        off = 12 if i % 2 else 0
        for wx in range(x0 + off, x1 - 34, 48):
            d.arc(R(wx, wy, wx + 28, wy + 10), 200, 340,
                  fill=(140, 170, 210), width=2 * S)
    # island (Qeshm) with a missile launcher, left
    isl = [(x0, sea_y), (x0, sea_y - 34), (x0 + 60, sea_y - 46),
           (x0 + 120, sea_y - 30), (x0 + 130, sea_y)]
    d.polygon([P(a, b) for a, b in isl], fill=(58, 52, 44))
    lx, ly = x0 + 62, sea_y - 44
    d.line([P(lx, ly), P(lx + 26, ly - 22)], fill=(200, 200, 200), width=5 * S)
    d.ellipse(R(lx + 22, ly - 30, lx + 32, ly - 20), fill=(230, 230, 230))
    # explosion on the island
    for dx, dy, r in ((-14, -6, 12), (6, -12, 15), (16, 2, 10)):
        d.ellipse(R(lx + 26 + dx - r, ly - 22 + dy - r,
                     lx + 26 + dx + r, ly - 22 + dy + r), fill=(255, 150, 40))
    # two burning tankers
    for tx, tw in ((x0 + 150, 78), (x0 + 238, 66)):
        ty = sea_y + 6
        d.polygon([P(tx, ty), P(tx + tw, ty), P(tx + tw - 8, ty + 14),
                   P(tx + 6, ty + 14)], fill=(30, 30, 34))
        d.rectangle(R(tx + 8, ty - 8, tx + 26, ty), fill=(200, 60, 40))
        fx, fy = tx + tw // 2, ty - 8
        for dx, dy, r in ((-8, 0, 9), (4, -8, 11), (10, 2, 7)):
            d.ellipse(R(fx + dx - r, fy + dy - r, fx + dx + r, fy + dy + r),
                      fill=(255, 140, 30))
        d.ellipse(R(fx - 5, fy - 2, fx + 5, fy + 8), fill=(255, 220, 80))
    # jets, top right, with dashed trails
    for jx, jy in ((x1 - 150, y0 + 16), (x1 - 108, y0 + 34)):
        d.line([P(jx - 46, jy + 14), P(jx - 6, jy + 2)], fill=(200, 210, 230),
               width=2 * S)
        jet = [(jx, jy + 8), (jx + 22, jy + 2), (jx + 40, jy + 6),
               (jx + 46, jy + 9), (jx + 40, jy + 12), (jx + 22, jy + 14),
               (jx + 8, jy + 16), (jx + 2, jy + 12)]
        d.polygon([P(a, b) for a, b in jet], fill=(225, 230, 240))
    f = font(True, 11)
    d.rectangle(R(x0, y1 - 22, x0 + 168, y1), fill=(30, 60, 90))
    d.text(P(x0 + 10, y1 - 19), "STRAIT OF HORMUZ", font=f, fill=(255, 255, 255))


def quad_scene(d, x0, y0, x1, y1):
    """Manila skyline at dusk with the four Quad flags below."""
    d.rectangle(R(x0, y0, x1, y1), fill=(233, 214, 178))
    d.ellipse(R(x1 - 80, y0 + 8, x1 - 36, y0 + 52), fill=(255, 236, 170))
    base = y0 + int((y1 - y0) * 0.62)
    d.rectangle(R(x0, base, x1, y1), fill=(120, 110, 96))
    skyline = [(0, 34), (34, 52), (70, 26), (104, 60), (140, 40), (176, 66),
               (212, 30), (246, 48), (280, 36)]
    for dx, bh in skyline:
        bx = x0 + dx
        bw = 30
        d.rectangle(R(bx, base - bh, bx + bw, base), fill=(70, 66, 60))
        for wy in range(base - bh + 6, base - 4, 12):
            for wx in (bx + 5, bx + 17):
                d.rectangle(R(wx, wy, wx + 6, wy + 6), fill=(255, 220, 120))
    # dome on the tallest tower
    d.pieslice(R(x0 + 176, base - 66 - 14, x0 + 206, base - 66 + 14), 180, 360,
               fill=(70, 66, 60))
    # four flags: US, Japan, Australia, India — above the caption strip
    fy, fw, fh = base + 2, 66, 20
    flags_x = [x0 + 10, x0 + 88, x0 + 166, x0 + 244]
    # US
    fx = flags_x[0]
    for i in range(7):
        d.rectangle(R(fx, fy + i * fh // 7, fx + fw, fy + (i + 1) * fh // 7),
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle(R(fx, fy, fx + fw * 2 // 5, fy + fh * 4 // 7), fill=(60, 59, 110))
    # Japan
    fx = flags_x[1]
    d.rectangle(R(fx, fy, fx + fw, fy + fh), fill=(255, 255, 255))
    d.ellipse(R(fx + 24, fy + 5, fx + 42, fy + 21), fill=(188, 0, 45))
    # Australia: blue field, canton, stars
    fx = flags_x[2]
    d.rectangle(R(fx, fy, fx + fw, fy + fh), fill=(0, 40, 120))
    d.rectangle(R(fx, fy, fx + 28, fy + 13), fill=(178, 34, 52))
    d.line([P(fx, fy), P(fx + 28, fy + 13)], fill=(255, 255, 255), width=2 * S)
    d.line([P(fx + 28, fy), P(fx, fy + 13)], fill=(255, 255, 255), width=2 * S)
    for sx, sy in ((fx + 44, fy + 6), (fx + 54, fy + 14), (fx + 40, fy + 18)):
        d.ellipse(R(sx, sy, sx + 5, sy + 5), fill=(255, 255, 255))
    # India
    fx = flags_x[3]
    for i, c in enumerate(((255, 153, 51), (255, 255, 255), (19, 136, 8))):
        d.rectangle(R(fx, fy + i * fh // 3, fx + fw, fy + (i + 1) * fh // 3),
                    fill=c)
    d.ellipse(R(fx + 28, fy + 9, fx + 38, fy + 18), fill=(6, 60, 150))
    for fx in flags_x:
        d.rectangle(R(fx, fy, fx + fw, fy + fh), outline=(120, 120, 120),
                    width=1 * S)
    f = font(True, 10)
    d.rectangle(R(x0, y1 - 16, x0 + 80, y1), fill=(30, 60, 90))
    d.text(P(x0 + 10, y1 - 14), "MANILA", font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- card icons
# Each fills a 192x50 panel (x0, y0, x1, y1).

def icon_nvidia(d, x0, y0, x1, y1):
    d.rectangle(R(x0, y0, x1, y1), fill=(18, 78, 46))
    cx, cy = x0 + 34, y0 + 25
    d.rectangle(R(cx - 14, cy - 14, cx + 14, cy + 14), fill=(240, 240, 240))
    d.rectangle(R(cx - 7, cy - 7, cx + 7, cy + 7), fill=(18, 78, 46))
    for dx in (-14, 0, 14):
        d.line([P(cx + dx, cy - 20), P(cx + dx, cy - 14)], fill=(240, 240, 240),
               width=2 * S)
        d.line([P(cx + dx, cy + 14), P(cx + dx, cy + 20)], fill=(240, 240, 240),
               width=2 * S)
    pts = [(x0 + 62, y0 + 38), (x0 + 88, y0 + 30), (x0 + 112, y0 + 34),
           (x0 + 138, y0 + 18), (x0 + 164, y0 + 10)]
    d.line([P(a, b) for a, b in pts], fill=(140, 220, 120), width=3 * S)
    d.polygon([P(x0 + 164, y0 + 10), P(x0 + 152, y0 + 10), P(x0 + 164, y0 + 20)],
              fill=(140, 220, 120))
    f = font(True, 13)
    d.text(P(x0 + 66, y0 + 4), "$115.8bn", font=f, fill=(255, 255, 255))


def icon_ebola(d, x0, y0, x1, y1):
    d.rectangle(R(x0, y0, x1, y1), fill=(250, 240, 230))
    for cx, cy, r in ((x0 + 30, y0 + 25, 13), (x0 + 62, y0 + 16, 9),
                      (x0 + 66, y0 + 36, 7)):
        for ang in range(0, 360, 45):
            a = math.radians(ang)
            d.line([P(cx + int(r * math.cos(a)), cy + int(r * math.sin(a))),
                    P(cx + int((r + 6) * math.cos(a)),
                      cy + int((r + 6) * math.sin(a)))],
                   fill=(178, 34, 52), width=2 * S)
        d.ellipse(R(cx - r, cy - r, cx + r, cy + r), fill=(178, 34, 52))
        d.ellipse(R(cx - 3, cy - 3, cx + 3, cy + 3), fill=(250, 240, 230))
    f = font(True, 16)
    d.text(P(x0 + 88, y0 + 15), "11,000+", font=f, fill=(178, 34, 52))
    f2 = font(True, 10)
    d.text(P(x0 + 88, y0 + 33), "CASES", font=f2, fill=GREY)


def icon_moldova(d, x0, y0, x1, y1):
    d.rectangle(R(x0, y0, x1, y1), fill=(205, 224, 240))
    cx, cy = x0 + 40, y0 + 24
    d.ellipse(R(cx - 16, cy - 6, cx + 16, cy + 6), fill=(60, 66, 72))
    for dx in (-22, 22):
        d.ellipse(R(cx + dx - 10, cy - 12, cx + dx + 10, cy - 8),
                  fill=(120, 126, 132))
        d.line([P(cx + dx, cy - 10), P(cx + dx * 2 // 3, cy - 2)],
               fill=(60, 66, 72), width=2 * S)
    d.ellipse(R(cx - 4, cy + 6, cx + 4, cy + 12), fill=(60, 66, 72))
    f = font(True, 14)
    d.text(P(x0 + 84, y0 + 8), "7 DRONES", font=f, fill=INK)
    f2 = font(True, 10)
    d.text(P(x0 + 84, y0 + 27), "OVER CHISINAU", font=f2, fill=GREY)


def icon_mongolia(d, x0, y0, x1, y1):
    d.rectangle(R(x0, y0, x1, y1), fill=(0, 90, 160))
    ax = x0 + 44
    d.polygon([P(ax - 14, y0 + 8), P(ax + 14, y0 + 8), P(ax + 14, y0 + 26),
               P(ax + 24, y0 + 26), P(ax, y0 + 44), P(ax - 24, y0 + 26),
               P(ax - 14, y0 + 26)], fill=(220, 40, 40))
    f = font(True, 15)
    d.text(P(x0 + 84, y0 + 8), "QUITS", font=f, fill=(255, 255, 255))
    f2 = font(True, 10)
    d.text(P(x0 + 84, y0 + 27), "PRESIDENT", font=f2, fill=(200, 220, 240))


def icon_an12(d, x0, y0, x1, y1):
    d.rectangle(R(x0, y0, x1, y1), fill=(96, 110, 126))
    # plane nose-down, smoke trail
    for i, (sx, sy, r) in enumerate(((x0 + 26, y0 + 10, 5), (x0 + 44, y0 + 16, 7),
                                     (x0 + 62, y0 + 24, 9))):
        d.ellipse(R(sx - r, sy - r, sx + r, sy + r), fill=(200, 200, 200))
    jx, jy = x0 + 78, y0 + 30
    jet = [(jx, jy), (jx + 26, jy - 12), (jx + 52, jy - 8), (jx + 58, jy - 4),
           (jx + 52, jy), (jx + 26, jy + 4), (jx + 8, jy + 8)]
    d.polygon([P(a, b) for a, b in jet], fill=(30, 34, 40))
    f = font(True, 14)
    d.text(P(x0 + 148, y0 + 8), "19", font=f, fill=(255, 255, 255))
    f2 = font(True, 10)
    d.text(P(x0 + 148, y0 + 26), "DEAD", font=f2, fill=(255, 220, 130))


def icon_knesset(d, x0, y0, x1, y1):
    d.rectangle(R(x0, y0, x1, y1), fill=(238, 240, 244))
    bx, by = x0 + 12, y0 + 10
    d.polygon([P(bx, by + 12), P(bx + 34, by), P(bx + 68, by + 12)],
              fill=(120, 130, 145))
    d.rectangle(R(bx, by + 12, bx + 68, by + 16), fill=(120, 130, 145))
    for i in range(4):
        d.rectangle(R(bx + 4 + i * 17, by + 16, bx + 12 + i * 17, by + 36),
                    fill=(90, 100, 115))
    d.rectangle(R(bx, by + 36, bx + 68, by + 40), fill=(120, 130, 145))
    f = font(True, 16)
    d.text(P(x0 + 96, y0 + 6), "66–52", font=f, fill=BLUE)
    f2 = font(True, 10)
    d.text(P(x0 + 96, y0 + 26), "NEW SPEAKER", font=f2, fill=GREY)


def icon_mondlane(d, x0, y0, x1, y1):
    d.rectangle(R(x0, y0, x1, y1), fill=(240, 234, 220))
    bx, by = x0 + 12, y0 + 8
    d.polygon([P(bx, by + 12), P(bx + 30, by), P(bx + 60, by + 12)],
              fill=(150, 120, 80))
    d.rectangle(R(bx, by + 12, bx + 60, by + 15), fill=(150, 120, 80))
    for i in range(3):
        d.rectangle(R(bx + 5 + i * 20, by + 15, bx + 13 + i * 20, by + 34),
                    fill=(120, 96, 62))
    d.rectangle(R(bx, by + 34, bx + 60, by + 38), fill=(150, 120, 80))
    f = font(True, 12)
    d.text(P(x0 + 86, y0 + 8), "TRIAL", font=f, fill=INK)
    d.text(P(x0 + 86, y0 + 24), "OPENS", font=f, fill=INK)
    f2 = font(True, 9)
    d.text(P(x0 + 142, y0 + 24), "MAPUTO", font=f2, fill=GREY)


def icon_brazil(d, x0, y0, x1, y1):
    d.rectangle(R(x0, y0, x1, y1), fill=(0, 140, 70))
    d.polygon([P(x0 + 40, y0 + 6), P(x0 + 76, y0 + 25), P(x0 + 40, y0 + 44),
               P(x0 + 4, y0 + 25)], fill=(255, 210, 0))
    d.ellipse(R(x0 + 28, y0 + 13, x0 + 52, y0 + 37), fill=(0, 60, 160))
    f = font(True, 20)
    d.text(P(x0 + 92, y0 + 12), "7–0", font=f, fill=(255, 255, 255))
    f2 = font(True, 10)
    d.text(P(x0 + 140, y0 + 18), "VINI ×3", font=f2, fill=(255, 230, 120))


def icon_germany(d, x0, y0, x1, y1):
    d.rectangle(R(x0, y0, x1, y0 + 17), fill=(20, 20, 20))
    d.rectangle(R(x0, y0 + 17, x1, y0 + 33), fill=(200, 0, 0))
    d.rectangle(R(x0, y0 + 33, x1, y1), fill=(255, 200, 0))
    f = font(True, 20)
    d.text(P(x0 + 16, y0 + 12), "5–0", font=f, fill=(255, 255, 255))
    f2 = font(True, 10)
    d.text(P(x0 + 84, y0 + 18), "WIRTZ ×2", font=f2, fill=(255, 255, 255))


def icon_tiger(d, x0, y0, x1, y1):
    d.rectangle(R(x0, y0, x1, y1), fill=(34, 120, 60))
    d.ellipse(R(x0 + 8, y0 + 34, x0 + 84, y0 + 46), fill=(90, 190, 110))
    # golfer: head, body leaning, club
    d.ellipse(R(x0 + 30, y0 + 8, x0 + 40, y0 + 18), fill=(30, 30, 30))
    d.line([P(x0 + 35, y0 + 18), P(x0 + 30, y0 + 32)], fill=(30, 30, 30),
           width=5 * S)
    d.line([P(x0 + 30, y0 + 32), P(x0 + 24, y0 + 42)], fill=(30, 30, 30),
           width=4 * S)
    d.line([P(x0 + 30, y0 + 32), P(x0 + 38, y0 + 42)], fill=(30, 30, 30),
           width=4 * S)
    d.line([P(x0 + 33, y0 + 22), P(x0 + 52, y0 + 40)], fill=(220, 220, 220),
           width=3 * S)
    d.ellipse(R(x0 + 52, y0 + 40, x0 + 57, y0 + 45), fill=(255, 255, 255))
    # flag
    d.line([P(x0 + 150, y0 + 10), P(x0 + 150, y0 + 40)], fill=(255, 255, 255),
           width=2 * S)
    d.polygon([P(x0 + 150, y0 + 10), P(x0 + 168, y0 + 15), P(x0 + 150, y0 + 20)],
              fill=(220, 40, 40))
    f = font(True, 14)
    d.text(P(x0 + 92, y0 + 14), "BACK", font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- world map

# Simplified continent outlines in (lon, lat). Rough but recognisable.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 72), (-85, 70),
     (-80, 73), (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 32), (-81, 25), (-85, 30), (-90, 21), (-97, 16), (-94, 17),
     (-87, 13), (-83, 9), (-79, 9), (-83, 15), (-90, 14), (-97, 16),
     (-105, 20), (-110, 23), (-114, 29), (-120, 34), (-124, 40),
     (-124, 48), (-130, 55), (-145, 60), (-158, 58), (-165, 60)],
    # South America
    [(-79, 9), (-75, 11), (-70, 12), (-62, 10), (-52, 5), (-50, 0),
     (-44, -3), (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-52, -33),
     (-58, -38), (-62, -41), (-65, -45), (-69, -52), (-71, -54), (-73, -50),
     (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-81, -4),
     (-80, 1)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 53), (3, 53), (8, 55),
     (8, 58), (5, 60), (10, 62), (18, 69), (25, 71), (30, 70), (32, 68),
     (28, 60), (24, 58), (21, 55), (24, 52), (30, 55), (32, 50), (28, 46),
     (30, 44), (28, 41), (23, 40), (26, 38), (22, 37), (19, 40), (16, 41),
     (12, 44), (8, 44), (3, 43), (-2, 37), (-6, 36)],
    # Africa
    [(-17, 15), (-16, 20), (-10, 31), (-6, 35), (0, 36), (10, 37), (11, 34),
     (20, 32), (30, 31), (32, 31), (35, 28), (37, 22), (39, 18), (43, 12),
     (48, 11), (51, 10), (46, 5), (41, 0), (40, -5), (39, -12), (36, -18),
     (33, -26), (28, -33), (20, -35), (17, -29), (15, -22), (12, -18),
     (13, -12), (9, -1), (9, 4), (-8, 5), (-13, 8)],
    # Asia
    [(30, 36), (36, 36), (35, 31), (39, 30), (43, 30), (48, 30), (50, 26),
     (56, 27), (57, 25), (61, 25), (66, 25), (68, 23), (72, 20), (76, 8),
     (80, 7), (80, 13), (84, 18), (88, 22), (91, 22), (94, 17), (97, 16),
     (98, 10), (100, 7), (103, 1), (104, 2), (103, 7), (100, 9), (99, 12),
     (101, 13), (105, 9), (107, 11), (109, 13), (106, 20), (108, 18),
     (110, 20), (114, 22), (118, 25), (120, 28), (122, 32), (120, 35),
     (122, 38), (126, 40), (130, 42), (132, 43), (135, 44), (138, 46),
     (141, 50), (142, 54), (141, 60), (137, 65), (142, 70), (150, 70),
     (158, 66), (162, 60), (170, 60), (178, 65), (178, 68), (170, 70),
     (160, 70), (150, 72), (140, 72), (130, 71), (120, 73), (110, 74),
     (100, 76), (90, 75), (80, 73), (70, 72), (60, 69), (55, 68), (50, 68),
     (45, 65), (40, 65), (35, 65), (32, 60), (30, 55), (28, 50), (30, 46),
     (32, 44), (35, 42), (38, 42), (40, 40), (44, 39), (40, 38)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (151, -24), (146, -19), (142, -15), (142, -11),
     (141, -13), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
    # New Zealand
    [(167, -45), (172, -41), (175, -38), (178, -38), (176, -40), (173, -42),
     (169, -46)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 57), (1, 53), (-1, 51)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (140, 36), (141, 39),
     (141, 42), (143, 44), (145, 44), (142, 42), (140, 38), (139, 35),
     (136, 34), (133, 34)],
    # Indonesia
    [(95, 5), (105, 0), (110, -7), (114, -8), (120, -10), (125, -9),
     (131, -3), (136, -2), (141, -3), (141, -8), (136, -8), (130, -7),
     (125, -9), (120, -9), (114, -8), (108, -7), (103, -5), (98, 2)],
    # Greenland
    [(-58, 64), (-52, 70), (-44, 74), (-32, 74), (-24, 70), (-32, 66),
     (-42, 60), (-52, 60)],
]

# (story number, lon, lat, label dx, label dy)
PINS = [
    (1, 33.0, 45.3, 22, 14),
    (2, 56.0, 27.0, 0, -14),
    (3, 121.0, 14.6, 0, 12),
    (4, -122.0, 37.4, -14, -10),
    (5, 25.0, 0.0, -16, 8),
    (6, 28.8, 47.0, -18, -12),
    (7, 106.9, 47.9, 0, -13),
    (8, 86.9, 55.4, 0, 12),
    (10, 32.6, -25.9, 10, 8),
    (11, 103.8, 1.35, -6, -14),
    (12, 13.4, 52.5, -14, -12),
    (14, -74.0, 40.7, 10, -10),
    (15, 37.6, 55.75, 16, -12),
    (17, 27.9, 42.7, 4, 16),
    (20, 30.5, 50.45, -16, 10),
    (24, 139.0, 36.0, 12, 8),
    (25, -150.0, 64.0, -8, 10),
    (29, 30.0, 13.0, 24, 2),
    (30, 90.4, 23.8, 0, 12),
    (39, -159.8, -21.2, 0, -13),
    (41, -80.2, 26.0, -12, 8),
]

MAP_LABELS = [
    ("NORTH AMERICA", -100, 58),
    ("SOUTH AMERICA", -60, -12),
    ("AFRICA", 17, 12),
    ("ASIA", 95, 62),
    ("AUSTRALIA", 134, -25),
]


def draw_map(d, x0, y0, x1, y1):
    """World map: sea, simplified continents, numbered pins."""
    d.rectangle(R(x0, y0, x1, y1), fill=MAPSEA, outline=BORDER, width=1 * S)

    def proj(lon, lat):
        px = x0 + 2 + (lon + 180) / 360 * (x1 - x0 - 4)
        py = y0 + 2 + (75 - lat) / 130 * (y1 - y0 - 4)
        return px, py

    # graticule: equator + tropics, faint
    for lat in (0, 23.4, -23.4):
        _, gy = proj(0, lat)
        d.line([P(x0 + 2, gy), P(x1 - 2, gy)], fill=(185, 210, 224),
               width=1 * S)
    for lon in (-120, -60, 0, 60, 120):
        gx, _ = proj(lon, 0)
        d.line([P(gx, y0 + 2), P(gx, y1 - 2)], fill=(185, 210, 224),
               width=1 * S)
    for poly in CONTINENTS:
        pts = [P(*proj(lon, lat)) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    f_lab = font(True, 8)
    for name, lon, lat in MAP_LABELS:
        lx, ly = proj(lon, lat)
        centred(d, lx, ly, name, f_lab, (130, 120, 100))
    # pins: dot at the true spot, leader line, numbered disc
    f_pin = font(True, 9)
    for num, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        lx, ly = px + dx, py + dy
        d.ellipse(R(px - 3, py - 3, px + 3, py + 3), fill=RED)
        d.line([P(px, py), P(lx, ly)], fill=(140, 60, 70), width=1 * S)
        d.ellipse(R(lx - 8, ly - 8, lx + 8, ly + 8), fill=RED,
                  outline=(255, 255, 255), width=1 * S)
        centred(d, lx, ly - 5, str(num), f_pin, (255, 255, 255))


# ---------------------------------------------------------------- story data

LARGE = [
    (1, bridge_scene, "WAR IN UKRAINE", RED,
     "Kerch Bridge road arch collapses into the sea",
     "Ukrainian drones and missiles bring down a 227m road span to Crimea. "
     "The road is cut; rail is damaged but running. Two killed, the governor says."),
    (2, gulf_scene, "WAR IN THE GULF", RED,
     "US jets strike IRGC missile site on Qeshm Island",
     "Hours after Iranian drones target a US radar in Bahrain, the third attack "
     "there in five days. Tankers burn in Hormuz as a third US carrier arrives."),
    (3, quad_scene, "DIPLOMACY", BLUE,
     "Trump hosts Quad leaders in Manila",
     "Four-nation talks days before a first-ever Xi–Trump–Putin trilateral in "
     "Shenzhen on Thursday, with the Iran war on the agenda."),
]

CARDS = [
    (4, icon_nvidia, "Nvidia revenue doubles to $115.8bn",
     "First results under interim chief Colette Kress."),
    (5, icon_ebola, "Ebola toll tops 11,000 cases",
     "WHO: ~5,400 dead in DR Congo; trials start next week."),
    (6, icon_moldova, "Seven Russian drones cross Moldova",
     "One over Chisinau; five crash near homes."),
    (7, icon_mongolia, "Mongolia's president quits",
     "Khurelsukh resigns over railway graft claims he denies."),
    (8, icon_an12, "Russian military plane crashes; 19 dead",
     "An-12 goes down near Yagunovo in Siberia."),
    (9, icon_knesset, "Knesset elects anti-Netanyahu speaker",
     "Kahana wins 66–52 as Eisenkot's bloc takes the gavel."),
    (10, icon_mondlane, "Mondlane on trial in Maputo",
     "Mozambique opposition leader faces 24 years; denies all."),
    (11, icon_brazil, "Vinícius hat-trick sinks Singapore 7–0",
     "Brazil's biggest win since 2012, at Kallang."),
    (12, icon_germany, "Wirtz brace as Germany rout Dutch 5–0",
     "Klopp's side top Nations League Group A2 in Berlin."),
    (13, icon_tiger, "Tiger Woods is back",
     "First event in two years: Hero World Challenge, Dec 3–6."),
]

# (number, headline, subtext) — one line each at 10px / 8.5px in ~300px.
LIST = [
    (14, "Dow falls 849 points",
     "Wall Street slides; S&P −1.03%, Nasdaq −0.74%."),
    (15, "Russia says 1,441 drones downed",
     "Moscow claims its biggest nightly toll of the war."),
    (16, "Gas tanker crew abandon ship in Hormuz",
     "Tara Gas hit twice; Oman rescues 24, one Indian missing."),
    (17, "Gas tanker sinks off Bulgaria",
     "Gas Husky goes down; all 19 Filipino crew rescued."),
    (18, "Houthis claim drones at Saudi pipeline",
     "Five drones aimed at two East-West pumping stations."),
    (19, "Houthis 100 km from Aden",
     "Saudi Arabia replaces its Yemen coalition commander."),
    (20, "Russia strikes bridges across Kyiv",
     "Strikes hit crossings over the Dnipro, Kyiv's mayor says."),
    (21, "Strike on Zaporizhzhia kills two",
     "Russian attack on industrial sites injures 38."),
    (22, "Israel strikes south Lebanon",
     "Jets and artillery hit Houla, al-Mansouri and Zebqin."),
    (23, "Five held over Iran-linked plot in Greece",
     "Skopje and Athens say they foiled an assassination."),
    (24, "Japan jets chase suspected Russian planes",
     "Two planes near Okinoshima; first breach since 2024."),
    (25, "Peltola flips Alaska Senate seat",
     "Democrat beats Sullivan; party claims 56 Senate seats."),
    (26, "UN warns of Gaza winter emergency",
     "1.7m still displaced; 1.4m face acute hunger, agencies say."),
    (27, "COP31 backs heat and cooling pact",
     "$20m+ pledged in Antalya; 1.5°C limit nears."),
    (28, "Serbia's student MPs sworn in",
     "Student List takes 140 of 250 seats, ending SNS rule."),
    (29, "Drones killed 3 in 4 Sudan war dead, UN says",
     "2,230 civilians verified killed this year; 1,630 by drone."),
    (30, "Bangladesh garment workers clash with police",
     "Tear gas in Gazipur as wage talks stall."),
    (31, "Police station torched in Bangladesh",
     "Lawmaker's home also burned in Tungipara, Gopalganj."),
    (32, "US loses measles-free status",
     "PAHO: 5,412 cases in 2026, the most in 35 years."),
    (33, "Deutsche Bank shares fall 6%",
     "Leak renews scrutiny of Epstein, Trump, Russia links."),
    (34, "Equinor hit by cyberattack",
     "Norway's gas giant: IT systems hit, output unaffected."),
    (35, "Apple outage locks users out of iCloud",
     "A faulty internal update, not a hack, Apple says."),
    (36, "Waymo halts freeway robotaxis",
     "California bans driverless cars from freeways."),
    (37, "Dubai airport traffic down 28%",
     "50.4m passengers in nine months; 70m expected for 2026."),
    (38, "Pakistan cuts fuel prices again",
     "Petrol Rs328, diesel Rs358 — tenth straight daily cut."),
    (39, "Cyclone Xavier strengthens near Cook Islands",
     "130-knot winds; gale warnings for northern islands."),
    (40, "Cyclone Akvan forms in Bay of Bengal",
     "40-knot storm heads for India's east coast."),
    (41, "Flash floods swamp south Florida",
     "Hollywood records 14 inches of rain in 24 hours."),
    (42, "Methane geyser erupts at California landfill",
     "Six workers hospitalised after Chiquita Canyon blast."),
    (43, "NatGeo names Pictures of the Year",
     "25 photos from a million; first wild moray eel spawning."),
    (44, "Irishman charged over wrecked C-130",
     "US indicts Daithi O'Corrain; $60m plane 'never to fly'."),
    (45, "Peoria ethanol worker indicted",
     "Kozak accused of bomb threat that evacuated 2,500 homes."),
    (46, "Voyager 1 hours from one light-day",
     "NASA asks the world to shine a light tonight."),
]


# ---------------------------------------------------------------- layout

def clipped_scene(img, fn, x0, y0, x1, y1):
    """Draw a scene onto a layer of exactly its box, then paste: nothing
    the scene draws can spill past its frame."""
    w, h = (x1 - x0) * S, (y1 - y0) * S
    layer = Image.new("RGB", (w, h), CARD)
    ld = ImageDraw.Draw(layer)
    fn(ld, 0, 0, x1 - x0, y1 - y0)
    img.paste(layer, (x0 * S, y0 * S))


def large_card(img, d, x, y, w, h, num, scene, tag_text, tag_color,
               headline, sub):
    d.rectangle(R(x, y, x + w, y + h), fill=CARD, outline=BORDER, width=2 * S)
    clipped_scene(img, scene, x + 2, y + 2, x + w - 2, y + 106)
    f_tag = font(True, 11)
    d.text(P(x + 12, y + 112), "%d · %s" % (num, tag_text), font=f_tag,
           fill=tag_color)
    f_h = font(True, 17)
    lines = wrap(d, headline, f_h, w - 24)
    text_block(d, x + 12, y + 128, lines, f_h, INK, 21)
    f_s = font(False, 11)
    sub_lines = wrap(d, sub, f_s, w - 24)
    text_block(d, x + 12, y + 128 + len(lines) * 21 + 6, sub_lines, f_s,
               (70, 70, 70), 14)


def small_card(img, d, x, y, w, h, num, icon, headline, sub):
    d.rectangle(R(x, y, x + w, y + h), fill=CARD, outline=BORDER, width=2 * S)
    clipped_scene(img, icon, x + 2, y + 2, x + w - 2, y + 52)
    f_n = font(True, 11)
    d.text(P(x + 8, y + 56), "%d." % num, font=f_n, fill=RED)
    f_h = font(True, 11)
    lines = wrap(d, headline, f_h, w - 34)
    text_block(d, x + 30, y + 56, lines, f_h, INK, 13)
    f_s = font(False, 9)
    sub_lines = wrap(d, sub, f_s, w - 16)
    text_block(d, x + 8, y + 56 + len(lines) * 13 + 3, sub_lines, f_s,
               (90, 90, 90), 11)


def main():
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    f_kick = font(True, 12)
    centred(d, W // 2, 8, "THE WORLD IN ONE PAGE", f_kick, GREY)
    f_date = font(True, 40, serif=True)
    centred(d, W // 2, 26, "TUESDAY 17 NOVEMBER 2026", f_date, INK)
    f_count = font(True, 13)
    centred(d, W // 2, 70,
            "46 STORIES  ·  6 CONTINENTS  ·  WAR  ·  DIPLOMACY  ·  MARKETS  "
            "·  CLIMATE  ·  SPORT",
            f_count, RED)
    d.line([P(14, 90), P(1010, 90)], fill=INK, width=3 * S)
    d.line([P(14, 94), P(1010, 94)], fill=INK, width=1 * S)

    # ---- three large stories ----
    for i, (num, scene, tg, tc, hd, sb) in enumerate(LARGE):
        large_card(img, d, 14 + i * 336, 100, 324, 222, num, scene, tg, tc,
                   hd, sb)

    # ---- ten small cards, two rows of five ----
    for i, (num, icon, hd, sb) in enumerate(CARDS):
        row, col = divmod(i, 5)
        small_card(img, d, 14 + col * 201, 330 + row * 118, 192, 110,
                   num, icon, hd, sb)

    # ---- map ----
    f_sec = font(True, 13)
    d.text(P(14, 566), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    f_note = font(False, 10)
    d.text(P(196, 568), "Pins mark the numbered stories above and below",
           font=f_note, fill=GREY)
    draw_map(d, 14, 586, 1010, 712)

    # ---- numbered list ----
    d.text(P(14, 720), "THE REST OF THE DAY", font=f_sec, fill=INK)
    d.text(P(196, 722), "Stories 14–46, one line each", font=f_note,
           fill=GREY)
    d.line([P(14, 740), P(1010, 740)], fill=BORDER, width=1 * S)
    f_num = font(True, 10)
    f_hl = font(True, 10)
    f_sb = font(False, 8)
    for i, (num, hd, sb) in enumerate(LIST):
        col, row = divmod(i, 11)
        cx = 14 + col * 336
        cy = 746 + row * 23
        d.text(P(cx, cy), "%d." % num, font=f_num, fill=RED)
        d.text(P(cx + 24, cy), hd, font=f_hl, fill=INK)
        d.text(P(cx + 24, cy + 12), sb, font=f_sb, fill=(90, 90, 90))

    # ---- footer ----
    d.rectangle(R(0, 1000, W, H), fill=NAVY)
    f_f = font(False, 11)
    centred(d, W // 2, 1007,
            "Every story above happened or was first reported on Tuesday "
            "17 November 2026  ·  Sources: Reuters · AP · AFP · UN News · "
            "WHO · JTWC · NWS",
            f_f, (225, 225, 225))

    img = img.resize((W, H), Image.LANCZOS)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
