# GN_MatchSize

[English](README.md)

![](https://picgo-mdeia.oss-cn-beijing.aliyuncs.com/picgo/github_media/2026-02-26_17-55-11_trimmed_compressed-ezgif.com-optimize.gif)

GN_MatchSize 是一个基于几何节点实现的尺寸匹配与对齐工具，灵感来自 Houdini 的 Match Size 节点。

在几何节点中引入 GN_MatchSize，它可以将多个几何对象调整到统一比例，并将位置归零，在面对不同来源的几何时非常有用。

这是一个为程序化建模、资产规范化、批量处理而设计的通用基础节点。


## 安装
> **Blender 4.2 +**

1. 下载 [gn_matchsize.zip](https://github.com/hendasheng/gn_matchsize/releases)
2. 打开 Blender，进入 `编辑` → `首选项` → `插件`
3. 点击右上角箭头，选择 **从磁盘安装**
4. 选择下载的 `gn_matchsize.zip` 并安装

安装完成后：
- 打开 **几何节点** 编辑器
- 按 `Shift + A`
- 选择 `群组` → `GN_MatchSize` (或者直接搜索 `Match Size`)
- 节点会自动出现在当前文件中

![](https://picgo-mdeia.oss-cn-beijing.aliyuncs.com/picgo/github_media/20260226182011.png)

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
