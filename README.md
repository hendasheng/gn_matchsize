# GN_MatchSize

[中文](README_CN.md)

![](https://picgo-mdeia.oss-cn-beijing.aliyuncs.com/picgo/github_media/2026-02-26_17-55-11_trimmed_compressed-ezgif.com-optimize.gif)

GN_MatchSize is a size matching and alignment tool built with Geometry Nodes, inspired by Houdini’s Match Size node.

When introduced into a Geometry Nodes setup, GN_MatchSize can bring multiple geometry objects to a unified scale and reset their position to the origin. It is particularly useful when handling geometry from different sources.

This is a general‑purpose base node designed for procedural modeling, asset normalization, and batch processing.

## Installation
> **Blender 4.2 +**

1. Download [gn_matchsize.zip](https://github.com/hendasheng/gn_matchsize/releases)
2. Open Blender, go to `Edit` → `Preferences` → `Get Extensions`
3. Click the arrow in the top right, select **Install from Disk...**
4. Select the downloaded `gn_matchsize.zip` to install

After installation:
- Open **Geometry Nodes** Editor
- Press `Shift + A`
- Select `Group` → `GN_MatchSize` (or search for `Match Size`)
- The node will appear in your current file

![](https://picgo-mdeia.oss-cn-beijing.aliyuncs.com/picgo/github_media/20260226182011.png)

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
