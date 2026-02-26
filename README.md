# GN_MatchSize
Houdini-style Match Size for Blender Geometry Nodes

> **Blender 4.5+**

GN_MatchSize 是一个基于 Geometry Nodes 实现的尺寸匹配与对齐工具，灵感来自 Houdini 的 Match Size SOP。

它可以：
- 自动计算几何 Bounding Box
- 支持 Uniform Scale（最长边匹配）
- 支持按轴对齐（Min / Center / Max）
- 支持实例与真实几何
- 纯节点实现，无脚本依赖

这是一个为程序化建模、资产规范化、批量处理而设计的通用基础节点。

## 功能说明

### 1. 自动尺寸计算
内部通过：
`Size = Max - Min`
分别计算 X / Y / Z 轴尺寸。
可用于：
- 统一资产比例
- 规范化导入模型
- 自动适配不同来源的几何

### 2. 等比缩放
缩放逻辑：
`scale = target / longest_axis`
确保最长边匹配目标尺寸，同时保持比例。

### 3. 轴向对齐（Align）
每个轴支持：
-1 = Min  
0 = Center  
1 = Max

通过数学方式计算偏移：
`offset = -(center + align * size * 0.5)`

无需分支节点，纯数学控制。
支持：
- 居中
- 贴底
- 贴顶
- 混合对齐（例如 X Min / Y Center / Z Max）

## 使用场景
- 资产标准化
- 程序化阵列
- 自动尺寸规范
- Geometry Nodes Pipeline
- 类 Houdini 工作流

## 技术实现特点
- 纯 Geometry Nodes
- 无 Python 依赖
- 可嵌入任意节点系统
- 可二次封装为资产工具
- 支持实例 Realize 或直接实例模式

