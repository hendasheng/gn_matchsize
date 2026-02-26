# GN_MatchSize

[English](README.md)

![](https://picgo-mdeia.oss-cn-beijing.aliyuncs.com/picgo/github_media/GN_MatchSize_Github@1x.png)

GN_MatchSize 是一个基于 Blender 几何节点（Geometry Nodes）实现的尺寸匹配与对齐工具，灵感来源于 Houdini 的 Match Size 节点。

在几何节点工作流中引入 GN_MatchSize，可以将多个几何对象统一到相同尺寸比例，并根据需求自动完成对齐与归零操作。在处理来自不同来源、尺度不统一的几何数据时尤为高效。

该节点特别适用于：
- 程序化建模流程
- 资产标准化处理
- 批量几何规范化
- 多来源模型的比例统一

GN_MatchSize 是一个为程序化建模与资产规范化设计的通用基础节点。

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

![](images/node.png)

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
