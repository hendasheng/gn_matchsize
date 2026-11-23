# Changelog

## 0.1.0 — 2026-11-23

### 新增 / Added

- 新增 `缩放？` 开关：关闭时只对齐不缩放，开启时才等比缩放到目标尺寸（默认关闭）
  Added a `缩放？` (scale) toggle: off = align only, on = align then scale to the
  target size. Off by default.
- 对齐逻辑抽成 `GN_Align` 子节点组，X / Y / Z 三轴复用同一份实现
  Alignment extracted into a `GN_Align` sub-group, shared by X / Y / Z.

### 变更 / Changed

- 节点组在资产文件中以 `GN_MatchSize_0.1.0` 保存，插件注入时重命名为 `GN_MatchSize`；
  插件同时兼容旧资产里的 `GN_MatchSize`
  The node group is stored as `GN_MatchSize_0.1.0` in the asset file and renamed
  to `GN_MatchSize` on injection; the loader still accepts the old name.
- 资产文件用 Blender 5.0 保存，`blender_version_min` 提升到 5.0.0
  Asset saved with Blender 5.0, `blender_version_min` raised to 5.0.0.
- 文档重写：参数表、对齐语义、实测数值、内部结构
  Docs rewritten: inputs table, alignment semantics, measured numbers, internals.

### 兼容性 / Compatibility

- 需要 Blender 5.0 及以上。0.0.1 的资产是 4.5 保存的，因此 0.0.1 仍可在 4.2+ 使用。
  Requires Blender 5.0+. The 0.0.1 asset was saved with 4.5 and still works on 4.2+.

## 0.0.1

- 首个发布版本：尺寸匹配 + 三轴对齐
  First release: size matching plus per-axis alignment.
