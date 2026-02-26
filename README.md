# GN_MatchSize

[中文](README_CN.md)

Houdini-style Match Size for Blender Geometry Nodes

> **Blender 4.5+**

**GN_MatchSize** is a size matching and alignment tool based on Geometry Nodes, inspired by Houdini's Match Size SOP.

It can:
- Automatically calculate geometry Bounding Box
- Support Uniform Scale (match longest axis)
- Support Axis Alignment (Min / Center / Max)
- Support both Instances and Real Geometry
- Pure node implementation, no script dependencies

This is a general-purpose utility node designed for procedural modeling, asset normalization, and batch processing.

## Features

### 1. Automatic Size Calculation
Internally calculates:
`Size = Max - Min`
Separately for X / Y / Z axes.
Useful for:
- Unifying asset scale
- Normalizing imported models
- Automatically adapting geometry from different sources

### 2. Uniform Scale
Scaling logic:
`scale = target / longest_axis`
Ensures the longest edge matches the target size while maintaining the aspect ratio.

### 3. Axis Alignment (Align)
Each axis supports:
- `-1` = Min
- `0` = Center
- `1` = Max

Calculates offset mathematically:
`offset = -(center + align * size * 0.5)`

No branch nodes, pure math control.
Supports:
- Center alignment
- Bottom alignment (grounding)
- Top alignment
- Mixed alignment (e.g., X Min / Y Center / Z Max)

## Use Cases
- Asset Standardization
- Procedural Arrays
- Automatic Size Normalization
- Geometry Nodes Pipeline
- Houdini-like Workflow

## Technical Implementation
- Pure Geometry Nodes
- No Python dependencies
- Embeddable in any node system
- Can be re-wrapped as an asset tool
- Supports Instance Realize or Direct Instance mode
