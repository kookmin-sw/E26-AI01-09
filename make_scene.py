import math, sys

W, H = 1600, 760
HORIZON = 440
INK = "#141A2B"      # silhouette
out = []
heads = {}           # name -> (x, y, r)

def add(s): out.append(s)

def limb(x1, y1, x2, y2, w, col=INK):
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round"/>')

def standing(name, x, gy, h, face=1, col=INK, hair=None, bag=False, arm="down", step=0.0, scale_w=1.0):
    r = 0.068 * h
    hx, hy = x + face * 0.01 * h, gy - h + r
    sh_y = gy - 0.80 * h
    hip_y = gy - 0.47 * h
    sw = 0.115 * h * scale_w
    hw = 0.09 * h * scale_w
    # legs
    lw = 0.075 * h
    limb(x - hw * 0.45, hip_y, x - hw * 0.5 - step * h, gy - lw / 2, lw, col)
    limb(x + hw * 0.45, hip_y, x + hw * 0.5 + step * h, gy - lw / 2, lw, col)
    # torso
    add(f'<path d="M{x-sw:.1f} {sh_y+0.02*h:.1f} Q{x-sw:.1f} {sh_y-0.03*h:.1f} {x-sw*0.6:.1f} {sh_y-0.035*h:.1f} L{x+sw*0.6:.1f} {sh_y-0.035*h:.1f} '
        f'Q{x+sw:.1f} {sh_y-0.03*h:.1f} {x+sw:.1f} {sh_y+0.02*h:.1f} L{x+hw:.1f} {hip_y+0.03*h:.1f} L{x-hw:.1f} {hip_y+0.03*h:.1f} Z" fill="{col}"/>')
    if bag:
        bx = x - face * (sw + 0.03 * h)
        add(f'<rect x="{bx-0.06*h:.1f}" y="{sh_y:.1f}" width="{0.12*h:.1f}" height="{0.2*h:.1f}" rx="{0.03*h:.1f}" fill="{col}"/>')
    # arms
    aw = 0.055 * h
    for side in (-1, 1):
        sx = x + side * sw * 0.92
        if arm == "gesture" and side == face:
            limb(sx, sh_y + 0.02 * h, x + face * 0.2 * h, gy - 0.62 * h, aw, col)
            limb(x + face * 0.2 * h, gy - 0.62 * h, x + face * 0.28 * h, gy - 0.70 * h, aw * 0.9, col)
        elif arm == "push" and side == face:
            limb(sx, sh_y + 0.02 * h, x + face * 0.24 * h, gy - 0.55 * h, aw, col)
        elif arm == "hold" and side == -face:
            limb(sx, sh_y + 0.02 * h, x - face * 0.22 * h, gy - 0.5 * h, aw, col)
        else:
            limb(sx, sh_y + 0.02 * h, sx + side * 0.02 * h, gy - 0.46 * h, aw, col)
    # neck + head
    limb(hx, hy + r * 0.6, x, sh_y - 0.02 * h, 0.06 * h, col)
    add(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{r:.1f}" fill="{col}"/>')
    if hair == "bun":
        add(f'<circle cx="{hx - face*r*0.7:.1f}" cy="{hy - r*0.8:.1f}" r="{r*0.45:.1f}" fill="{col}"/>')
    elif hair == "pony":
        add(f'<path d="M{hx - face*r*0.7:.1f} {hy - r*0.3:.1f} q{-face*r*0.9:.1f} {r*0.5:.1f} {-face*r*0.5:.1f} {r*1.6:.1f}" stroke="{col}" stroke-width="{r*0.5:.1f}" stroke-linecap="round" fill="none"/>')
    elif hair == "long":
        add(f'<path d="M{hx - r:.1f} {hy:.1f} L{hx - r*1.05:.1f} {hy + r*1.6:.1f} L{hx + r*1.05:.1f} {hy + r*1.6:.1f} L{hx + r:.1f} {hy:.1f} Z" fill="{col}"/>')
    elif hair == "cap":
        add(f'<path d="M{hx - r:.1f} {hy - r*0.2:.1f} Q{hx:.1f} {hy - r*1.5:.1f} {hx + r:.1f} {hy - r*0.2:.1f} L{hx + face*r*1.8:.1f} {hy - r*0.1:.1f} Z" fill="{col}"/>')
    heads[name] = (hx, hy, r)

def seated(name, x, gy, h, face=1, col=INK, hair=None, seat_y=None):
    # h = equivalent standing height
    r = 0.068 * h
    seat_y = seat_y if seat_y is not None else gy - 0.27 * h
    hip_x = x
    sh_y = seat_y - 0.33 * h
    sw = 0.11 * h
    hx, hy = x + face * 0.015 * h, sh_y - 0.06 * h - r
    # thigh + shin
    knee_x = x + face * 0.24 * h
    limb(hip_x, seat_y - 0.03 * h, knee_x, seat_y - 0.03 * h, 0.085 * h, col)
    limb(knee_x, seat_y - 0.03 * h, knee_x + face * 0.02 * h, gy - 0.035 * h, 0.07 * h, col)
    # torso
    add(f'<path d="M{x-sw:.1f} {sh_y+0.02*h:.1f} Q{x-sw:.1f} {sh_y-0.03*h:.1f} {x-sw*0.6:.1f} {sh_y-0.035*h:.1f} L{x+sw*0.6:.1f} {sh_y-0.035*h:.1f} '
        f'Q{x+sw:.1f} {sh_y-0.03*h:.1f} {x+sw:.1f} {sh_y+0.02*h:.1f} L{x+0.1*h:.1f} {seat_y:.1f} L{x-0.1*h:.1f} {seat_y:.1f} Z" fill="{col}"/>')
    # arm resting on lap
    limb(x + face * sw * 0.8, sh_y + 0.02 * h, x + face * 0.14 * h, seat_y - 0.07 * h, 0.055 * h, col)
    limb(x + face * 0.14 * h, seat_y - 0.07 * h, x + face * 0.24 * h, seat_y - 0.08 * h, 0.05 * h, col)
    limb(hx, hy + r * 0.6, x, sh_y - 0.02 * h, 0.06 * h, col)
    add(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{r:.1f}" fill="{col}"/>')
    if hair == "long":
        add(f'<path d="M{hx - r:.1f} {hy:.1f} L{hx - r*1.05:.1f} {hy + r*1.6:.1f} L{hx + r*1.05:.1f} {hy + r*1.6:.1f} L{hx + r:.1f} {hy:.1f} Z" fill="{col}"/>')
    elif hair == "bun":
        add(f'<circle cx="{hx - face*r*0.7:.1f}" cy="{hy - r*0.8:.1f}" r="{r*0.45:.1f}" fill="{col}"/>')
    heads[name] = (hx, hy, r)
    return seat_y

def wheelchair(name, x, gy, h, face=1, col=INK):
    wr = 0.17 * h
    wcx = x - face * 0.02 * h
    wcy = gy - wr
    seat_y = gy - 0.30 * h
    # wheel
    add(f'<circle cx="{wcx:.1f}" cy="{wcy:.1f}" r="{wr:.1f}" fill="none" stroke="{col}" stroke-width="{0.022*h:.1f}"/>')
    add(f'<circle cx="{wcx:.1f}" cy="{wcy:.1f}" r="{wr*0.82:.1f}" fill="none" stroke="{col}" stroke-width="{0.008*h:.1f}" opacity=".8"/>')
    for a in range(0, 180, 30):
        dx, dy = math.cos(math.radians(a)) * wr * 0.82, math.sin(math.radians(a)) * wr * 0.82
        add(f'<line x1="{wcx-dx:.1f}" y1="{wcy-dy:.1f}" x2="{wcx+dx:.1f}" y2="{wcy+dy:.1f}" stroke="{col}" stroke-width="{0.005*h:.1f}" opacity=".7"/>')
    add(f'<circle cx="{wcx:.1f}" cy="{wcy:.1f}" r="{0.02*h:.1f}" fill="{col}"/>')
    # caster
    cx = x + face * 0.27 * h
    add(f'<circle cx="{cx:.1f}" cy="{gy - 0.035*h:.1f}" r="{0.035*h:.1f}" fill="{col}"/>')
    limb(cx, gy - 0.035 * h, cx - face * 0.02 * h, seat_y + 0.02 * h, 0.018 * h, col)
    # frame / seat / back / push handle
    limb(x - face * 0.12 * h, seat_y + 0.02 * h, x + face * 0.22 * h, seat_y + 0.02 * h, 0.03 * h, col)
    limb(x - face * 0.13 * h, seat_y + 0.02 * h, x - face * 0.15 * h, seat_y - 0.30 * h, 0.03 * h, col)
    limb(x - face * 0.15 * h, seat_y - 0.30 * h, x - face * 0.24 * h, seat_y - 0.31 * h, 0.022 * h, col)
    # footrest
    limb(x + face * 0.22 * h, gy - 0.07 * h, x + face * 0.31 * h, gy - 0.07 * h, 0.018 * h, col)
    seated(name, x, gy - 0.04 * h, h, face, col, seat_y=seat_y)
    return (x - face * 0.24 * h, seat_y - 0.31 * h)  # handle point

def bench(x1, x2, gy, sh, col=INK):
    seat_y = gy - sh
    limb(x1, seat_y, x2, seat_y, 9, col)
    limb(x1 + 4, seat_y - 34, x2 - 4, seat_y - 34, 6, col)
    limb(x1 + 4, seat_y - 52, x2 - 4, seat_y - 52, 6, col)
    for xx in (x1 + 14, x2 - 14):
        limb(xx, seat_y, xx, gy, 7, col)
        limb(xx, seat_y, xx, seat_y - 56, 5, col)
    return seat_y

def tree(x, gy, s, col):
    limb(x, gy, x, gy - 110 * s, 14 * s, col)
    limb(x, gy - 70 * s, x + 30 * s, gy - 105 * s, 7 * s, col)
    for dx, dy, rr in [(0, -170, 70), (-50, -135, 52), (52, -138, 55), (-20, -205, 48), (30, -200, 50)]:
        add(f'<circle cx="{x+dx*s:.1f}" cy="{gy+dy*s:.1f}" r="{rr*s:.1f}" fill="{col}"/>')

def lamp(x, gy, h, col):
    limb(x, gy, x, gy - h, 6, col)
    limb(x, gy - h, x + 22, gy - h - 4, 5, col)
    add(f'<circle cx="{x+24}" cy="{gy-h+6}" r="40" fill="url(#lampglow)"/>')
    add(f'<circle cx="{x+24}" cy="{gy-h+4}" r="6" fill="#FFE2B8"/>')

def link(a, b, col, lift=60, width=3.0, glow=True, dots=True):
    ax, ay, ar = heads[a]; bx, by, br = heads[b]
    sx, sy = ax, ay - ar * 1.2
    ex, ey = bx, by - br * 1.2
    mx, my = (sx + ex) / 2, min(sy, ey) - lift
    d = f'M{sx:.1f} {sy:.1f} Q{mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}'
    if glow:
        add(f'<path d="{d}" stroke="{col}" stroke-width="{width*4:.1f}" fill="none" opacity=".18" filter="url(#blur)"/>')
    add(f'<path d="{d}" stroke="{col}" stroke-width="{width:.1f}" fill="none" stroke-linecap="round" {"stroke-dasharray=" + chr(34) + "2 9" + chr(34) if dots else ""}/>')
    add(f'<path d="{d}" stroke="{col}" stroke-width="{width*0.45:.1f}" fill="none" opacity=".55"/>')

def aura(name, col, k=2.1):
    x, y, r = heads[name]
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*k:.1f}" fill="none" stroke="{col}" stroke-width="1.6" opacity=".55"/>')
    add(f'<circle cx="{x - r*0.15:.1f}" cy="{y - r*0.25:.1f}" r="{r*0.22:.1f}" fill="{col}"/>')

# ---------------- background ----------------
add(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
 <linearGradient id="sky" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{HORIZON}">
  <stop offset="0" stop-color="#151B3A"/><stop offset=".38" stop-color="#3B4070"/>
  <stop offset=".72" stop-color="#A0677A"/><stop offset="1" stop-color="#F4AE86"/></linearGradient>
 <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#4E5670"/><stop offset=".35" stop-color="#3A4560"/><stop offset="1" stop-color="#232B42"/></linearGradient>
 <linearGradient id="path" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#8E8597"/><stop offset="1" stop-color="#5B5C74"/></linearGradient>
 <radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFD7B0" stop-opacity=".95"/><stop offset=".35" stop-color="#FFB487" stop-opacity=".55"/><stop offset="1" stop-color="#FF8F66" stop-opacity="0"/></radialGradient>
 <radialGradient id="lampglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFD9A8" stop-opacity=".7"/><stop offset="1" stop-color="#FFD9A8" stop-opacity="0"/></radialGradient>
 <filter id="blur" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<circle cx="980" cy="{HORIZON-10}" r="230" fill="url(#sun)"/>
<circle cx="980" cy="{HORIZON+6}" r="46" fill="#FFE1C2" opacity=".9"/>''')
# stars
import random
random.seed(7)
for _ in range(60):
    sx, sy = random.uniform(0, W), random.uniform(0, 200)
    add(f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{random.uniform(.6,1.6):.1f}" fill="#fff" opacity="{random.uniform(.2,.7):.2f}"/>')
# skyline
random.seed(3)
x = 0
sk = []
while x < W:
    bw = random.randint(30, 80); bh = random.randint(30, 150)
    if 820 < x < 1140: bh = random.randint(20, 60)
    sk.append((x, bw, bh)); x += bw + random.randint(0, 8)
for (bx, bw, bh) in sk:
    add(f'<rect x="{bx}" y="{HORIZON-bh}" width="{bw}" height="{bh+4}" fill="#4A4B72" opacity=".45"/>')
    for wy in range(HORIZON - bh + 10, HORIZON - 8, 14):
        for wx in range(bx + 6, bx + bw - 6, 12):
            if random.random() < 0.12:
                add(f'<rect x="{wx}" y="{wy}" width="4" height="5" fill="#FFD7A0" opacity=".55"/>')
# tower with signal (future city hint)
add(f'<line x1="300" y1="{HORIZON-150}" x2="300" y2="{HORIZON-260}" stroke="#3B3F62" stroke-width="6"/>')
add(f'<circle cx="300" cy="{HORIZON-262}" r="5" fill="#5CC9D6"/>')
# ground
add(f'<path d="M0 {HORIZON} L{W} {HORIZON} L{W} {H} L0 {H} Z" fill="url(#ground)"/>')
add(f'<path d="M0 {H} C 300 600, 520 560, 760 520 C 980 485, 1230 470, {W} 455 L{W} 500 C 1250 515, 1000 545, 800 590 C 560 640, 360 700, 260 {H} Z" fill="url(#path)" opacity=".85"/>')
# far trees + far hedge
add(f'<path d="M0 {HORIZON+6} Q 200 {HORIZON-24} 420 {HORIZON+4} T 860 {HORIZON+2} T 1300 {HORIZON} T {W} {HORIZON-4} L{W} {HORIZON+20} L0 {HORIZON+20} Z" fill="#2A3150"/>')
tree(120, HORIZON + 60, 1.25, "#1E2540")
tree(1500, HORIZON + 70, 1.35, "#1E2540")
tree(640, HORIZON + 30, 0.75, "#2A3150")
tree(1240, HORIZON + 26, 0.6, "#2A3150")
lamp(560, HORIZON + 150, 190, "#1B2136")
lamp(1110, HORIZON + 120, 170, "#1B2136")

# ground shadows
for (sx, sy, rx) in [(250, 716, 150), (800, 646, 220), (960, 652, 50), (645, 648, 50), (1130, 678, 60), (1300, 670, 50), (1420, 668, 100)]:
    add(f'<ellipse cx="{sx}" cy="{sy}" rx="{rx}" ry="9" fill="#0E1221" opacity=".35"/>')
# ---------------- people ----------------
FAR = "#2B3352"
# far: parent + child (small), linked
standing("parent", 1012, HORIZON + 46, 104, face=1, col=FAR, hair="long", arm="hold")
standing("child", 1044, HORIZON + 46, 66, face=-1, col=FAR, arm="gesture")
# far: jogger alone
# far pair on grass
standing("far1", 430, HORIZON + 52, 100, face=1, col=FAR)
standing("far2", 468, HORIZON + 52, 96, face=-1, col=FAR, hair="bun")

# group 1: wheelchair + caregiver (foreground left)
handle = wheelchair("wc", 300, 712, 330, face=1)
standing("care", 175, 716, 335, face=1, hair="bun", arm="push")

# group 2: friends at bench (center)
seat = bench(700, 900, 640, 60)
seated("f1", 745, 640, 270, face=1, hair="long", seat_y=seat - 4)
seated("f2", 845, 640, 275, face=-1, seat_y=seat - 4)
standing("f3", 960, 650, 300, face=-1, arm="gesture", hair="cap")
standing("f4", 645, 646, 285, face=1, hair="bun")

# group 3: traveler + vendor with cart (right)
# cart (vendor stands beside it)
add(f'<line x1="1350" y1="500" x2="1350" y2="560" stroke="{INK}" stroke-width="6"/><line x1="1500" y1="500" x2="1500" y2="560" stroke="{INK}" stroke-width="6"/>')
add(f'<path d="M1330 506 L1520 506 L1500 466 L1350 466 Z" fill="#E0512B" opacity=".92"/>')
add(f'<path d="M1350 466 L1500 466 L1492 458 L1358 458 Z" fill="#B23F22"/>')
add(f'<rect x="1340" y="556" width="170" height="86" rx="8" fill="{INK}"/>')
add(f'<circle cx="1372" cy="650" r="18" fill="{INK}"/><circle cx="1480" cy="650" r="18" fill="{INK}"/>')
standing("vendor", 1300, 668, 285, face=-1, hair="cap")
standing("trav", 1130, 676, 310, face=1, bag=True, arm="gesture")

# ---------------- signals ----------------
ORANGE, CYAN, VIOLET = "#FF8A5C", "#6FE3EE", "#C6B8FF"
link("care", "wc", ORANGE, lift=70, width=3.4)
for n in ("care", "wc"): aura(n, ORANGE)
link("f1", "f2", CYAN, lift=55)
link("f2", "f3", CYAN, lift=60)
link("f4", "f1", CYAN, lift=55)
link("f4", "f3", CYAN, lift=110, width=2.2)
for n in ("f1", "f2", "f3", "f4"): aura(n, CYAN)
link("trav", "vendor", VIOLET, lift=90, width=3.2)
for n in ("trav", "vendor"): aura(n, VIOLET)
# translation marker on traveler link
tx, ty, _ = heads["trav"]; vx, vy, _ = heads["vendor"]
mx, my = (tx + vx) / 2, min(ty, vy) - 90
add(f'<g transform="translate({mx-26:.0f},{my-14:.0f})"><rect width="52" height="28" rx="14" fill="#141A2B" stroke="{VIOLET}" stroke-width="2"/>'
    f'<text x="26" y="19" text-anchor="middle" font-family="Noto Sans CJK KR, sans-serif" font-size="14" font-weight="700" fill="{VIOLET}">A↔가</text></g>')
link("parent", "child", ORANGE, lift=30, width=1.8)
link("far1", "far2", CYAN, lift=26, width=1.6)
add('</svg>')

open(sys.argv[1], "w", encoding="utf-8").write("\n".join(out))
