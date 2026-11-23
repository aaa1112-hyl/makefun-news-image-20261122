"""Draw the front page for 22 November 2026 with Pillow.

A newspaper front page, 1024x1024: masthead, one lead story and seven
smaller panels, each with a short headline and a flat-style illustration
drawn from simple shapes. All text is rendered by Pillow, so every word
is crisp and legible. Run: python3 generate_image.py -> entry.png
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (176, 42, 42)
GREY = (90, 86, 78)
SKY = (174, 214, 232)
SEA = (38, 98, 140)
SAND = (232, 214, 170)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap, returns list of lines fitting width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=1.18):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def kicker(draw, x, y, label, width):
    f = font(SANS_B, 19)
    draw.text((x, y), label.upper(), font=f, fill=RED)
    return y + 26


def headline(draw, x, y, text, size, width, max_lines=3):
    f = font(SERIF, size)
    lines = wrap(draw, text, f, width)[:max_lines]
    return text_block(draw, x, y, lines, f, leading=1.06)


def deck(draw, x, y, text, width, size=21):
    f = font(SANS, size)
    lines = wrap(draw, text, f, width)
    return text_block(draw, x, y, lines, f, leading=1.25)


def rule(draw, x, y, x2, width=2, fill=INK):
    draw.line([(x, y), (x2, y)], fill=fill, width=width)


def panel_box(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.line([(x, y + 2), (x + w, y + 2)], fill=INK, width=2)


# ---------- flat illustrations (simple shapes, clean colours) ----------

def draw_globe(d, x, y, w, h):
    """Earth cracking under a hot sun: the climate summit."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 226, 178))
    d.ellipse([x + w - 95, y + 12, x + w - 15, y + 92], fill=(240, 150, 40))
    cx, cy, r = x + w // 2 - 20, y + h // 2 + 25, 118
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 140, 190))
    d.ellipse([cx - 70, cy - 88, cx + 5, cy - 30], fill=(74, 160, 90))
    d.ellipse([cx + 10, cy - 10, cx + 85, cy + 55], fill=(74, 160, 90))
    d.ellipse([cx - 45, cy + 45, cx + 30, cy + 100], fill=(74, 160, 90))
    # crack across the globe
    d.line([(cx - 60, cy - 95), (cx - 20, cy - 40), (cx - 45, cy + 5),
            (cx + 10, cy + 45), (cx - 5, cy + 95)], fill=(30, 30, 30), width=7)


def draw_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + 62, x + w, y + h], fill=SEA)
    # funnel
    d.rectangle([x + w - 150, y + 6, x + w - 110, y + 38], fill=(200, 200, 200))
    # fire and smoke above the deck
    d.ellipse([x + 130, y + 4, x + 190, y + 44], fill=(255, 150, 40))
    d.ellipse([x + 160, y + 0, x + 230, y + 40], fill=(255, 200, 80))
    d.ellipse([x + 200, y + 12, x + 260, y + 52], fill=(90, 90, 90))
    d.ellipse([x + 235, y + 2, x + 295, y + 42], fill=(120, 120, 120))
    # burning tanker hull
    d.rectangle([x + 60, y + 38, x + w - 60, y + 62], fill=(140, 40, 32))
    d.rectangle([x + 60, y + 62, x + w - 60, y + 70], fill=(90, 26, 22))
    # second tanker, distant
    d.rectangle([x + w - 260, y + 48, x + w - 40, y + 66], fill=(110, 60, 50))
    d.line([(x + 20, y + 82), (x + 120, y + 82)], fill=(255, 255, 255), width=3)
    d.line([(x + w - 220, y + 90), (x + w - 60, y + 90)], fill=(255, 255, 255), width=3)


def draw_warship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 225, 235))
    d.rectangle([x, y + 62, x + w, y + h], fill=(50, 90, 120))
    # superstructure and mast
    d.rectangle([x + 150, y + 6, x + 260, y + 34], fill=(90, 100, 110))
    d.rectangle([x + 190, y + 0, x + 205, y + 8], fill=(90, 100, 110))
    # warship hull
    d.polygon([(x + 40, y + 34), (x + w - 30, y + 34),
               (x + w - 90, y + 62), (x + 80, y + 62)], fill=(70, 80, 90))
    # explosion above the deck, kept inside the sky
    d.ellipse([x + w - 210, y + 6, x + w - 130, y + 62], fill=(255, 170, 40))
    d.ellipse([x + w - 185, y + 0, x + w - 115, y + 48], fill=(255, 220, 90))
    d.ellipse([x + w - 235, y + 20, x + w - 175, y + 60], fill=(80, 80, 80))
    d.line([(x + 30, y + 78), (x + 130, y + 78)], fill=(255, 255, 255), width=3)
    d.line([(x + w - 200, y + 86), (x + w - 40, y + 86)], fill=(255, 255, 255), width=3)


def draw_flats(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 220, 200))
    # two apartment blocks, one hit (scaled to the box width)
    bw = w // 2 - 14
    d.rectangle([x + 8, y + 55, x + 8 + bw, y + h - 8], fill=(150, 140, 125))
    d.rectangle([x + w // 2 + 6, y + 75, x + w - 8, y + h - 8],
                fill=(120, 112, 100))
    for r in range(3):
        for c in range(2):
            d.rectangle([x + 16 + c * 40, y + 68 + r * 30,
                         x + 36 + c * 40, y + 88 + r * 30],
                        fill=(255, 230, 140))
    for r in range(2):
        for c in range(2):
            d.rectangle([x + w // 2 + 14 + c * 40, y + 88 + r * 30,
                         x + w // 2 + 34 + c * 40, y + 108 + r * 30],
                        fill=(255, 230, 140))
    # smoke and fire from the hit block
    d.ellipse([x + 20, y + 6, x + 80, y + 52], fill=(255, 140, 30))
    d.ellipse([x + 55, y - 4, x + 105, y + 36], fill=(90, 90, 90))
    d.ellipse([x + 2, y + 18, x + 45, y + 48], fill=(130, 130, 130))


def draw_un(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 228, 235))
    # UN-style slab building with flag poles (scaled to the box width)
    bw = w - 60
    d.rectangle([x + 30, y + 48, x + 30 + bw, y + h - 8], fill=(170, 190, 205))
    for r in range(4):
        for c in range(3):
            d.rectangle([x + 42 + c * 40, y + 62 + r * 24,
                         x + 66 + c * 40, y + 80 + r * 24],
                        fill=(40, 70, 100))
    d.rectangle([x + 14, y + 26, x + 18, y + 48], fill=INK)
    d.rectangle([x + w - 18, y + 26, x + w - 14, y + 48], fill=INK)
    d.polygon([(x + 18, y + 26), (x + 44, y + 33), (x + 18, y + 40)],
              fill=(60, 110, 200))
    # drone strike burst
    d.ellipse([x + w - 70, y + 8, x + w - 16, y + 56], fill=(255, 170, 40))
    d.ellipse([x + w - 58, y + 20, x + w - 28, y + 48], fill=(255, 220, 90))


def draw_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(215, 228, 240))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 150, 110))
    cx = x + w // 2
    # dome
    d.ellipse([cx - 30, y + 10, cx + 30, y + 62], fill=(240, 240, 235))
    d.rectangle([cx - 36, y + 56, cx + 36, y + h - 24], fill=(235, 235, 230))
    d.rectangle([cx - 3, y + 2, cx + 3, y + 12], fill=INK)
    for i in range(4):
        px = cx - 26 + i * 14
        d.rectangle([px, y + 64, px + 7, y + h - 24], fill=(200, 205, 200))
    d.rectangle([x + 8, y + h - 24, x + w - 8, y + h - 18],
                fill=(220, 220, 215))


def draw_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 185, 160))
    cx = x + w // 2
    # mountain with tunnel entrance
    d.polygon([(x, y + h), (cx, y + 8), (x + w, y + h)], fill=(110, 100, 88))
    d.polygon([(cx - 30, y + h), (cx, y + 62), (cx + 30, y + h)],
              fill=(40, 38, 34))
    d.rectangle([cx - 5, y + 80, cx + 5, y + h - 10], fill=(220, 220, 220))
    d.polygon([(cx - 5, y + 80), (cx, y + 66), (cx + 5, y + 80)],
              fill=(200, 60, 50))
    d.rectangle([x + 8, y + h - 30, x + w - 8, y + h - 24], fill=(90, 82, 72))


def draw_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 214, 195))
    # factory with sawtooth roof and chimney smoke
    d.rectangle([x + 8, y + 78, x + w - 8, y + h - 8], fill=(160, 120, 90))
    d.polygon([(x + 8, y + 78), (x + w // 2 - 6, y + 52),
               (x + w // 2 + 6, y + 78)], fill=(120, 90, 66))
    d.polygon([(x + w // 2 - 6, y + 78), (x + w - 20, y + 52),
               (x + w - 8, y + 78)], fill=(120, 90, 66))
    d.rectangle([x + w - 24, y + 24, x + w - 12, y + 78], fill=(140, 60, 50))
    d.ellipse([x + w - 52, y - 4, x + w - 8, y + 36], fill=(90, 90, 90))
    d.ellipse([x + w - 66, y + 16, x + w - 30, y + 48], fill=(120, 120, 120))
    d.ellipse([x + 16, y + 80, x + 56, y + 106], fill=(255, 150, 40))
    for i in range(2):
        d.rectangle([x + 16 + i * 34, y + 96, x + 36 + i * 34, y + 116],
                    fill=(255, 230, 140))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    f_mast = font(SERIF, 96)
    d.text((W // 2, 8), "THE WORLD", font=f_mast, fill=INK, anchor="ma")
    rule(d, 24, 116, W - 24, width=3)
    f_date = font(SANS_B, 26)
    d.text((24, 126), "SUNDAY 22 NOVEMBER 2026", font=f_date, fill=RED)
    d.text((W - 24, 126), "THE WORLD IN ONE IMAGE", font=f_date, fill=INK,
           anchor="ra")

    # ---- lead story: COP31 ----
    y0 = 164
    lead_h = 300
    panel_box(d, 24, y0, W - 48, lead_h)
    d.rectangle([24, y0, W - 24, y0 + lead_h], fill=PAPER)
    d.rectangle([24, y0, 500, y0 + lead_h], fill=(250, 246, 238))
    draw_globe(d, 512, y0 + 8, 464, lead_h - 16)
    x = 44
    y = y0 + 16
    y = kicker(d, x, y, "Climate — Antalya, Turkey", 440)
    y = headline(d, x, y + 4, "CLIMATE TALKS COLLAPSE", 54, 440)
    y = deck(d, x, y + 10,
             "COP31 ends with no deal: the EU rejects a text that never "
             "mentions fossil fuels.", 440, size=20)

    # ---- middle row: two panels ----
    y1 = 472
    ph = 250
    pw = 476
    # Hormuz
    panel_box(d, 24, y1, pw, ph)
    draw_tanker(d, 26, y1 + 2, pw - 4, 104)
    yy = y1 + 112
    yy = kicker(d, 36, yy, "Gulf — Strait of Hormuz", pw - 24)
    yy = headline(d, 36, yy + 2, "TANKERS HIT BY MINES", 32, pw - 24)
    deck(d, 36, yy + 4, "Two supertankers catch fire east of the strait.",
         pw - 24, size=18)
    # Benghazi
    panel_box(d, 524, y1, pw, ph)
    draw_warship(d, 526, y1 + 2, pw - 4, 104)
    yy = y1 + 112
    yy = kicker(d, 536, yy, "Libya — Benghazi", pw - 24)
    yy = headline(d, 536, yy + 2, "DRONE HITS RUSSIAN WARSHIP", 32, pw - 24)
    deck(d, 536, yy + 4, "A sea drone strikes the corvette Merkury.",
         pw - 24, size=18)

    # ---- second row: two panels ----
    y2 = 730
    ph2 = 158
    # Kyiv
    panel_box(d, 24, y2, pw, ph2)
    draw_flats(d, 26, y2 + 2, 190, ph2 - 4)
    xx = 232
    yy = y2 + 10
    yy = kicker(d, xx, yy, "Ukraine — Kyiv region", pw - 220)
    yy = headline(d, xx, yy + 2, "FLATS HIT, EIGHT KILLED", 28, pw - 220)
    deck(d, xx, yy + 4, "Russian drones strike an apartment block; a boy "
         "of 7 dies in Kryvyi Rih.", pw - 220, size=17)
    # Khartoum
    panel_box(d, 524, y2, pw, ph2)
    draw_un(d, 526, y2 + 2, 190, ph2 - 4)
    xx = 732
    yy = y2 + 10
    yy = kicker(d, xx, yy, "Sudan — Khartoum", pw - 220)
    yy = headline(d, xx, yy + 2, "DRONES HIT UN BUILDING", 28, pw - 220)
    deck(d, xx, yy + 4, "Four killed near the capital in attacks blamed "
         "on the RSF.", pw - 220, size=17)

    # ---- bottom row: three small panels, kicker + headline only ----
    y3 = 896
    ph3 = 112
    bw = 312
    # Washington
    panel_box(d, 24, y3, bw, ph3)
    draw_capitol(d, 26, y3 + 2, 100, ph3 - 4)
    xx = 140
    yy = y3 + 8
    yy = kicker(d, xx, yy, "USA", bw - 128)
    headline(d, xx, yy + 2, "DEMOCRATS TAKE THE HOUSE", 22, bw - 128)
    # Iran
    panel_box(d, 356, y3, bw, ph3)
    draw_missile(d, 358, y3 + 2, 100, ph3 - 4)
    xx = 472
    yy = y3 + 8
    yy = kicker(d, xx, yy, "Iran", bw - 128)
    headline(d, xx, yy + 2, "MISSILE CITY UNVEILED", 22, bw - 128)
    # Indonesia
    panel_box(d, 688, y3, bw, ph3)
    draw_factory(d, 690, y3 + 2, 100, ph3 - 4)
    xx = 804
    yy = y3 + 8
    yy = kicker(d, xx, yy, "Indonesia", bw - 128)
    headline(d, xx, yy + 2, "FACTORY FIRE: 3 DEAD", 22, bw - 128)

    return img


if __name__ == "__main__":
    build().save("entry.png", optimize=True)
    print("wrote entry.png")
