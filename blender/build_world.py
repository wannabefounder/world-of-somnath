"""Builds the World of Somnath locality in Blender and exports engine-ready GLBs.

Run:  /home/claude/bpyenv/bin/python blender/build_world.py
Outputs (static/): scenery/scenery.glb, terrain/terrain.glb, respawns/respawnsReferences.glb,
oakTrees/oakTreesReferences.glb (rain trees), cherryTrees/cherryTreesReferences.glb (tabebuia),
bushes/bushesReferences.glb, flowers/flowersReferences.glb, areas/areas.glb
and blender/world-of-somnath.blend (open in Blender 5 to refine).

Conventions follow the engine (Bruno Simon's folio-2025, MIT):
  *PhysicalFixed / *PhysicalDynamic objects carry collider children named cuboid*/tube*/ball*;
  ref* names are references; material 'palette' maps UVs onto static/palette.png swatches.
"""
import sys, os, math, random, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Matrix, Vector
from lib import *
from layout import *

rng = random.Random(20261009)
rr = lambda a, b: a + (b - a) * rng.random()
pick = lambda a: a[int(rng.random() * len(a))]
ATLAS = json.load(open(os.path.join(HERE, 'atlas', 'atlas.json')))

reset()
scene = bpy.context.scene
def coll(name):
    c = bpy.data.collections.new(name); scene.collection.children.link(c); return c
C_SCENERY, C_TERRAIN, C_RESPAWN, C_RAIN, C_TABE, C_BUSH, C_FLOW, C_AREAS = [coll(n) for n in
    ['scenery', 'terrain', 'respawns', 'rainTrees', 'tabebuia', 'bushes', 'flowers', 'areas']]

# materials
mat('palette', hexrgba('#ffffff'))
mat('signs', image=os.path.join(HERE, 'atlas', 'signs.png'))
mat('ads', image=os.path.join(HERE, 'atlas', 'ads.png'))
mat('black', hexrgba('#383039'))
mat('windowLit', hexrgba('#ffd08a'))
mat('streetLamp', hexrgba('#fff1c9'))

scenery_objects = []
def add_scenery(ob):
    scenery_objects.append(ob); return ob

WALLS = ['palepink', 'mint', 'lemon', 'sky', 'cream', 'peach', 'lilac', 'sand', 'sage', 'apricot', 'palepink', 'cream']
TRIM = {'palepink': 'pink', 'mint': 'sage', 'lemon': 'yellow', 'sky': 'cyan', 'cream': 'sand', 'peach': 'salmon',
        'lilac': 'purple', 'sand': 'khaki', 'sage': 'olive', 'apricot': 'orange'}

# ============================================================== streets
def build_streets():
    road = MeshBuilder()
    paint = MeshBuilder()
    walk = MeshBuilder()
    for zc, w, _ in MAINS:
        road.box((0, 0.01, zc), (EXTENT * 2, 0.02, w), P['dark'], mat='black')
    for xc, w, _ in CROSSES:
        road.box((xc, 0.011, 0), (w, 0.02, EXTENT * 2), P['dark'], mat='black')
    # markings: dashed centre lines (skip junction boxes), zebra crossings at every junction
    def in_junction(x, z, pad=1.5):
        return any(abs(x - xc) < w / 2 + FP + pad for xc, w, _ in CROSSES) and any(abs(z - zc) < w2 / 2 + FP + pad for zc, w2, _ in MAINS)
    for zc, w, _ in MAINS:
        x = -EXTENT + 2
        while x < EXTENT - 2:
            if not in_junction(x, zc): paint.box((x, 0.03, zc), (2.6, 0.012, 0.14), P['cream'])
            x += 6
    for xc, w, _ in CROSSES:
        z = -EXTENT + 2
        while z < EXTENT - 2:
            if not in_junction(xc, z): paint.box((xc, 0.03, z), (0.14, 0.012, 2.6), P['cream'])
            z += 6
    for zc, wz, _ in MAINS:
        for xc, wx, _ in CROSSES:
            for side in (-1, 1):  # zebra across the cross road, both sides of the main
                zz = zc + side * (wz / 2 + 1.6)
                for i in range(int(wx / 0.9)):
                    paint.box((xc - wx / 2 + 0.45 + i * 0.9, 0.03, zz), (0.45, 0.012, 2.4), P['cream'])
    # footpaths (raised slabs with yellow/black painted curb lip)
    fp_colliders = []
    def footpath(x0, x1, z0, z1, curb):
        cx, cz, w, d = (x0 + x1) / 2, (z0 + z1) / 2, x1 - x0, z1 - z0
        walk.box((cx, FPH / 2, cz), (w, FPH, d), P['concrete'])
        fp_colliders.append(((cx, FPH / 2, cz), (w, FPH, d)))
        # alternating curb paint, 1 m segments
        if curb in ('z0', 'z1'):
            zc = z0 + 0.09 if curb == 'z0' else z1 - 0.09
            n = int(w)
            for i in range(n):
                walk.box((x0 + i + 0.5, FPH / 2 + 0.01, zc), (1.0, FPH + 0.04, 0.18), P['autoYellow'] if i % 2 == 0 else P['black'])
        else:
            xc = x0 + 0.09 if curb == 'x0' else x1 - 0.09
            n = int(d)
            for i in range(n):
                walk.box((xc, FPH / 2 + 0.01, z0 + i + 0.5), (0.18, FPH + 0.04, 1.0), P['autoYellow'] if i % 2 == 0 else P['black'])
    for zc, w, _ in MAINS:
        for (x0, x1) in X_BANDS:
            footpath(x0, x1, zc + w / 2, zc + w / 2 + FP, 'z0')
            footpath(x0, x1, zc - w / 2 - FP, zc - w / 2, 'z1')
    for xc, w, _ in CROSSES:
        for (z0, z1) in Z_BANDS:
            footpath(xc + w / 2, xc + w / 2 + FP, z0, z1, 'x0')
            footpath(xc - w / 2 - FP, xc - w / 2, z0, z1, 'x1')
    # speed breakers (humps) on the cross roads near the junction — painted, solid
    humps = []
    for xc, w, _ in CROSSES:
        for z in (17.0, -17.0):
            humps.append((xc, z, w))
    hump = MeshBuilder()
    for xc, z, w in humps:
        for i in range(int(w / 0.6)):
            hump.box((xc - w / 2 + 0.3 + i * 0.6, 0.06, z), (0.6, 0.12, 0.9), P['autoYellow'] if i % 2 == 0 else P['black'])
    ro = add_scenery(road.to_object('refRoad', collection=C_SCENERY))
    add_scenery(paint.to_object('roadMarkings', collection=C_SCENERY))
    wo = add_scenery(walk.to_object('footpathsPhysicalFixed', collection=C_SCENERY))
    for i, (c, s) in enumerate(fp_colliders):
        collider(wo, 'cuboid', c, s, name=f'cuboid.fp{i:03d}')
    ho = add_scenery(hump.to_object('humpsPhysicalFixed', collection=C_SCENERY))
    for i, (xc, z, w) in enumerate(humps):
        collider(ho, 'cuboid', (xc, 0.04, z), (w, 0.1, 0.9), name=f'cuboid.hump{i}')

# ============================================================== buildings
SHOP_KEYS = ['bakery', 'darshini', 'medicals', 'xerox', 'fancy', 'mobile', 'condiments', 'tailors', 'juice', 'salon', 'hardware']
shop_queue = list(SHOP_KEYS)
POSTERS = ['pRent', 'pWater', 'pKannada', 'pYoga', 'pLostDog', 'pHackathon', 'pCoffee', 'pRain']
BILLBOARDS = ['bbBeega', 'bbHogona', 'bbOota', 'bbCowork']
bb_queue = list(BILLBOARDS)
lit_windows = MeshBuilder()   # all lit windows in one mesh (material switched at night by the engine)
building_count = [0]
roof_points = []   # for billboards
FH = 3.05

def window(mb, M, x, y, z, w=1.3, h=1.35, lit=False, wall='cream'):
    target = lit_windows if lit else mb
    target.box((x, y, z + 0.02), (w, h, 0.06), P['glass'] if not lit else P['cream'], M=M, mat='windowLit' if lit else 'palette')
    # frame + sill + grill bars
    mb.box((x, y - h / 2 - 0.04, z + 0.06), (w + 0.16, 0.07, 0.14), P['ltgrey'], M=M)
    for k in (-1, 0, 1):
        mb.box((x + k * w / 3.2, y, z + 0.09), (0.03, h, 0.03), P['dark'], M=M)
    mb.box((x, y + 0.15, z + 0.09), (w, 0.03, 0.03), P['dark'], M=M)

def building(M, w, d, floors, kind, wall=None, sign=None, setback=None, seed=None, mb=None, cols=None):
    """Local frame: front face at z=0 facing +z, building spans x∈[-w/2,w/2], z∈[-d,0].
    Geometry goes into the block's MeshBuilder `mb`; the collider spec is appended to `cols`."""
    building_count[0] += 1
    name = f'b{building_count[0]:03d}'
    wall = wall or pick(WALLS); trim = TRIM.get(wall, 'ltgrey')
    sb = setback if setback is not None else (rr(1.2, 2.2) if kind == 'house' else 0.15)
    fz = -sb; bd = d - sb; H = floors * FH; cz = fz - bd / 2; Y0 = FPH
    bw = w - 0.3
    mb.box((0, Y0 + H / 2, cz), (bw, H, bd), P[wall], M=M)
    for f in range(1, floors + 1):  # slab bands
        mb.box((0, Y0 + f * FH, cz), (bw + 0.12, 0.2, bd + 0.14), P['cream'] if wall != 'cream' else P['ltgrey'], M=M)
    # parapet
    py = Y0 + H + 0.45
    for (c, s) in [((0, py, fz - 0.08), (bw, 0.9, 0.16)), ((0, py, fz - bd + 0.08), (bw, 0.9, 0.16)),
                   ((-bw / 2 + 0.08, py, cz), (0.16, 0.9, bd)), ((bw / 2 - 0.08, py, cz), (0.16, 0.9, bd))]:
        mb.box(c, s, P[wall], M=M)
    nwin = max(1, int((bw - 1.0) / 2.5))
    start_floor = 1 if kind == 'shop' else 0
    for f in range(start_floor, floors):
        yb = Y0 + f * FH
        balcony = f > 0 and rng.random() < 0.5
        for k in range(nwin):
            x = -bw / 2 + bw * (k + 0.5) / nwin
            lit = rng.random() < 0.38
            window(mb, M, x, yb + 1.55, fz, lit=lit)
            mb.box((x, yb + 2.42, fz + 0.28), (1.8, 0.07, 0.58), P['cream'], M=M)   # chajja (sunshade)
        if balcony:
            bwid = min(bw - 0.8, rr(2.6, 4.6)); bx = rr(-(bw - bwid) / 2 + 0.3, (bw - bwid) / 2 - 0.3)
            mb.box((bx, yb + 0.07, fz + 0.55), (bwid, 0.14, 1.1), P['cream'], M=M)
            if rng.random() < 0.45:
                mb.box((bx, yb + 0.55, fz + 1.05), (bwid, 0.9, 0.1), P[trim], M=M)
            else:
                mb.box((bx, yb + 1.0, fz + 1.07), (bwid, 0.05, 0.05), P['dark'], M=M)
                n = int(bwid / 0.14)
                for i in range(n): mb.box((bx - bwid / 2 + 0.07 + i * 0.14, yb + 0.55, fz + 1.07), (0.02, 0.9, 0.02), P['dark'], M=M)
            if rng.random() < 0.6:  # potted plants (bush refs)
                for p in range(int(bwid / 0.8)):
                    px = bx - bwid / 2 + 0.4 + p * 0.8
                    mb.cyl((px, yb + 0.3, fz + 0.75), 0.15, 0.32, P['terracotta'], M=M, seg=10, r2=0.18)
                    wp = M @ Vector((px, yb + 0.7, fz + 0.75, 1))
                    ref(f'bush{name}{f}{p}', (wp[0], wp[1], wp[2]), scale=(0.32,) * 3, collection=C_BUSH, mesh=True)
            if rng.random() < 0.35:  # clothes drying on the balcony rail
                for i in range(int(bwid / 0.6)):
                    cw = rr(0.3, 0.55)
                    mb.quad([(bx - bwid / 2 + 0.3 + i * 0.6 - cw / 2, yb + 0.35, fz + 1.12), (bx - bwid / 2 + 0.3 + i * 0.6 + cw / 2, yb + 0.35, fz + 1.12),
                             (bx - bwid / 2 + 0.3 + i * 0.6 + cw / 2, yb + 1.02, fz + 1.12), (bx - bwid / 2 + 0.3 + i * 0.6 - cw / 2, yb + 1.02, fz + 1.12)],
                            sw=P[pick(['red', 'cyan', 'yellow', 'purple', 'pink', 'orange', 'mint', 'cream'])], M=M, double=True)
    # side windows (small)
    for f in range(start_floor, floors):
        for sx in (-1, 1):
            if rng.random() < 0.5:
                zz = cz + rr(-bd / 4, bd / 4)
                mb.box((sx * (bw / 2 + 0.02), Y0 + f * FH + 1.6, zz), (0.06, 0.9, 0.8), P['glass'], M=M)
    # ground floor
    if kind == 'shop':
        nshop = 2 if bw > 8.0 else 1
        sw_ = bw / nshop
        for k in range(nshop):
            x = -bw / 2 + sw_ * (k + 0.5)
            opening = rr(1.7, 2.2)
            mb.box((x, Y0 + 1.1, fz - 1.3), (sw_ - 0.35, 2.2, 0.1), P['cream'], M=M)            # back wall
            for s in range(3):  # shelves with colourful stock
                sy = Y0 + 0.5 + s * 0.6
                mb.box((x, sy, fz - 1.15), (sw_ - 0.5, 0.05, 0.3), P['dkbrown'], M=M)
                xx = x - (sw_ - 0.6) / 2
                while xx < x + (sw_ - 0.6) / 2:
                    pw = rr(0.12, 0.3); ph = rr(0.15, 0.35)
                    mb.box((xx + pw / 2, sy + ph / 2 + 0.03, fz - 1.15), (pw, ph, 0.22), P[pick(['red', 'yellow', 'cyan', 'orange', 'mint', 'purple', 'pink', 'autoGreen', 'cream'])], M=M)
                    xx += pw + 0.04
            mb.box((x, Y0 + 0.02, fz - 0.65), (sw_ - 0.35, 0.04, 1.3), P['grey'], M=M)            # shop floor
            mb.box((x, Y0 + opening + (2.4 - opening) / 2, fz + 0.03), (sw_ - 0.3, 2.4 - opening, 0.08), P['ltgrey'], M=M)  # rolled shutter
            mb.box((x, Y0 + 2.45, fz + 0.08), (sw_ - 0.2, 0.22, 0.22), P['grey'], M=M)            # shutter drum
            for sx in (-1, 1):
                mb.box((x + sx * (sw_ / 2 - 0.12), Y0 + 1.2, fz - 0.6), (0.22, 2.4, 1.3), P[wall], M=M)
        # signboard (atlas)
        key = sign or (shop_queue.pop(0) if shop_queue else pick(SHOP_KEYS))
        u0, v0, u1, v1 = ATLAS['signs'][key]
        sbw = bw - 0.5; sbh = min(1.0, sbw / 4.0)
        mb.box((0, Y0 + 2.95, fz + 0.12), (sbw, sbh, 0.1), P['dark'], M=M, mat='signs', uvrect=(u0, v0, u1, v1), uvface='pz')
        # tin awning
        mb.box((0, Y0 + 2.36, fz + 0.66), (bw - 0.3, 0.04, 1.3), P[pick(['cyan', 'autoGreen', 'red', 'yellow', 'grey'])], M=M, rot=(0.22, 0, 0))
    else:
        mb.box((rr(-bw / 4, bw / 4), Y0 + 1.1, fz + 0.03), (1.1, 2.2, 0.08), P['dkbrown'], M=M)  # door
        gx = rr(-bw / 2 + 1.4, bw / 2 - 1.4)
        lw = (gx - 0.8) - (-bw / 2); rw = (bw / 2) - (gx + 0.8)
        if lw > 0.2: mb.box((-bw / 2 + lw / 2, Y0 + 0.62, -0.08), (lw, 1.25, 0.16), P[trim], M=M)
        if rw > 0.2: mb.box((bw / 2 - rw / 2, Y0 + 0.62, -0.08), (rw, 1.25, 0.16), P[trim], M=M)
        mb.box((gx, Y0 + 0.62, -0.06), (1.6, 1.2, 0.05), P['dark'], M=M)                         # gate
        for sx in (-1, 1): mb.box((sx * (bw / 2 - 0.08), Y0 + 0.62, -sb / 2), (0.16, 1.25, sb), P[trim], M=M)
        mb.box((rr(-bw / 3, bw / 3), Y0 + 0.012, -sb / 2), (0.9, 0.02, 0.9), P['cream'], M=M)    # rangoli spot
        if rng.random() < 0.6:  # garden bushes in the setback
            for k in range(2):
                p = M @ Vector((rr(-bw / 2 + 0.6, bw / 2 - 0.6), Y0 + 0.4, -sb * rr(0.3, 0.7), 1))
                ref(f'bush{name}g{k}', (p[0], p[1], p[2]), scale=(rr(0.45, 0.7),) * 3, collection=C_BUSH, mesh=True)
        if rng.random() < 0.5:  # poster on the compound wall
            key = pick(POSTERS); u0, v0, u1, v1 = ATLAS['ads'][key]
            px = -bw / 2 + lw / 2 if lw > 1.2 else (bw / 2 - rw / 2 if rw > 1.2 else None)
            if px is not None:
                mb.quad([(px - 0.42, Y0 + 0.3, 0.005), (px + 0.42, Y0 + 0.3, 0.005), (px + 0.42, Y0 + 1.14, 0.005), (px - 0.42, Y0 + 1.14, 0.005)], uvrect=(u0, v0, u1, v1), mat='ads', M=M)
    # roof: Sintex-style black tank on a stand, stair-head room, dish, clothesline
    ry = Y0 + H
    tx = rr(-bw / 2 + 1.0, bw / 2 - 1.0); tz = fz - bd + rr(1.0, 2.2)
    mb.box((tx, ry + 0.25, tz), (1.3, 0.5, 1.3), P['concrete'], M=M)
    mb.cyl((tx, ry + 1.08, tz), 0.62, 1.15, P['black'], M=M, seg=18)
    mb.cyl((tx, ry + 1.72, tz), 0.3, 0.14, P['black'], M=M, seg=12, r2=0.26)
    for yy in (0.75, 1.15, 1.45): mb.cyl((tx, ry + yy, tz), 0.64, 0.05, P['dark'], M=M, seg=18)
    if floors >= 2 and rng.random() < 0.75:
        mx = (bw / 2 - 1.5) * (1 if rng.random() < 0.5 else -1)
        mb.box((mx, ry + 1.25, fz - bd + 1.5), (2.4, 2.5, 2.6), P[wall], M=M)
        mb.box((mx, ry + 2.56, fz - bd + 1.5), (2.7, 0.12, 2.9), P['cream'], M=M)
        mb.box((mx, ry + 1.05, fz - bd + 2.81), (0.9, 2.0, 0.04), P['dkbrown'], M=M)
        if rng.random() < 0.5:
            mb.cyl((mx + 0.6, ry + 2.95, fz - bd + 1.2), 0.38, 0.08, P['ltgrey'], M=M, seg=14, rot=(-0.9, 0.5, 0))
    if rng.random() < 0.55:
        lz = fz - rr(1.0, bd - 1.5); x0, x1 = -bw / 2 + 0.7, bw / 2 - 0.7
        for xx in (x0, x1): mb.box((xx, ry + 0.75, lz), (0.05, 1.5, 0.05), P['grey'], M=M)
        mb.box(((x0 + x1) / 2, ry + 1.48, lz), (x1 - x0, 0.015, 0.015), P['dark'], M=M)
        xx = x0 + 0.4
        while xx < x1 - 0.3:
            cw, ch = rr(0.3, 0.65), rr(0.45, 0.9)
            mb.quad([(xx - cw / 2, ry + 1.48 - ch, lz), (xx + cw / 2, ry + 1.48 - ch, lz), (xx + cw / 2, ry + 1.48, lz), (xx - cw / 2, ry + 1.48, lz)],
                    sw=P[pick(['red', 'cyan', 'yellow', 'purple', 'pink', 'orange', 'mint', 'cream', 'autoGreen'])], M=M, double=True)
            xx += rr(0.5, 0.95)
    roof_points.append((M, bw, bd, fz, ry, floors))
    c = M @ Vector((0, Y0 + H / 2, cz, 1))
    yaw = math.atan2(M[0][2], M[0][0])
    cols.append(((c[0], c[1], c[2]), (bw, H, bd), yaw, name))

def plots_along(a0, a1, place, minw=7.4, maxw=10.6):
    a = a0
    while a < a1 - 5.5:
        w = min(rr(minw, maxw), a1 - a)
        if a1 - (a + w) < 5.5: w = a1 - a
        place(a + w / 2, w)
        a += w

def in_rect(x, z, r, pad=0.0):
    return r['x0'] - pad <= x <= r['x1'] + pad and r['z0'] - pad <= z <= r['z1'] + pad

HERO_RECT = {'x0': HERO['x0'], 'x1': HERO['x0'] + HERO['w'], 'z0': HERO['z0'], 'z1': HERO['z0'] + HERO['d']}

def floors_for(kind, dist):
    base = 3 if dist < 30 else 2
    if kind == 'shop': return int(rr(base, base + 2.6))
    return int(rr(1, base + 1.6))

def build_blocks():
    for b in blocks():
        bmb = MeshBuilder(); bcols = []
        x0, x1, z0, z1 = b['x0'] + 0.1, b['x1'] - 0.1, b['z0'] + 0.1, b['z1'] - 0.1
        bw, bd = x1 - x0, z1 - z0
        # which sides face a road (blocks at the world edge have one side open)
        faces = {'z1': z1 < EXTENT - 1, 'z0': z0 > -EXTENT + 1, 'x1': x1 < EXTENT - 1, 'x0': x0 > -EXTENT + 1}
        taken = []
        def skip(cx, cz):
            return in_rect(cx, cz, HERO_RECT, 1.0) or in_rect(cx, cz, PARK, 1.0) or in_rect(cx, cz, VACANT, 1.0)
        def place_row(side):
            if side in ('z1', 'z0'):
                zf = z1 if side == 'z1' else z0
                ry = 0.0 if side == 'z1' else math.pi
                def place(cx, w):
                    cz_ = zf - PLOT_DEPTH / 2 if side == 'z1' else zf + PLOT_DEPTH / 2
                    if skip(cx, cz_): return
                    dist = math.hypot(cx, zf)
                    kind = 'shop' if (abs(zf) < 12 or rng.random() < 0.35) and rng.random() < 0.85 else 'house'
                    building(xform(cx, zf, ry), w, PLOT_DEPTH, floors_for(kind, dist), kind, mb=bmb, cols=bcols)
                plots_along(x0, x1, place)
            else:
                xf = x1 if side == 'x1' else x0
                ry = math.pi / 2 if side == 'x1' else -math.pi / 2
                lo = z0 + (PLOT_DEPTH if faces['z0'] else 0); hi = z1 - (PLOT_DEPTH if faces['z1'] else 0)
                def place(cz, w):
                    cx_ = xf - PLOT_DEPTH / 2 if side == 'x1' else xf + PLOT_DEPTH / 2
                    if skip(cx_, cz): return
                    dist = math.hypot(xf, cz)
                    kind = 'shop' if abs(xf) < 12 and rng.random() < 0.7 else ('shop' if rng.random() < 0.2 else 'house')
                    building(xform(xf, cz, ry), w, PLOT_DEPTH, floors_for(kind, dist), kind, mb=bmb, cols=bcols)
                plots_along(lo, hi, place)
        for side, ok in faces.items():
            if ok: place_row(side)
        # interior back-fill (seen from above): simple massing so the camera never sees voids
        ix0, ix1 = x0 + (PLOT_DEPTH if faces['x0'] else 0) + 0.6, x1 - (PLOT_DEPTH if faces['x1'] else 0) - 0.6
        iz0, iz1 = z0 + (PLOT_DEPTH if faces['z0'] else 0) + 0.6, z1 - (PLOT_DEPTH if faces['z1'] else 0) - 0.6
        if ix1 - ix0 > 6 and iz1 - iz0 > 6:
            z = iz0
            while z < iz1 - 5:
                d = min(rr(9, 13), iz1 - z)
                plots_along(ix0, ix1, lambda cx, w, z=z, d=d: (None if skip(cx, z + d / 2) else building(xform(cx, z + d, 0), w, d, int(rr(1, 3.6)), 'house', setback=rr(1.5, 3), mb=bmb, cols=bcols)), minw=9, maxw=14)
                z += d + 0.4
        if not bmb.empty():
            cx_, cz_ = (x0 + x1) / 2, (z0 + z1) / 2
            ob = add_scenery(bmb.to_object(f"block{b['id']}PhysicalFixed", origin=(cx_, 0, cz_), collection=C_SCENERY))
            for (c, s_, yaw, nm) in bcols:
                collider(ob, 'cuboid', (c[0] - cx_, c[1], c[2] - cz_), s_, name=f'cuboid.{nm}', rot=yaw)

# ============================================================== Somnath Nilaya (hero, corner plot NE of the junction)
def build_hero():
    mb = MeshBuilder(); lit = lit_windows
    x0, z0, w, d = HERO['x0'], HERO['z0'], HERO['w'], HERO['d']
    floors, fh = 6, 3.25; H = floors * fh; Y0 = FPH
    bx0, bx1, bz0, bz1 = x0 + 0.9, x0 + w - 0.2, z0 + 0.9, z0 + d - 0.2
    cx, cz, bw, bd = (bx0 + bx1) / 2, (bz0 + bz1) / 2, bx1 - bx0, bz1 - bz0
    # compound + garden + gate (faces both roads: south = -z side is 8th Main, west = -x side is 4th Cross)
    for (c, s) in [((x0 + w / 2 + 1.5, Y0 + 0.55, z0 + 0.1), (w - 3.0, 1.1, 0.18)), ((x0 + 0.1, Y0 + 0.55, z0 + d / 2 + 1.0), (0.18, 1.1, d - 2.0))]:
        mb.box(c, s, P['concrete'])
    mb.box((x0 + 1.2, Y0 + 0.6, z0 + 0.1), (2.0, 1.15, 0.06), P['dark'])   # corner gate
    # main mass: white frame + terracotta brick back
    mb.box((bx1 - bw * 0.22, Y0 + H / 2, cz), (bw * 0.44, H, bd), P['terracotta'])
    mb.box((cx, Y0 + H / 2, bz1 - bd * 0.2), (bw, H, bd * 0.4), P['terracotta'])
    for f in range(floors + 1):
        y = Y0 + f * fh
        mb.box((cx - 0.25, y, cz - 0.25), (bw + 0.6, 0.32, bd + 0.6), P['cream'])
        if f == floors: break
        lit_floor = f in (1, 3, 5)
        gx0, gx1 = bx0, bx0 + bw * 0.58; gz0, gz1 = bz0, bz0 + bd * 0.6
        tgt = lit if lit_floor else mb
        tgt.box(((gx0 + gx1) / 2, y + fh / 2, gz0 + 0.04), (gx1 - gx0, fh - 0.36, 0.06), P['cream'] if lit_floor else P['glass'], mat='windowLit' if lit_floor else 'palette')
        tgt.box((gx0 + 0.04, y + fh / 2, (gz0 + gz1) / 2), (0.06, fh - 0.36, gz1 - gz0), P['cream'] if lit_floor else P['glass'], mat='windowLit' if lit_floor else 'palette')
        for k in range(7):
            mb.box((gx0 + k * (gx1 - gx0) / 6, y + fh / 2, gz0 + 0.08), (0.07, fh - 0.3, 0.09), P['black'])
            mb.box((gx0 + 0.08, y + fh / 2, gz0 + k * (gz1 - gz0) / 6), (0.09, fh - 0.3, 0.07), P['black'])
        # interiors visible through the glass
        mb.box(((gx0 + gx1) / 2, y + fh / 2, gz1), (gx1 - gx0, fh - 0.3, 0.1), P['peach'] if lit_floor else P['ltgrey'])
        mb.box((gx1, y + fh / 2, (gz0 + gz1) / 2), (0.1, fh - 0.3, gz1 - gz0), P['peach'] if lit_floor else P['ltgrey'])
        if f in (2, 4):  # projecting balconies with planters
            mb.box((gx0 + (gx1 - gx0) / 2, y + 0.08, gz0 - 0.75), (gx1 - gx0, 0.16, 1.5), P['cream'])
            mb.box((gx0 + (gx1 - gx0) / 2, y + 0.62, gz0 - 1.48), (gx1 - gx0, 0.95, 0.04), P['sky'])
            for k in range(4):
                px = gx0 + 0.9 + k * (gx1 - gx0 - 1.8) / 3
                mb.box((px, y + 0.38, gz0 - 1.1), (0.75, 0.45, 0.55), P['dark'])
                ref(f'bushHero{f}{k}', (px, y + 0.85, gz0 - 1.1), scale=(0.5,) * 3, collection=C_BUSH, mesh=True)
    # ground floor 'front desk': deep canopy
    mb.box((bx0 + bw * 0.32, Y0 + 3.05, bz0 - 1.4), (bw * 0.64, 0.25, 3.0), P['cream'])
    for px in (bx0 + 0.3, bx0 + bw * 0.62): mb.box((px, Y0 + 1.5, bz0 - 2.75), (0.18, 3.0, 0.18), P['black'])
    # terrace: parapet, pergola, tank, planters, name board
    ry = Y0 + H
    for (c, s) in [((cx, ry + 0.55, bz0 - 0.2), (bw + 0.6, 1.1, 0.2)), ((bx0 - 0.2, ry + 0.55, cz), (0.2, 1.1, bd + 0.6)),
                   ((cx, ry + 0.55, bz1 + 0.15), (bw + 0.6, 1.1, 0.2)), ((bx1 + 0.15, ry + 0.55, cz), (0.2, 1.1, bd + 0.6))]:
        mb.box(c, s, P['cream'])
    mb.box((cx, ry + 0.18, cz), (bw, 0.04, bd), P['sand'])
    for k in range(6): mb.box((bx1 - 0.5 - k * 0.85, ry + 2.75, bz1 - bd * 0.25), (0.12, 0.16, bd * 0.48), P['dkbrown'])
    for (px, pz) in [(bx1 - 0.5, bz1 - 0.5), (bx1 - 4.8, bz1 - 0.5), (bx1 - 0.5, bz1 - bd * 0.48), (bx1 - 4.8, bz1 - bd * 0.48)]:
        mb.box((px, ry + 1.4, pz), (0.14, 2.6, 0.14), P['dkbrown'])
    mb.box((bx1 - 1.1, ry + 0.35, bz0 + 1.4), (1.5, 0.5, 1.5), P['concrete'])
    mb.cyl((bx1 - 1.1, ry + 1.25, bz0 + 1.4), 0.7, 1.3, P['black'], seg=20)
    for k in range(3):
        mb.cyl((bx0 + 0.7, ry + 0.45, bz1 - 1.1 - k * 1.5), 0.32, 0.5, P['terracotta'], seg=12, r2=0.26)
        ref(f'bushHeroRoof{k}', (bx0 + 0.7, ry + 1.0, bz1 - 1.1 - k * 1.5), scale=(0.6,) * 3, collection=C_BUSH, mesh=True)
    u0, v0, u1, v1 = ATLAS['signs']['bakery']  # placeholder region replaced below
    ob = add_scenery(mb.to_object('somnathNilayaPhysicalFixed', origin=(cx, 0, cz), collection=C_SCENERY))
    collider(ob, 'cuboid', (0, Y0 + H / 2, 0), (bw, H, bd))
    for (c, s) in [((0, ry + 0.6, bz0 - 0.2 - cz), (bw + 0.6, 1.2, 0.2)), ((bx0 - 0.2 - cx, ry + 0.6, 0), (0.2, 1.2, bd + 0.6)),
                   ((0, ry + 0.6, bz1 + 0.15 - cz), (bw + 0.6, 1.2, 0.2)), ((bx1 + 0.15 - cx, ry + 0.6, 0), (0.2, 1.2, bd + 0.6)),
                   ((bx1 - 1.1 - cx, ry + 0.95, bz0 + 1.4 - cz), (1.5, 1.9, 1.5))]:
        collider(ob, 'cuboid', c, s)
    # references the engine uses
    ref('refHeroTerrace', (cx - 1.0, ry + 0.4, cz - 1.0), collection=C_SCENERY)
    ref('refHeroBoard', (bx0 + bw * 0.4, ry + 0.9, bz0 - 0.32), collection=C_SCENERY)
    return (bx0, bx1, bz0, bz1, ry)

# ============================================================== street furniture, cables, trees
POLE_H = 8.2
def build_furniture():
    mb = MeshBuilder(); cables = MeshBuilder(); lamps = MeshBuilder()
    poles = []
    for zc, w, _ in MAINS:
        for side in (-1, 1):
            z = zc + side * (w / 2 + 0.4)
            x = -EXTENT + 8 + (0 if side > 0 else 11)
            while x < EXTENT - 4:
                if not any(abs(x - xc) < cw / 2 + FP + 1.5 for xc, cw, _ in CROSSES):
                    poles.append(((x, z), side, 'main'))
                x += 22
    for xc, w, _ in CROSSES:
        z = -EXTENT + 18
        while z < EXTENT - 4:
            if not any(abs(z - zc) < mw / 2 + FP + 1.5 for zc, mw, _ in MAINS):
                poles.append(((xc - w / 2 - 0.4, z), 0, 'cross'))
            z += 22
    for (x, z), side, kind in poles:
        mb.box((x, FPH + POLE_H / 2, z), (0.22, POLE_H, 0.22), P['concrete'])
        for k in (-1, 0, 1): mb.box((x, FPH + 7.6 + k * 0.25, z), (0.9 if kind == 'main' else 0.06, 0.05, 0.06 if kind == 'main' else 0.9), P['dark'])
        toward = (0, 0, -side * 1.4) if kind == 'main' else (1.4, 0, 0)
        mb.box((x + toward[0] / 2, FPH + 6.6, z + toward[2] / 2), (abs(toward[0]) + 0.06, 0.06, abs(toward[2]) + 0.06), P['grey'])
        lamps.box((x + toward[0], FPH + 6.52, z + toward[2]), (0.5, 0.12, 0.26) if kind == 'main' else (0.26, 0.12, 0.5), P['cream'], mat='streetLamp')
        ref('refStreetLight', (x + toward[0], FPH + 6.2, z + toward[2]), collection=C_SCENERY)
    # cables between consecutive poles on the same line (sagging catenaries)
    def catenary(a, b, sag, r=0.014):
        pts = []
        for i in range(13):
            t = i / 12
            pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t - math.sin(t * math.pi) * sag, a[2] + (b[2] - a[2]) * t))
        cables.tube(pts, r, P['black'])
    by_line = {}
    for (x, z), side, kind in poles:
        key = (kind, round(z, 1)) if kind == 'main' else (kind, round(x, 1))
        by_line.setdefault(key, []).append((x, z))
    for key, pts in by_line.items():
        pts.sort(key=lambda p: p[0] if key[0] == 'main' else p[1])
        for a, b in zip(pts, pts[1:]):
            if math.hypot(a[0] - b[0], a[1] - b[1]) > 26: continue
            for k in (-1, 0, 1):
                catenary((a[0], FPH + 7.6 + k * 0.25, a[1]), (b[0], FPH + 7.6 + k * 0.25, b[1]), rr(0.35, 0.8))
            if rng.random() < 0.5:  # the classic tangle: loops of optic fibre
                catenary((a[0], FPH + 7.0, a[1]), (b[0], FPH + 7.1, b[1]), rr(1.0, 1.8), r=0.02)
    # cables across the street to buildings
    for (x, z), side, kind in poles[::3]:
        if kind != 'main': continue
        tz = z - side * rr(8, 11); tx = x + rr(-5, 5)
        catenary((x, FPH + 7.3, z), (tx, rr(6, 8.5), tz), rr(0.8, 1.6), r=0.01)
    add_scenery(mb.to_object('poles', collection=C_SCENERY))
    add_scenery(cables.to_object('cables', collection=C_SCENERY))
    add_scenery(lamps.to_object('streetLamps', collection=C_SCENERY))

def tree_positions():
    rain, tabe = [], []
    def along(sideline, a0, a1, horiz, kind_bias):
        a = a0 + rr(2, 8)
        while a < a1 - 2:
            x, z = (a, sideline) if horiz else (sideline, a)
            if not any(abs(x - xc) < cw / 2 + FP + 3 for xc, cw, _ in CROSSES) or not horiz:
                if horiz or not any(abs(z - zc) < mw / 2 + FP + 3 for zc, mw, _ in MAINS):
                    (tabe if rng.random() < kind_bias else rain).append((x, z))
            a += rr(13, 21)
    for zc, w, _ in MAINS:
        for side in (-1, 1): along(zc + side * (w / 2 + FP - 0.7), -EXTENT + 3, EXTENT - 3, True, 0.45)
    for xc, w, _ in CROSSES:
        for side in (-1, 1): along(xc + side * (w / 2 + FP - 0.7), -EXTENT + 3, EXTENT - 3, False, 0.35)
    # park trees
    for i in range(7):
        p = (rr(PARK['x0'] + 2, PARK['x1'] - 2), rr(PARK['z0'] + 2, PARK['z1'] - 2))
        (tabe if i % 2 == 0 else rain).append(p)
    # don't plant inside the hero plot, the auto stand or the cricket ground
    keep = lambda p: not in_rect(p[0], p[1], HERO_RECT, 2) and math.hypot(p[0] - AUTO_STAND[0], p[1] - AUTO_STAND[1]) > 6
    return [p for p in rain if keep(p)], [p for p in tabe if keep(p)]

def build_trees():
    rain, tabe = tree_positions()
    for i, (x, z) in enumerate(rain):
        s = rr(1.1, 1.45)
        ref(f'treeBody.r{i:03d}', (x, FPH, z), scale=(s, s, s), roty=rr(0, 6.28), collection=C_RAIN, mesh=True)
    for i, (x, z) in enumerate(tabe):
        s = rr(0.9, 1.2)
        ref(f'treeBody.t{i:03d}', (x, FPH, z), scale=(s, s, s), roty=rr(0, 6.28), collection=C_TABE, mesh=True)
    return rain + tabe

# ============================================================== park, vacant site, junction life
def build_park():
    mb = MeshBuilder()
    x0, x1, z0, z1 = PARK['x0'], PARK['x1'], PARK['z0'], PARK['z1']
    cx, cz, w, d = (x0 + x1) / 2, (z0 + z1) / 2, x1 - x0, z1 - z0
    # low wall + green railing on the two road-facing sides
    walls = [((cx, FPH + 0.3, z0 + 0.12), (w, 0.6, 0.25)), ((x1 - 0.12, FPH + 0.3, cz), (0.25, 0.6, d))]
    for c, s in walls: mb.box(c, s, P['cream'])
    x = x0 + 0.2
    while x < x1 - 1.6:
        if not (x0 + w * 0.55 < x < x0 + w * 0.55 + 1.6): mb.box((x, FPH + 1.0, z0 + 0.12), (0.03, 0.8, 0.03), P['autoGreen'])
        x += 0.2
    z = z0 + 0.2
    while z < z1:
        mb.box((x1 - 0.12, FPH + 1.0, z), (0.03, 0.8, 0.03), P['autoGreen']); z += 0.2
    mb.box((cx, FPH + 1.42, z0 + 0.12), (w, 0.05, 0.05), P['autoGreen']); mb.box((x1 - 0.12, FPH + 1.42, cz), (0.05, 0.05, d), P['autoGreen'])
    # walking track loop (slabs, also painted into terrain)
    for (c, s) in [((cx, FPH * 0.5, z0 + 2.2), (w - 3.0, 0.06, 1.4)), ((cx, FPH * 0.5, z1 - 2.2), (w - 3.0, 0.06, 1.4)),
                   ((x0 + 2.2, FPH * 0.5, cz), (1.4, 0.06, d - 3.0)), ((x1 - 2.2, FPH * 0.5, cz), (1.4, 0.06, d - 3.0))]:
        mb.box(c, s, P['taupe'])
    # benches + yoga mats + a swing
    for k in range(3):
        bx = x0 + 4 + k * 5.5
        mb.box((bx, 0.45, z1 - 3.4), (1.8, 0.08, 0.5), P['dkbrown']); mb.box((bx, 0.75, z1 - 3.62), (1.8, 0.5, 0.08), P['dkbrown'])
        for sx in (-0.8, 0.8): mb.box((bx + sx, 0.22, z1 - 3.4), (0.08, 0.44, 0.48), P['dark'])
    for k in range(3):
        mb.box((cx - 3 + k * 1.4, 0.025, cz + 1.0), (0.65, 0.02, 1.7), P[pick(['purple', 'cyan', 'pink'])])
    sx, sz = x0 + 4.5, z0 + 5.5
    for dx in (-1.1, 1.1): mb.box((sx + dx, 1.25, sz), (0.1, 2.5, 0.1), P['red'])
    mb.box((sx, 2.5, sz), (2.4, 0.1, 0.1), P['red'])
    mb.box((sx, 0.55, sz), (0.8, 0.06, 0.35), P['yellow'])
    for dx in (-0.35, 0.35): mb.box((sx + dx, 1.5, sz), (0.015, 1.9, 0.015), P['dark'])
    # board
    u0, v0, u1, v1 = ATLAS['ads']['pYoga']
    mb.quad([(x1 - 0.9, FPH + 1.0, z0 + 0.0), (x1 - 2.5, FPH + 1.0, z0 + 0.0), (x1 - 2.5, FPH + 2.6, z0 + 0.0), (x1 - 0.9, FPH + 2.6, z0 + 0.0)], uvrect=(u0, v0, u1, v1), mat='ads')
    for dx in (-2.4, -1.0): mb.box((x1 + dx, FPH + 1.0, z0 + 0.25), (0.06, 2.0, 0.06), P['grey'])
    ob = add_scenery(mb.to_object('parkPhysicalFixed', origin=(cx, 0, cz), collection=C_SCENERY))
    for c, s in walls: collider(ob, 'cuboid', (c[0] - cx, c[1] + 0.4, c[2] - cz), (s[0], 1.4, s[2]))
    # flowers + bushes in park beds
    for i in range(40):
        ref(f'flowers.p{i}', (rr(x0 + 1, x1 - 1), 0.0, rr(z0 + 3.2, z0 + 4.5) if i % 2 else rr(z1 - 1.6, z1 - 0.8)), scale=(1, 1, 1), roty=rr(0, 6), collection=C_FLOW, mesh=True)
    for i in range(10):
        ref(f'bushPark{i}', (rr(x0 + 1, x1 - 1), 0.5, z1 - 1.2), scale=(rr(0.7, 1.1),) * 3, collection=C_BUSH, mesh=True)

def build_vacant():
    """Vacant site with weeds, a 'site for sale' board and gully cricket."""
    mb = MeshBuilder()
    x0, x1, z0, z1 = VACANT['x0'], VACANT['x1'], VACANT['z0'], VACANT['z1']
    # broken compound wall stubs
    for x in [x0 + 1, x0 + 6, x0 + 13]:
        mb.box((x, 0.5, z1 - 0.2), (rr(2, 4), 1.0, 0.2), P['ltgrey'])
    # rubble + bricks heap
    for i in range(18):
        mb.box((rr(x0 + 1, x0 + 5), rr(0.05, 0.25), rr(z0 + 1, z0 + 5)), (rr(0.2, 0.5), rr(0.1, 0.3), rr(0.15, 0.3)), P[pick(['terracotta', 'ltgrey', 'taupe'])], rot=(0, rr(0, 3), 0))
    # 'site for sale' board
    u0, v0, u1, v1 = ATLAS['ads']['pRent']
    bx, bz = x1 - 3, z1 - 0.5
    mb.quad([(bx - 0.9, 1.2, bz), (bx + 0.9, 1.2, bz), (bx + 0.9, 3.0, bz), (bx - 0.9, 3.0, bz)], uvrect=(u0, v0, u1, v1), mat='ads', double=True)
    for dx in (-0.8, 0.8): mb.box((bx + dx, 1.2, bz - 0.04), (0.07, 2.4, 0.07), P['dkbrown'])
    add_scenery(mb.to_object('vacantSite', collection=C_SCENERY))

def dyn(name, mb, colliders, pos, mass, roty=0.0):
    """A dynamic prop: mesh + collider children, custom 'mass' extra."""
    ob = add_scenery(mb.to_object(name + 'PhysicalDynamic', origin=pos, collection=C_SCENERY))
    ob['mass'] = mass
    ob.rotation_euler = (0, 0, roty)
    for i, (kind, c, s) in enumerate(colliders):
        collider(ob, kind, (c[0] - pos[0], c[1] - pos[1], c[2] - pos[2]), s, name=f'{kind}.{name}{i}')
    return ob

def build_props():
    n = [0]
    def uid(p): n[0] += 1; return f'{p}{n[0]:03d}'
    # gully cricket on the vacant site
    cx, cz = (VACANT['x0'] + VACANT['x1']) / 2, (VACANT['z0'] + VACANT['z1']) / 2
    for k in (-1, 0, 1):
        mb = MeshBuilder(); p = (cx + k * 0.11, 0.36, cz)
        mb.cyl(p, 0.02, 0.71, P['cream'], seg=8)
        dyn(uid('stump'), mb, [('tube', p, (0.05, 0.71, 0.05))], p, 0.6)
    mb = MeshBuilder(); p = (cx - 0.5, 0.05, cz + 7)
    mb.cyl(p, 0.035, 0.07, P['autoYellow'], seg=10)
    dyn(uid('tennisBall'), mb, [('ball', p, (0.07, 0.07, 0.07))], p, 0.06)
    mb = MeshBuilder(); p = (cx + 0.9, 0.42, cz - 0.4)
    mb.box(p, (0.11, 0.84, 0.04), P['sand'])
    dyn(uid('bat'), mb, [('cuboid', p, (0.11, 0.84, 0.04))], p, 1.1)
    # waste bins near the hero (green wet / blue dry), cartons and 20L water cans outside shops
    for k, sw in enumerate(['autoGreen', 'cyan']):
        mb = MeshBuilder(); p = (HERO['x0'] + 1.5 + k * 0.8, FPH + 0.45, HERO['z0'] - 1.2)
        mb.cyl(p, 0.3, 0.85, P[sw], seg=14, r2=0.33); mb.cyl((p[0], p[1] + 0.45, p[2]), 0.35, 0.06, P[sw], seg=14)
        dyn(uid('bin'), mb, [('tube', p, (0.66, 0.9, 0.66))], p, 4)
    for i in range(6):
        mb = MeshBuilder(); p = (14 + (i % 3) * 0.6, FPH + 0.2 + (i // 3) * 0.41, -7.6)
        mb.box(p, (0.55, 0.4, 0.45), P['khaki'])
        dyn(uid('carton'), mb, [('cuboid', p, (0.55, 0.4, 0.45))], p, 1.5)
    for i in range(5):
        mb = MeshBuilder(); p = (-15 + i * 0.4, FPH + 0.25, -7.4)
        mb.cyl(p, 0.14, 0.48, P['sky'], seg=12); mb.cyl((p[0], p[1] + 0.29, p[2]), 0.05, 0.1, P['cyan'], seg=8)
        dyn(uid('waterCan'), mb, [('tube', p, (0.28, 0.5, 0.28))], p, 2)
    # plastic chairs at the chai stall (outside the darshini row)
    for i in range(4):
        mb = MeshBuilder(); p = (-12 + i * 0.75, FPH + 0.45, -7.2); col = 'red' if i % 2 == 0 else 'cyan'
        mb.box((p[0], p[1], p[2]), (0.46, 0.05, 0.44), P[col]); mb.box((p[0], p[1] + 0.24, p[2] - 0.22), (0.46, 0.42, 0.05), P[col])
        for dx, dz in [(-0.2, -0.19), (0.2, -0.19), (-0.2, 0.19), (0.2, 0.19)]: mb.box((p[0] + dx, p[1] - 0.22, p[2] + dz), (0.04, 0.42, 0.04), P[col])
        dyn(uid('chair'), mb, [('cuboid', (p[0], p[1] - 0.2, p[2]), (0.46, 0.44, 0.44)), ('cuboid', (p[0], p[1] + 0.24, p[2] - 0.22), (0.46, 0.42, 0.05))], p, 2.2)
    # traffic cones around a dug-up patch (classic)
    for i in range(5):
        mb = MeshBuilder(); p = (30 + i * 1.1, 0.33, 2.2 + (i % 2) * 0.6)
        mb.cyl(p, 0.05, 0.62, P['orange'], seg=10, r2=0.05); mb.cyl((p[0], 0.33, p[2]), 0.22, 0.62, P['orange'], seg=12, r2=0.04)
        mb.box((p[0], 0.03, p[2]), (0.4, 0.06, 0.4), P['black'])
        dyn(uid('cone'), mb, [('cuboid', p, (0.4, 0.66, 0.4))], p, 1.0)
    dug = MeshBuilder(); dug.box((32.2, 0.03, 2.5), (5, 0.04, 1.6), P['khaki'])
    for i in range(10): dug.box((rr(30, 34.5), 0.08, rr(1.9, 3.1)), (rr(0.3, 0.6), rr(0.08, 0.2), rr(0.3, 0.6)), P['taupe'])
    add_scenery(dug.to_object('dugUpRoad', collection=C_SCENERY))

def build_junction_life():
    """Fixed pieces that make the junction read as Bengaluru: chai cart, milk booth, auto stand, transformer, billboards, road signs, potholes."""
    mb = MeshBuilder()
    # chai cart on the south footpath of 8th Main, west of the junction
    x, z = -9.0, -7.2
    mb.box((x, FPH + 0.75, z), (1.6, 0.9, 0.9), P['cream'])
    mb.box((x, FPH + 2.05, z), (1.9, 0.05, 1.2), P['cyan'], rot=(0.1, 0, 0))
    for sx in (-0.8, 0.8): mb.box((x + sx, FPH + 1.55, z + 0.4), (0.05, 1.0, 0.05), P['dark'])
    for k in range(2): mb.cyl((x - 0.4 + k * 0.6, FPH + 1.37, z), 0.16, 0.32, P['ltgrey'], seg=14, r2=0.12)
    u0, v0, u1, v1 = ATLAS['signs']['chai']
    mb.quad([(x - 0.75, FPH + 1.5, z + 0.47), (x + 0.75, FPH + 1.5, z + 0.47), (x + 0.75, FPH + 1.87, z + 0.47), (x - 0.75, FPH + 1.87, z + 0.47)], uvrect=(u0, v0, u1, v1), mat='signs')
    for wx, wz in [(-0.6, 0.46), (0.6, 0.46), (-0.6, -0.46), (0.6, -0.46)]: mb.cyl((x + wx, FPH + 0.22, z + wz), 0.22, 0.06, P['black'], seg=12, axis='z')
    # milk booth (blue kiosk) at the park corner
    x, z = PARK['x1'] - 1.0, PARK['z0'] - 0.9
    mb.box((x, FPH + 1.2, z), (1.6, 2.4, 1.4), P['sky'])
    mb.box((x, FPH + 2.5, z), (1.9, 0.12, 1.7), P['cyan'])
    u0, v0, u1, v1 = ATLAS['signs']['milk']
    mb.quad([(x + 0.78, FPH + 2.0, z - 0.71), (x - 0.78, FPH + 2.0, z - 0.71), (x - 0.78, FPH + 2.4, z - 0.71), (x + 0.78, FPH + 2.4, z - 0.71)], uvrect=(u0, v0, u1, v1), mat='signs')
    mb.box((x, FPH + 1.0, z - 0.71), (1.2, 0.8, 0.04), P['dark'])
    # transformer box (green) + its plinth, on the hero side of 8th Main
    x, z = 26.0, 7.4
    mb.box((x, FPH + 0.15, z), (2.4, 0.3, 1.2), P['concrete']); mb.box((x, FPH + 1.0, z), (2.0, 1.4, 0.9), P['autoGreen'])
    # AUTO STAND sign
    x, z = AUTO_STAND
    mb.box((x, FPH + 1.4, z), (0.08, 2.8, 0.08), P['ltgrey'])
    mb.box((x + 0.02, FPH + 2.6, z), (0.04, 0.6, 1.6), P['autoYellow'])
    # road name signs at the junction corners
    for (x, z, key, ry) in [(-5.6, 7.0, 'roadMain', 0.0), (5.6, -7.1, 'roadCross', math.pi)]:
        mb.box((x, FPH + 1.5, z), (0.07, 3.0, 0.07), P['ltgrey'])
        u0, v0, u1, v1 = ATLAS['signs'][key]
        mb.box((x, FPH + 3.0, z), (2.2, 0.55, 0.05), P['cream'], mat='signs', uvrect=(u0, v0, u1, v1), uvface='pz', rot=(0, ry, 0))
    # potholes (dark patches) on 8th Main
    for i in range(7):
        mb.cyl((rr(-60, 60), 0.024, rr(-4, 4)), rr(0.25, 0.6), 0.01, P['black'], seg=10)
    add_scenery(mb.to_object('junctionLife', collection=C_SCENERY))
    # rooftop billboards on the four buildings nearest the junction (steel frame + ad)
    near = sorted(roof_points, key=lambda r: math.hypot((r[0] @ Vector((0, 0, 0, 1)))[0], (r[0] @ Vector((0, 0, 0, 1)))[2]))
    bbm = MeshBuilder(); used = 0
    for (M, bw, bd, fz, ry, floors) in near:
        if used >= len(BILLBOARDS): break
        if floors < 2: continue
        key = BILLBOARDS[used]; u0, v0, u1, v1 = ATLAS['ads'][key]
        W, Hh = min(bw - 0.6, 6.4), min(bw - 0.6, 6.4) / 2
        y0 = ry + 1.2
        bbm.quad([(-W / 2, y0, -0.6), (W / 2, y0, -0.6), (W / 2, y0 + Hh, -0.6), (-W / 2, y0 + Hh, -0.6)], uvrect=(u0, v0, u1, v1), mat='ads', M=M)
        bbm.box((0, y0 + Hh / 2, -0.7), (W + 0.2, Hh + 0.2, 0.08), P['dark'], M=M)
        for sx in (-W / 2 + 0.4, W / 2 - 0.4):
            bbm.box((sx, ry + 0.6 + Hh / 2, -1.0), (0.1, 1.2 + Hh, 0.1), P['grey'], M=M)
            bbm.box((sx, ry + 0.6 + Hh / 2, -1.6), (0.08, 1.2 + Hh, 0.08), P['grey'], M=M, rot=(0.5, 0, 0))
        used += 1
    add_scenery(bbm.to_object('billboards', collection=C_SCENERY))

# ============================================================== terrain + references
def build_terrain():
    import bmesh as _bm
    bm = _bm.new()
    _bm.ops.create_grid(bm, x_segments=128, y_segments=128, size=EXTENT)
    me = bpy.data.meshes.new('terrainMesh'); bm.to_mesh(me); bm.free()
    me.materials.append(mat('terrain', hexrgba('#ffffff')))
    ob = bpy.data.objects.new('terrain', me); C_TERRAIN.objects.link(ob)
    return ob

def build_refs():
    x, y, z = SPAWN
    r = ref('respawnLanding', (x, y, z), roty=math.pi * 0.75, collection=C_RESPAWN)
    ref('respawnHero', (HERO['x0'] - 1.0, 0.6, HERO['z0'] - 2.0), collection=C_RESPAWN)
    ref('respawnPark', (PARK['x0'] + 3, 0.6, PARK['z0'] + 3), collection=C_RESPAWN)
    ref('respawnGround', ((VACANT['x0'] + VACANT['x1']) / 2, 0.6, VACANT['z1'] - 3), collection=C_RESPAWN)
    for zc, w, nm in MAINS:
        for xc, w2, nm2 in CROSSES:
            ref('respawn' + (nm + nm2).replace(' ', ''), (xc + w2 / 2 + 1.2, 0.6, zc + w / 2 + 1.2), collection=C_RESPAWN)
    # areas: 'home' holds the interactive references used by the HomeArea class
    home = bpy.data.objects.new('home', None); C_AREAS.objects.link(home); home.location = bv(0, 0, 0)
    ref('refAutoStandInteractivePoint', (AUTO_STAND[0] + 1.5, 1.2, AUTO_STAND[1] + 1.0), collection=C_AREAS, parent=home)
    ref('refAutoParking', (AUTO_STAND[0] + 2.4, 0.9, AUTO_STAND[1] + 3.0), roty=-math.pi / 2, collection=C_AREAS, parent=home)
    ref('refHeroInteractivePoint', (HERO['x0'] + 1.2, 1.2, HERO['z0'] - 1.0), collection=C_AREAS, parent=home)
    ref('refZoneBounding', (0, 0, 0), scale=(30, 30, 30), collection=C_AREAS, parent=home)
    return home

# ============================================================== run
build_streets()
build_blocks()
hero = build_hero()
build_furniture()
trees = build_trees()
build_park()
build_vacant()
build_props()
build_junction_life()
lo = lit_windows.to_object('windowsLit', collection=C_SCENERY); scenery_objects.append(lo)
terrain = build_terrain()
home = build_refs()

out = lambda p: os.path.join(STATIC, p)
export(out('scenery/scenery.glb'), scenery_objects)
export(out('terrain/terrain.glb'), [terrain], extras=False)
export(out('respawns/respawnsReferences.glb'), list(C_RESPAWN.objects))
export(out('oakTrees/oakTreesReferences.glb'), list(C_RAIN.objects))
export(out('cherryTrees/cherryTreesReferences.glb'), list(C_TABE.objects))
export(out('bushes/bushesReferences.glb'), list(C_BUSH.objects))
export(out('flowers/flowersReferences.glb'), list(C_FLOW.objects))
export(out('areas/areas.glb'), [home])
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, 'world-of-somnath.blend'))
json.dump({'trees': [list(t) for t in trees]}, open(os.path.join(HERE, 'atlas', 'world.json'), 'w'))
print('BUILT', building_count[0], 'buildings,', len(scenery_objects), 'scenery objects,', len(trees), 'trees')
