#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: a one-page infographic summing up
Tuesday 17 November 2026. Renders at 2x and downscales for crisp edges.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

NAVY = (14, 42, 71)
NAVY_DK = (9, 28, 48)
GOLD = (212, 160, 23)
RED = (192, 57, 43)
PAPER = (247, 243, 234)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)
INK = (24, 24, 24)
GREY = (90, 90, 90)
SKY = (183, 216, 235)
SEA = (64, 120, 168)
SEA_DK = (40, 86, 128)


def font(bold, size):
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


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for i, line in enumerate(lines):
        draw.text(P(x, y + i * leading), line, font=fnt, fill=fill)


def tag(draw, x, y, text, color):
    f = font(True, 15)
    tw = draw.textlength(text, font=f) // S + 16
    draw.rectangle(R(x, y, x + tw, y + 24), fill=color)
    draw.text(P(x + 8, y + 3), text, font=f, fill=(255, 255, 255))
    return tw


def bridge_scene(draw, x0, y0, x1, y1):
    """Kerch Bridge with its road span collapsed into the strait."""
    draw.rectangle(R(x0, y0, x1, y1), fill=SKY)
    # sun haze
    draw.ellipse(R(x1 - 90, y0 + 18, x1 - 30, y0 + 78), fill=(255, 236, 170))
    # sea
    sea_y = y0 + int((y1 - y0) * 0.68)
    draw.rectangle(R(x0, sea_y, x1, y1), fill=SEA)
    for i, wy in enumerate(range(sea_y + 14, y1 - 8, 22)):
        off = 12 if i % 2 else 0
        for wx in range(x0 + off, x1 - 40, 56):
            draw.arc(R(wx, wy, wx + 34, wy + 14), 200, 340, fill=(255, 255, 255), width=2 * S)
    # bridge deck with a gap in the middle
    deck_y = y0 + int((y1 - y0) * 0.52)
    gap_l = x0 + int((x1 - x0) * 0.46)
    gap_r = x0 + int((x1 - x0) * 0.62)
    deck_c = (70, 74, 80)
    draw.rectangle(R(x0, deck_y, gap_l, deck_y + 14), fill=deck_c)
    draw.rectangle(R(gap_r, deck_y, x1, deck_y + 14), fill=deck_c)
    # pylons
    for px in (x0 + 60, x0 + 150, x1 - 170, x1 - 80):
        draw.rectangle(R(px, deck_y - 70, px + 12, deck_y), fill=deck_c)
    # cables
    for px in (x0 + 66, x0 + 156, x1 - 164, x1 - 74):
        draw.line([P(px, deck_y - 70), P(px - 40, deck_y)], fill=(120, 124, 130), width=2 * S)
        draw.line([P(px, deck_y - 70), P(px + 40, deck_y)], fill=(120, 124, 130), width=2 * S)
    # broken arch: two jagged stubs at the gap
    draw.polygon([P(gap_l, deck_y), P(gap_l + 26, deck_y - 34), P(gap_l + 12, deck_y)],
                 fill=deck_c)
    draw.polygon([P(gap_r, deck_y), P(gap_r - 26, deck_y - 34), P(gap_r - 12, deck_y)],
                 fill=deck_c)
    # fallen span in the water, tilted
    draw.polygon([P(gap_l - 6, sea_y + 26), P(gap_r + 6, sea_y + 10),
                  P(gap_r - 2, sea_y + 30), P(gap_l + 2, sea_y + 44)], fill=(52, 56, 62))
    draw.polygon([P(gap_l + 8, sea_y + 44), P(gap_r - 14, sea_y + 30),
                  P(gap_r - 20, sea_y + 40), P(gap_l + 4, sea_y + 52)], fill=(70, 74, 80))
    # splash
    for sx in (gap_l + 4, (gap_l + gap_r) // 2, gap_r - 14):
        draw.arc(R(sx, sea_y + 2, sx + 26, sea_y + 22), 180, 360, fill=(255, 255, 255), width=3 * S)
    # smoke puffs at the break
    cx, cy = (gap_l + gap_r) // 2, deck_y - 40
    for dx, dy, r in ((-28, 8, 22), (0, -6, 28), (28, 10, 20), (-8, -26, 18)):
        draw.ellipse(R(cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r),
                     fill=(120, 120, 120))
    # explosion starburst
    ex, ey = cx, deck_y - 6
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 10, 26
        a = math.radians(ang)
        draw.line([P(ex + int(r1 * math.cos(a)), ey + int(r1 * math.sin(a))),
                   P(ex + int(r2 * math.cos(a)), ey + int(r2 * math.sin(a)))],
                  fill=(255, 140, 0), width=4 * S)
    draw.ellipse(R(ex - 9, ey - 9, ex + 9, ey + 9), fill=(255, 200, 40))
    # caption inside scene, on a dark strip so the waves stay behind it
    f = font(True, 15)
    draw.rectangle(R(x0, y1 - 30, x1, y1), fill=(30, 60, 90))
    draw.text(P(x0 + 12, y1 - 26), "KERCH STRAIT  •  ROAD LINK CUT", font=f, fill=(255, 255, 255))


def flags_row(draw, x, y):
    """US, China, Russia flag bars, fixed 64x40 each."""
    w, h = 64, 40
    # US: stripes + canton
    ux = x
    for i in range(7):
        draw.rectangle(R(ux, y + i * h // 7, ux + w, y + (i + 1) * h // 7),
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle(R(ux, y, ux + w * 2 // 5, y + h * 4 // 7), fill=(60, 59, 110))
    # China: red + stars
    cx = x + w + 10
    draw.rectangle(R(cx, y, cx + w, y + h), fill=(222, 41, 16))
    draw.ellipse(R(cx + 8, y + 7, cx + 20, y + 19), fill=(255, 222, 0))
    for sx, sy in ((cx + 26, y + 6), (cx + 30, y + 13), (cx + 26, y + 20)):
        draw.ellipse(R(sx, sy, sx + 7, sy + 7), fill=(255, 222, 0))
    # Russia: white / blue / red
    rx = cx + w + 10
    for i, c in enumerate(((255, 255, 255), (0, 87, 184), (213, 0, 50))):
        draw.rectangle(R(rx, y + i * h // 3, rx + w, y + (i + 1) * h // 3), fill=c)
    for fx in (ux, cx, rx):
        draw.rectangle(R(fx, y, fx + w, y + h), outline=(150, 150, 150), width=1 * S)


def jet_icon(draw, x, y):
    """Fighter jet silhouette over a red sun disc, dashed flight path."""
    w, h = 210, 86
    draw.ellipse(R(x + w - 66, y + 4, x + w - 6, y + 64), fill=(188, 0, 45))
    # dashed path
    dash = True
    px = x + 6
    while px < x + w - 70:
        if dash:
            draw.line([P(px, y + 62), P(px + 12, y + 56)], fill=(120, 120, 120), width=3 * S)
        px += 18
        dash = not dash
    # jet: simple delta silhouette pointing right
    jx, jy = x + 60, y + 18
    jet = [(jx, jy + 18), (jx + 46, jy + 6), (jx + 96, jy + 16), (jx + 108, jy + 20),
           (jx + 96, jy + 24), (jx + 46, jy + 30), (jx + 20, jy + 34), (jx + 8, jy + 26)]
    draw.polygon([P(a, b) for a, b in jet], fill=(52, 58, 64))
    draw.polygon([P(jx + 40, jy + 18), P(jx + 58, jy + 2), P(jx + 64, jy + 18)],
                 fill=(52, 58, 64))


def tents_icon(draw, x, y):
    """Aid tents + big displaced figure."""
    w = 210
    ground = y + 70
    draw.rectangle(R(x, ground, x + w, ground + 4), fill=(150, 140, 120))
    for tx, tc in ((x + 6, (200, 120, 60)), (x + 58, (90, 130, 170)), (x + 110, (200, 120, 60))):
        draw.polygon([P(tx, ground), P(tx + 22, y + 22), P(tx + 44, ground)], fill=tc)
        draw.polygon([P(tx + 17, ground), P(tx + 22, y + 46), P(tx + 27, ground)],
                     fill=(60, 50, 40))
    f = font(True, 28)
    draw.text(P(x + 162, y + 26), "1.7m", font=f, fill=RED)


def sun_icon(draw, x, y):
    """Sun + thermometer for the heat pact."""
    import math
    cx, cy, r = x + 44, y + 42, 26
    for a in range(0, 360, 30):
        ar = math.radians(a)
        draw.line([P(cx + int((r + 6) * math.cos(ar)), cy + int((r + 6) * math.sin(ar))),
                   P(cx + int((r + 16) * math.cos(ar)), cy + int((r + 16) * math.sin(ar)))],
                  fill=(230, 150, 20), width=4 * S)
    draw.ellipse(R(cx - r, cy - r, cx + r, cy + r), fill=(255, 200, 40))
    # thermometer
    tx = x + 120
    draw.rounded_rectangle(R(tx, y + 8, tx + 22, y + 66), radius=11 * S,
                           fill=(230, 230, 230), outline=(150, 150, 150), width=2 * S)
    draw.ellipse(R(tx - 6, y + 56, tx + 28, y + 84), fill=(210, 60, 40))
    draw.rectangle(R(tx + 6, y + 30, tx + 16, y + 66), fill=(210, 60, 40))


def ballot_icon(draw, x, y):
    """Ballot box with a check mark."""
    bx, by = x + 16, y + 16
    draw.rectangle(R(bx, by, bx + 78, by + 52), fill=(31, 97, 163))
    draw.rectangle(R(bx - 6, by - 8, bx + 84, by + 6), fill=(21, 70, 120))
    draw.rectangle(R(bx + 28, by - 4, bx + 50, by + 2), fill=(20, 20, 20))
    # check
    draw.line([P(bx + 16, by + 30), P(bx + 32, by + 44), P(bx + 64, by + 12)],
              fill=(255, 255, 255), width=6 * S, joint="curve")


def panel(draw, x, y, w, h, tag_text, tag_color, headline, sub, icon, wide=False):
    draw.rectangle(R(x, y, x + w, y + h), fill=CARD, outline=BORDER, width=2 * S)
    tag(draw, x + 14, y + 12, tag_text, tag_color)
    f_h = font(True, 25)
    f_s = font(False, 19)
    if wide:
        icon(draw, x + 14, y + 48)
        tx = x + 228
        tw = w - 228 - 14
        lines = wrap(draw, headline, f_h, tw)
        draw_text_block(draw, tx, y + 48, lines, f_h, INK, 30)
        sub_lines = wrap(draw, sub, f_s, tw)
        draw_text_block(draw, tx, y + 48 + len(lines) * 30 + 8, sub_lines, f_s, GREY, 24)
        return
    icon(draw, x + 14, y + 44)
    lines = wrap(draw, headline, f_h, w - 28)
    draw_text_block(draw, x + 14, y + 124, lines, f_h, INK, 30)
    sub_lines = wrap(draw, sub, f_s, w - 28)
    draw_text_block(draw, x + 14, y + 124 + len(lines) * 30 + 8, sub_lines, f_s, GREY, 24)


def main():
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle(R(0, 0, W, 118), fill=NAVY)
    d.rectangle(R(0, 112, W, 118), fill=GOLD)
    f_kick = font(True, 19)
    kick = "THE WORLD IN ONE IMAGE  •  WORLD NEWS"
    d.text(P((W - d.textlength(kick, font=f_kick) // S) // 2, 12), kick,
           font=f_kick, fill=GOLD)
    f_date = font(True, 52)
    date = "TUESDAY 17 NOVEMBER 2026"
    d.text(P((W - d.textlength(date, font=f_date) // S) // 2, 44), date,
           font=f_date, fill=(255, 255, 255))

    # ---- lead story: Kerch Bridge ----
    lx, ly, lw, lh = 16, 132, 992, 318
    d.rectangle(R(lx, ly, lx + lw, ly + lh), fill=CARD, outline=BORDER, width=2 * S)
    bridge_scene(d, lx + 14, ly + 14, lx + 500, ly + lh - 14)
    tx = lx + 528
    tag(d, tx, ly + 18, "WAR IN UKRAINE", RED)
    f_h = font(True, 38)
    head = wrap(d, "Kerch Bridge span drops into the sea", f_h, lw - 528 - 28)
    draw_text_block(d, tx, ly + 56, head, f_h, INK, 46)
    f_s = font(False, 21)
    sub = ("Ukrainian drones and missiles collapse the road arch "
           "linking Russia to Crimea. The road link is cut; "
           "the rail line is damaged but standing.")
    draw_text_block(d, tx, ly + 56 + len(head) * 46 + 14,
                    wrap(d, sub, f_s, lw - 528 - 28), f_s, GREY, 28)

    # ---- row 1: three panels ----
    gy, gh = 464, 278
    pw, gap = 322, 13
    panels1 = [
        ("DIPLOMACY", (31, 111, 178), "Trump in Manila, eyes Xi–Putin talks",
         "Quad talks in the Philippines; Shenzhen trilateral due Thursday.",
         flags_row),
        ("SECURITY", (125, 60, 152), "Japan scrambles jets on Russian incursion",
         "Two suspected Russian planes enter its airspace — the first breach since 2024.",
         jet_icon),
        ("HUMANITARIAN", (183, 121, 31), "UN warns of Gaza winter emergency",
         "1.7m people still displaced; 1.4m face acute hunger, agencies say.",
         tents_icon),
    ]
    for i, (tg, tc, hd, sb, ic) in enumerate(panels1):
        panel(d, 16 + i * (pw + gap), gy, pw, gh, tg, tc, hd, sb, ic)

    # ---- row 2: two wide panels ----
    gy2, gh2 = 755, 214
    pw2 = 489
    panels2 = [
        ("CLIMATE", (46, 125, 50), "COP31 backs heat and cooling pact",
         "$20m+ pledged in Antalya as the world is set to pass 1.5°C.",
         sun_icon),
        ("U.S. POLITICS", (21, 101, 192), "Peltola flips Alaska Senate seat",
         "The Democrat beats Sen. Sullivan; her party claims 56 Senate seats.",
         ballot_icon),
    ]
    for i, (tg, tc, hd, sb, ic) in enumerate(panels2):
        panel(d, 16 + i * (pw2 + 14), gy2, pw2, gh2, tg, tc, hd, sb, ic, wide=True)

    # ---- footer ----
    d.rectangle(R(0, 982, W, H), fill=NAVY)
    f_f = font(False, 16)
    foot = ("All events happened or were first reported on 17 November 2026  •  "
            "Sources: Reuters, AP, UNEP, Kyodo News")
    d.text(P((W - d.textlength(foot, font=f_f) // S) // 2, 996), foot,
           font=f_f, fill=(220, 220, 220))

    img = img.resize((W, H), Image.LANCZOS)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
