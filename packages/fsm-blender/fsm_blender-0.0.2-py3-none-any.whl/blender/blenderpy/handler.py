import bpy
import bmesh
from mathutils import Vector
from bmesh.types import BMVert

from blender.data import *
from blender.blenderpy.util import *
from blender.default_cfg import MODE_ANIMATION
from blender.blenderpy.graph import *

limits = []
x_pos = []
FR, MAX_FR, all_frames, all_frames_max, SUM, DATA_MAX, DATA_MIN = get_constants(DATA)

def handler_bar(scene):
    """updates size of bars"""
    frame_cur = scene.frame_current
    objList = [obj for obj in bpy.data.objects if 'cube' in obj.name]

    for i, obj in enumerate(objList[:len(DATA)]):
        hooks = [h for h in obj.children if "Hook" in h.name]
        for j, hook in enumerate(hooks):
            dist = all_frames[i][frame_cur] / all_frames_max[frame_cur] * 100
            pos_init = Vector((0, hook.location[1], hook.location[2]))
            hook.location = pos_init + Vector((dist, 0, 0))


def handler_timeframe(scene):
    """updates time object at keyframe"""
    text = bpy.data.objects['label_time']
    frame = scene.frame_current
    for i, val in enumerate(np.arange(0, MAX_FR, 48)):
        if frame >= val:
            text.data.body = f"timeframe {i}"
            # text.location = Vector((100,30,1))
            text.location = Vector(LABEL_TIME_LOC)


def handler_grid(scene):
    if MODE_ANIMATION == "static":
        frame = bpy.context.scene.frame_current
        labels = [obj for obj in bpy.data.objects if 'value_label' in obj.name]
        frame = bpy.context.scene.frame_current

        for i, cube in enumerate([c for c in bpy.data.objects if "cube" in c.name]):
            x_pos.append(dict())
            hooks = [h.location[0] for h in cube.children if "Hook" in h.name]
            print(hooks)
            x_pos[i][frame] = max(hooks)
        for i, label in enumerate(labels):
            if frame in x_pos[i]:
                value = "{:.2f}".format(x_pos[i][frame] * DATA_MAX / 100)
                label.data.body = value
                # print(value)

    if MODE_ANIMATION == "max":
        frame = bpy.context.scene.frame_current
        if frame <= MAX_FR:
            max_value = all_frames_max[frame]
        upper_limit = cceil(max_value)
        # lower_limit = upper_limit/10

        cur_limits = np.arange(0, upper_limit, upper_limit/4)
        cur_limits[0] = upper_limit
        for limit in cur_limits:
            if limit not in limits:
                limits.append(limit)

        for upper_limit in limits:
            name = f"upper_limit_{upper_limit}"
            if f"line_{name}" not in bpy.data.objects:
                add_line(name)

            for name in [line.name for line in bpy.data.objects if "line" in line.name]:
                value = float(name.split("_")[-1])
                line = bpy.data.objects[f"{name}"]
                line_label = bpy.data.objects[f"label_{name.split('line_')[-1]}"]

                line.location = Vector((value/max_value*100,0,1))
                line_label.location = Vector((line.location[0] - line_label.dimensions[0]/2,26.5,0))
                line_label.data.body = f"{value:g}"

                grid_material = bpy.data.materials.get(f"material_{name.split('line_')[-1]}")
                grid_material.use_nodes = True
                node_tree = grid_material.node_tree
                nodes = node_tree.nodes
                bsdf = nodes.get("Principled BSDF")

                if value/max_value <= 0.15:
                    bsdf.inputs['Alpha'].default_value = min(1, max(bsdf.inputs['Alpha'].default_value - 0.005, 0))
                elif value/max_value > 0.99:
                    bsdf.inputs['Alpha'].default_value = min(1, max(bsdf.inputs['Alpha'].default_value - 0.005, 0))
                else:
                    bsdf.inputs['Alpha'].default_value = min(1, max(bsdf.inputs['Alpha'].default_value + 0.0025, 0))


def handler_value_label(scene):
    frame = bpy.context.scene.frame_current
    for i, _ in enumerate(DATA):
        label = bpy.data.objects[f"value_label_{i}"]
        if frame <=MAX_FR:
            label.data.body = "{:.2f}".format(all_frames[i][frame])


def handler_pie(scene):
    bpy.ops.object.select_all(action='DESELECT')

    # Select the object
    if bpy.data.objects.get("pie_chart") is not None:
        bpy.data.objects['pie_chart'].select_set(True)

    bpy.ops.object.delete()

    pie_chart()

    # Select the object
    if bpy.data.objects.get("pie_chart") is not None:
        bpy.data.objects['pie_chart'].select_set(True)
        obj = bpy.data.objects['pie_chart']

    obj = bpy.data.objects['pie_chart']
    frame = bpy.context.scene.frame_current
    # all_frames = get_all_frames()
    # total = get_sum()

    per100 = [floor(all_frames[i][frame]/SUM[frame] * 100) for i,_ in enumerate(DATA)]
    if sum(per100) < 100:
        per100[per100.index(max(per100))] += 100 - sum(per100)

    EPSILON = 1.0e-5
    up_vector = Vector((0,0,1))

    bm = bmesh.new()
    bm.from_mesh(obj.data, face_normals=True)

    faces=[f for f in bm.faces if (f.normal-up_vector).length < EPSILON]

    bar2face = ([], [], [])
    for i, face in enumerate(faces):
        if i<=per100[0]:
            obj.data.polygons[face.index].material_index = 1
            bar2face[0].append(face.index)
        elif per100[0] < i < per100[0] + per100[1]:
            obj.data.polygons[face.index].material_index = 2
            bar2face[1].append(face.index)
        else:
            obj.data.polygons[face.index].material_index = 3
            bar2face[2].append(face.index)


    id_first = per100.index(sorted(per100)[-1])
    id_second = per100.index(sorted(per100)[-2])

    bm = bmesh.new()
    bm.from_mesh(obj.data, face_normals=True)
    faces = [f for f in bm.faces if f.index in bar2face[id_first]]
    extruded = bmesh.ops.extrude_face_region(bm, geom=faces)

    # Move extruded geometry
    translate_verts = [v for v in extruded['geom'] if isinstance(v, BMVert)]
    vec = up_vector * 0.5
    bmesh.ops.translate(bm, vec=vec, verts=translate_verts)

    # Second
    bm.faces.ensure_lookup_table()
    faces = [f for f in bm.faces if (f.normal-up_vector).length < EPSILON]
    faces = [f for f in bm.faces if f.index in bar2face[id_second]]
    extruded = bmesh.ops.extrude_face_region(bm, geom=faces)

    # Move extruded geometry
    translate_verts = [v for v in extruded['geom'] if isinstance(v, BMVert)]
    vec = up_vector * 0.25
    bmesh.ops.translate(bm, vec=vec, verts=translate_verts)

    # Update mesh and free Bmesh
    bm.normal_update()
    bm.to_mesh(obj.data)
    bm.free()
