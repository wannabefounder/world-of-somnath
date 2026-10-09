"""Hoardings for the ten project buildings on 8th Main (World of Somnath).
Writes blender/atlas/projects.png (2048x2048, 2 x 8 slots of 1024x256) and adds a 'projects' key to atlas.json.
Run with the system python: python3 blender/make_project_boards.py"""
from PIL import Image, ImageDraw, ImageFont
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = next(p for p in [os.path.join(HERE, '..', '..', 'fonts'), '/home/claude/somnath-world/fonts'] if os.path.isdir(p))
DISP = os.path.join(FONTS, 'AnybodyCond.ttf'); FUN = os.path.join(FONTS, 'FunnelDisplay.ttf'); KN = os.path.join(FONTS, 'NotoSansKannada.ttf')

def font(path, size, wght=800, wdth=None):
    f = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
    try:
        vals = []
        for a in f.get_variation_axes():
            n = a.get('name', b''); n = n.decode() if isinstance(n, bytes) else n
            if 'idth' in n: vals.append(wdth if wdth else a['default'])
            elif 'eight' in n or n.lower().startswith('w'): vals.append(wght)
            else: vals.append(a['default'])
        f.set_variation_by_axes(vals)
    except Exception:
        pass
    return f

def fit(d, text, path, maxw, start, wght=800, wdth=None):
    s = start
    while s > 10:
        f = font(path, s, wght, wdth)
        if d.textlength(text, font=f) <= maxw: return f
        s -= 2
    return font(path, 10, wght, wdth)

# slug, number, board title, kicker, bg, fg, accent  (from site-v2/assets/cases.js)
PROJECTS = [
    ('snapmint-upi', '01', 'SNAPMINT UPI', 'Product design · Icons · Motion · Film', '#ff6f00', '#ffffff', '#ffd23f'),
    ('credit-line-on-upi', '02', 'CREDIT LINE ON UPI', 'Flows · Landing page · AI film campaign', '#0e3b2c', '#f4f1e8', '#9be15d'),
    ('checkout-and-onboarding', '03', 'CHECKOUT & ONBOARDING', 'Product design · Before / after · Motion', '#2340d9', '#ffffff', '#f5c400'),
    ('whitelabel-widget', '04', 'WHITE-LABEL PAY LATER', 'Design system · Merchant widgets', '#f6efe2', '#17150f', '#234a87'),
    ('mokshavastra', '05', 'MOKSHAVASTRA', 'My clothing brand · Catalogue · Store', '#0b0b0a', '#f4ead8', '#e8a33d'),
    ('ajay-sanjay', '06', 'AJAY SANJAY', 'Commerce platform · Designed and built', '#ffd23f', '#151a17', '#008632'),
    ('id-studio', '07', 'ID STUDIO', 'Internal tool · Designed and built', '#fff3e6', '#17150f', '#ff6f00'),
    ('qr-studio', '08', 'QR STUDIO', 'Internal tool · Designed and built', '#1a1814', '#f6f1e7', '#ff6b2b'),
    ('gatti', '09', 'GATTI', 'Concept · Brand · Character films', '#ff5fa2', '#17150f', '#ffd23f'),
    ('buy-the-way', '10', 'BUY THE WAY', 'Podcast identity · Edit', '#111111', '#ffffff', '#ff6f00'),
]
INK, YEL, PAPER = '#17150f', '#f5c400', '#f4f1e8'

def hoarding(n, title, kicker, bg, fg, acc):
    W, H = 1024, 256
    im = Image.new('RGB', (W, H), bg); d = ImageDraw.Draw(im)
    # number block: yellow tab with the case number, like a building number plate
    d.rectangle([0, 0, 214, H], fill=INK)
    fn = font(DISP, 170, 900, 60); d.text((107, H / 2 + 6), n, font=fn, fill=YEL, anchor='mm')
    # accent rule + title + kicker
    d.rectangle([214, H - 22, W, H], fill=acc)
    ft = fit(d, title, DISP, W - 214 - 70, 132, 900, 62); d.text((246, 104), title, font=ft, fill=fg, anchor='lm')
    # case-study tag, English first with the small Kannada word beside it
    tag = 'CASE STUDY'; ftg = font(FUN, 22, 700)
    tw = d.textlength(tag, font=ftg); fkn = font(KN, 20, 700); kw = d.textlength('ಕೇಸ್ ಸ್ಟಡಿ', font=fkn)
    x1 = W - 26; x0 = x1 - tw - kw - 46
    d.rounded_rectangle([x0, 168, x1, 212], radius=22, fill=INK)
    d.text((x0 + 16, 190), tag, font=ftg, fill=YEL, anchor='lm')
    d.text((x1 - 16, 191), 'ಕೇಸ್ ಸ್ಟಡಿ', font=fkn, fill=PAPER, anchor='rm')
    fk = fit(d, kicker, FUN, x0 - 248 - 24, 30, 600); d.text((248, 190), kicker, font=fk, fill=fg, anchor='lm')
    # frame
    d.rectangle([3, 3, W - 4, H - 4], outline=INK, width=6)
    return im

def street_board():
    """Gateway arch board over 8th Main: names the strip."""
    W, H = 1024, 256
    im = Image.new('RGB', (W, H), YEL); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 34], fill=INK); d.rectangle([0, H - 34, W, H], fill=INK)
    ft = fit(d, 'THE WORK · 8TH MAIN', DISP, W - 80, 120, 900, 62); d.text((W / 2, 120), 'THE WORK · 8TH MAIN', font=ft, fill=INK, anchor='mm')
    fk = font(FUN, 30, 700); d.text((W / 2, 190), 'Ten buildings, ten case studies. Drive up and press E.', font=fk, fill=INK, anchor='mm')
    return im

items = [(p[0], hoarding(*p[1:])) for p in PROJECTS] + [('strip', street_board())]
size = 2048; at = Image.new('RGB', (size, size), INK); meta = {}
for i, (key, img) in enumerate(items):
    col, row = i % 2, i // 2; x, y = col * 1024, row * 256
    at.paste(img, (x, y))
    meta[key] = [x / size, 1 - (y + 256) / size, (x + 1024) / size, 1 - y / size]
at.save(os.path.join(HERE, 'atlas', 'projects.png'), optimize=True)
path = os.path.join(HERE, 'atlas', 'atlas.json'); A = json.load(open(path)); A['projects'] = meta
json.dump(A, open(path, 'w'), indent=1)
json.dump([{'slug': p[0], 'n': p[1], 'title': p[2], 'kicker': p[3]} for p in PROJECTS], open(os.path.join(HERE, 'atlas', 'projects.json'), 'w'), indent=1)
print('projects atlas', len(meta))
