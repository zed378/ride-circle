"""Generate RideCircle brand variants from the master SVGs in the repo root.

Masters (never modified): ridecircle-symbol.svg (mark geometry), ridecircle-lockup.svg (layout, type, colors).
"""
import json, math, os, re, shutil, subprocess
from shapely.geometry import LineString, Point
from shapely.ops import unary_union
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))          # brand/tools
OUT = os.path.dirname(HERE)                                  # brand
ROOT = os.path.dirname(OUT)                                  # repo root (masters live here)
GENERATED = ["logo", "symbol", "app-icon", "ios", "android", "web", "social", "brand-sheet.svg", "brand-sheet.png"]

# ------------------------------------------------------------------ palette
LIME = "#D8FF3E"      # mark (master files)
INK = "#0B0C0D"       # background (master lockup)
PAPER = "#F3F3EF"     # wordmark on dark (master lockup)
MUTED = "#A5A8AA"     # tagline (master lockup)
GRAPHITE = "#17191C"  # dark text on light / icon tile (reference board)
SURFACE = "#1A1D20"   # secondary dark surface (reference board)
ACCENT = "#FF6B35"    # support accent (reference board)


# ------------------------------------------------------------------ master geometry
def read_master_symbol():
    src = open(os.path.join(ROOT, "ridecircle-symbol.svg"), encoding="utf-8").read()
    segs = re.findall(r'<path d="([^"]+)"[^>]*stroke-width="([\d.]+)"', src)
    assert len(segs) == 5, "unexpected master symbol structure"
    return [(d, float(w)) for d, w in segs]


def read_master_lockup():
    src = open(os.path.join(ROOT, "ridecircle-lockup.svg"), encoding="utf-8").read()
    texts = re.findall(r'<text x="([\d.]+)" y="([\d.]+)" font-size="([\d.]+)"([^>]*)>([^<]+)</text>', src)
    arcs = re.findall(r'<path d="M([\d.]+),([\d.]+) A([\d.]+),', src)
    return texts, arcs


SEGMENTS = read_master_symbol()                     # [(path d, stroke width)] in a 200x200 space
CENTER, RADIUS = (100.0, 100.0), 60.0               # from the master arcs
# Optical-size variant for <= 32 px: same arcs, thin end thickened so it survives rasterization
SMALL_WIDTHS = [10, 13, 16, 19, 23]


def arc_points(d, n=120):
    m = re.match(r"M([\d.]+),([\d.]+) A([\d.]+),([\d.]+) 0 0 1 ([\d.]+),([\d.]+)", d)
    x0, y0, r, _, x1, y1 = map(float, m.groups())
    a0 = math.atan2(y0 - CENTER[1], x0 - CENTER[0])
    a1 = math.atan2(y1 - CENTER[1], x1 - CENTER[0])
    if a1 < a0:
        a1 += 2 * math.pi
    return [(CENTER[0] + r * math.cos(a0 + (a1 - a0) * i / n), CENTER[1] + r * math.sin(a0 + (a1 - a0) * i / n))
            for i in range(n + 1)]


def mark_shape(widths):
    return unary_union([LineString(arc_points(d)).buffer(w / 2, quad_segs=32)
                        for (d, _), w in zip(SEGMENTS, widths)])


MARK_W = [w for _, w in SEGMENTS]
SHAPE = mark_shape(MARK_W)
SHAPE_SMALL = mark_shape(SMALL_WIDTHS)
OUTER_R = CENTER[0] - SHAPE.bounds[0]               # farthest extent from ring center (left side)


def f(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


def mark_svg(color, tx, ty, s, widths=None, indent="  "):
    widths = widths or MARK_W
    paths = "\n".join(
        f'{indent}  <path d="{d}" fill="none" stroke="{color}" stroke-width="{w:g}" stroke-linecap="round"/>'
        for (d, _), w in zip(SEGMENTS, widths))
    return f'{indent}<g transform="translate({f(tx)} {f(ty)}) scale({f(s)})">\n{paths}\n{indent}</g>'


def placed(cx, cy, outer_r):
    """Transform placing the ring center at (cx, cy) with the mark's outer extent = outer_r."""
    s = outer_r / OUTER_R
    return cx - CENTER[0] * s, cy - CENTER[1] * s, s


# ------------------------------------------------------------------ type (outlined from the master's font)
# Arial, as specified by ridecircle-lockup.svg. Override with RC_FONT_BOLD / RC_FONT_REGULAR on non-Windows machines.
FONT_BOLD = os.environ.get("RC_FONT_BOLD", r"C:/Windows/Fonts/arialbd.ttf")
FONT_REG = os.environ.get("RC_FONT_REGULAR", r"C:/Windows/Fonts/arial.ttf")


def outline(text, font_path, size):
    font = TTFont(font_path)
    cmap, gs, upem = font.getBestCmap(), font.getGlyphSet(), font["head"].unitsPerEm
    sc = size / upem
    kern = {}
    if "kern" in font:
        for sub in font["kern"].kernTables:
            kern.update(sub.kernTable)
    pen, bpen, x = SVGPathPen(gs), BoundsPen(gs), 0.0
    names = [cmap[ord(c)] for c in text]
    for i, g in enumerate(names):
        for p in (pen, bpen):
            gs[g].draw(TransformPen(p, (sc, 0, 0, -sc, x * sc, 0)))
        x += font["hmtx"][g][0] + (kern.get((g, names[i + 1]), 0) if i + 1 < len(names) else 0)
    return pen.getCommands(), bpen.bounds, font["OS/2"].sCapHeight * sc


TEXTS, _ = read_master_lockup()
(name_x, name_y, name_size, _, name_text), (tag_x, tag_y, tag_size, _, tag_text) = TEXTS
NAME = outline(name_text, FONT_BOLD, float(name_size))     # (d, bounds, cap)
TAG = outline(tag_text, FONT_REG, float(tag_size))


def svg_doc(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(w)}" height="{f(h)}" viewBox="0 0 {f(w)} {f(h)}" '
            f'role="img" aria-label="{title}">\n  <title>{title}</title>\n{body}\n</svg>\n')


def text_path(d, color, x, y):
    return f'  <path fill="{color}" transform="translate({f(x)} {f(y)})" d="{d}"/>'


def crop(items, pad, bg=None):
    """items: list of (svg_fragment_builder(dx, dy), (minx, miny, maxx, maxy)). Returns (w, h, body)."""
    minx = min(b[0] for _, b in items); miny = min(b[1] for _, b in items)
    maxx = max(b[2] for _, b in items); maxy = max(b[3] for _, b in items)
    dx, dy = pad - minx, pad - miny
    w, h = maxx - minx + 2 * pad, maxy - miny + 2 * pad
    body = [f'  <rect width="{f(w)}" height="{f(h)}" fill="{bg}"/>'] if bg else []
    body += [build(dx, dy) for build, _ in items]
    return w, h, "\n".join(body)


def mark_item(color, cx, cy, s, widths=None):
    b = (SHAPE_SMALL if widths else SHAPE).bounds
    tx, ty = cx - CENTER[0] * s, cy - CENTER[1] * s
    bounds = (tx + b[0] * s, ty + b[1] * s, tx + b[2] * s, ty + b[3] * s)
    return (lambda dx, dy: mark_svg(color, tx + dx, ty + dy, s, widths)), bounds


def text_item(outl, color, x, y):
    d, b, _ = outl
    return (lambda dx, dy: text_path(d, color, x + dx, y + dy)), (x + b[0], y + b[1], x + b[2], y + b[3])


# ------------------------------------------------------------------ logo variants
def lockup(mark_c, name_c, tag_c, with_tagline=True, bg=None):
    # Exact master layout: ring center (70,80) r=38, name baseline (150,94) 36px, tagline (150,118) 14px
    s = 38 / RADIUS
    items = [mark_item(mark_c, 70, 80, s), text_item(NAME, name_c, float(name_x), float(name_y))]
    if with_tagline:
        items.append(text_item(TAG, tag_c, float(tag_x), float(tag_y)))
        return crop(items, pad=20, bg=bg)
    # Compact: master mark/type proportions without the tagline — ring re-centered on the cap height
    cap = NAME[2]
    s = (cap * 2.3) / (2 * OUTER_R)
    items = [mark_item(mark_c, 0, -cap / 2, s),
             text_item(NAME, name_c, OUTER_R * s + cap * 0.55 - NAME[1][0], 0)]
    return crop(items, pad=cap * 0.6, bg=bg)


def stacked(mark_c, name_c, tag_c, bg=None):
    cap = NAME[2]
    s = (cap * 3.2) / (2 * OUTER_R)
    name_w = NAME[1][2] - NAME[1][0]
    tag_w = TAG[1][2] - TAG[1][0]
    ring_bottom = OUTER_R * s
    items = [mark_item(mark_c, 0, 0, s),
             text_item(NAME, name_c, -name_w / 2 - NAME[1][0], ring_bottom + cap * 0.9 + cap),
             text_item(TAG, tag_c, -tag_w / 2 - TAG[1][0], ring_bottom + cap * 0.9 + cap + cap * 0.95)]
    return crop(items, pad=cap * 0.8, bg=bg)


def wordmark(color):
    return crop([text_item(NAME, color, 0, 0)], pad=6)


def symbol(color, widths=None):
    s = 1.0
    return crop([mark_item(color, 100, 100, s, widths)], pad=max(widths or MARK_W))  # clear space = thickest stroke


# ------------------------------------------------------------------ icon canvases
def square_icon(size, bg, mark_c, mark_frac, rx=0, widths=None, circle=False):
    """Square canvas; ring center at canvas center, mark outer extent = mark_frac * size / 2."""
    tx, ty, s = placed(size / 2, size / 2, mark_frac * size / 2)
    parts = []
    if bg and circle:
        parts.append(f'  <circle cx="{f(size / 2)}" cy="{f(size / 2)}" r="{f(size / 2)}" fill="{bg}"/>')
    elif bg:
        parts.append(f'  <rect width="{size}" height="{size}"' + (f' rx="{f(rx)}"' if rx else "") + f' fill="{bg}"/>')
    parts.append(mark_svg(mark_c, tx, ty, s, widths))
    return "\n".join(parts)


def android_vector(size_dp, viewport, color, outer_r, widths=None, name_comment=""):
    tx, ty, s = placed(viewport / 2, viewport / 2, outer_r)
    widths = widths or MARK_W
    paths = "\n".join(
        f'        <path\n            android:pathData="{d}"\n            android:strokeColor="{color}"\n'
        f'            android:strokeWidth="{w:g}"\n            android:strokeLineCap="round" />'
        for (d, _), w in zip(SEGMENTS, widths))
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<!-- {name_comment} Generated from ridecircle-symbol.svg -->\n'
            f'<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
            f'    android:width="{size_dp}dp"\n    android:height="{size_dp}dp"\n'
            f'    android:viewportWidth="{viewport}"\n    android:viewportHeight="{viewport}">\n'
            f'    <group\n        android:translateX="{f(tx)}"\n        android:translateY="{f(ty)}"\n'
            f'        android:scaleX="{f(s)}"\n        android:scaleY="{f(s)}">\n{paths}\n    </group>\n</vector>\n')


# ------------------------------------------------------------------ writing
SVG_FILES, PNG_JOBS, POST = {}, [], []


def put_svg(rel, w, h, body, title):
    SVG_FILES[rel] = svg_doc(w, h, body, title)


def put_png(src_rel, out_rel, width, opaque=False):
    PNG_JOBS.append({"src": os.path.join(OUT, src_rel), "out": os.path.join(OUT, out_rel), "width": width})
    if opaque:
        POST.append(("rgb", out_rel))


def main():
    for g in GENERATED:  # clean previous output, never touches tools/ or README.md
        p = os.path.join(OUT, g)
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.isfile(p):
            os.remove(p)

    # --- logo
    for variant, (m, n, t) in {
        "on-dark": (LIME, PAPER, MUTED), "on-light": (LIME, GRAPHITE, "#5E6266"),
        "mono-white": (PAPER, PAPER, PAPER), "mono-black": (GRAPHITE, GRAPHITE, GRAPHITE),
    }.items():
        put_svg(f"logo/lockup/ridecircle-lockup-{variant}.svg", *lockup(m, n, t), "RideCircle — social riding platform")
        put_svg(f"logo/lockup-compact/ridecircle-lockup-compact-{variant}.svg", *lockup(m, n, t, with_tagline=False), "RideCircle")
        put_svg(f"logo/lockup-stacked/ridecircle-lockup-stacked-{variant}.svg", *stacked(m, n, t), "RideCircle — social riding platform")
    put_svg("logo/wordmark/ridecircle-wordmark-white.svg", *wordmark(PAPER), "RideCircle")
    put_svg("logo/wordmark/ridecircle-wordmark-black.svg", *wordmark(GRAPHITE), "RideCircle")

    # --- symbol
    put_svg("symbol/ridecircle-symbol.svg", *symbol(LIME), "RideCircle")
    put_svg("symbol/ridecircle-symbol-mono-white.svg", *symbol(PAPER), "RideCircle")
    put_svg("symbol/ridecircle-symbol-mono-black.svg", *symbol(GRAPHITE), "RideCircle")
    put_svg("symbol/ridecircle-symbol-small.svg", *symbol(LIME, SMALL_WIDTHS), "RideCircle")
    put_svg("symbol/ridecircle-symbol-small-mono-black.svg", *symbol(GRAPHITE, SMALL_WIDTHS), "RideCircle")

    # --- app icon masters (1024)
    put_svg("app-icon/app-icon.svg", 1024, 1024, square_icon(1024, GRAPHITE, LIME, 0.62), "RideCircle app icon")
    put_svg("app-icon/app-icon-dark.svg", 1024, 1024, square_icon(1024, None, LIME, 0.62), "RideCircle app icon (dark appearance)")
    put_svg("app-icon/app-icon-tinted.svg", 1024, 1024, square_icon(1024, "#000000", "#FFFFFF", 0.62), "RideCircle app icon (tinted appearance)")
    put_svg("app-icon/app-icon-rounded-preview.svg", 1024, 1024, square_icon(1024, GRAPHITE, LIME, 0.62, rx=229), "RideCircle app icon preview")

    # --- iOS AppIcon.appiconset (Xcode 14+ single-size, iOS 18 dark + tinted appearances)
    ios = "ios/AppIcon.appiconset"
    put_png("app-icon/app-icon.svg", f"{ios}/AppIcon-1024.png", 1024, opaque=True)
    put_png("app-icon/app-icon-dark.svg", f"{ios}/AppIcon-1024-dark.png", 1024)
    put_png("app-icon/app-icon-tinted.svg", f"{ios}/AppIcon-1024-tinted.png", 1024, opaque=True)
    contents = {"images": [
        {"filename": "AppIcon-1024.png", "idiom": "universal", "platform": "ios", "size": "1024x1024"},
        {"appearances": [{"appearance": "luminosity", "value": "dark"}], "filename": "AppIcon-1024-dark.png",
         "idiom": "universal", "platform": "ios", "size": "1024x1024"},
        {"appearances": [{"appearance": "luminosity", "value": "tinted"}], "filename": "AppIcon-1024-tinted.png",
         "idiom": "universal", "platform": "ios", "size": "1024x1024"},
    ], "info": {"author": "xcode", "version": 1}}
    POST.append(("text", f"{ios}/Contents.json", json.dumps(contents, indent=2) + "\n"))
    put_png("app-icon/app-icon.svg", "ios/AppStore-1024.png", 1024, opaque=True)

    # --- Android (adaptive icon, legacy mipmaps, Play Store, notification)
    res = "android/res"
    # Foreground safe zone: 66dp circle in a 108dp canvas -> keep mark within r=30
    POST.append(("text", f"{res}/drawable/ic_launcher_foreground.xml", android_vector(108, 108, LIME, 30, name_comment="Adaptive icon foreground.")))
    POST.append(("text", f"{res}/drawable/ic_launcher_monochrome.xml", android_vector(108, 108, "#FFFFFFFF", 30, name_comment="Android 13+ themed icon.")))
    POST.append(("text", f"{res}/drawable/ic_stat_ridecircle.xml", android_vector(24, 24, "#FFFFFFFF", 10.5, SMALL_WIDTHS, "Notification small icon (white silhouette).")))
    adaptive = ('<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
                '    <background android:drawable="@color/ic_launcher_background" />\n'
                '    <foreground android:drawable="@drawable/ic_launcher_foreground" />\n'
                '    <monochrome android:drawable="@drawable/ic_launcher_monochrome" />\n</adaptive-icon>\n')
    POST.append(("text", f"{res}/mipmap-anydpi-v26/ic_launcher.xml", adaptive))
    POST.append(("text", f"{res}/mipmap-anydpi-v26/ic_launcher_round.xml", adaptive))
    POST.append(("text", f"{res}/values/ic_launcher_background.xml",
                 f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">{GRAPHITE}</color>\n</resources>\n'))
    for sfx, widths in (("", None), ("-small", SMALL_WIDTHS)):
        put_svg(f"android/_src/legacy-square{sfx}.svg", 192, 192, square_icon(192, GRAPHITE, LIME, 0.62, rx=26, widths=widths), "legacy")
        put_svg(f"android/_src/legacy-round{sfx}.svg", 192, 192, square_icon(192, GRAPHITE, LIME, 0.58, circle=True, widths=widths), "legacy round")
    for density, px in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
        sfx = "-small" if px < 96 else ""  # optical-size mark below 96 px
        put_png(f"android/_src/legacy-square{sfx}.svg", f"{res}/mipmap-{density}/ic_launcher.png", px)
        put_png(f"android/_src/legacy-round{sfx}.svg", f"{res}/mipmap-{density}/ic_launcher_round.png", px)
    put_png("app-icon/app-icon.svg", "android/play-store-icon-512.png", 512)
    # Android 12+ splash screen icon: 288dp canvas, keep within the 192dp circle (r=96 -> mark r~84)
    POST.append(("text", f"{res}/drawable/splash_icon.xml", android_vector(288, 288, LIME, 84, name_comment="Android 12+ SplashScreen icon.")))

    # --- Web
    put_svg("web/favicon.svg", 64, 64, square_icon(64, GRAPHITE, LIME, 0.8, rx=14, widths=SMALL_WIDTHS), "RideCircle")
    for px in (16, 32, 48):
        put_png("web/favicon.svg", f"web/favicon-{px}.png", px)
    put_png("app-icon/app-icon.svg", "web/apple-touch-icon.png", 180, opaque=True)
    put_png("app-icon/app-icon.svg", "web/icon-192.png", 192)
    put_png("app-icon/app-icon.svg", "web/icon-512.png", 512)
    # Maskable: mark within the 80% safe circle
    put_svg("web/_src/icon-maskable.svg", 512, 512, square_icon(512, GRAPHITE, LIME, 0.5), "maskable")
    put_png("web/_src/icon-maskable.svg", "web/icon-maskable-512.png", 512)
    put_svg("web/safari-pinned-tab.svg", *symbol("#000000", SMALL_WIDTHS), "RideCircle")
    manifest = {
        "name": "RideCircle", "short_name": "RideCircle", "theme_color": INK, "background_color": INK,
        "display": "standalone",
        "icons": [
            {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    POST.append(("text", "web/site.webmanifest", json.dumps(manifest, indent=2) + "\n"))
    POST.append(("ico", "web/favicon.ico"))
    # Open Graph / link preview 1200x630
    w, h, body = lockup(LIME, PAPER, MUTED)
    sc = 760 / w
    og = (f'  <rect width="1200" height="630" fill="{INK}"/>\n'
          f'  <g transform="translate({f((1200 - w * sc) / 2)} {f((630 - h * sc) / 2)}) scale({f(sc)})">\n{body}\n  </g>')
    put_svg("social/_src/og-image.svg", 1200, 630, og, "RideCircle")
    put_png("social/_src/og-image.svg", "social/og-image-1200x630.png", 1200, opaque=True)
    # Profile picture (circle-crop safe)
    put_svg("social/_src/avatar.svg", 1080, 1080, square_icon(1080, INK, LIME, 0.56), "RideCircle")
    put_png("social/_src/avatar.svg", "social/avatar-1080.png", 1080, opaque=True)

    # --- brand sheet
    put_svg("brand-sheet.svg", *sheet(), "RideCircle brand identity")
    put_png("brand-sheet.svg", "brand-sheet.png", 1600, opaque=True)

    # write svgs
    for rel, content in SVG_FILES.items():
        p = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8", newline="\n").write(content)
    # render pngs
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
        json.dump(PNG_JOBS, tmp)
    subprocess.run(["node", os.path.join(HERE, "export.mjs"), tmp.name], check=True, cwd=HERE)
    os.remove(tmp.name)
    # post-process
    for item in POST:
        kind, rel = item[0], item[1]
        p = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if kind == "rgb":
            im = Image.open(p).convert("RGBA")
            flat = Image.new("RGB", im.size, (0, 0, 0))
            flat.paste(im, mask=im.split()[3])
            flat.save(p, optimize=True)
        elif kind == "text":
            open(p, "w", encoding="utf-8", newline="\n").write(item[2])
        elif kind == "ico":
            im = Image.open(os.path.join(OUT, "web/favicon-48.png"))
            im.save(p, sizes=[(16, 16), (32, 32), (48, 48)])
    # intermediate render sources are not deliverables
    for tmp in ("android/_src", "web/_src", "social/_src"):
        shutil.rmtree(os.path.join(OUT, tmp), ignore_errors=True)


# ------------------------------------------------------------------ overview sheet
def nest(rel, x, y, width=None, height=None):
    doc = SVG_FILES[rel]
    w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', doc).groups())
    if width is not None:
        height = h * width / w
    else:
        width = w * height / h
    inner = doc[doc.index("</title>") + 8: doc.rindex("</svg>")]
    return f'  <svg x="{f(x)}" y="{f(y)}" width="{f(width)}" height="{f(height)}" viewBox="0 0 {f(w)} {f(h)}">{inner}</svg>', width, height


def sheet():
    W, H = 1600, 1100
    FS = "Arial, sans-serif"
    out = []

    def label(x, y, t, fill=MUTED, size=14, anchor="start", weight="normal"):
        out.append(f'  <text x="{f(x)}" y="{f(y)}" fill="{fill}" font-family="{FS}" font-size="{size}" '
                   f'font-weight="{weight}" letter-spacing="1" text-anchor="{anchor}">{t}</text>')

    def panel(x, y, w, h, fill, title, tfill=MUTED):
        out.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>')
        label(x + 32, y + 40, title, tfill)
        out.append(f'  <rect x="{x + 32}" y="{y + 54}" width="{w - 64}" height="1" fill="{tfill}" opacity="0.3"/>')

    def center(rel, cx, cy, width=None, height=None):
        _, w, h = nest(rel, 0, 0, width, height)
        out.append(nest(rel, cx - w / 2, cy - h / 2, width, height)[0])

    panel(0, 0, 1000, 300, INK, "PRIMARY LOCKUP")
    center("logo/lockup/ridecircle-lockup-on-dark.svg", 290, 175, width=440)
    center("logo/lockup-compact/ridecircle-lockup-compact-on-dark.svg", 760, 175, width=340)
    label(290, 280, "with tagline", size=12, anchor="middle")
    label(760, 280, "compact", size=12, anchor="middle")

    panel(0, 300, 1000, 330, INK, "SYMBOL-ONLY MARK &amp; STACKED")
    center("symbol/ridecircle-symbol.svg", 190, 470, height=200)
    center("symbol/ridecircle-symbol-mono-white.svg", 390, 470, height=110)
    center("symbol/ridecircle-symbol-small.svg", 510, 470, height=48)
    label(390, 600, "mono", size=12, anchor="middle")
    label(510, 600, "small sizes", size=12, anchor="middle")
    center("logo/lockup-stacked/ridecircle-lockup-stacked-on-dark.svg", 800, 470, height=230)

    panel(0, 630, 1000, 250, PAPER, "LIGHT BACKGROUND VERSION", "#5E6266")
    center("logo/lockup/ridecircle-lockup-on-light.svg", 290, 770, width=420)
    center("logo/lockup-compact/ridecircle-lockup-compact-on-light.svg", 760, 770, width=320)

    panel(0, 880, 500, 220, INK, "MONOCHROME — ON DARK")
    center("logo/lockup-compact/ridecircle-lockup-compact-mono-white.svg", 250, 1000, width=300)
    panel(500, 880, 500, 220, PAPER, "MONOCHROME — ON LIGHT", "#5E6266")
    center("logo/lockup-compact/ridecircle-lockup-compact-mono-black.svg", 750, 1000, width=300)

    panel(1000, 0, 600, 560, SURFACE, "APP ICON")
    center("app-icon/app-icon-rounded-preview.svg", 1160, 230, width=240)
    label(1160, 385, "iOS / Android · 1024 px", fill=PAPER, size=13, anchor="middle")
    for i, (rel, cap) in enumerate((("app-icon/app-icon-dark.svg", "iOS dark"), ("app-icon/app-icon-tinted.svg", "iOS tinted"))):
        cx = 1110 + i * 110
        out.append(f'  <rect x="{cx - 45}" y="{425}" width="90" height="90" rx="20" fill="{INK if i == 0 else "#2A2D31"}"/>')
        out.append(nest(rel, cx - 45, 425, width=90)[0])
        label(cx, 540, cap, size=11, anchor="middle")
    label(1480, 110, "FAVICON", size=12, anchor="middle")
    for i, px in enumerate((64, 32, 16)):
        cy = 170 + i * 100
        out.append(nest("web/favicon.svg", 1480 - px / 2, cy - px / 2, width=px)[0])
        label(1480, cy + 50, f"{px} px", size=11, anchor="middle")

    panel(1000, 560, 600, 540, GRAPHITE, "COLOR")
    sw = [("Ride Lime", LIME), ("Ink", INK), ("Graphite", GRAPHITE), ("Surface", SURFACE),
          ("Paper", PAPER), ("Muted", MUTED), ("Support Accent", ACCENT)]
    for i, (nm, hx) in enumerate(sw):
        x, y = 1032 + (i % 4) * 138, 640 + (i // 4) * 210
        stroke = ' stroke="#3A3E42"' if hx in (INK, GRAPHITE, SURFACE) else ""
        out.append(f'  <rect x="{x}" y="{y}" width="120" height="120" rx="12" fill="{hx}"{stroke}/>')
        label(x, y + 146, nm, fill=PAPER, size=13, weight="bold")
        label(x, y + 166, hx, size=12)
    return W, H, "\n".join(out)


if __name__ == "__main__":
    main()
    count = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("files:", count)
