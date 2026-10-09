"""World of Somnath — locality layout (three.js space, metres).
A fictional Bengaluru neighbourhood laid out on the classic Main/Cross grid.
Shared by the Blender builder and the terrain-texture generator."""

EXTENT = 96.0           # world is 192 x 192 m (engine terrain size)
FP = 2.2                # footpath width
FPH = 0.16              # footpath height
PLOT_DEPTH = 12.2       # 30x40 ft site = 9.1 x 12.2 m

# Roads running along X (Mains) : (z centre, width, name)
MAINS = [(-56.0, 8.0, '7th Main'), (0.0, 12.0, '8th Main'), (56.0, 8.0, '9th Main')]
# Roads running along Z (Crosses): (x centre, width, name)
CROSSES = [(-56.0, 8.0, '3rd Cross'), (0.0, 9.0, '4th Cross'), (56.0, 8.0, '5th Cross')]

def intervals(roads):
    """Free intervals (between road+footpath bands) along one axis."""
    edges = [-EXTENT]
    out = []
    for c, w, _ in roads:
        a = c - w / 2 - FP
        out.append((edges[-1], a))
        edges.append(c + w / 2 + FP)
    out.append((edges[-1], EXTENT))
    return out

X_BANDS = intervals(CROSSES)   # x ranges of blocks
Z_BANDS = intervals(MAINS)     # z ranges of blocks

def blocks():
    out = []
    for zi, (z0, z1) in enumerate(Z_BANDS):
        for xi, (x0, x1) in enumerate(X_BANDS):
            out.append({'id': f'b{xi}{zi}', 'xi': xi, 'zi': zi, 'x0': x0, 'x1': x1, 'z0': z0, 'z1': z1})
    return out

# The junction of 8th Main x 4th Cross is the heart of the world (origin).
HERO = {'x0': 0 + 4.5 + FP + 0.2, 'z0': 0 + 6.0 + FP + 0.2, 'w': 15.0, 'd': 15.0}   # NE corner plot
PARK = {'x0': -30.0, 'x1': -(4.5 + FP + 0.2), 'z0': 6.0 + FP + 0.2, 'z1': 30.0}     # NW corner
VACANT = {'x0': -26.0, 'x1': -(4.5 + FP + 0.2), 'z0': -28.0, 'z1': -(6.0 + FP + 0.2)}  # SW corner: gully cricket ground
AUTO_STAND = (-(4.5 + FP) - 0.2, 9.5)        # on the NW footpath edge, beside the park
SPAWN = (-6.0, 0.6, 14.0)                     # companion spawns near the auto stand, facing the junction
