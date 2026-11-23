# GN_MatchSize

[English](README_EN.md)

![GN_MatchSize](https://picgo-mdeia.oss-cn-beijing.aliyuncs.com/picgo/github_media/GN_MatchSize_Github@1x.png)

GN_MatchSize 是一个基于 Blender 几何节点（Geometry Nodes）的尺寸匹配与对齐节点组，灵感来自 Houdini 的 Match Size。

把任意来源、尺度不一的几何体统一到同一个目标尺寸，并按 X / Y / Z 三个轴分别对齐到原点——全部在几何节点里完成，没有 Python 依赖。

- 版本 **0.1.0**，需要 **Blender 5.0+**
- 纯 Geometry Nodes，可嵌入任意节点树，也可二次封装成自己的资产

## 安装

### 用 Blender 扩展安装（推荐）

1. 在 [Releases](https://github.com/hendasheng/gn_matchsize/releases) 下载 `gn_matchsize-0.1.0.zip`
2. 打开 Blender：`编辑` → `偏好设置` → `插件`
3. 右上角箭头 → **从磁盘安装**，选择下载的 zip
4. 勾选启用 **GN MatchSize**

### 手动安装

把仓库目录放到 Blender 的 `scripts/addons/`（或扩展目录）下，启用 **GN MatchSize**。

启用后回到几何节点编辑器：`Shift + A` → `群组` → `GN_MatchSize`（搜索 `MatchSize` 也能找到）。

> 插件会在启用时和每次打开文件时自动把节点组注入当前 .blend，所以旧的工程文件打开后也能直接用。

## 参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| Geometry | 几何 | 输入几何，网格 / 曲线 / 点 / 实例都可以 |
| 缩放？ | 布尔 | 关闭：只对齐、不改尺寸；开启：对齐后等比缩放到 Scale |
| Scale | 浮点（≥ 1） | 目标尺寸，指**最长轴**的长度；统一缩放 = `Scale / 最长轴` |
| Align → X Axis / Y Axis / Z Axis | 浮点（−1 ~ 1） | 每个轴独立对齐：`0` 居中、`1` 贴正向、`−1` 贴负向 |

## 对齐是怎么算的

节点对每个轴做两件事：

1. 用 `Bounding Box` 拿到 Min / Max，算出尺寸 `Size = Max − Min` 和中心 `Center = (Min + Max) / 2`
2. 平移 `offset = −Center + Align × Size × 0.5`

所以 **Align 就是「包围盒的哪个面贴到原点」**：

| Align | 结果 |
| --- | --- |
| `0` | 包围盒中心落在原点 |
| `1` | Min 面贴原点，几何体伸向正方向（Z 轴即「贴地」） |
| `−1` | Max 面贴原点，几何体伸向负方向（Z 轴即「吊顶」） |

三个轴可以混搭，例如 `X=1 / Y=0 / Z=1` 就是「X 贴正、Y 居中、Z 贴地」。

## 实测行为

输入一个 1 × 2 × 0.5 的立方体，并故意把网格数据挪到 x = 2.5 ~ 3.5（远离原点）：

| 缩放？ | Scale | Align (X/Y/Z) | 输出尺寸 | 输出包围盒 |
| --- | --- | --- | --- | --- |
| 关 | – | 0 / 0 / 0 | 1 × 2 × 0.5 | x −0.5 ~ 0.5，y −1 ~ 1，z −0.25 ~ 0.25 |
| 关 | – | 1 / 1 / 1 | 1 × 2 × 0.5 | x 0 ~ 1，y 0 ~ 2，z 0 ~ 0.5 |
| 关 | – | −1 / 0 / 1 | 1 × 2 × 0.5 | x −1 ~ 0，y −1 ~ 1，z 0 ~ 0.5 |
| 开 | 4 | 1 / 1 / 1 | 2 × 4 × 1 | x 0 ~ 2，y 0 ~ 4，z 0 ~ 1 |
| 开 | 10 | 0 / 0 / 0 | 5 × 10 × 2.5 | 居中于原点 |

两点值得注意：

- 处理顺序是**先对齐、后缩放**，而缩放以原点为基准，所以「Align 1/1/1 + Scale」的结果仍然贴在原点上
- 缩放是等比的，比例由最长轴决定，短轴跟着一起变

## 内部结构

- `Bounding Box` → `Max − Min` → `Minimum` 取最长轴 → `Scale / 最长轴` 得到统一缩放系数
- 对齐：三份 `GN_Align` 子节点组把 `−1 ~ 1` 映射成 `0 ~ 1` 的系数，再乘 `Size / 2` 作为偏移
- 测量前会 `Realize Instances`，所以实例输入的包围盒是真实几何尺寸；**输出不强制展开实例**
- 除了缩放开关的一个 `Switch`，其余全部是数学节点，没有循环、没有 Python

## 和 0.0.1 的差异

- 新增 `缩放？` 开关，默认关闭：默认行为从「总是缩放」变成「只对齐」，需要缩放时再打开
- 对齐逻辑抽成 `GN_Align` 子节点组，X / Y / Z 三轴复用同一份实现
- 资产文件升级为 Blender 5.0 保存，最低版本相应提升到 5.0

完整记录见 [CHANGELOG.md](CHANGELOG.md)。

## 已知限制

- 几何节点只能读几何体的**局部坐标**，物体的 Location / Rotation / Scale 不参与计算
- `Scale` 最小值为 1，不支持把最长轴缩到 1 以下
- 对齐和缩放都以**对象自身的原点**为基准，不是世界原点

## 许可

GPL-3.0-or-later，见 [LICENSE](LICENSE)。
