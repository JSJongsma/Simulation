#!/usr/bin/env python3
"""
Trace what happens to the ray after first reflection
"""
import sys
import os
sys.path.append(os.path.abspath('.'))

from Core.Build_Geometry import BuildGeometry
from Physics.lightray import Lightray
from Core.open_csv import CSVLoader

config_file_path = "geometry_10_config.csv"
builder = BuildGeometry(config_file_path)
config = builder.read_config()

# Build cell
gas_cell, lightray = builder.build_gas_cell(config)

print("="*80)
print("INITIAL RAY:")
print(f"  Origin: {lightray.origin}")
print(f"  Direction: {lightray.direction}")
print("="*80)

# Get mirrors
mirrors = gas_cell.propagation.cell_geometry.get_mirrors()
for m in mirrors:
    print(f"\n{m.name}:")
    print(f"  Position: {m.origin}")
    print(f"  Normal: {m.normal}")
    if m.hole:
        print(f"  Hole: radius={m.hole.radius}, pos={m.hole.origin}")

print("\n" + "="*80)
print("RUNNING SIMULATION (max 33 reflections):")
print("="*80)

track_mem = gas_cell.run_simulation(initial_ray=lightray, max_reflections=33)
print(f"\nTotal reflections: {len(track_mem)}")

for i, state in enumerate(track_mem.memory):
    print(f"\nReflection {i+1}:")
    print(f"  Mirror: {state.mirror_name}")
    print(f"  Position: ({state.position.x:.3f}, {state.position.y:.3f}, {state.position.z:.3f})")
    print(f"  Local (u,v): ({state.u:.3f}, {state.v:.3f})")
    if state.mirror_name == "M2" and state.u >= 1.0:  # Near exit hole
        print(f"  >>> NEAR EXIT HOLE!")

# Load saved track memory for comparison
print("\n" + "="*80)
print("SAVED TRACK MEMORY (from geometry_10_track_memory.csv):")
print("="*80)
saved_track = CSVLoader.load_track_memory_from_csv("geometry_10_track_memory.csv")
print(f"Total reflections: {len(saved_track)}")
for i, state in enumerate(saved_track.memory):
    print(f"  {i+1}. {state.mirror_name}: u={state.u:.3f}, v={state.v:.3f}")
