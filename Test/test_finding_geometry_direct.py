#!/usr/bin/env python3
"""
Test FindingGeometry with explicit parameters
"""
import sys
import os
sys.path.append(os.path.abspath('.'))

from Core.FindingGeometry import FindingGeometry
from Core.open_csv import CSVLoader

# Load config
config_file_path = "geometry_10_config.csv"
config_dict = {
    "m2_x": 44.23730222145917,
    "m2_y": 6.1193569029538235,
    "m3_x": 39.767188934158646,
    "m3_y": 31.022062868167268,
    "m2_phi": 1.7241082612380456,
    "m3_theta": 1.4127122887888444,
    "ray_pitch": -0.43186972670298457,
    "ray_yaw": 0.0,
}

print("="*80)
print("Testing FindingGeometry directly")
print("="*80)

# Create with the SAME parameters as Build_Geometry defaults
finder = FindingGeometry(
    target_reflections=10,
    hole_diameter=0.4,  # This becomes 0.2 radius
    entry_hole_diameter=0.4  # This becomes 0.2 radius
)

print(f"FindingGeometry configured with:")
print(f"  hole_diameter: {finder.hole_diameter} cm -> radius: {finder.hole_radius} cm")
print(f"  entry_hole_diameter: {finder.entry_hole_diameter} cm -> radius: {finder.entry_hole_radius} cm")

cell, pos_m2, ray_dir = finder._setup_cell(config_dict)

if cell is None:
    print("ERROR: cell is None - minimum distance check failed")
else:
    from Physics.lightray import Lightray
    lightray = Lightray(finder.entry_hole_world + (ray_dir * 0.01), ray_dir)
    track_mem = cell.run_simulation(initial_ray=lightray, max_reflections=33)
    print(f"\nRESULT: {len(track_mem)} reflections")
    
    for i, state in enumerate(track_mem.memory):
        print(f"  {i+1}. {state.mirror_name}: u={state.u:.3f}, v={state.v:.3f}")

# Now load what the SAVED track memory shows
print("\n" + "="*80)
print("SAVED track memory for reference:")
print("="*80)
saved_track = CSVLoader.load_track_memory_from_csv("geometry_10_track_memory.csv")
print(f"Total reflections in file: {len(saved_track)}")
for i, state in enumerate(saved_track.memory):
    print(f"  {i+1}. {state.mirror_name}: u={state.u:.3f}, v={state.v:.3f}")
