import bpy
import bmesh
import random
from bpy import context
from mathutils import Vector
from math import floor
from bmesh.types import BMVert

from blender.blenderpy.util import *
from blender.pie import *
# from blender.data import *

class Graph:

    def __init__(self, cfg):
        self.cfg = cfg
        self.available_colors = []
        self.limits = []
        self.x_pos = []
        self.FR, self.MAX_FR, self.all_frames, self.all_frames_max, self.SUM, self.DATA_MAX, self.DATA_MIN = self.get_constants()

    def create_label(self, pos, name):
        # label
        bpy.ops.object.text_add(enter_editmode=False)
        bpy.context.active_object.location = pos
        bpy.context.active_object.name = name
        bpy.context.active_object.scale = (2, 2, 1)
        bpy.context.active_object.data.font = bpy.data.fonts.load(self.cfg.FONT)
        return bpy.context.active_object

    def add_line(self, name):

        def create_vert(coords, name):
            # create the Curve Datablock
            curveData = bpy.data.curves.new('myCurve', type='CURVE')
            curveData.dimensions = '3D'
            curveData.resolution_u = 2

            # map coords to spline
            polyline = curveData.splines.new('POLY')
            polyline.points.add(len(coords)-1)
            for i, coord in enumerate(coords):
                x,y,z = coord
                polyline.points[i].co = (x, y, z, 1)

            # create Object
            curveOB = bpy.data.objects.new(name, curveData)
            curveData.bevel_depth = 0.05
            curveData.bevel_mode = 'PROFILE'
            curveData.bevel_resolution = 24

            # attach to scene and validate context
            # scn = bpy.context.scene
            bpy.context.collection.objects.link(curveOB)

        create_vert([(0, GRID_LINE_HEIGHT, 0), (0, -GRID_LINE_HEIGHT, 0)], f"line_{name}")
        self.create_label((0, GRID_LINE_HEIGHT + 1, 0), f"label_{name}")

        if f"material_{name}" not in bpy.data.materials:
            grid_material = bpy.data.materials.new(f"material_{name}")
        else:
            grid_material = bpy.data.materials.get(f"material_{name}")

        grid_material.use_nodes = True
        grid_material.blend_method = 'BLEND'
        grid_material.shadow_method = 'NONE'


        node_tree = grid_material.node_tree
        nodes = node_tree.nodes
        bsdf = nodes.get("Principled BSDF")

        bsdf.inputs['Alpha'].default_value = 1.0
        bsdf.inputs['Base Color'].default_value = (23/255, 23/255, 23/255, 1.0)
        bpy.data.objects[f"line_{name}"].data.materials.append(grid_material)
        bpy.data.objects[f"label_{name}"].data.materials.append(grid_material)

        bpy.data.objects[f"line_{name}"].parent = bpy.data.objects['grid_dynamic']
        bpy.data.objects[f"label_{name}"].parent = bpy.data.objects['grid_dynamic']

    def camera(self):
        bpy.ops.object.select_all(action='DESELECT')
        loc_origin = self.cfg.CAM_LOC
        bpy.ops.object.camera_add(location=loc_origin,
                                rotation=(0, 0, 0),
        )
        context.object.name = "cam"
        bpy.context.scene.camera = context.object
        bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.object.empty_add(
                location=(50,0,0)
                )
        bpy.context.active_object.name = "cam_focus"
        bpy.ops.object.select_all(action='DESELECT')

        set_parent(bpy.data.objects['cam'], bpy.data.objects['cam_focus'])
        bpy.ops.object.select_all(action='DESELECT')

    def move_camera(self):
        bpy.ops.object.select_all(action='DESELECT')
        loc_origin = self.cfg.CAM_LOC
        PAN_UP = 16
        PAN_DOWN = -16
        cam = bpy.data.objects["cam"]
        cam_focus = bpy.data.objects["cam_focus"]

        for i, frame in enumerate(self.FR[::1]):
            if i % 4 == 0:
                cam_focus.rotation_euler[0] = 0
                cam_focus.keyframe_insert(data_path="rotation_euler", index=0, frame=frame)
                # cam.location = Vector((loc_origin))
                # cam.keyframe_insert(data_path="location", frame=frame)
            if i % 4 == 1:
                pass
                # cam_focus.rotation_euler[0] = 0.35
                # cam_focus.keyframe_insert(data_path="rotation_euler", index=0, frame=frame)
                # cam.location = Vector((loc_origin[0] + PAN_UP, loc_origin[1], loc_origin[2]+10))
                # cam.keyframe_insert(data_path="location", frame=frame)
            if i % 4 == 2:
                cam_focus.rotation_euler[0] = 0.70
                cam_focus.keyframe_insert(data_path="rotation_euler", index=0, frame=frame)
                # cam.location = Vector(loc_origin)
                # cam.keyframe_insert(data_path="location", frame=frame)
            if i % 4 == 3:
                pass
                # cam_focus.rotation_euler[0] = 0.35
                # cam_focus.keyframe_insert(data_path="rotation_euler", index=0, frame=frame)
                # cam.location = Vector((loc_origin[0] + PAN_DOWN, loc_origin[1], loc_origin[2]+10))
                # cam.keyframe_insert(data_path="location", frame=frame)

    def label_timeframe(self):
        bpy.ops.object.select_all(action='DESELECT')
        # mat
        mat = bpy.data.materials.new(f"material_time")
        mat.diffuse_color = (23/255, 23/255, 23/255, 1.0)
        mat.roughness = 0.8
        mat.shadow_method = 'NONE'

        #text
        bpy.ops.object.text_add(enter_editmode=False)
        bpy.context.active_object.location = (self.cfg.Gridx, self.cfg.Gridy*0.6, 1)
        bpy.context.active_object.scale = (2, 2, 1)
        bpy.context.active_object.name = "label_time"
        bpy.context.active_object.data.font = bpy.data.fonts.load(self.cfg.FONT)
        bpy.context.active_object.data.materials.append(mat)

        bpy.context.view_layer.objects.active = bpy.data.objects["cam"]
        bpy.data.objects["label_time"].select_set(True)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        bpy.ops.object.select_all(action='DESELECT')

    def title(self):
        bpy.ops.object.select_all(action='DESELECT')
        # mat
        mat = bpy.data.materials.new(f"material_title")
        mat.diffuse_color = (23/255, 23/255, 23/255, 1.0)
        mat.roughness = 0.8
        mat.shadow_method = 'NONE'

        #Title
        bpy.ops.object.text_add(enter_editmode=True)
        bpy.context.active_object.name = f'title_main'
        bpy.context.active_object.scale = (4,4,1)
        change_text(self.cfg.graphTitle)
        title = bpy.data.objects["title_main"]

        # bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.data.objects["cam"]
        bpy.data.objects["title_main"].select_set(True)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        bpy.ops.object.select_all(action='DESELECT')

        title.data.font = bpy.data.fonts.load(self.cfg.FONT)
        title.data.materials.append(mat)

    def loc_fix_labels(self):
        bpy.ops.object.select_all(action='DESELECT')
        graph = bpy.data.objects["graph"]
        title = bpy.data.objects["title_main"]
        title_x = bpy.data.objects["title_x"]
        title_y = bpy.data.objects["title_y"]
        label_time = bpy.data.objects["label_time"]

        title.location = Vector((graph.location[0] - title.dimensions[0]/2, self.cfg.Gridy/2, 0.1))
        title_x.location = Vector((graph.location[0], self.cfg.xLabelHeight , 0.1))
        # label_time.location = Vector((100, 30, 1))

    def title_axis(self):
        bpy.ops.object.select_all(action='DESELECT')
        # mat
        mat = bpy.data.materials.new(f"material_title")
        mat.diffuse_color = (23/255, 23/255, 23/255, 1.0)
        mat.roughness = 0.8
        mat.shadow_method = 'NONE'

        #x axis title
        bpy.ops.object.text_add(enter_editmode=True)
        bpy.context.active_object.name = f'title_x'
        bpy.context.active_object.scale = (2, 2, 1)
        txtcleanup(xAxisTitle, 0, xLabelHeight - 2.4 , 0.2, 0.0)
        bpy.context.active_object.data.materials.append(mat)

        bpy.context.view_layer.objects.active = bpy.data.objects["cam"]
        bpy.data.objects["title_x"].select_set(True)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        bpy.ops.object.select_all(action='DESELECT')

        #y axis title
        TITLE_Y_LOC = Vector((self.cfg.labelLocx-10, 0, 0.1))
        TITLE_Y_R = 1.570796
        bpy.ops.object.text_add(enter_editmode=True)
        bpy.context.active_object.name = f'title_y'
        bpy.context.active_object.scale = (2, 2, 1)
        txtcleanup(self.cfg.yAxisTitle, *TITLE_Y_LOC, TITLE_Y_R)
        bpy.context.active_object.data.materials.append(mat)

        bpy.context.view_layer.objects.active = bpy.data.objects["cam"]
        bpy.data.objects["title_y"].select_set(True)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        bpy.ops.object.select_all(action='DESELECT')

    def materials(self):
        #text material
        labelMat = bpy.data.materials.new(name='LabelMaterial')
        labelMat.diffuse_color=(0, 0, 0, 1)

        graph_elems = ['label', 'title']
        for obj in bpy.data.objects:
            if any((w in obj.name for w in graph_elems)):
                bpy.data.objects[obj.name].data.materials.append(labelMat)

        if not self.available_colors:
            self.available_colors.extend([hex_to_rgb(i) for i in self.cfg.COLOR_PALETTE])

        #bars material
        for obj in bpy.data.objects:
            if 'cube' in obj.name:
                mat = bpy.data.materials.new(name=f"material_{obj.name}")
                r,g,b = self.available_colors.pop(random.randrange(len(self.available_colors)))
                mat.diffuse_color=(r/255,g/255,b/255, 1)
                mat.shadow_method = 'NONE'
                bpy.data.objects[obj.name].data.materials.append(mat)

    def grid(self, mode="max"):
        if mode == "max":
            bpy.ops.object.empty_add(
                    location=(0,0,0)
                    )
            bpy.context.active_object.name = "grid_dynamic"

        elif mode == "static":
            #Grid
            bpy.ops.mesh.primitive_grid_add(x_subdivisions = self.cfg.nsubs, y_subdivisions = 1, size = 1, location = (50, 0, 0))
            bpy.data.objects['Grid'].scale = (self.cfg.Gridx, self.cfg.Gridy, 1)
            bpy.data.objects['Grid'].color = (0,0,0,0)
            grid = bpy.data.objects['Grid'].modifiers.new('Wireframe', type='WIREFRAME')
            grid.thickness = 0.0025

            currentMat = bpy.data.materials.new(name="material_grid")
            currentMat.diffuse_color=(0.8,0.8,0.8,1.0)
            bpy.data.objects["Grid"].data.materials.append(currentMat)

    def bars(self):
        for i in range(len(self.cfg.data)):
            currentBarWidth = self.cfg.Gridx * self.cfg.barHeight
            currentBarLocationx = -1*(self.cfg.Gridx/2) + currentBarWidth/2
            bpy.ops.mesh.primitive_cube_add(size = 1, scale = [1,1,1], location = (currentBarLocationx, self.cfg.barLocation[i], 0.01))
            context.active_object.name = f"cube_{i}"
            context.active_object.scale = (currentBarWidth, self.cfg.barThick, 1)

    def label_axis(self, mode="max"):
        """labels for x & y-axis"""
        mode = self.cfg.MODE_ANIMATION

        # x labels
        if mode == "static":
            for i in range(self.cfg.nxlabels):
                currentxLabelLocationx = -1*(self.cfg.Gridx/2) + self.cfg.tickStep*i
                bpy.ops.object.text_add(enter_editmode=True)
                bpy.context.active_object.name = f'x_label_{i}'
                txtcleanup(str(self.cfg.tickLabels[i]), currentxLabelLocationx, self.cfg.xLabelHeight, 0.1, 0.0)
                bpy.context.active_object.scale = (self.cfg.labelSize, self.cfg.labelSize, 1)

        #y labels
        for i in range(self.cfg.nylabels):
            mat = bpy.data.materials.new(f"material_y_label_{i}")
            mat.diffuse_color = (23/255, 23/255, 23/255, 1.0)
            mat.roughness = 0.8
            mat.shadow_method = 'NONE'

            bpy.ops.object.text_add(enter_editmode=True)
            bpy.context.active_object.name = f'y_label_{i}'
            bpy.context.active_object.scale = (2, 2, 1)
            bpy.context.active_object.data.font = bpy.data.fonts.load(self.cfg.FONT)
            txtcleanup(self.cfg.barLabels[i], self.cfg.labelLocx, self.cfg.barLocation[i], 0.1, 0.785)
            bpy.context.active_object.scale = (self.cfg.tickSize, self.cfg.tickSize, 1)
            bpy.context.active_object.data.materials.append(mat)

    def group_graph(self):
        """"groups all elements in graph object"""

        bpy.ops.object.empty_add(
                location=(0,0,0)
                )
        bpy.context.active_object.name = "graph"
        for name in [obj.name for obj in bpy.data.objects if "cube" in obj.name]:
            bpy.data.objects[name].select_set(True)
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
            bpy.ops.object.select_all(action='DESELECT')

        # move graph to x = 0
        bpy.context.active_object.location = bpy.context.active_object.location + Vector((self.cfg.Gridx/2,0,0))
        bpy.ops.object.select_all(action='DESELECT')

    def group_bars(self):
        """groups cubes, hooks & y-labels"""
        objList = [obj for obj in bpy.data.objects if 'cube' in obj.name]

        for j, obj in enumerate(objList):
            # Group Hooks and Cubes
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            for i in range(4):
                bpy.data.objects[f'C{j}_Hook_{i}'].select_set(True)
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            bpy.ops.object.select_all(action='DESELECT')

            # Group y-labels and Cubes
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.data.objects[f'y_label_{j}'].select_set(True)
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            bpy.ops.object.select_all(action='DESELECT')

            # sets initial keyframe of hooks to 0
            # for i in range(4):
            #     bpy.data.objects[f'C{j}_Hook_{i}'].keyframe_insert(data_path="location", frame=0)

            # bpy.ops.anim.keyframe_insert_menu(type='Location')
            bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.object.select_all(action='DESELECT')

    def group_value_labels(self):
        """group value labels to hooks, also centers them"""

        objList = [obj for obj in bpy.data.objects if 'cube' in obj.name]

        for i, obj in enumerate(objList):
            hook = bpy.data.objects[f'C{i}_Hook_0']
            bpy.context.view_layer.objects.active = hook

            value_label = bpy.data.objects[f'value_label_{i}'] # Is this created here?
            value_label.select_set(True)

            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            value_label.location = hook.location
            value_label.location += Vector((0.5, self.cfg.barThick/2 - value_label.dimensions[1]/2, 1))

            bpy.ops.object.select_all(action='DESELECT')

    def hooks(self):
        """add hook elements"""
        obj = bpy.context.scene.objects.get("cube_0")
        obj.select_set(True)

        #all bars
        objList = [obj for obj in bpy.data.objects if 'cube' in obj.name]

        for j, obj in enumerate(objList):
            obj.select_set(True)

            for v in obj.data.vertices[:4]:
                name = f"C{j}_Hook_{v.index}"
                bpy.ops.object.empty_add(
                        location=obj.matrix_world @ v.co
                        )
                mt = bpy.context.selected_objects[0]
                mt.name = name
                hook = obj.modifiers.new(
                        name=name,
                        type='HOOK',
                        )
                hook.object = mt
                hook.vertex_indices_set([v.index])

            bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.object.select_all(action='DESELECT')

    def animate_sorting(self):

        objList = [obj.name for obj in bpy.data.objects if 'cube' in obj.name]
        objs = [obj for obj in bpy.data.objects if 'cube' in obj.name]

        y_locations = [obj.location[1] for obj in objs]

        for frame in range(0, self.MAX_FR+1, self.cfg.SPEED_SORT):
            bpy.context.scene.frame_set(frame)
            sorted_cubes = sorted([obj for obj in objs], key = lambda obj: float(bpy.data.objects[f"value_label_{obj.name.split('_')[-1]}"].data.body))
            for i, cube in enumerate(sorted_cubes):
                cube.location[1] = y_locations[i]

            for i in objList:
                bpy.data.objects[i].select_set(True)
                bpy.data.objects[i].keyframe_insert(data_path="location", frame=frame)
                bpy.data.objects[i].select_set(False)

    def label_value(self):
        for i in range(len(self.cfg.data)):
            name = f"value_label_{i}"
            label = self.create_label((self.cfg.labelLocx, self.cfg.barLocation[i], 1), name)

            # mat
            mat = bpy.data.materials.new(f"material_{name}")
            mat.diffuse_color = (23/255, 23/255, 23/255, 1.0)
            mat.shadow_method = 'NONE'
            mat.roughness = 0.8
            label.data.materials.append(mat)

        bpy.ops.object.select_all(action='DESELECT')

    def background_image(self):
        cam = bpy.context.scene.camera
        filepath = "/home/philippy/youtube/00_tarantino_fucks/desktop.jpg"
        img = bpy.data.images.load(filepath)
        cam.data.show_background_images = True
        bg = cam.data.background_images.new()
        bg.image = img

    def light(self):
        light_data = bpy.data.lights.new(name="my-light-data", type='SUN')
        light_data.energy = 1.1
        # Create new object, pass the light data
        light_object = bpy.data.objects.new(name="light", object_data=light_data)
        # Link object to collection in context
        bpy.context.collection.objects.link(light_object)
        # Change light position
        light_object.location = (50, 0, 100)

    def background_plane(self):
        # mat first
        bpy.data.materials.new("material_bg")
        bpy.ops.mesh.primitive_plane_add(size=200, location=(100, 0, -50))
        bpy.context.active_object.name = f"bg"
        bpy.context.active_object.scale = [1.920, 1.080, 1]
        mat = bpy.data.materials["material_bg"]
        mat.use_nodes = True
        # The Background shader node is used to add background light emission.
        # This node should only be used for the world surface output.
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
        bpy.data.objects[f"bg"].data.materials.append(mat)


    def pie_chart(self):
        bpy.ops.mesh.primitive_cylinder_add(vertices=100, end_fill_type='TRIFAN', enter_editmode=False, align='WORLD', location=(75, -20, 0.1), scale=(8, 8, 1))
        obj = context.object
        obj.name = "pie_chart"

        # mat
        if "material_pie_base" not in bpy.data.materials:
            mat = bpy.data.materials.new("material_pie_base")
            mat.diffuse_color = (255/255, 255/255, 255/255, 1.0)
            obj.data.materials.append(mat)
        for i in range(len(self.cfg.data)):
            mat = bpy.data.materials[f"material_cube_{i}"]
            if mat.name not in obj.data.materials:
                obj.data.materials.append(mat)


    def circle_chart(self):
        c = make_cylinder('circle_chart', 100, 2)
        c.location = Vector((-20, 0, 1))


        EPSILON = 1.0e-5
        up_vector = Vector((0,0,1))
        down_vector = Vector((0,0,-1))


        #bpy.ops.mesh.primitive_cylinder_add(vertices=100, end_fill_type='TRIFAN', enter_editmode=False, align='WORLD', location=(75, -20, 0.1), scale=(8, 8, 1))
        obj = bpy.data.objects['circle_chart']
        bm = bmesh.new()
        bm.from_mesh(obj.data, face_normals=True)

        faces=[f for f in bm.faces if (f.normal-up_vector).length < EPSILON]
        new_faces = []
        #bmesh.ops.inset_region(bm, faces=faces, thickness=2, depth=0)
        for face in faces:
            geom = bmesh.ops.inset_region(bm, faces=[face], thickness=2, depth=0)
            bmesh.ops.translate(bm, verts = face.verts, vec = down_vector)
        #    new_faces.extend(geom['faces'])
        #    new_faces.append(face)
        faces=[f for f in bm.faces if (f.normal-up_vector).length < EPSILON]
        new_faces = []
        #bmesh.ops.inset_region(bm, faces=faces, thickness=2, depth=0)

        faces=[f for f in bm.faces if (f.normal-down_vector).length < EPSILON]
        for face in faces:
            geom = bmesh.ops.inset_region(bm, faces=[face], thickness=2, depth=0)
            bmesh.ops.translate(bm, verts = face.verts, vec = up_vector)


        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        obj.modifiers["Solidify"].thickness = 0.33

    def handler_bar(self, scene, _):
        """updates size of bars"""
        frame_cur = scene.frame_current
        objList = [obj for obj in bpy.data.objects if 'cube' in obj.name]

        for i, obj in enumerate(objList[:len(self.cfg.data)]):
            hooks = [h for h in obj.children if "Hook" in h.name]
            for j, hook in enumerate(hooks):
                # danger zone
                if self.all_frames_max[frame_cur] == 0.0:
                    dist = 0.0
                else:
                    dist = self.all_frames[i][frame_cur] / self.all_frames_max[frame_cur] * 100
                pos_init = Vector((0, hook.location[1], hook.location[2]))
                hook.location = pos_init + Vector((dist, 0, 0))


    def handler_timeframe(self, scene, _):
        """updates time object at keyframe"""
        text = bpy.data.objects['label_time']
        frame = scene.frame_current
        for i, val in enumerate(np.arange(0, self.MAX_FR, 48)):
            if frame >= val:
                text.data.body = f"timeframe {i}"
                # text.location = Vector((100,30,1))
                text.location = Vector(self.cfg.LABEL_TIME_LOC)


    def handler_grid(self, scene, _):
        if self.cfg.MODE_ANIMATION == "static":
            frame = bpy.context.scene.frame_current
            labels = [obj for obj in bpy.data.objects if 'value_label' in obj.name]
            frame = bpy.context.scene.frame_current

            for i, cube in enumerate([c for c in bpy.data.objects if "cube" in c.name]):
                self.x_pos.append(dict())
                hooks = [h.location[0] for h in cube.children if "Hook" in h.name]
                self.x_pos[i][frame] = max(hooks)
            for i, label in enumerate(labels):
                if frame in self.x_pos[i]:
                    value = "{:.2f}".format(self.x_pos[i][frame] * self.DATA_MAX / 100)
                    label.data.body = value

        if MODE_ANIMATION == "max":
            frame = bpy.context.scene.frame_current
            if frame <= self.MAX_FR:
                max_value = self.all_frames_max[frame]
            upper_limit = cceil(max_value)
            # lower_limit = upper_limit/10

            cur_limits = np.arange(0, upper_limit, upper_limit/4)
            cur_limits[0] = upper_limit
            for limit in cur_limits:
                if limit not in self.limits:
                    self.limits.append(limit)

            for upper_limit in self.limits:
                name = f"upper_limit_{upper_limit}"
                if f"line_{name}" not in bpy.data.objects:
                    self.add_line(name)

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


    def handler_value_label(self, scene, _):
        frame = bpy.context.scene.frame_current
        for i, _ in enumerate(self.cfg.data):
            label = bpy.data.objects[f"value_label_{i}"]
            if frame <= self.MAX_FR:
                label.data.body = "{:.2f}".format(self.all_frames[i][frame])


    def handler_pie(self, scene, _):
        bpy.ops.object.select_all(action='DESELECT')

        # Select the object
        if bpy.data.objects.get("pie_chart") is not None:
            bpy.data.objects['pie_chart'].select_set(True)

        bpy.ops.object.delete()

        self.pie_chart()

        # Select the object
        if bpy.data.objects.get("pie_chart") is not None:
            bpy.data.objects['pie_chart'].select_set(True)
            obj = bpy.data.objects['pie_chart']

        obj = bpy.data.objects['pie_chart']
        frame = bpy.context.scene.frame_current
        # all_frames = get_all_frames()
        # total = get_sum()

        per100 = [floor(self.all_frames[i][frame]/self.SUM[frame] * 100) for i,_ in enumerate(self.cfg.data)]
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

    # import bpy
    # import bmesh

    # obj = bpy.data.objects['pie_chart']
    # obj.data.polygons[20].select = True

    # DATA
    def get_all_frames(self):
        all_frames = []
        for j, bar in enumerate(self.cfg.data):
            all_frames.append([])
            for i, value in enumerate(bar[:-1]):
                next = bar[i+1]
                if value-next == 0.0:
                    per_frame = np.arange(next, value, 0.01/self.cfg.FPS)[::-1]
                elif value >= next:
                    # print(next, value, self.cfg.FPS)
                    per_frame = np.arange(next, value, (value-next)/self.cfg.FPS)[::-1]
                else:
                    per_frame = np.arange(value, next, (next-value)/self.cfg.FPS)
                if not per_frame.any():
                    per_frame = [value] * self.cfg.FPS
                all_frames[j].extend(per_frame)
            all_frames[j].extend([bar[-1]] * self.cfg.FPS)
        return all_frames

    def get_all_frames_max(self):
        all_frames_max = []
        all_frames = self.get_all_frames()
        for frame, value in enumerate(all_frames[0]):
            all_frames_max.append(max([bar[frame] for bar in all_frames]))
        return [i if i != 0.0 else 0.01 for i in all_frames_max]

    def get_all_frames_sum(self):
        all_frames = self.get_all_frames()
        res = []
        for frame in range(0, self.get_LAST_FR()):
            total = sum([all_frames[i][frame] for i, _ in enumerate(self.cfg.data)])
            res.append(total)
        return res

    def get_LAST_FR(self):
        LAST_FR = self.cfg.FPS*len(self.cfg.data[0]) #2 secs(48 frames) worth of animation for each datapoint
        return LAST_FR

    def get_FR(self):
        FR = tuple(range(0, self.get_LAST_FR()+1, self.cfg.FPS))
        return FR

    def get_data(self):
        # if self.data:
        #     return self.data
        return self.cfg.data

    def get_DATA_MAX(self):
        DATA_MAX = max([point for bar in self.cfg.data for point in bar])
        return DATA_MAX

    def get_DATA_MIN(self):
        DATA_MIN = min([point for bar in self.cfg.data for point in bar])
        return DATA_MIN

    def get_constants(self):
        FR = self.get_FR()
        LAST_FR = self.get_LAST_FR()
        all_frames = self.get_all_frames()
        all_frames_max = self.get_all_frames_max()
        SUM_FR = self.get_all_frames_sum()
        MAX_FR = self.get_DATA_MAX()
        MIN_FR = self.get_DATA_MIN()
        return FR, LAST_FR, all_frames, all_frames_max, SUM_FR, MAX_FR, MIN_FR
