import bpy
import decimal
import numpy as np
from math import floor, ceil, sqrt
from mathutils import Vector

from blender.default_cfg import *
# from blender.data import *

# all_frames = get_all_frames(DATA)

class CustomError(Exception):
    pass

# def create_label(pos, name):
#     # label
#     bpy.ops.object.text_add(enter_editmode=False)
#     bpy.context.active_object.location = pos
#     bpy.context.active_object.name = name
#     bpy.context.active_object.scale = (2, 2, 1)
#     bpy.context.active_object.data.font = bpy.data.fonts.load(FONT)
#     return bpy.context.active_object

def delete_all():
    for o in [i.name for i in list(bpy.data.objects)]:
        obj = bpy.context.scene.objects.get(o)
        if obj: obj.select_set(True)

    bpy.ops.object.delete()
    for obj in list(bpy.data.objects):
        bpy.ops.object.delete()

def txtcleanup(name, x, y, z, r):
    [bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION') for j in range(4)]
    [bpy.ops.font.text_insert(text=char) for char in name]
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.context.object.location = (x, y, z)
    bpy.context.object.rotation_euler[2] = r

def change_text(txt):
    [bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION') for j in range(4)]
    [bpy.ops.font.text_insert(text=char) for char in txt]
    bpy.ops.object.editmode_toggle()

# def add_line(name):

#     def create_vert(coords, name):
#         # create the Curve Datablock
#         curveData = bpy.data.curves.new('myCurve', type='CURVE')
#         curveData.dimensions = '3D'
#         curveData.resolution_u = 2

#         # map coords to spline
#         polyline = curveData.splines.new('POLY')
#         polyline.points.add(len(coords)-1)
#         for i, coord in enumerate(coords):
#             x,y,z = coord
#             polyline.points[i].co = (x, y, z, 1)

#         # create Object
#         curveOB = bpy.data.objects.new(name, curveData)
#         curveData.bevel_depth = 0.05
#         curveData.bevel_mode = 'PROFILE'
#         curveData.bevel_resolution = 24

#         # attach to scene and validate context
#         # scn = bpy.context.scene
#         bpy.context.collection.objects.link(curveOB)

#     create_vert([(0, GRID_LINE_HEIGHT, 0), (0, -GRID_LINE_HEIGHT, 0)], f"line_{name}")
#     create_label((0, GRID_LINE_HEIGHT + 1, 0), f"label_{name}")

#     if f"material_{name}" not in bpy.data.materials:
#         grid_material = bpy.data.materials.new(f"material_{name}")
#     else:
#         grid_material = bpy.data.materials.get(f"material_{name}")

#     grid_material.use_nodes = True
#     grid_material.blend_method = 'BLEND'
#     grid_material.shadow_method = 'NONE'


#     node_tree = grid_material.node_tree
#     nodes = node_tree.nodes
#     bsdf = nodes.get("Principled BSDF")

#     bsdf.inputs['Alpha'].default_value = 1.0
#     bsdf.inputs['Base Color'].default_value = (23/255, 23/255, 23/255, 1.0)
#     bpy.data.objects[f"line_{name}"].data.materials.append(grid_material)
#     bpy.data.objects[f"label_{name}"].data.materials.append(grid_material)

#     bpy.data.objects[f"line_{name}"].parent = bpy.data.objects['grid_dynamic']
#     bpy.data.objects[f"label_{name}"].parent = bpy.data.objects['grid_dynamic']


def cceil(x):
    def get_decimals(x):
        x = str(x)
        x = x.rstrip('0')
        x = decimal.Decimal(x)
        x = x.as_tuple().exponent
        x = abs(x)
        return x

    if str(x)[0] != "0":
        l = len(str(x).split(".")[0])
        res = ceil(x/(10**l))* 10 ** l
    else:
        res = 1 * 10 ** - (get_decimals(x)-1)

    return res

def hex_to_rgb(hex):
    hex = hex.split("#")[-1]
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)

    return tuple(rgb)

def set_parent(obj, parent):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    parent.select_set(True)
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
    bpy.ops.object.select_all(action='DESELECT')

def set_render_settings():
    """set render options -> color management"""
    bpy.context.scene.view_settings.view_transform = 'Standard'

def force_div_by_zero_error():
    return 1 / 0

def force_value_error():
    sqrt(-2)


def force_value_error_custom(x):
    try:
        res = sqrt(x)
    except ValueError as ve:
    # except:
        print(f'You entered {x}, which is not a positive number.')
        raise CustomError("everything is broken")
