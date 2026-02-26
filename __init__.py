bl_info = {
    "name": "GN MatchSize",
    "author": "HenDaSheng",
    "version": (0, 0, 1),
    "blender": (4, 5, 0),
    "location": "Geometry Nodes > Add > Group",
    "description": "Houdini-style Match Size node group",
    "category": "Geometry Nodes",
}

import bpy
import os

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
            groups = getattr(data_from, "node_groups", None)
            if not groups or NODEGROUP_NAME not in groups:
                print(f"[GN_MatchSize] Node group '{NODEGROUP_NAME}' not found in {ASSET_BLEND}")
                return True
            data_to.node_groups = [NODEGROUP_NAME]
    except Exception as e:
        print(f"[GN_MatchSize] Append failed: {e}")
        return True

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