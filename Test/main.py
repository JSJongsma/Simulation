#main.py
# here we will test the setups found in the simulation, and see if we can reproduce the results.
# the importance lies in the rounding of the nnumbers, since we have to compare to the experiment.
# We do not have the infinite precision of the simulation, thus we must round the numbers to a certain decimal'.

import math
from Math.vector import Vector
from Math.matrix import Matrix
from Math.grid import TwoGrid
from Geometry.mirror import Mirror
from Geometry.hole import Hole
from Geometry.cell_geometry import CellGeometry
from Physics.lightray import Lightray
from Physics.Physics import PhysicsUtils
from Core.gas_cell import GasCell
from Results.hitmap import Hitmap
from Results.trajectory_result import TrajectoryResult, TrajectoryResultsFromCSV
from Results.Config import Config
from Results.track_memory import TrackMemory
from Core.open_csv import CSVLoader

csv_config = "C:/Users/Jaïr/OneDrive/Lectoraat/Spektrik/GasCell/Simulation/GasCellOptimalizations/best_geometry_28_config.csv"
csv_memory = "C:/Users/Jaïr/OneDrive/Lectoraat/Spektrik/GasCell/Simulation/GasCellOptimalizations/best_geometry_28_track_memory.csv"

# load configurations 
config = CSVLoader.load_config_from_csv(csv_config)
print(config)

# making gas cell object
gas_cell = GasCell(cell_geometry=CellGeometry(name="Verificationcell", cell_dimensions=(50, 40, 30)))

pos_m1 = Vector(0, 20, 25)
pos_m2 = Vector(config.m2_x, config.m2_y, 25)
pos_m3 = Vector(config.m3_x, config.m3_y, 25)

# M1 normaal ligt naar +x, want de eerste spiegel kijkt vanaf de linkerkant naar rechts.
n1_normal = Vector(1, 0, 0)

# Bereken de ideale baseline normals met de bestaande reflectie-setup:
# - M2 moet een straal vanaf M1 naar M3 sturen
# - M3 moet een straal vanaf M2 naar M1 sturen
entry_hole_world = pos_m1 + Vector(0, -1.2, 0)
n2_base = PhysicsUtils.calculate_ideal_normal(entry_hole_world, pos_m2, pos_m3)
n3_base = PhysicsUtils.calculate_ideal_normal(pos_m2, pos_m3, entry_hole_world)

rot_m2 = Matrix.rotation_z(math.radians(config.m2_phi))
rot_m3 = Matrix.rotation_z(math.radians(config.m3_theta))

normal_m2 = (rot_m2 @ n2_base)
normal_m2.z = 0.0
normal_m2 = normal_m2.normalize()

normal_m3 = (rot_m3 @ n3_base)
normal_m3.z = 0.0
normal_m3 = normal_m3.normalize()

# Instellen van de spiegels
gas_cell.cell_geometry.add_mirror(Mirror(name="m1", origin=pos_m1,
                                         normal=n1_normal,
                                         grid=TwoGrid(5.08, 5.08, 0.1),
                                         reflection_coef=0.98))

gas_cell.cell_geometry.add_mirror(Mirror(name="m2", origin=pos_m2,
                                         normal=normal_m2,
                                         grid=TwoGrid(5.08, 5.08, 0.1),
                                         reflection_coef=0.98,
                                         hole=Hole(name="ExitHole", origin=Vector(1.2, 0.0, 0.0), radius=0.2, grid=None)))

gas_cell.cell_geometry.add_mirror(Mirror(name="m3", origin=pos_m3,
                                         normal=normal_m3,
                                         grid=TwoGrid(5.08, 5.08, 0.1),
                                         reflection_coef=0.98))

