# GN_MatchSize

[中文](README.md)

![GN_MatchSize](https://picgo-mdeia.oss-cn-beijing.aliyuncs.com/picgo/github_media/GN_MatchSize_Github@1x.png)

GN_MatchSize is a Geometry Nodes group for Blender that matches sizes and aligns
geometry, inspired by Houdini's Match Size node.

It brings geometry from any source and any scale to one target size, then aligns
it to the origin per axis (X / Y / Z) — entirely in geometry nodes, no Python
dependency.

- Version **0.1.0**, requires **Blender 5.0+**
- Pure Geometry Nodes; drop it into any node tree or wrap it in your own asset

## Installation

### As a Blender extension (recommended)

1. Download `gn_matchsize-0.1.0.zip` from
   [Releases](https://github.com/hendasheng/gn_matchsize/releases)
2. In Blender: `Edit` → `Preferences` → `Add-ons`
3. Top-right arrow → **Install from Disk**, pick the zip
4. Enable **GN MatchSize**

### Manually

Copy this repository into Blender's `scripts/addons/` (or an extension
directory) and enable **GN MatchSize**.

Then, in the Geometry Node editor: `Shift + A` → `Group` → `GN_MatchSize`
(searching `MatchSize` works too).

> The add-on injects the node group into the current .blend on enable and after
> every file load, so existing projects pick it up as well.

## Inputs

| Input | Type | Description |
| --- | --- | --- |
| Geometry | Geometry | Mesh / curve / point cloud / instances |
| 缩放？ (Scale?) | Boolean | Off: align only, keep the size. On: align, then scale uniformly to `Scale` |
| Scale | Float (≥ 1) | Target size of the **longest axis**; uniform scale = `Scale / longest_axis` |
| Align → X Axis / Y Axis / Z Axis | Float (−1 … 1) | Per-axis alignment: `0` centre, `1` positive side, `−1` negative side |

> The boolean socket is labelled `缩放？` in 0.1.0 — it is the scale toggle.

## How alignment works

For every axis the group:

1. reads `Min` / `Max` from `Bounding Box`, giving `Size = Max − Min` and
   `Center = (Min + Max) / 2`
2. offsets the geometry by `offset = −Center + Align × Size × 0.5`

So **Align answers "which face of the bounding box touches the origin"**:

| Align | Result |
| --- | --- |
| `0` | Bounding-box centre sits on the origin |
| `1` | Min face on the origin, geometry extends to the positive side (on Z: sits on the ground) |
| `−1` | Max face on the origin, geometry extends to the negative side (on Z: hangs below) |

The three axes mix freely: `X=1 / Y=0 / Z=1` means "positive X, centred Y, on the
ground Z".

## Measured behaviour

Input: a 1 × 2 × 0.5 box whose mesh data was deliberately moved to
x = 2.5 … 3.5, i.e. far from the origin.

| 缩放？ | Scale | Align (X/Y/Z) | Output size | Output bounds |
| --- | --- | --- | --- | --- |
| off | – | 0 / 0 / 0 | 1 × 2 × 0.5 | x −0.5 … 0.5, y −1 … 1, z −0.25 … 0.25 |
| off | – | 1 / 1 / 1 | 1 × 2 × 0.5 | x 0 … 1, y 0 … 2, z 0 … 0.5 |
| off | – | −1 / 0 / 1 | 1 × 2 × 0.5 | x −1 … 0, y −1 … 1, z 0 … 0.5 |
| on | 4 | 1 / 1 / 1 | 2 × 4 × 1 | x 0 … 2, y 0 … 4, z 0 … 1 |
| on | 10 | 0 / 0 / 0 | 5 × 10 × 2.5 | centred on the origin |

Two things worth knowing:

- the order is **align first, then scale**, and the scale is about the origin —
  so "Align 1/1/1 + Scale" stays pinned to the origin
- scaling is uniform, driven by the longest axis; the other axes follow

## How it is built

- `Bounding Box` → `Max − Min` → `Minimum` picks the longest axis →
  `Scale / longest_axis` gives the uniform factor
- alignment: three `GN_Align` sub-groups map `−1 … 1` to a `0 … 1` factor, then
  multiply by `Size / 2` for the offset
- `Realize Instances` runs **for measuring only**, so instanced input gets a true
  bounding box; the output keeps instances instead of flattening them
- apart from one `Switch` for the scale toggle, it is all math nodes — no loops,
  no Python

## Changes since 0.0.1

- new `缩放？` toggle, off by default: the default behaviour is now "align only"
  instead of "always scale"
- alignment extracted into a `GN_Align` sub-group, reused by all three axes
- asset file saved with Blender 5.0, so the minimum version is now 5.0

See [CHANGELOG.md](CHANGELOG.md) for details.

## Limitations

- geometry nodes only see **local** coordinates, so an object's
  Location / Rotation / Scale plays no part
- `Scale` has a minimum of 1 — the longest axis cannot go below 1
- alignment and scaling are relative to the object's own origin, not world origin

## License

GPL-3.0-or-later, see [LICENSE](LICENSE).
