#!/usr/bin/env python3
"""
Vergelijkt Build_Geometry en FindingGeometry side-by-side
"""
import sys
import os
sys.path.append(os.path.abspath('.'))

from Core.Build_Geometry import BuildGeometry
from Core.FindingGeometry import FindingGeometry
from Core.open_csv import CSVLoader
from Results.Config import Config

# Laad een config
config_file_path = "OptimizedGeometries/10Reflections/best_geometry_10_config.csv"
builder = BuildGeometry(config_file_path)
original_config = builder.read_config()

print("="*80)
print("ORIGINELE CONFIG:")
print(original_config)
print("="*80)

# Test 1: Build_Geometry
print("\n" + "="*80)
print("TEST 1: BUILD_GEOMETRY")
print("="*80)
try:
    gas_cell_build, lightray_build = builder.build_gas_cell(original_config)
    track_build = builder.run_simulation(lightray=lightray_build, gas_cell=gas_cell_build, config=original_config)
    print(f"\nRESULT: {len(track_build)} reflections")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 2: FindingGeometry
print("\n" + "="*80)
print("TEST 2: FINDINGGEOMETRY")
print("="*80)
try:
    finder = FindingGeometry(target_reflections=10)
    
    # Convert Config object to dict for FindingGeometry
    config_dict = {
        "m2_x": original_config.m2_x,
        "m2_y": original_config.m2_y,
        "m3_x": original_config.m3_x,
        "m3_y": original_config.m3_y,
        "m2_phi": original_config.m2_phi,
        "m3_theta": original_config.m3_theta,
        "ray_pitch": original_config.ray_pitch,
        "ray_yaw": original_config.ray_yaw,
    }
    
    cell_finding, pos_m2, ray_dir = finder._setup_cell(config_dict)
    if cell_finding is None:
        print("ERROR: cell_finding is None")
    else:
        from Physics.lightray import Lightray
        lightray_finding = Lightray(finder.entry_hole_world + (ray_dir * 0.01), ray_dir)
        track_finding = cell_finding.run_simulation(initial_ray=lightray_finding, max_reflections=33)
        print(f"\nRESULT: {len(track_finding)} reflections")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("VERGELIJKING:")
print(f"  Build_Geometry: {len(track_build)} reflections")
print(f"  FindingGeometry: {len(track_finding)} reflections")
print("="*80)
