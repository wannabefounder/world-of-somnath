"""The player's vehicle: a Bengaluru auto rickshaw, built to the engine's vehicle contract.

Contract (see sources/Game/World/VisualVehicle.js):
  chassis            group, forward = +x, the physics body sits at the chassis origin
    bodyPainted      mesh whose material is swapped for the paint choice (green by default)
    blinkerLeft/Right, stopLights, backLights   emissive meshes toggled by the engine
  wheelContainer     cloned four times by the engine
    wheelCylinder    spins
      wheel          tyre
      wheelPainted   hub, painted like the body
    wheelSuspension  scaled on y by the engine
Physics: wheels at x ±0.9, z ±0.75, radius 0.4. Run: bpyenv/bin/python blender/build_auto.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import reset, MeshBuilder, P, export, STATIC, ROOT, mat, hexrgba
import bpy

reset()
col = bpy.context.scene.collection
mat('redGradient', hexrgba('#1f8a4c'))                     # engine swaps this for the paint choice
mat('emissiveOrangeRadialGradient', hexrgba('#ffb020'))    # engine emissive material, matched by name

CH_Y = 0.907
chassis = bpy.data.objects.new('chassis', None); col.objects.link(chassis)
from lib import bv
chassis.location = bv(0, CH_Y, 0)

def part(name, build):
    mb = MeshBuilder(); build(mb)
    ob = mb.to_object(name, (0, 0, 0), col)
    ob.parent = chassis
    ob.location = bv(0, 0, 0)
    return ob

Y0 = -0.45     # floor pan bottom, chassis-local (world ~0.46)
G, Yel, Blk, Dk, Gl, Cr, Gry, Conc = P['autoGreen'], P['autoYellow'], P['black'], P['dark'], P['glass'], P['cream'], P['grey'], P['concrete']

# ---------- painted body (green): tub, nose cowl, front fenders, rear shell ----------
def body(mb):
    m = 'redGradient'
    mb.box((0.05, Y0 + 0.2, 0), (2.1, 0.4, 1.26), G, mat=m)                      # floor tub
    mb.box((-0.55, Y0 + 0.62, 0), (0.95, 0.45, 1.26), G, mat=m)                  # rear body under the bench
    mb.box((1.18, Y0 + 0.55, 0), (0.42, 0.75, 0.72), G, mat=m, rot=(0, 0, -0.18))  # nose cowl, raked back
    mb.box((1.38, Y0 + 0.2, 0), (0.3, 0.4, 0.82), G, mat=m)                     # front apron
    for z in (-0.75, 0.75):                                                    # fenders over the front pair
        mb.box((0.9, Y0 + 0.52, z), (0.7, 0.07, 0.34), G, mat=m)
        mb.box((-0.9, Y0 + 0.66, z * 0.98), (0.75, 0.07, 0.3), G, mat=m)       # rear mudguards
    mb.box((-1.04, Y0 + 0.86, 0), (0.12, 0.62, 1.22), G, mat=m)                 # back panel
part('bodyPainted', body)

# ---------- everything else (palette) ----------
def common(mb):
    # yellow belt line + yellow canopy trim, the Bengaluru livery
    mb.box((0.05, Y0 + 0.43, 0.635), (2.1, 0.06, 0.02), Yel)
    mb.box((0.05, Y0 + 0.43, -0.635), (2.1, 0.06, 0.02), Yel)
    mb.box((1.18, Y0 + 0.95, 0), (0.36, 0.08, 0.74), Yel, rot=(0, 0, -0.18))
    # canopy: black tarp roof, rear hood, side flaps rolled up
    mb.box((-0.05, Y0 + 1.62, 0), (2.08, 0.1, 1.34), Blk)
    mb.box((-1.07, Y0 + 1.28, 0), (0.1, 0.62, 1.3), Blk)
    mb.box((0.98, Y0 + 1.6, 0), (0.12, 0.12, 1.34), Yel)                        # yellow front edge
    for z in (-0.64, 0.64):
        mb.box((-0.05, Y0 + 1.5, z), (2.0, 0.12, 0.04), Dk)                     # rolled flap
        mb.cyl((0.95, Y0 + 1.1, z), 0.028, 1.02, Gry)                           # front pillars
        mb.cyl((-0.15, Y0 + 1.22, z), 0.024, 0.8, Gry)                          # mid hoop
    # windshield + wiper
    mb.quad([(1.0, Y0 + 0.96, 0.5), (1.0, Y0 + 0.96, -0.5), (0.98, Y0 + 1.56, -0.56), (0.98, Y0 + 1.56, 0.56)], Gl, double=True)
    mb.box((1.01, Y0 + 1.0, 0.1), (0.02, 0.02, 0.4), Blk, rot=(0.4, 0, 0))
    # passenger bench + backrest, driver seat, handlebar, meter
    mb.box((-0.6, Y0 + 0.9, 0), (0.62, 0.14, 1.12), P['crimson'])
    mb.box((-0.93, Y0 + 1.18, 0), (0.12, 0.48, 1.12), P['crimson'])
    mb.box((0.38, Y0 + 0.9, 0), (0.42, 0.12, 0.42), Dk)
    mb.tube([(0.86, Y0 + 1.02, -0.3), (0.82, Y0 + 1.08, -0.18), (0.82, Y0 + 1.08, 0.18), (0.86, Y0 + 1.02, 0.3)], 0.022, Blk)
    mb.box((0.84, Y0 + 1.12, 0.32), (0.08, 0.1, 0.12), Cr)                      # fare meter
    # headlight on the nose, horn, mirrors
    mb.cyl((1.42, Y0 + 0.86, 0), 0.11, 0.08, Cr, axis='x')
    mb.cyl((1.0, Y0 + 1.26, 0.6), 0.012, 0.25, Gry, rot=(0.6, 0, 0))
    mb.box((1.0, Y0 + 1.38, 0.68), (0.03, 0.08, 0.1), Gl)
    mb.cyl((1.0, Y0 + 1.26, -0.6), 0.012, 0.25, Gry, rot=(-0.6, 0, 0))
    mb.box((1.0, Y0 + 1.38, -0.68), (0.03, 0.08, 0.1), Gl)
    # yellow commercial number plates, front and rear
    mb.box((1.54, Y0 + 0.28, 0), (0.02, 0.12, 0.34), Yel)
    mb.box((-1.11, Y0 + 0.62, 0), (0.02, 0.12, 0.34), Yel)
    # spare wheel on the back
    mb.cyl((-1.13, Y0 + 1.05, 0), 0.22, 0.12, Blk, axis='x')
    mb.cyl((-1.19, Y0 + 1.05, 0), 0.1, 0.02, Gry, axis='x')
    # exhaust
    mb.cyl((-0.95, Y0 + 0.08, 0.45), 0.04, 0.4, Gry, axis='x')
part('common', common)

def emissive_box(name, boxes):
    def b(mb):
        for c, s in boxes: mb.box(c, s, Yel, mat='emissiveOrangeRadialGradient')
    return part(name, b)

emissive_box('headlights', [((1.47, Y0 + 0.86, 0), (0.02, 0.16, 0.16))])
emissive_box('backLights', [((-1.11, Y0 + 0.9, 0.5), (0.02, 0.08, 0.12)), ((-1.11, Y0 + 0.9, -0.5), (0.02, 0.08, 0.12))])
emissive_box('stopLights', [((-1.12, Y0 + 0.78, 0.5), (0.02, 0.1, 0.14)), ((-1.12, Y0 + 0.78, -0.5), (0.02, 0.1, 0.14))])
emissive_box('blinkerLeft', [((1.3, Y0 + 0.98, -0.3), (0.08, 0.06, 0.06)), ((-1.1, Y0 + 0.98, -0.58), (0.04, 0.06, 0.06))])
emissive_box('blinkerRight', [((1.3, Y0 + 0.98, 0.3), (0.08, 0.06, 0.06)), ((-1.1, Y0 + 0.98, 0.58), (0.04, 0.06, 0.06))])

# ---------- wheel ----------
wc = bpy.data.objects.new('wheelContainer', None); col.objects.link(wc)
wc.location = bv(0.9, -0.45, -0.75)
cyl = bpy.data.objects.new('wheelCylinder', None); col.objects.link(cyl); cyl.parent = wc

def tyre(mb):
    mb.cyl((0, 0, 0), 0.4, 0.22, Blk, axis='z', seg=20)
    mb.cyl((0, 0, -0.112), 0.27, 0.01, Dk, axis='z', seg=16)
wh = MeshBuilder(); tyre(wh); w = wh.to_object('wheel', (0, 0, 0), col); w.parent = cyl
hub = MeshBuilder(); hub.cyl((0, 0, -0.125), 0.16, 0.03, G, axis='z', seg=12, mat='redGradient')
for k in range(5):
    a = k * 2 * math.pi / 5
    hub.box((math.cos(a) * 0.1, math.sin(a) * 0.1, -0.14), (0.04, 0.04, 0.02), Gry)
h = hub.to_object('wheelPainted', (0, 0, 0), col); h.parent = cyl
sus = MeshBuilder(); sus.box((0, 0.42, 0.05), (0.07, 0.84, 0.07), Gry)
s = sus.to_object('wheelSuspension', (0, 0, 0), col); s.parent = wc

out = os.path.join(STATIC, 'vehicle', 'auto.glb')
export(out, [chassis, wc])
print('AUTO', out, os.path.getsize(out))
