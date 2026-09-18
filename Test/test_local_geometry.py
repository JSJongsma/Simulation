#!/usr/bin/env python3
"""
Test met LOCALE geometry config files
"""
import sys
import os
sys.path.append(os.path.abspath('.'))

from Core.Build_Geometry import BuildGeometry
from Core.open_csv import CSVLoader

# Test met LOCALE geometry_10_config.csv
local_config_file = "geometry_10_config.csv"
print(f"Testing with local config: {local_config_file}")
print("="*80)

builder = BuildGeometry(local_config_file)
original_config = builder.read_config()

print(f"Loaded config: {original_config}")
print("="*80)

# Build and run
gas_cell, lightray = builder.build_gas_cell(original_config)
track_memory = builder.run_simulation(lightray=lightray, gas_cell=gas_cell, config=original_config)
print(f"\nRESULT: {len(track_memory)} reflections")

# Compare with saved track memory
track_df = CSVLoader.load_track_memory_from_csv("geometry_10_track_memory.csv")
print(f"SAVED track memory: {len(track_df)} reflections")

print("\n" + "="*80)
print("First few saved reflections:")
for i, row in track_df.head(5).iterrows():
    print(f"  {row['mirror_name']}: ({row['position_x']:.2f}, {row['position_y']:.2f}, {row['position_z']:.2f})")
