"""
Line-art designs for "Color & Smile!" - a big & easy coloring book for ages 3-5.

Every design is drawn on a 600 x 700 canvas. Each closed shape is a
"region" that a child can fill (on paper or with a tap on the website).
Helpers take an optional colour `f` that is only used for the coloured
cover/preview renders; the coloring pages themselves are always white.
"""
import math

STROKE = 7


class Art:
    def __init__(self, title):
        self.title = title
        self.items = []  # (kind, markup-without-fill-attr, colour)

    # ---- fillable regions -------------------------------------------------
    def _r(self, tag, attrs, f):
        self.items.append(("region", tag, attrs, f))
        return self

    def c(self, x, y, r, f="#fff"):
        return self._r("circle", f'cx="{x}" cy="{y}" r="{r}"', f)

    def e(self, x, y, rx, ry, rot=0, f="#fff"):
        t = f' transform="rotate({rot} {x} {y})"' if rot else ""
        return self._r("ellipse", f'cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"{t}', f)

    def rect(self, x, y, w, h, rx=0, f="#fff", rot=0):
        t = f' transform="rotate({rot} {x + w / 2} {y + h / 2})"' if rot else ""
        return self._r("rect", f'x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"{t}', f)

    def poly(self, pts, f="#fff"):
        s = " ".join(f"{round(a, 1)},{round(b, 1)}" for a, b in pts)
        return self._r("polygon", f'points="{s}"', f)

    def p(self, d, f="#fff"):
        return self._r("path", f'd="{d}"', f)

    def star(self, x, y, R, r, n=5, rot=-90, f="#fff"):
        pts = []
        for i in range(n * 2):
            rad = R if i % 2 == 0 else r
            a = math.radians(rot + i * 180 / n)
            pts.append((x + rad * math.cos(a), y + rad * math.sin(a)))
        return self.poly(pts, f)

    # ---- decoration (not fillable) ----------------------------------------
    def line(self, d, w=STROKE):
        self.items.append(("line", "path", f'd="{d}" stroke-width="{w}"', None))
        return self

    def dot(self, x, y, r=9):
        self.items.append(("dot", "circle", f'cx="{x}" cy="{y}" r="{r}"', None))
        return self

    def eyes(self, x1, y1, x2, y2, r=10):
        for x, y in ((x1, y1), (x2, y2)):
            self.dot(x, y, r)
            self.items.append(("shine", "circle", f'cx="{x + r * 0.35}" cy="{y - r * 0.35}" r="{r * 0.3}"', None))
        return self

    def smile(self, x, y, w=40, h=18):
        return self.line(f"M{x - w / 2},{y} Q{x},{y + h * 2} {x + w / 2},{y}")

    # ---- output -------------------------------------------------------------
    def svg_body(self, colored=False, interactive=False):
        out = []
        rid = 0
        for kind, tag, attrs, f in self.items:
            if kind == "region":
                fill = f if colored else "#fff"
                extra = f' class="rg" data-r="{rid}"' if interactive else ""
                out.append(f'<{tag} {attrs} fill="{fill}"{extra}/>')
                rid += 1
            elif kind == "line":
                out.append(f'<{tag} {attrs} fill="none" class="ln"/>')
            elif kind == "dot":
                out.append(f'<{tag} {attrs} fill="#111" stroke="none" class="ln"/>')
            elif kind == "shine":
                out.append(f'<{tag} {attrs} fill="#fff" stroke="none" class="ln"/>')
        return "\n".join(out)

    def svg(self, colored=False, interactive=False, label=True, bg=True):
        body = self.svg_body(colored, interactive)
        h = 700
        lab = ""
        if label:
            h = 800
            fill = "#fff"
            extra = ' class="rg lbl"' if interactive else ""
            lab = (f'<text x="300" y="770" text-anchor="middle" font-family="Fredoka, sans-serif" '
                   f'font-weight="700" font-size="74" letter-spacing="4" fill="{fill}" stroke="#111" '
                   f'stroke-width="5" paint-order="stroke"{extra}>{self.title.upper()}</text>')
        bgrect = ""
        if bg:
            extra = ' class="rg bg"' if interactive else ""
            bgrect = f'<rect x="0" y="0" width="600" height="{h}" fill="#fff" stroke="none"{extra}/>'
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 {h}">'
                f'<g stroke="#111" stroke-width="{STROKE}" stroke-linejoin="round" stroke-linecap="round">'
                f'{bgrect}{body}</g>{lab}</svg>')


def ground(a, y=610, f="#9be37a"):
    a.p(f"M-10,{y} Q150,{y - 30} 300,{y} T610,{y} L610,710 L-10,710 Z", f)


# ---------------------------------------------------------------------------
def sun():
    a = Art("Sun")
    for i in range(12):
        ang = math.radians(i * 30)
        cx, cy = 300, 330
        tip = (cx + 250 * math.cos(ang), cy + 250 * math.sin(ang))
        l = (cx + 150 * math.cos(ang - 0.2), cy + 150 * math.sin(ang - 0.2))
        r = (cx + 150 * math.cos(ang + 0.2), cy + 150 * math.sin(ang + 0.2))
        a.poly([l, tip, r], "#ff9f1c")
    a.c(300, 330, 150, "#ffd93d")
    a.c(225, 375, 24, "#ff8fab").c(375, 375, 24, "#ff8fab")
    a.eyes(250, 300, 350, 300, 14).smile(300, 380, 90, 22)
    return a


def cat():
    a = Art("Cat")
    a.p("M430,560 C560,560 560,380 500,330 C480,315 465,335 480,350 C520,400 510,520 430,520 Z", "#f4a261")
    a.e(300, 500, 150, 120, 0, "#f4a261")
    a.e(300, 530, 80, 70, 0, "#ffe8d6")
    a.poly([(185, 200), (205, 70), (285, 165)], "#f4a261")
    a.poly([(415, 200), (395, 70), (315, 165)], "#f4a261")
    a.poly([(208, 175), (215, 110), (255, 160)], "#ffb4c2")
    a.poly([(392, 175), (385, 110), (345, 160)], "#ffb4c2")
    a.c(300, 270, 130, "#f4a261")
    a.e(220, 620, 55, 30, 0, "#f4a261").e(380, 620, 55, 30, 0, "#f4a261")
    a.eyes(250, 250, 350, 250, 15)
    a.poly([(285, 290), (315, 290), (300, 308)], "#ff8fab")
    a.line("M300,308 L300,325 M300,325 Q280,345 262,330 M300,325 Q320,345 338,330")
    a.line("M240,300 L160,285 M240,315 L160,320 M360,300 L440,285 M360,315 L440,320", 5)
    return a


def fish():
    a = Art("Fish")
    a.c(110, 160, 22, "#bde0fe").c(80, 90, 14, "#bde0fe").c(140, 60, 10, "#bde0fe")
    a.poly([(440, 360), (570, 250), (570, 470)], "#ff7b54")
    a.p("M250,250 Q300,150 380,250 Z", "#ffb26b")
    a.p("M260,450 Q300,540 360,450 Z", "#ffb26b")
    a.e(290, 360, 190, 120, 0, "#ff9f43")
    a.p("M330,250 Q380,360 330,470", "#ffd56b")
    a.c(180, 330, 30, "#fff")
    a.dot(188, 330, 14)
    a.line("M120,390 Q140,410 165,395")
    a.e(300, 650, 280, 30, 0, "#f6e3a1")
    a.p("M470,640 C450,560 500,540 480,470 C520,520 520,580 500,640 Z", "#7bd389")
    return a


def house():
    a = Art("House")
    ground(a, 620)
    a.rect(390, 150, 50, 110, 0, "#c0392b")
    a.poly([(90, 330), (300, 140), (510, 330)], "#e76f51")
    a.rect(130, 320, 340, 290, 0, "#ffd166")
    a.rect(255, 450, 90, 160, 10, "#8d5524")
    a.dot(325, 530, 8)
    a.rect(160, 370, 70, 70, 6, "#a2d2ff").rect(370, 370, 70, 70, 6, "#a2d2ff")
    a.line("M195,370 L195,440 M160,405 L230,405 M405,370 L405,440 M370,405 L440,405", 5)
    a.c(300, 260, 30, "#a2d2ff")
    a.c(90, 100, 50, "#ffd93d")
    return a


def apple():
    a = Art("Apple")
    a.rect(290, 130, 26, 90, 12, "#8d5524", rot=10)
    a.p("M318,170 Q380,90 460,130 Q400,210 318,170 Z", "#57cc99")
    a.p("M300,220 C230,160 90,190 100,360 C110,520 220,600 300,560 "
        "C380,600 490,520 500,360 C510,190 370,160 300,220 Z", "#ef476f")
    a.p("M170,300 Q160,360 185,410", "#fff")
    a.eyes(250, 380, 350, 380, 13).smile(300, 430, 70, 18)
    return a


def butterfly():
    a = Art("Butterfly")
    a.line("M290,210 Q250,120 210,100 M310,210 Q350,120 390,100")
    a.c(210, 100, 16, "#9b5de5").c(390, 100, 16, "#9b5de5")
    a.e(180, 290, 140, 110, -25, "#f15bb5").e(420, 290, 140, 110, 25, "#f15bb5")
    a.e(200, 480, 100, 80, 30, "#fee440").e(400, 480, 100, 80, -30, "#fee440")
    a.c(170, 280, 45, "#00bbf9").c(430, 280, 45, "#00bbf9")
    a.c(200, 490, 30, "#00f5d4").c(400, 490, 30, "#00f5d4")
    a.e(300, 380, 30, 170, 0, "#9b5de5")
    a.c(300, 200, 40, "#9b5de5")
    a.eyes(285, 195, 315, 195, 7).smile(300, 215, 26, 8)
    return a


def car():
    a = Art("Car")
    a.rect(0, 560, 600, 140, 0, "#adb5bd")
    a.line("M40,630 L120,630 M200,630 L280,630 M360,630 L440,630 M520,630 L590,630", 10)
    a.p("M170,330 Q200,220 300,220 L370,220 Q430,220 460,330 Z", "#4cc9f0")
    a.p("M60,350 Q60,320 100,330 L500,330 Q560,330 560,380 L560,470 Q560,500 530,500 L70,500 Q50,500 50,470 Z", "#f72585")
    a.p("M205,320 Q225,245 290,245 L300,245 L300,320 Z", "#caf0f8")
    a.p("M325,320 L325,245 L365,245 Q415,245 435,320 Z", "#caf0f8")
    a.rect(510, 370, 40, 30, 8, "#ffd93d")
    a.c(170, 500, 65, "#333").c(430, 500, 65, "#333")
    a.c(170, 500, 28, "#ced4da").c(430, 500, 28, "#ced4da")
    a.line("M290,380 L330,380", 8)
    return a


def flower():
    a = Art("Flower")
    a.rect(285, 330, 30, 260, 10, "#57cc99")
    a.e(220, 470, 70, 30, -30, "#80ed99").e(380, 430, 70, 30, 30, "#80ed99")
    for i in range(8):
        ang = i * 45
        x = 300 + 110 * math.cos(math.radians(ang))
        y = 250 + 110 * math.sin(math.radians(ang))
        a.e(round(x, 1), round(y, 1), 70, 42, ang, "#ff70a6")
    a.c(300, 250, 75, "#ffd670")
    a.eyes(272, 240, 328, 240, 11).smile(300, 270, 50, 12)
    a.poly([(170, 570), (430, 570), (395, 690), (205, 690)], "#e07a5f")
    a.rect(150, 545, 300, 50, 10, "#f2a07b")
    return a


def dinosaur():
    a = Art("Dinosaur")
    ground(a, 640, "#b5e48c")
    for x, y in [(170, 340), (240, 300), (320, 300), (395, 330)]:
        a.poly([(x - 35, y + 40), (x, y - 30), (x + 35, y + 40)], "#ff9f1c")
    a.p("M120,460 Q40,470 20,380 Q90,440 160,410 Z", "#06d6a0")
    a.rect(170, 480, 60, 140, 25, "#06d6a0").rect(350, 480, 60, 140, 25, "#06d6a0")
    a.e(290, 440, 190, 120, 0, "#06d6a0")
    a.p("M400,400 Q420,260 450,220 L520,240 Q490,300 480,420 Z", "#06d6a0")
    a.e(490, 200, 85, 60, 0, "#06d6a0")
    a.e(280, 470, 110, 60, 0, "#b8f2e6")
    a.eyes(500, 185, 0, 0, 12)
    a.items.pop(); a.items.pop()  # only one eye (side view)
    a.smile(530, 225, 50, 10)
    a.dot(560, 195, 5)
    return a


def rocket():
    a = Art("Rocket")
    a.star(90, 120, 40, 18, f="#ffd93d").star(510, 200, 32, 14, f="#ffd93d").star(120, 520, 28, 12, f="#ffd93d")
    a.p("M260,560 Q300,690 340,560 Z", "#ff9f1c")
    a.p("M280,560 Q300,630 320,560 Z", "#ffd93d")
    a.p("M230,430 L150,560 L240,540 Z", "#ef476f").p("M370,430 L450,560 L360,540 Z", "#ef476f")
    a.p("M300,90 C400,170 400,400 370,560 L230,560 C200,400 200,170 300,90 Z", "#e9ecef")
    a.p("M300,90 C340,120 360,160 372,200 L228,200 C240,160 260,120 300,90 Z", "#ef476f")
    a.c(300, 300, 50, "#4cc9f0").c(300, 300, 30, "#a2d2ff")
    a.rect(270, 390, 60, 120, 20, "#ef476f")
    return a


def turtle():
    a = Art("Turtle")
    ground(a, 600, "#c7f9cc")
    a.e(160, 520, 45, 35, 0, "#8ac926").e(440, 520, 45, 35, 0, "#8ac926")
    a.poly([(520, 440), (580, 470), (520, 480)], "#8ac926")
    a.c(110, 380, 75, "#8ac926")
    a.p("M140,480 Q150,240 320,240 Q490,240 500,480 Z", "#6a994e")
    a.rect(130, 465, 380, 40, 20, "#a7c957")
    hexes = [(320, 330), (240, 400), (400, 400), (320, 430)]
    for x, y in hexes:
        a.poly([(x + 45 * math.cos(math.radians(60 * k)), y + 40 * math.sin(math.radians(60 * k))) for k in range(6)], "#f2e8cf")
    a.eyes(90, 360, 0, 0, 11)
    a.items.pop(); a.items.pop()
    a.smile(80, 400, 40, 10)
    return a


def icecream():
    a = Art("Ice Cream")
    a.poly([(190, 380), (410, 380), (300, 670)], "#e9c46a")
    a.line("M230,430 L360,540 M260,400 L400,420 M210,430 L340,600 M360,430 L250,560 M300,400 L220,460 M400,400 L280,640", 5)
    a.c(300, 330, 110, "#ff8fab")
    a.c(225, 230, 90, "#a0e7e5").c(375, 230, 90, "#b4f8c8")
    a.c(300, 130, 80, "#ffe5ec")
    a.c(300, 45, 28, "#e63946")
    a.line("M300,20 Q310,0 330,-5")
    a.eyes(265, 330, 335, 330, 11).smile(300, 365, 50, 12)
    return a


def duck():
    a = Art("Duck")
    a.rect(0, 540, 600, 160, 0, "#90e0ef")
    a.line("M40,600 q30,-20 60,0 q30,20 60,0 M380,640 q30,-20 60,0 q30,20 60,0 M200,670 q30,-20 60,0", 6)
    a.p("M120,420 Q120,580 320,580 Q500,580 500,430 Q540,380 520,330 Q470,400 400,400 Z", "#ffd60a")
    a.p("M220,440 Q300,400 380,450 Q330,520 240,500 Z", "#ffc300")
    a.c(210, 300, 100, "#ffd60a")
    a.p("M110,300 Q60,290 40,320 Q70,345 120,335 Z", "#fb8500")
    a.eyes(200, 270, 0, 0, 13)
    a.items.pop(); a.items.pop()
    a.e(245, 330, 22, 14, 0, "#ffafcc")
    return a


def balloons():
    a = Art("Balloons")
    a.line("M180,350 Q200,500 290,640 M300,300 Q300,480 290,640 M420,370 Q390,500 290,640", 5)
    a.e(180, 230, 95, 120, -10, "#ef476f").poly([(168, 350), (192, 350), (180, 335)], "#ef476f")
    a.e(420, 250, 95, 120, 10, "#118ab2").poly([(408, 370), (432, 370), (420, 355)], "#118ab2")
    a.e(300, 180, 100, 125, 0, "#ffd166").poly([(288, 305), (312, 305), (300, 290)], "#ffd166")
    a.e(260, 130, 18, 35, 20, "#fff")
    a.rect(255, 620, 70, 40, 12, "#06d6a0")
    return a


def cupcake():
    a = Art("Cupcake")
    xs = [150, 200, 250, 300, 350, 400, 450]
    for i in range(6):
        x0, x1 = xs[i], xs[i + 1]
        top_l, top_r = x0, x1
        bot_l = 300 + (x0 - 300) * 0.75
        bot_r = 300 + (x1 - 300) * 0.75
        a.poly([(top_l, 400), (top_r, 400), (bot_r, 640), (bot_l, 640)], "#a0c4ff" if i % 2 else "#bdb2ff")
    a.p("M140,410 Q100,330 180,320 Q170,240 260,250 Q300,180 350,250 Q440,240 420,320 Q500,330 460,410 Z", "#ffc6ff")
    a.rect(285, 100, 30, 120, 8, "#fdffb6")
    a.p("M300,40 Q330,75 300,95 Q270,75 300,40 Z", "#ffadad")
    a.c(230, 330, 14, "#ffd6a5").c(360, 300, 14, "#caffbf").c(300, 350, 14, "#9bf6ff").c(400, 370, 14, "#ffadad").c(200, 390, 14, "#fdffb6")
    a.eyes(260, 500, 340, 500, 12).smile(300, 535, 60, 14)
    return a


def owl():
    a = Art("Owl")
    a.rect(20, 600, 560, 50, 25, "#a47148")
    a.e(300, 400, 170, 210, 0, "#b08968")
    a.poly([(150, 250), (170, 160), (230, 220)], "#b08968").poly([(450, 250), (430, 160), (370, 220)], "#b08968")
    a.e(140, 430, 50, 120, 15, "#7f5539").e(460, 430, 50, 120, -15, "#7f5539")
    a.e(300, 470, 110, 120, 0, "#ede0d4")
    a.c(230, 300, 65, "#fff").c(370, 300, 65, "#fff")
    a.c(230, 300, 30, "#ffd166").c(370, 300, 30, "#ffd166")
    a.dot(230, 300, 15).dot(370, 300, 15)
    a.poly([(280, 350), (320, 350), (300, 390)], "#ff9f1c")
    a.line("M260,450 q20,15 40,0 q20,15 40,0 M250,500 q25,15 50,0 q25,15 50,0", 5)
    a.e(240, 610, 35, 20, 0, "#ff9f1c").e(360, 610, 35, 20, 0, "#ff9f1c")
    return a


def whale():
    a = Art("Whale")
    a.rect(0, 560, 600, 140, 0, "#48cae4")
    a.line("M30,610 q35,-25 70,0 q35,25 70,0 q35,-25 70,0 M330,650 q35,-25 70,0 q35,25 70,0 q35,-25 70,0", 6)
    a.line("M290,195 Q260,120 215,118 M290,195 L290,100 M290,195 Q320,120 365,118")
    a.c(210, 110, 18, "#ade8f4").c(370, 110, 18, "#ade8f4").c(290, 80, 18, "#ade8f4")
    a.p("M450,420 Q520,330 580,300 Q560,380 590,450 Q520,430 470,470 Z", "#0077b6")
    a.p("M80,400 Q80,200 290,200 Q470,200 480,420 Q480,560 290,560 Q90,560 80,400 Z", "#0096c7")
    a.p("M100,440 Q290,520 470,440 Q440,560 290,560 Q130,560 100,440 Z", "#caf0f8")
    a.eyes(190, 340, 0, 0, 13)
    a.items.pop(); a.items.pop()
    a.smile(170, 400, 60, 12)
    a.e(230, 390, 20, 12, 0, "#ffafcc")
    return a


def ladybug():
    a = Art("Ladybug")
    a.p("M80,620 Q60,300 300,180 Q540,300 520,620 Q300,700 80,620 Z", "#80ed99")
    a.line("M300,190 L300,640", 5)
    a.line("M260,180 Q230,100 190,90 M340,180 Q370,100 410,90")
    a.c(190, 90, 14, "#222").c(410, 90, 14, "#222")
    a.c(300, 400, 170, "#e63946")
    a.p("M175,290 Q300,180 425,290 Q300,230 175,290 Z", "#222")
    a.c(300, 230, 75, "#333")
    a.line("M300,305 L300,570", 6)
    for x, y, r in [(230, 380, 30), (370, 380, 30), (210, 470, 25), (390, 470, 25), (260, 540, 20), (340, 540, 20)]:
        a.c(x, y, r, "#222")
    a.c(270, 220, 16, "#fff").c(330, 220, 16, "#fff")
    a.dot(270, 222, 8).dot(330, 222, 8)
    a.smile(300, 255, 34, 8)
    return a


def stars():
    a = Art("Stars")
    a.e(130, 610, 120, 50, 0, "#f1faee").e(470, 600, 130, 55, 0, "#f1faee")
    a.p("M480,90 A80,80 0 1,0 540,220 A65,65 0 1,1 480,90 Z", "#ffe066")
    a.star(300, 360, 210, 95, f="#ffd93d")
    a.star(100, 140, 55, 24, f="#ffd6a5").star(520, 400, 50, 22, f="#ffd6a5").star(110, 430, 40, 18, f="#ffd6a5")
    a.eyes(260, 350, 340, 350, 14).smile(300, 395, 60, 16)
    a.c(240, 400, 18, "#ff8fab").c(360, 400, 18, "#ff8fab")
    return a


def rainbow():
    a = Art("Rainbow")
    cols = ["#ef476f", "#ff9f1c", "#ffd166", "#06d6a0", "#118ab2", "#8338ec"]
    R = 270
    for i, col in enumerate(cols):
        ro = R - i * 35
        ri = ro - 35
        a.p(f"M{300 - ro},470 A{ro},{ro} 0 0,1 {300 + ro},470 L{300 + ri},470 A{ri},{ri} 0 0,0 {300 - ri},470 Z", col)
    for cx in (110, 490):
        a.p(f"M{cx - 110},520 Q{cx - 110},430 {cx - 40},440 Q{cx - 20},380 {cx + 30},410 Q{cx + 100},400 {cx + 100},470 Q{cx + 130},520 {cx + 70},540 L{cx - 80},540 Q{cx - 115},540 {cx - 110},520 Z", "#f1faee")
    a.eyes(80, 480, 140, 480, 9).eyes(460, 480, 520, 480, 9)
    a.smile(110, 505, 30, 8).smile(490, 505, 30, 8)
    a.c(300, 620, 45, "#ffd93d")
    return a


def train():
    a = Art("Train")
    a.rect(0, 600, 600, 30, 0, "#8d99ae")
    a.line("M30,630 L30,660 M110,630 L110,660 M190,630 L190,660 M270,630 L270,660 M350,630 L350,660 M430,630 L430,660 M510,630 L510,660 M590,630 L590,660", 8)
    a.c(150, 130, 40, "#e9ecef").c(210, 90, 50, "#e9ecef").c(290, 70, 35, "#e9ecef")
    a.rect(130, 190, 50, 120, 6, "#3a0ca3")
    a.rect(110, 170, 90, 30, 8, "#3a0ca3")
    a.rect(330, 220, 190, 230, 14, "#f72585")
    a.rect(310, 200, 230, 40, 12, "#7209b7")
    a.rect(370, 260, 110, 90, 10, "#caf0f8")
    a.rect(70, 300, 270, 250, 16, "#4361ee")
    a.p("M70,450 L20,560 L80,560 Z", "#ffd166")
    a.rect(340, 450, 200, 100, 10, "#4361ee")
    a.c(40, 380, 26, "#ffd93d")
    for x in (140, 270, 400, 490):
        a.c(x, 570, 45, "#333")
        a.c(x, 570, 16, "#ced4da")
    return a


def bunny():
    a = Art("Bunny")
    ground(a, 640, "#b9fbc0")
    a.e(240, 140, 40, 120, -10, "#f8f9fa").e(360, 140, 40, 120, 10, "#f8f9fa")
    a.e(240, 150, 18, 90, -10, "#ffc8dd").e(360, 150, 18, 90, 10, "#ffc8dd")
    a.c(420, 520, 40, "#f8f9fa")
    a.e(300, 480, 130, 140, 0, "#f8f9fa")
    a.e(300, 500, 70, 90, 0, "#ffe5ec")
    a.c(300, 290, 110, "#f8f9fa")
    a.e(220, 615, 55, 28, 0, "#f8f9fa").e(380, 615, 55, 28, 0, "#f8f9fa")
    a.p("M120,470 L60,560 Q50,580 70,575 L150,500 Z", "#fb8500")
    a.p("M140,480 Q150,430 120,410 M140,480 Q180,450 175,420", "#57cc99")
    a.eyes(260, 270, 340, 270, 13)
    a.p("M290,310 Q300,300 310,310 Q300,325 290,310 Z", "#ff8fab")
    a.line("M300,322 L300,340 M300,340 Q285,355 272,345 M300,340 Q315,355 328,345")
    a.rect(287, 345, 26, 22, 4, "#fff")
    return a


def snail():
    a = Art("Snail")
    ground(a, 600, "#d8f3dc")
    a.p("M60,560 Q60,500 120,500 L480,500 Q560,500 560,420 L580,330 Q600,280 560,270 Q520,265 510,320 L490,430 Q480,560 400,560 Z", "#ffd6a5")
    a.line("M545,275 L525,190 M570,275 L590,190")
    a.c(525, 185, 16, "#ffd6a5").c(590, 185, 16, "#ffd6a5")
    a.c(300, 360, 160, "#c77dff")
    a.c(300, 360, 115, "#e0aaff")
    a.c(300, 360, 70, "#c77dff")
    a.c(300, 360, 30, "#e0aaff")
    a.dot(545, 330, 9)
    a.smile(560, 370, 30, 8)
    return a


def teddy():
    a = Art("Teddy")
    a.c(185, 140, 55, "#c68b59").c(415, 140, 55, "#c68b59")
    a.c(185, 140, 28, "#f2d0a9").c(415, 140, 28, "#f2d0a9")
    a.e(140, 440, 50, 95, 25, "#c68b59").e(460, 440, 50, 95, -25, "#c68b59")
    a.e(300, 470, 150, 160, 0, "#c68b59")
    a.e(300, 490, 85, 100, 0, "#f2d0a9")
    a.e(200, 620, 70, 55, 0, "#c68b59").e(400, 620, 70, 55, 0, "#c68b59")
    a.c(200, 625, 30, "#f2d0a9").c(400, 625, 30, "#f2d0a9")
    a.c(300, 240, 135, "#c68b59")
    a.e(300, 290, 60, 45, 0, "#f2d0a9")
    a.e(300, 270, 22, 15, 0, "#333")
    a.line("M300,285 L300,305 M300,305 Q285,320 270,308 M300,305 Q315,320 330,308")
    a.eyes(250, 220, 350, 220, 13)
    a.p("M300,375 L230,340 L230,410 Z", "#ef476f").p("M300,375 L370,340 L370,410 Z", "#ef476f")
    a.c(300, 375, 18, "#ff8fab")
    return a


def heart():
    a = Art("Heart")
    for x, y, s in [(110, 120, 0.35), (500, 140, 0.3), (100, 560, 0.3), (510, 560, 0.35)]:
        a.p(f"M{x},{y + 40 * s} C{x - 120 * s},{y - 80 * s} {x - 260 * s},{y + 80 * s} {x},{y + 260 * s} "
            f"C{x + 260 * s},{y + 80 * s} {x + 120 * s},{y - 80 * s} {x},{y + 40 * s} Z", "#ffafcc")
    a.p("M300,230 C230,90 40,140 60,320 C80,470 250,560 300,640 C350,560 520,470 540,320 C560,140 370,90 300,230 Z", "#ef476f")
    a.eyes(250, 340, 350, 340, 14).smile(300, 390, 70, 18)
    a.c(215, 395, 22, "#ffafcc").c(385, 395, 22, "#ffafcc")
    return a


DESIGNS = [sun, cat, fish, house, apple, butterfly, car, flower, dinosaur, rocket, turtle, icecream,
           duck, balloons, cupcake, owl, whale, ladybug, stars, rainbow, train, bunny, snail, teddy, heart]


def all_art():
    return [d() for d in DESIGNS]
