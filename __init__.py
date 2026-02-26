import bpy
import os

NODEGROUP_NAME = "GN_MatchSize"
ASSET_BLEND = "GN_MatchSize.blend"

def append_node_group():
    path = os.path.join(os.path.dirname(__file__), "assets", ASSET_BLEND)

    if NODEGROUP_NAME in bpy.data.node_groups:
        return

    with bpy.data.libraries.load(path, link=False) as (data_from, data_to):
        if NODEGROUP_NAME in data_from.node_groups:
            data_to.node_groups = [NODEGROUP_NAME]

def register():
    append_node_group()

def unregister():
    pass