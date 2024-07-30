# %%
from operator import itemgetter
from build123d import *
from ocp_vscode import *

# %%
# PCB Enclosure
# Hole and Box Dimensions
hole_diameter = 5.2  # mm
L, W, H, t = 7 * IN, 7 * IN, 4 * IN, 0.25 * IN

pts = [
    (0, -L / 2 + t),
    (W / 2 - 3 * t, -L / 2 + t),
    (W / 2 - 3 * t, -L / 2 + 3 * t),
    (W / 2 - t, -L / 2 + 3 * t),
    (W / 2 - t, -L / 2 + t),
    (W / 2, -L / 2 + t),
    (W / 2, L / 2 - t),
    (W / 2 - t, L / 2 - t),
    (W / 2 - t, L / 2 - 3 * t),
    (W / 2 - 3 * t, L / 2 - 3 * t),
    (W / 2 - 3 * t, L / 2 - t),
    (0, L / 2 - t),
]

box = Box(L, W, H)
line = Polyline(*pts)
line += mirror(line, about=Plane.YZ)
face = make_face(Plane.XY * line)
ex = extrude(face, amount=H / 2)
ex += extrude(face, amount=H / 2 - t, dir=(0, 0, -1))
box -= ex

# %%
# Mains Power 20, -20
circle1 = Pos(-20, L / 2, -30) * Circle(radius=3.4 / 2).rotate(Axis.X, 90)
circle2 = Pos(-60, L / 2, -30) * Circle(radius=3.4 / 2).rotate(Axis.X, 90)
rect = Rectangle(28, 20).rotate(Axis.X, 90)
rect = chamfer(itemgetter(0, 2)(rect.vertices()), length=5)
rect = fillet(itemgetter(1, 5)(rect.vertices()), radius=4)
rect = Pos(-40, L / 2, -30) * rect
box -= extrude(rect, amount=t, dir=(0, -1, 0))
box -= extrude(circle1, amount=t, dir=(0, -1, 0))
box -= extrude(circle2, amount=t, dir=(0, -1, 0))
mains_power = import_step("703W-00_04/703W-00_04.stp")
# Move part into place (referenced slightly off in Axis.X)
mains_power = Pos(-42.4, L / 2 - 0.5, -30) * mains_power

# %%
# Heat-set Inserts
lid_pts = [
    (-W / 2 + 2 * t, -L / 2 + 2 * t, H / 2 - t / 2),
    (W / 2 - 2 * t, -L / 2 + 2 * t, H / 2 - t / 2),
    (-W / 2 + 2 * t, L / 2 - 2 * t, H / 2 - t / 2),
    (W / 2 - 2 * t, L / 2 - 2 * t, H / 2 - t / 2),
]

side_pts = [
    (-W / 2 + 1.5 * t, -L / 2 + 2 * t, H / 2 - 2 * t),
    (-W / 2 + 1.5 * t, -L / 2 + 2 * t, -H / 2 + 3 * t),
    (-W / 2 + 1.5 * t, L / 2 - 2 * t, H / 2 - 2 * t),
    (-W / 2 + 1.5 * t, L / 2 - 2 * t, -H / 2 + 3 * t),
    (W / 2 - 1.5 * t, -L / 2 + 2 * t, H / 2 - 2 * t),
    (W / 2 - 1.5 * t, -L / 2 + 2 * t, -H / 2 + 3 * t),
    (W / 2 - 1.5 * t, L / 2 - 2 * t, H / 2 - 2 * t),
    (W / 2 - 1.5 * t, L / 2 - 2 * t, -H / 2 + 3 * t),
]

for pos in lid_pts:
    box -= Pos(pos) * Cylinder(radius=hole_diameter / 2, height=t)

for pos in side_pts:
    box -= Pos(pos) * Cylinder(radius=hole_diameter / 2, height=t, rotation=(0, 90, 0))

M4_insert = import_step("M4_Standard.step")

lid_insert_pts = [
    (-W / 2 + 2 * t, -L / 2 + 2 * t, H / 2 - 0.325 * IN),
    (W / 2 - 2 * t, -L / 2 + 2 * t, H / 2 - 0.325 * IN),
    (-W / 2 + 2 * t, L / 2 - 2 * t, H / 2 - 0.325 * IN),
    (W / 2 - 2 * t, L / 2 - 2 * t, H / 2 - 0.325 * IN),
]

LHS_insert_pts = [
    (-W / 2 + 0.575 * IN, -L / 2 + 2 * t, H / 2 - 2 * t),
    (-W / 2 + 0.575 * IN, -L / 2 + 2 * t, -H / 2 + 3 * t),
    (-W / 2 + 0.575 * IN, L / 2 - 2 * t, H / 2 - 2 * t),
    (-W / 2 + 0.575 * IN, L / 2 - 2 * t, -H / 2 + 3 * t),
]

RHS_insert_pts = [
    (W / 2 - 0.575 * IN, -L / 2 + 2 * t, H / 2 - 2 * t),
    (W / 2 - 0.575 * IN, -L / 2 + 2 * t, -H / 2 + 3 * t),
    (W / 2 - 0.575 * IN, L / 2 - 2 * t, H / 2 - 2 * t),
    (W / 2 - 0.575 * IN, L / 2 - 2 * t, -H / 2 + 3 * t),
]

inserts = [Pos(pos) * M4_insert for pos in lid_insert_pts]
M4_insert = M4_insert.rotate(Axis.Y, -90)
inserts += [Pos(pos) * M4_insert for pos in LHS_insert_pts]
M4_insert = M4_insert.rotate(Axis.Y, 180)
inserts += [Pos(pos) * M4_insert for pos in RHS_insert_pts]

# %%
# LID, LHS and RHS
LID = Pos(0, 0, H / 2 + t / 2) * Box(W, L, t)
LHS = Pos(-W / 2 + t / 2, 0, 0 + t / 2) * Box(t, L - 2 * t, H - t)
RHS = Pos(W / 2 - t / 2, 0, 0 + t / 2) * Box(t, L - 2 * t, H - t)

LID_borehole_pts = [
    (-W / 2 + 2 * t, -L / 2 + 2 * t, H / 2),
    (W / 2 - 2 * t, -L / 2 + 2 * t, H / 2),
    (-W / 2 + 2 * t, L / 2 - 2 * t, H / 2),
    (W / 2 - 2 * t, L / 2 - 2 * t, H / 2),
]

LID_boreholes = [
    Pos(pos)
    * CounterBoreHole(
        radius=hole_diameter / 2,
        counter_bore_radius=hole_diameter,
        depth=t,
        counter_bore_depth=t / 2,
    )
    for pos in LID_borehole_pts
]

LID -= LID_boreholes

LHS_screw_pts = [
    (-W / 2, -L / 2 + 2 * t, H / 2 - 2 * t),
    (-W / 2, -L / 2 + 2 * t, -H / 2 + 3 * t),
    (-W / 2, L / 2 - 2 * t, H / 2 - 2 * t),
    (-W / 2, L / 2 - 2 * t, -H / 2 + 3 * t),
]

LHS_screws = [
    extrude(Pos(pos) * Circle(4.3 / 2).rotate(Axis.Y, -90), amount=t, dir=(1, 0, 0))
    for pos in LHS_screw_pts
]
LHS -= LHS_screws

# LHS_boreholes = [
#     Pos(pos)
#     * CounterBoreHole(
#         radius=hole_diameter / 2,
#         counter_bore_radius=hole_diameter,
#         depth=t,
#         counter_bore_depth=t / 2,
#     ).rotate(Axis.Y, -90)
#     for pos in LHS_borehole_pts
# ]

# LHS -= LHS_boreholes

RHS_screw_pts = [
    (W / 2, -L / 2 + 2 * t, H / 2 - 2 * t),
    (W / 2, -L / 2 + 2 * t, -H / 2 + 3 * t),
    (W / 2, L / 2 - 2 * t, H / 2 - 2 * t),
    (W / 2, L / 2 - 2 * t, -H / 2 + 3 * t),
]

RHS_screws = [
    extrude(Pos(pos) * Circle(4.3 / 2).rotate(Axis.Y, 90), amount=t, dir=(-1, 0, 0))
    for pos in RHS_screw_pts
]
RHS -= RHS_screws

# RHS_boreholes = [
#     Pos(pos)
#     * CounterBoreHole(
#         radius=hole_diameter / 2,
#         counter_bore_radius=hole_diameter,
#         depth=t,
#         counter_bore_depth=t / 2,
#     ).rotate(Axis.Y, 90)
#     for pos in RHS_borehole_pts
# ]

# RHS -= RHS_boreholes

# %%
# LHS and RHS Fan Cutouts
LHS_main_circle = Pos(-W / 2, -L / 6, 0) * Circle(34).rotate(Axis.Y, 90)
LHS -= extrude(LHS_main_circle, amount=t, dir=(1, 0, 0))

LHS_screw_pts = [
    (-W / 2, -L / 6 - 61.5 / 2, 61.5 / 2),
    (-W / 2, -L / 6 - 61.5 / 2, -61.5 / 2),
    (-W / 2, -L / 6 + 61.5 / 2, -61.5 / 2),
    (-W / 2, -L / 6 + 61.5 / 2, 61.5 / 2),
]

LHS_fan_screws = [
    extrude(Pos(pos) * Circle(4.3 / 2).rotate(Axis.Y, -90), amount=t, dir=(1, 0, 0))
    for pos in LHS_screw_pts
]
LHS -= LHS_fan_screws

RHS_main_circle = Pos(W / 2, -L / 6, 0) * Circle(34).rotate(Axis.Y, 90)
RHS -= extrude(RHS_main_circle, amount=t, dir=(-1, 0, 0))

RHS_screw_pts = [
    (W / 2, -L / 6 - 61.5 / 2, 61.5 / 2),
    (W / 2, -L / 6 - 61.5 / 2, -61.5 / 2),
    (W / 2, -L / 6 + 61.5 / 2, -61.5 / 2),
    (W / 2, -L / 6 + 61.5 / 2, 61.5 / 2),
]

RHS_fan_screws = [
    extrude(Pos(pos) * Circle(4.3 / 2).rotate(Axis.Y, 90), amount=t, dir=(-1, 0, 0))
    for pos in RHS_screw_pts
]
RHS -= RHS_fan_screws

# Import Fan Model
fan = import_step("70mm-case-fan/70mm-Fan.stp")
LHS_fan = Pos(-W / 2 + t + 15.0 / 2, -L / 6, 0) * fan.rotate(Axis.Y, -90)
RHS_fan = Pos(W / 2 - t - 15.0 / 2, -L / 6, 0) * fan.rotate(Axis.Y, 90)

# %%
# Standoffs
standoff_pts = [
    (57, L / 2 - 2 * t, -H / 2 + 2 * t),
    (-5.621, L / 2 - 2 * t, -H / 2 + 2 * t),
    (-5.621, L / 2 - 2 * t - 116.977, -H / 2 + 2 * t),
    (57, L / 2 - 2 * t - 116.977, -H / 2 + 2 * t),
    (-42, -6 - 4.25 * IN / 2, -H / 2 + 2 * t),
]
standoff = Box(2 * t, 2 * t, 2 * t) - Pos(0, 0, t / 2) * Cylinder(
    radius=3.25 / 2, height=t
)
standoffs = [Pos(pos) * standoff for pos in standoff_pts]

standoff_insert_pts = [
    (57, L / 2 - 2 * t, -H / 2 + 2 * t + 0.55),
    (-5.621, L / 2 - 2 * t, -H / 2 + 2 * t + 0.55),
    (-5.621, L / 2 - 2 * t - 116.977, -H / 2 + 2 * t + 0.55),
    (57, L / 2 - 2 * t - 116.977, -H / 2 + 2 * t + 0.55),
]
M3_insert = import_step("M3_Standard.step")
standoff_inserts = [Pos(pos) * M3_insert for pos in standoff_insert_pts]

# PCBs
pcb = Pos(25.6, 17.6, -H / 2 + 3 * t) * import_step("sstc.step").rotate(Axis.Z, 180)
lil_pcb = Pos(-40, -10, -H / 2 + 19 + 2 * t) * Box(1.8 * IN, 4.25 * IN, 1 * IN)

lil_pcb_pt = (-42, -6 - 4.25 * IN / 2, -H / 2 + 2 * t + 0.55)
lil_pcb_insert = Pos(lil_pcb_pt) * M3_insert

lil_pcb_boxed = Pos(-40, -20 + 4.75 * IN / 2, -H / 2 + 2.5 * t) * Box(
    13 + 1.75 * IN, 1 * IN, 3 * t
)
lil_pcb_boxed -= lil_pcb

# heat sinks
heat_sink = import_step("M47118B011000G/M47118B011000G.stp")
LHS_heat_sink = Pos(-10, -L / 2 + 26, -H / 2 + 10) * heat_sink.rotate(Axis.X, 90)
RHS_heat_sink = Pos(31, -L / 2 + 26, -H / 2 + 10) * heat_sink.rotate(Axis.X, 90)

# fiber optic reciever
fiber_optic_hole = Pos(48.5, L / 2, -H / 2 + 2 * t + 15) * Circle(radius=10 / 2).rotate(
    Axis.X, 90
)
box -= extrude(fiber_optic_hole, amount=t, dir=(0, -1, 0))


## TODO LAST
# Do this after all the holes and cutouts are in place
box = fillet(
    itemgetter(2, 3, 6, 9)(box.edges().filter_by(Axis.Z)),
    radius=5,
)

standoffs = [
    fillet(standoff.edges().filter_by(Axis.Z), radius=6.25) for standoff in standoffs
]

# lil_pcb_boxed = fillet(lil_pcb_boxed.edges(), radius=2)
lil_pcb_boxed = fillet(lil_pcb_boxed.edges().filter_by(Axis.Z), radius=2)

LID = fillet(LID.edges().filter_by(Axis.Z), radius=5)
#  topf = ex19.faces().sort_by(Axis.Z)[-1]
# topf = LID.faces().sort_by(Axis.Z)[-1]
# LID = fillet(LID.edges().filter_by(topf), radius=5)

show(
    box,
    pcb,
    standoffs,
    standoff_inserts,
    lil_pcb,
    lil_pcb_insert,
    lil_pcb_boxed,
    LID,
    LHS,
    RHS,
    LHS_fan,
    RHS_fan,
    mains_power,
    LHS_heat_sink,
    RHS_heat_sink,
    inserts,
    fiber_optic_hole,
)
