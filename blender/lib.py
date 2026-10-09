"""Shared helpers for building World of Somnath assets with Blender (bpy).

Coordinates: everything is authored in *three.js space* (x right, y up, z towards camera)
and converted to Blender (z up) on write: blender = (x, -z, y). The glTF exporter
converts back, so numbers in our scripts match what the engine sees.
"""
import bpy, bmesh, math, json, os
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
STATIC = os.path.join(ROOT, 'static')

# 32 swatches x 4px = palette.png (128x4). 0-23 kept from the original engine palette, 24-31 are ours.
PALETTE = [
    '#7c7691', '#ebd1a3', '#574e37', '#3dbbe7', '#c8c2c1', '#4a413c', '#575a5e', '#eec3af',
    '#e4a90c', '#91ad78', '#e49a78', '#988165', '#abae2b', '#a49876', '#b36d45', '#e56202',
    '#ec3f1c', '#fde6e1', '#f8a658', '#c30e3a', '#c366ef', '#ed719f', '#1e0603', '#fff2e8',
    '#a9dcc5', '#a7c8ec', '#f3e18f', '#cdb9e9', '#1f8a4c', '#f5c400', '#2f3a48', '#b9b2a6',
]
P = {  # names for readability
    'lav': 0, 'sand': 1, 'dkbrown': 2, 'cyan': 3, 'ltgrey': 4, 'dark': 5, 'grey': 6, 'peach': 7,
    'yellow': 8, 'sage': 9, 'salmon': 10, 'khaki': 11, 'olive': 12, 'taupe': 13, 'terracotta': 14, 'orange': 15,
    'red': 16, 'palepink': 17, 'apricot': 18, 'crimson': 19, 'purple': 20, 'pink': 21, 'black': 22, 'cream': 23,
    'mint': 24, 'sky': 25, 'lemon': 26, 'lilac': 27, 'autoGreen': 28, 'autoYellow': 29, 'glass': 30, 'concrete': 31,
}

def write_palette():
    from PIL import Image  # noqa: only used when run with system python
    raise RuntimeError('use write_palette_png() from system python')

def swatch_uv(idx):
    return ((idx * 4 + 2) / 128.0, 0.5)

def bv(x, y, z):
    return Vector((x, -z, y))

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

_mats = {}
def mat(name, color=(1, 1, 1, 1), image=None, emissive=None):
    if name in _mats:
        return _mats[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    if image:
        img = bpy.data.images.load(image)
        tex = m.node_tree.nodes.new('ShaderNodeTexImage')
        tex.image = img
        tex.interpolation = 'Linear'
        m.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    else:
        bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = 0.8
    _mats[name] = m
    return m

def hexrgba(h):
    h = h.lstrip('#')
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, 1)

# ------------------------------------------------------------------ mesh builder
class MeshBuilder:
    """Accumulates boxes / cylinders / quads into one bmesh, UVs pointing at palette swatches
    or atlas rects, per-face material index (slot list)."""
    def __init__(self):
        self.bm = bmesh.new()
        self.uv = self.bm.loops.layers.uv.new('UVMap')
        self.slots = []  # material names

    def slot(self, name):
        if name not in self.slots:
            self.slots.append(name)
        return self.slots.index(name)

    def _xf(self, p, M):
        # p in three local coords -> world three coords via M (4x4, three space) -> blender
        v = M @ Vector((p[0], p[1], p[2], 1.0)) if M is not None else Vector((p[0], p[1], p[2], 1.0))
        return bv(v[0], v[1], v[2])

    def box(self, c, s, sw, M=None, rot=None, mat='palette', uvrect=None, uvface=None):
        """c=center (three), s=size, sw=swatch index, rot=(rx,ry,rz) local euler (three, radians)."""
        cx, cy, cz = c; sx, sy, sz = s
        hx, hy, hz = sx / 2, sy / 2, sz / 2
        corners = [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
                   (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)]
        R = Matrix.Identity(4)
        if rot:
            R = (Matrix.Rotation(rot[1], 4, 'Y') @ Matrix.Rotation(rot[0], 4, 'X') @ Matrix.Rotation(rot[2], 4, 'Z'))
        L = Matrix.Translation((cx, cy, cz)) @ R
        T = (M @ L) if M is not None else L
        vs = [self.bm.verts.new(self._xf(p, T)) for p in corners]
        # faces (three local): -z,+z,-x,+x,-y,+y ; winding outward in three space -> after axis swap still valid
        faces = {'nz': (0, 3, 2, 1), 'pz': (4, 5, 6, 7), 'nx': (0, 4, 7, 3), 'px': (1, 2, 6, 5), 'ny': (0, 1, 5, 4), 'py': (3, 7, 6, 2)}
        mi = self.slot(mat)
        made = {}
        for key, idx in faces.items():
            try:
                f = self.bm.faces.new([vs[i] for i in idx])
            except ValueError:
                continue
            f.material_index = mi
            made[key] = f
            if uvrect and key == uvface:
                u0, v0, u1, v1 = uvrect
                # local face corner order -> map to rect
                quad = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
                for loop, q in zip(f.loops, self._face_uv_order(key, quad)):
                    loop[self.uv].uv = q
            else:
                u = swatch_uv(sw)
                for loop in f.loops:
                    loop[self.uv].uv = u
        return made

    @staticmethod
    def _face_uv_order(key, quad):
        u0v0, u1v0, u1v1, u0v1 = quad
        # vertex orders above, viewed from outside:
        if key == 'pz':   # 4(-x,-y) 5(+x,-y) 6(+x,+y) 7(-x,+y)
            return [u0v0, u1v0, u1v1, u0v1]
        if key == 'nz':   # 0(-x,-y) 3(-x,+y) 2(+x,+y) 1(+x,-y)  viewed from -z: +x is left
            return [u1v0, u1v1, u0v1, u0v0]
        if key == 'px':   # 1(z-) 2(y+,z-) 6(y+,z+) 5(z+) viewed from +x: +z is left... -z right
            return [u1v0, u1v1, u0v1, u0v0]
        if key == 'nx':   # 0(z-) 4(z+) 7(y+,z+) 3(y+,z-) viewed from -x: -z left, +z right
            return [u0v0, u1v0, u1v1, u0v1]
        return quad

    def cyl(self, c, r, h, sw, M=None, seg=16, r2=None, mat='palette', axis='y', rot=None):
        r2 = r if r2 is None else r2
        cx, cy, cz = c
        R = Matrix.Identity(4)
        if axis == 'x': R = Matrix.Rotation(math.pi / 2, 4, 'Z')
        if axis == 'z': R = Matrix.Rotation(math.pi / 2, 4, 'X')
        if rot: R = Matrix.Rotation(rot[1], 4, 'Y') @ Matrix.Rotation(rot[0], 4, 'X') @ Matrix.Rotation(rot[2], 4, 'Z') @ R
        T = Matrix.Translation((cx, cy, cz)) @ R
        if M is not None: T = M @ T
        bot, top = [], []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            bot.append(self.bm.verts.new(self._xf((math.cos(a) * r, -h / 2, math.sin(a) * r), T)))
            top.append(self.bm.verts.new(self._xf((math.cos(a) * r2, h / 2, math.sin(a) * r2), T)))
        mi = self.slot(mat); u = swatch_uv(sw)
        fl = []
        for i in range(seg):
            j = (i + 1) % seg
            fl.append(self.bm.faces.new([bot[i], top[i], top[j], bot[j]]))
        fl.append(self.bm.faces.new(bot))
        fl.append(self.bm.faces.new(list(reversed(top))))
        for f in fl:
            f.material_index = mi
            for loop in f.loops: loop[self.uv].uv = u

    def quad(self, corners3, sw=None, uvrect=None, mat='palette', M=None, double=False):
        """corners3: 4 points (three coords, counter-clockwise seen from the front)."""
        vs = [self.bm.verts.new(self._xf(p, M)) for p in corners3]
        f = self.bm.faces.new(vs)
        f.material_index = self.slot(mat)
        if uvrect:
            u0, v0, u1, v1 = uvrect
            for loop, q in zip(f.loops, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]): loop[self.uv].uv = q
        else:
            for loop in f.loops: loop[self.uv].uv = swatch_uv(sw)
        if double:
            vs2 = [self.bm.verts.new(self._xf(p, M)) for p in reversed(corners3)]
            f2 = self.bm.faces.new(vs2); f2.material_index = f.material_index
            if uvrect:
                u0, v0, u1, v1 = uvrect
                for loop, q in zip(f2.loops, [(u0, v1), (u1, v1), (u1, v0), (u0, v0)][::-1]): loop[self.uv].uv = q
            else:
                for loop in f2.loops: loop[self.uv].uv = swatch_uv(sw)

    def tube(self, pts, r, sw, seg=5, mat='palette'):
        """Polyline tube through three-space points (cables)."""
        rings = []
        for i, p in enumerate(pts):
            a = Vector(pts[max(i - 1, 0)]); b = Vector(pts[min(i + 1, len(pts) - 1)])
            t = (b - a).normalized()
            n = t.cross(Vector((0, 1, 0)))
            if n.length < 1e-4: n = Vector((1, 0, 0))
            n.normalize(); bn = t.cross(n).normalized()
            ring = []
            for k in range(seg):
                ang = 2 * math.pi * k / seg
                q = Vector(p) + (n * math.cos(ang) + bn * math.sin(ang)) * r
                ring.append(self.bm.verts.new(bv(q.x, q.y, q.z)))
            rings.append(ring)
        mi = self.slot(mat); u = swatch_uv(sw)
        for i in range(len(rings) - 1):
            for k in range(seg):
                j = (k + 1) % seg
                f = self.bm.faces.new([rings[i][k], rings[i][j], rings[i + 1][j], rings[i + 1][k]])
                f.material_index = mi
                for loop in f.loops: loop[self.uv].uv = u

    def empty(self):
        return len(self.bm.faces) == 0

    def to_object(self, name, origin=(0, 0, 0), collection=None):
        """Create an object; vertices are shifted so the object origin sits at `origin` (three coords)."""
        o = bv(*origin)
        for v in self.bm.verts: v.co -= o
        me = bpy.data.meshes.new(name)
        self.bm.to_mesh(me); self.bm.free()
        for n in self.slots:
            if n == 'palette': me.materials.append(mat('palette', hexrgba('#ffffff')))
            else: me.materials.append(_mats.get(n) or mat(n))
        ob = bpy.data.objects.new(name, me)
        ob.location = o
        (collection or bpy.context.scene.collection).objects.link(ob)
        return ob

def collider(parent, kind, center, size, name=None, rot=None):
    """Unit primitive scaled to size, parented, in parent-local three coords.
    kind: cuboid | tube (size=(diameter, height, diameter)) | ball (size=(d,d,d))."""
    if kind == 'cuboid':
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    elif kind == 'tube':
        bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.5, radius2=0.5, depth=1.0)
    else:
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=0.5)
    me = bpy.data.meshes.new((name or kind) + 'Mesh'); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name or kind, me)
    for c in parent.users_collection: c.objects.link(ob)
    ob.parent = parent
    ob.location = bv(*center)
    # three size (x,y,z) -> blender scale (x, z, y)
    ob.scale = (size[0], size[2], size[1])
    if rot is not None: ob.rotation_euler = (0, 0, rot)
    return ob

def ref(name, pos, scale=(1, 1, 1), roty=0.0, collection=None, parent=None, mesh=False):
    """A reference marker (empty or tiny mesh) at three-space pos."""
    if mesh:
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=0.2)
        me = bpy.data.meshes.new(name + 'Mesh'); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(name, me)
    else:
        ob = bpy.data.objects.new(name, None)
    (collection or bpy.context.scene.collection).objects.link(ob)
    if parent: ob.parent = parent
    ob.location = bv(*pos)
    ob.scale = (scale[0], scale[2], scale[1])
    ob.rotation_euler = (0, 0, roty)
    return ob

def export(path, objects, extras=True):
    bpy.ops.object.select_all(action='DESELECT')
    def sel(o):
        o.select_set(True)
        for c in o.children: sel(c)
    for o in objects: sel(o)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_extras=extras,
                              export_yup=True, export_apply=False, export_materials='EXPORT',
                              export_image_format='AUTO', export_texcoords=True, export_normals=True,
                              export_cameras=False, export_lights=False, export_animations=False)

def xform(x, z, roty, y=0.0):
    """three-space placement matrix: rotate about +Y by roty, then translate."""
    c, s = math.cos(roty), math.sin(roty)
    return Matrix(((c, 0, s, x), (0, 1, 0, y), (-s, 0, c, z), (0, 0, 0, 1)))
