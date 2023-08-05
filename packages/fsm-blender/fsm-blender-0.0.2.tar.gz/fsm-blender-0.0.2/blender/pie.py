import bpy
import bmesh
import math


# ------------------------------------------------------------------------------
# Utility Functions

def set_smooth(obj):
    """ Enable smooth shading on an mesh object """

    for face in obj.data.polygons:
        face.use_smooth = True


def object_from_data(data, name, scene, select=True):
    """ Create a mesh object and link it to a scene """

    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(data['verts'], data['edges'], data['faces'])

    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    mesh.update(calc_edges=True)
    mesh.validate(verbose=True)

    return obj


def recalculate_normals(mesh):
    """ Make normals consistent for mesh """

    bm = bmesh.new()
    bm.from_mesh(mesh)

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    bm.to_mesh(mesh)
    bm.free()


# ------------------------------------------------------------------------------
# Geometry functions

def vertex_circle(segments, z):
    """ Return a ring of vertices """
    verts = []

    for i in range(segments):
        angle = (math.pi*2) * i / segments
        verts.append((math.cos(angle), math.sin(angle), z))

    return verts


def face(segments, i, row):
    """ Return a face on a cylinder """

    if i == segments - 1:
        ring_start = segments * row
        base = segments * (row + 1)

        return (base - 1, ring_start, base, (base + segments) - 1)

    else:
        base = (segments * row) + i
        return (base, base + 1, base + segments + 1, base + segments)


def bottom_cap(verts, faces, segments, cap='NGON'):
    """ Build bottom caps as triangle fans """

    if cap == 'TRI':
        verts.append((0, 0, 0))
        center_vert = len(verts) - 1

        [faces.append((i, i+1, center_vert)) for i in range(segments - 1)]
        faces.append((segments - 1, 0, center_vert))

    elif cap == 'NGON':
        faces.append([i for i in range(segments)])

    else:
        print('[!] Passed wrong type to bottom cap')


def top_cap(verts, faces, segments, rows, cap='NGON'):
    """ Build top caps as triangle fans """

    if cap == 'TRI':
        verts.append((0, 0, rows - 1))
        center_vert = len(verts) - 1
        base = segments * (rows - 1)

        [faces.append((base+i, base+i+1, center_vert))
                       for i in range(segments - 1)]

        faces.append((segments * rows - 1, base, center_vert))

    elif cap == 'NGON':
        base = (rows - 1) * segments
        faces.append([i + base for i in range(segments)])

    else:
        print('[!] Passed wrong type to top cap')


# ------------------------------------------------------------------------------
# Main Functions

def make_circle(name, segments=32, fill=None):
    """ Make a circle """

    data = {
            'verts': vertex_circle(segments, 0),
            'edges': [],
            'faces': [],
           }

    if fill:
        bottom_cap(data['verts'], data['faces'], segments, fill)
    else:
        data['edges'] = [(i, i+1) for i in range(segments)]
        data['edges'].append((segments - 1, 0))

    scene = bpy.context.scene
    return object_from_data(data, name, scene)


def make_cylinder(name, segments=64, rows=4, cap=None):
    """ Make a cylinder """

    data = { 'verts': [], 'edges': [], 'faces': [] }

    for z in range(rows):
        data['verts'].extend(vertex_circle(segments, z))

    for i in range(segments):
        for row in range(0, rows - 1):
            data['faces'].append(face(segments, i, row))

    if cap:
        bottom_cap(data['verts'], data['faces'], segments, cap)
        top_cap(data['verts'], data['faces'], segments, rows, cap)


    scene = bpy.context.scene
    obj = object_from_data(data, name, scene)
    recalculate_normals(obj.data)
    set_smooth(obj)

    bevel = obj.modifiers.new('Bevel', 'BEVEL')
    bevel.limit_method = 'ANGLE'

    obj.modifiers.new('Edge Split', 'EDGE_SPLIT')

    return obj


# ------------------------------------------------------------------------------
# Main Code

#make_circle('Circle', 64)
# make_cylinder('Cylinder', 100, 2, 'TRI')
# bpy.ops.object.editmode_toggle()
# bpy.ops.mesh.inset(use_boundary=False, use_even_offset=False, use_relative_offset=False, use_edge_rail=False, thickness=0.307055, depth=0, use_outset=False, use_select_inset=False, use_individual=False, use_interpolate=True)
# bpy.ops.object.editmode_toggle()

#bpy.ops.mesh.bridge_edge_loops()
