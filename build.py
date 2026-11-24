"""Render entry.png (1024x1024) for make.fun news-image-20261123.

Build-time only (needs Pillow): python3 build.py. main.py just copies the PNG.
"""
from PIL import Image, ImageDraw, ImageFont

K = 2  # draw at 2x, downsample at the end for smooth edges
SIZE = 1024
FONTS = '/usr/share/fonts/truetype/noto/'

NAVY, AMBER, INK, CARD, BG = '#10243f', '#f4a52a', '#161616', '#fffdf7', '#f2ede2'
COL = {
    'WAR': '#bf2f2f', 'POLITICS': '#2d5b9e', 'MARKETS': '#18804a', 'SPORT': '#d1561a',
    'CULTURE': '#7a3b98', 'SCIENCE': '#11869a', 'SOCIETY': '#86681c',
}


def font(name, px):
    return ImageFont.truetype(f'{FONTS}NotoSans-Condensed{name}.ttf', round(px * K))


def serif(px):
    return ImageFont.truetype(FONTS + 'NotoSerif-CondensedBlack.ttf', round(px * K))


class Pen:
    """Draws on an image in 1x coordinates, scaled by K."""

    def __init__(self, im):
        self.im = im
        self.d = ImageDraw.Draw(im, 'RGBA')

    def box(self, x0, y0, x1, y1, fill=None, edge=None, w=1, r=0):
        self.d.rounded_rectangle([x0 * K, y0 * K, x1 * K, y1 * K], radius=r * K, fill=fill,
                                 outline=edge, width=round(w * K))

    def dot(self, x, y, r, fill, edge=None, w=1):
        self.d.ellipse([(x - r) * K, (y - r) * K, (x + r) * K, (y + r) * K], fill=fill,
                       outline=edge, width=round(w * K))

    def oval(self, x, y, rx, ry, fill):
        self.d.ellipse([(x - rx) * K, (y - ry) * K, (x + rx) * K, (y + ry) * K], fill=fill)

    def shape(self, pts, fill, edge=None, w=1):
        self.d.polygon([(x * K, y * K) for x, y in pts], fill=fill, outline=edge, width=round(w * K))

    def stroke(self, pts, fill, w):
        self.d.line([(x * K, y * K) for x, y in pts], fill=fill, width=round(w * K), joint='curve')

    def say(self, x, y, s, f, fill, anchor='la'):
        self.d.text((x * K, y * K), s, font=f, fill=fill, anchor=anchor)

    def width(self, s, f):
        return self.d.textlength(s, font=f) / K

    def fade(self, x0, y0, x1, y1, top, bot):
        a = [int(top[i:i + 2], 16) for i in (1, 3, 5)]
        b = [int(bot[i:i + 2], 16) for i in (1, 3, 5)]
        n = (y1 - y0) * K
        for i in range(n):
            t = i / max(1, n - 1)
            self.d.line([(x0 * K, y0 * K + i), (x1 * K, y0 * K + i)],
                        fill=tuple(round(p + (q - p) * t) for p, q in zip(a, b)))

    def tag(self, x, y, s):
        f = font('ExtraBold', 11)
        self.box(x, y, x + self.width(s, f) + 12, y + 17, fill=(0, 0, 0, 175), r=3)
        self.say(x + 6, y + 8.5, s, f, 'white', 'lm')

    def lines(self, s, f, maxw, most):
        out, cur = [], ''
        for word in s.split():
            trial = f'{cur} {word}'.strip()
            if self.width(trial, f) <= maxw:
                cur = trial
            else:
                out.append(cur)
                cur = word
        out.append(cur)
        assert len(out) <= most, (s, out)  # self-check: text fits its box
        return out


page = Pen(Image.new('RGB', (SIZE * K, SIZE * K), BG))


def inset(draw, x, y, w, h):
    sub = Pen(Image.new('RGB', (w * K, h * K), 'white'))
    draw(sub, w, h)
    page.im.paste(sub.im, (x * K, y * K))


# ------------------------------------------------------------------ hero pictures
def pic_nvidia(p, w, h):
    p.fade(0, 0, w, h, '#0b1f14', '#14391f')
    for gx in range(0, w, 30):
        p.stroke([(gx, 0), (gx, h)], '#1f4a2c', 1)
    for gy in range(0, h, 30):
        p.stroke([(0, gy), (w, gy)], '#1f4a2c', 1)
    # chip
    p.box(22, 30, 92, 100, fill='#76b900', r=6)
    p.box(34, 42, 80, 88, fill='#0f1a10', r=3)
    p.say(57, 65, 'AI', font('ExtraBold', 20), '#76b900', 'mm')
    for k in range(5):
        for x0, y0, x1, y1 in [(28 + k * 14, 22, 28 + k * 14, 30), (28 + k * 14, 100, 28 + k * 14, 108),
                               (14, 36 + k * 14, 22, 36 + k * 14), (92, 36 + k * 14, 100, 36 + k * 14)]:
            p.stroke([(x0, y0), (x1, y1)], '#c8e68a', 2)
    # price line rockets up on the right
    pts = [(108, 112), (130, 118), (150, 108), (168, 116), (186, 104), (204, 60), (226, 22)]
    p.stroke(pts, '#7dff9a', 4)
    p.shape([(226, 12), (234, 30), (216, 28)], '#7dff9a')
    p.say(150, 90, '+31%', font('ExtraBold', 26), 'white', 'mm')
    p.tag(6, h - 24, 'WALL STREET · NVIDIA')


def pic_libya(p, w, h):
    p.fade(0, 0, w, 90, '#f3b562', '#8a4f6d')
    p.box(0, 90, w, h, fill='#1b365a')
    p.box(0, 78, 70, 92, fill='#2a2c40')  # quay
    p.stroke([(18, 78), (18, 46), (46, 46), (46, 60)], '#2a2c40', 3)  # dock crane
    for x, y, r in [(156, 50, 20), (176, 32, 16), (138, 30, 14), (166, 14, 11)]:
        p.dot(x, y, r, '#5d636e')  # smoke
    p.shape([(76, 110), (214, 82), (222, 94), (96, 124)], '#59606d')  # listing hull
    p.shape([(76, 110), (214, 82), (216, 87), (79, 115)], '#9b2226')  # keel showing
    p.shape([(122, 100), (158, 92), (152, 70), (130, 75)], '#6d7584')
    p.stroke([(142, 73), (134, 46)], '#3b4150', 2.5)
    p.box(0, 110, w, h, fill=(27, 54, 90, 150))  # water over the sunk side
    p.dot(152, 84, 11, '#ff7a00')
    p.dot(152, 86, 6, '#ffd166')
    for bx, by in [(30, 128), (54, 138)]:  # sea drones and wakes
        p.shape([(bx, by), (bx + 16, by - 3), (bx + 16, by + 3)], '#0f0f0f')
        p.stroke([(bx - 26, by - 7), (bx, by)], '#cfe8ff', 1.5)
        p.stroke([(bx - 26, by + 7), (bx, by)], '#cfe8ff', 1.5)
    p.tag(6, h - 24, 'BENGHAZI, LIBYA')


def pic_nato(p, w, h):
    p.fade(0, 0, w, h, '#1d3f72', '#0e2140')
    # Poland outline (rough) with red-white band
    pl = [(70, 40), (120, 30), (168, 36), (186, 58), (180, 96), (190, 118), (150, 126), (110, 120),
          (80, 112), (62, 84), (66, 58)]
    p.shape(pl, '#e9edf3', '#ffffff', 1.5)
    p.shape([(62, 84), (80, 112), (110, 120), (150, 126), (190, 118), (180, 96), (64, 90)], '#dc143c')
    # two crash sites in the east
    for x, y in [(164, 100), (172, 72)]:
        p.dot(x, y, 9, '#ff7a00')
        p.dot(x, y, 4, '#ffd166')
    # missile tracks from the east
    p.stroke([(w, 70), (172, 72)], '#ffb3b3', 2)
    p.stroke([(w, 110), (164, 100)], '#ffb3b3', 2)
    # NATO compass star
    cx, cy = 36, 36
    p.dot(cx, cy, 22, '#0b1a33', '#ffffff', 2)
    p.shape([(cx, cy - 18), (cx + 4, cy), (cx, cy + 18), (cx - 4, cy)], '#ffffff')
    p.shape([(cx - 18, cy), (cx, cy - 4), (cx + 18, cy), (cx, cy + 4)], '#ffffff')
    p.tag(6, h - 24, 'NATO HQ · BRUSSELS')


def pic_hormuz(p, w, h):
    p.fade(0, 0, w, 94, '#ffd3a0', '#e3855a')
    p.box(0, 94, w, h, fill='#244652')
    for x, y, r in [(92, 68, 15), (84, 48, 18), (96, 26, 21), (80, 8, 19)]:
        p.dot(x, y, r, '#383838')
    p.shape([(30, 94), (200, 94), (190, 112), (40, 112)], '#2d2d38')  # tanker
    p.box(34, 90, 196, 95, fill='#7a2e2e')
    p.box(168, 72, 188, 91, fill='#f0f0f0')
    p.box(174, 64, 180, 73, fill='#d62828')
    p.dot(94, 86, 12, '#ff7a00')
    p.dot(94, 88, 6, '#ffd166')
    p.dot(60, 128, 8, '#101010')  # naval mine
    for ax, ay in [(-11, 0), (11, 0), (0, -11), (-8, -8), (8, -8)]:
        p.stroke([(60, 128), (60 + ax, 128 + ay)], '#101010', 2)
    p.box(150, 118, 236, 140, fill='#e6ecf2', r=3)  # blockade line of buoys
    p.say(193, 129, 'US BLOCKADE', font('ExtraBold', 11), '#1a2b44', 'mm')
    p.tag(6, h - 24, 'STRAIT OF HORMUZ')


HEROES = [
    (pic_nvidia, 'MARKETS', 'TECH · USA', 'Nvidia brings back Huang; stocks soar',
     'Board reinstates Jensen Huang as CEO. Nvidia +31%, Nasdaq +6.5%: best day since April 2025.'),
    (pic_libya, 'WAR', 'UKRAINE · RUSSIA · LIBYA', 'Zelensky: drones sank Russian warship',
     'Ukraine says sea drones sank a corvette in Benghazi. Kremlin calls a Baltic ship strike "terrorist".'),
    (pic_nato, 'POLITICS', 'NATO · POLAND', 'NATO meets on missiles in Poland',
     'Emergency council in Brussels after Russian missiles fell in Poland; AWACS jets reinforce.'),
    (pic_hormuz, 'WAR', 'IRAN · GULF', 'Hormuz tankers hit; Iran defies blockade',
     'IRGC says tankers hit mines as ship attacks hit a record pace; Iran vows "every means" vs US blockade.'),
]

# ------------------------------------------------------------------ grid stories 5..24
GRID = [  # (category, tag, headline, summary, lon, lat)
    ('POLITICS', 'USA · COURTS', 'Trump hush-money bid revived', 'Appeals court reopens his push to move the case to federal court.', -74.0, 40.7),
    ('SOCIETY', 'USA · IOWA', 'Court clears Iowa Army blast', '8th Circuit lets Army detonate ~5 tons of unstable lead azide.', -91.2, 40.8),
    ('POLITICS', 'CHINA', 'Spy official sentenced to death', 'Official "Ma" leaked state secrets to a foreign spy agency.', 116.4, 39.9),
    ('POLITICS', 'ZAMBIA', 'Opposition chief faces treason', 'Brian Mundubile and 13 others charged with plotting a coup.', 28.3, -15.4),
    ('SOCIETY', 'GERMANY · DENMARK', 'Bomb threats hit 450 schools', 'Emailed hoax threats in both countries; no evacuations ordered.', 10.5, 53.5),
    ('POLITICS', 'BELGIUM', 'De Wever sets budget deadline', 'No deal by Dec 31 ends his government, PM warns, amid a strike.', 4.35, 50.85),
    ('POLITICS', 'HUNGARY · UKRAINE', 'Magyar to visit Ukraine', 'Hungarian PM plans first trip by a Hungarian leader since 2015.', 19.0, 47.5),
    ('WAR', 'GAZA', 'Israeli strike kills UN worker', 'UNRWA staffer killed at a Jabalia water well; 3 others wounded.', 34.5, 31.5),
    ('WAR', 'SOUTH SUDAN', '24 civilians killed in Warrap', 'Attack blamed on SPLA-IO opposition forces; 7 children among dead.', 28.5, 8.5),
    ('WAR', 'COLOMBIA', 'Drones hit Cúcuta police base', 'Three civilians hurt, a baby among them; 60 homes damaged.', -72.5, 7.9),
    ('MARKETS', 'BRAZIL', 'Lula fiscal bill passes 353-128', 'Lower house approves spending curbs; dollar tops 6 reais.', -47.9, -15.8),
    ('MARKETS', 'OIL', 'Brent falls below $90', 'Lowest since August as Gulf supply recovers; surplus fears grow.', 51.5, 25.3),
    ('POLITICS', 'INDIA · NEPAL', 'India pledges $1.6bn to Nepal', 'Modi offers aid to rebuild after August Himalayan floods.', 77.2, 28.6),
    ('SOCIETY', 'INDIA', 'Delhi may admit only BS-VI cars', 'Supreme Court weighs a cleaner-vehicle-only rule against smog.', 82.0, 22.5),
    ('CULTURE', 'JAPAN', 'Shuri Castle hall reopens', 'Okinawa main hall rebuilt 7 years after 2019 fire opens to public.', 127.7, 26.2),
    ('SCIENCE', 'SPACE · NASA', 'NASA seeks a Moon reactor', 'Asks industry to build 20 kW Lunar Reactor-1 by 2030.', -81.7, 41.4),
    ('CULTURE', 'TV · NEW YORK', 'International Emmys', "France's 'Carême' wins best drama; Argentina takes comedy.", -76.0, 37.0),
    ('SPORT', 'CRICKET · NEW ZEALAND', 'NZ hold India to a draw', 'Wellington Test drawn; NZ 239/5 after India made 720/9 dec.', 174.8, -41.3),
    ('SPORT', 'FOOTBALL · ENGLAND', 'Brentford 4-0 Everton', 'Lewis-Potter double; Tarkowski sent off in Monday game.', -0.3, 51.5),
    ('SPORT', 'NFL · USA', 'Commanders stun Bengals 22-20', 'Drew Stevens kicks a walk-off field goal on Monday Night Football.', -84.5, 39.1),
]
assert len(GRID) == 20

# ------------------------------------------------------------------ masthead
page.box(0, 0, SIZE, 100, fill=NAVY)
page.say(22, 15, 'THE WORLD IN ONE PAGE  ·  DAILY NEWS SUMMARY', font('Bold', 14), AMBER)
page.say(20, 60, 'MONDAY 23 NOVEMBER 2026', serif(48), 'white', 'lm')
page.say(1004, 30, '24 stories · 6 continents', font('ExtraBold', 20), AMBER, 'rm')
page.say(1004, 55, 'Events that happened or were first', font('Medium', 14), '#dde5ef', 'rm')
page.say(1004, 74, 'reported on 23 Nov 2026 (any time zone)', font('Medium', 14), '#dde5ef', 'rm')
page.box(0, 100, SIZE, 104, fill=AMBER)

# ------------------------------------------------------------------ hero cards
XS = [16 + i * 250 for i in range(4)]
for i, (draw, cat, kicker, head, blurb) in enumerate(HEROES):
    x, y = XS[i], 112
    page.box(x, y, x + 242, 390, fill=CARD, edge='#d5cebf')
    inset(draw, x, y, 242, 146)
    page.dot(x + 228, y + 14, 11, NAVY, 'white', 1.5)
    page.say(x + 228, y + 14, str(i + 1), font('ExtraBold', 13), 'white', 'mm')
    page.box(x, y + 146, x + 242, y + 150, fill=COL[cat])
    page.say(x + 8, y + 158, kicker, font('ExtraBold', 12), COL[cat])
    for k, s in enumerate(page.lines(head, font('ExtraBold', 20), 228, 2)):
        page.say(x + 8, y + 174 + k * 23, s, font('ExtraBold', 20), INK)
    for k, s in enumerate(page.lines(blurb, font('Medium', 14), 228, 3)):
        page.say(x + 8, y + 224 + k * 17, s, font('Medium', 14), '#333333')

# ------------------------------------------------------------------ grid cards
TOP, STEP = 638, 72
for n, (cat, kicker, head, blurb, _, _) in enumerate(GRID):
    x, y = XS[n % 4], TOP + (n // 4) * STEP
    page.box(x, y, x + 242, y + 68, fill=CARD, edge='#dcd4c3')
    page.box(x, y, x + 5, y + 68, fill=COL[cat])
    page.say(x + 12, y + 4, f'{n + 5}  {kicker}', font('ExtraBold', 11), COL[cat])
    assert page.width(head, font('ExtraBold', 16)) <= 224, head
    page.say(x + 12, y + 17, head, font('ExtraBold', 16), INK)
    for k, s in enumerate(page.lines(blurb, font('Medium', 12.5), 224, 2)):
        page.say(x + 12, y + 38 + k * 14.5, s, font('Medium', 12.5), '#383838')

# ------------------------------------------------------------------ map band
MX, MY, MW, MH = 16, 398, 662, 232
W0, E0, N0, S0 = -130, 186, 66, -46  # lon/lat window


def at(lon, lat):
    return (lon - W0) * MW / (E0 - W0), (N0 - lat) * MH / (N0 - S0)


CONTINENTS = [
    # North America
    [(-165, 64), (-150, 70), (-125, 70), (-95, 72), (-80, 66), (-64, 58), (-56, 48), (-68, 44), (-72, 41),
     (-77, 35), (-81, 30), (-80, 25), (-85, 29), (-95, 29), (-97, 22), (-91, 17), (-87, 20), (-86, 13),
     (-80, 8), (-90, 13), (-104, 19), (-112, 27), (-118, 33), (-123, 39), (-124, 47), (-131, 55), (-148, 60)],
    # Greenland
    [(-52, 61), (-42, 61), (-22, 70), (-24, 80), (-58, 80), (-68, 75), (-54, 67)],
    # South America
    [(-79, 9), (-70, 12), (-61, 10), (-51, 2), (-36, -5), (-40, -20), (-49, -28), (-57, -36), (-64, -41),
     (-69, -51), (-74, -46), (-72, -32), (-70, -19), (-77, -12), (-81, -4), (-77, 4)],
    # Eurasia
    [(-9, 37), (-9, 43), (-1, 46), (-4, 48), (2, 51), (7, 54), (9, 58), (6, 62), (16, 69), (30, 70), (42, 67),
     (62, 70), (82, 73), (110, 76), (142, 72), (180, 68), (178, 63), (160, 59), (141, 52), (134, 43),
     (128, 36), (123, 39), (121, 30), (116, 23), (107, 20), (105, 9), (100, 12), (101, 3), (98, 9), (96, 17),
     (90, 22), (85, 20), (80, 13), (77, 8), (72, 21), (66, 25), (57, 25), (51, 29), (49, 28), (55, 24),
     (59, 21), (54, 16), (44, 12), (39, 21), (34, 28), (35, 33), (36, 36), (27, 37), (26, 41), (22, 37),
     (19, 41), (13, 45), (16, 40), (11, 38), (9, 44), (3, 43), (-4, 36)],
    # Africa
    [(-16, 22), (-17, 14), (-9, 5), (6, 4), (9, 2), (9, -2), (13, -11), (12, -17), (19, -34), (27, -33),
     (33, -25), (36, -18), (40, -14), (41, -2), (51, 11), (44, 11), (39, 16), (33, 28), (31, 31), (19, 31),
     (10, 36), (-1, 36), (-7, 35), (-11, 28)],
    # Britain and Ireland
    [(-5, 50), (1, 51), (0, 53), (-3, 56), (-5, 58), (-6, 56), (-4, 54)],
    [(-10, 52), (-6, 52), (-6, 55), (-9, 54)],
    # Japan
    [(130, 32), (136, 34), (140, 35), (141, 39), (142, 44), (140, 43), (139, 38), (135, 35), (131, 34)],
    # Australia
    [(114, -23), (121, -19), (129, -14), (136, -12), (142, -11), (145, -17), (153, -26), (150, -37),
     (141, -38), (136, -34), (130, -32), (117, -35), (115, -30)],
    # Indonesia and New Guinea
    [(95, 5), (105, -5), (103, -5), (98, 1)],
    [(109, 2), (118, 7), (119, 1), (116, -4), (110, -3)],
    [(106, -6), (114, -7), (114, -8), (106, -7)],
    [(131, -1), (141, -3), (150, -10), (142, -9), (137, -5)],
    # Madagascar, New Zealand
    [(44, -25), (50, -16), (49, -12), (43, -22)],
    [(173, -35), (178, -38), (175, -41), (168, -46), (172, -42)],
]


def pic_map(p, w, h):
    p.box(0, 0, w, h, fill='#d7e5ee')
    for c in CONTINENTS:
        p.shape([at(*pt) for pt in c], '#cdc5af', '#b2a990', 0.8)
    pins = [(-77.0, 38.9, 'MARKETS'), (20.1, 32.1, 'WAR'), (22.5, 50.5, 'POLITICS'), (56.3, 26.6, 'WAR')]
    pins += [(lon, lat, cat) for cat, _, _, _, lon, lat in GRID]
    for lon, lat, cat in pins:
        px, py = at(lon, lat)
        p.dot(px, py, 5.5, COL[cat], 'white', 1.5)
    p.box(8, 8, 168, 28, fill=NAVY, r=3)
    p.say(16, 18, 'WHERE IT HAPPENED', font('ExtraBold', 13), 'white', 'lm')
    p.box(8, 118, 86, 224, fill=(255, 255, 255, 205), r=3)  # legend over the Pacific
    for k, (cat, c) in enumerate(COL.items()):
        p.dot(18, 128 + k * 15, 5, c, 'white', 1)
        p.say(28, 128 + k * 15, cat.title(), font('Bold', 12), '#25303e', 'lm')
    p.box(0, 0, w, h, edge='#b5c5d2')


inset(pic_map, MX, MY, MW, MH)

# ------------------------------------------------------------------ numbers box
NX0, NX1 = 686, 1008
page.box(NX0, MY, NX1, MY + MH, fill=NAVY)
page.say(NX0 + 14, MY + 18, 'THE DAY IN NUMBERS', font('ExtraBold', 15), AMBER, 'lm')
NUMBERS = [
    ('+31%', 'Nvidia shares on Huang return'),
    ('+6.5%', 'Nasdaq: best day since April 2025'),
    ('450', 'German schools sent bomb threats'),
    ('353-128', "Brazil's lower-house fiscal vote"),
    ('20 kW', 'NASA Moon reactor, due by 2030'),
]
for k, (big, small) in enumerate(NUMBERS):
    y = MY + 50 + k * 39
    page.say(NX0 + 14, y, big, font('ExtraBold', 25), AMBER, 'lm')
    assert page.width(big, font('ExtraBold', 25)) <= 112, big
    assert page.width(small, font('Medium', 13)) <= NX1 - NX0 - 140, small
    page.say(NX0 + 128, y, small, font('Medium', 13), '#edf1f7', 'lm')
    if k:
        page.stroke([(NX0 + 14, y - 19.5), (NX1 - 14, y - 19.5)], '#2e3f62', 1)

# ------------------------------------------------------------------ footer
page.say(16, 1015, 'Sources: Reuters · AP · AFP · CNBC · CNN · Al Jazeera · NASA · ESPNcricinfo · Sky Sports · '
         'Japan Times · Deadline · Euronews · Rio Times · ANI', font('Medium', 11), '#555555', 'lm')

page.im.resize((SIZE, SIZE), Image.LANCZOS).save('entry.png', optimize=True)
print('wrote entry.png')
