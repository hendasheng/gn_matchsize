bl_info = {
    "name": "GN MatchSize",
    "author": "HenDaSheng",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "location": "Geometry Nodes > Add > Group",
    "description": "Houdini-style Match Size node group",
    "category": "Geometry Nodes",
}

import bpy
import os

# 节点组在 assets/GN_MatchSize.blend 里的名字，按优先级排列：
# 0.1.0 起节点组以 "GN_MatchSize_0.1.0" 保存，旧文件里叫 "GN_MatchSize"。
NODEGROUP_CANDIDATES = ("GN_MatchSize_0.1.0", "GN_MatchSize")
# 注入到用户文件后显示的名字（Add 菜单里看到的名字）。
NODEGROUP_NAME = "GN_MatchSize"
ASSET_BLEND = "GN_MatchSize.blend"


def _asset_blend_path():
    return os.path.join(os.path.dirname(__file__), "assets", ASSET_BLEND)


def _append_node_group_once():
    # 1) 受限状态下 bpy.data 会是 _RestrictData，直接退出等待下次 timer
    try:
        _ = bpy.data.node_groups
    except Exception:
        return False

    # 2) 已经存在就不重复追加
    if NODEGROUP_NAME in bpy.data.node_groups:
        return True

    path = _asset_blend_path()
    if not os.path.exists(path):
        print(f"[GN_MatchSize] Missing asset file: {path}")
        return True  # 不再重试（否则会无限循环）

    try:
        with bpy.data.libraries.load(path, link=False) as (data_from, data_to):
            available = getattr(data_from, "node_groups", None) or []
            source_name = next((n for n in NODEGROUP_CANDIDATES if n in available), None)
            if source_name is None:
                print(f"[GN_MatchSize] No MatchSize node group found in {ASSET_BLEND}")
                return True
            data_to.node_groups = [source_name]
    except Exception as e:
        print(f"[GN_MatchSize] Append failed: {e}")
        return True

    # 3) 追加进来的组统一改名为 GN_MatchSize，Add 菜单里更好找
    group = bpy.data.node_groups.get(source_name)
    if group is not None and NODEGROUP_NAME not in bpy.data.node_groups:
        group.name = NODEGROUP_NAME
    if group is not None:
        print(f"[GN_MatchSize] Loaded '{source_name}' as '{group.name}'")

    return True


def _timer_try_append():
    done = _append_node_group_once()
    # 返回 None = 停止 timer；返回秒数 = 继续重试
    return None if done else 0.5


def _on_load_post(_dummy):
    # 打开/新建文件后也确保注入
    bpy.app.timers.register(_timer_try_append, first_interval=0.1)


def register():
    # 1) 启用扩展时：延迟注入（避免 _RestrictData）
    bpy.app.timers.register(_timer_try_append, first_interval=0.1)

    # 2) 之后每次 load file：也自动注入
    if _on_load_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(_on_load_post)


def unregister():
    if _on_load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(_on_load_post)
