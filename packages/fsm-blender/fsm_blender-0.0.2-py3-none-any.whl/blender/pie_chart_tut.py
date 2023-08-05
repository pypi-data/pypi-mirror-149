#Pie Graph Experiment Final Script

#import modules
import bpy, random

#Define a function for cleaning up text objects
def txtCleanup(title):
    bpy.ops.object.text_add(enter_editmode=True) #Generalise this; Done
    [bpy.ops.font.delete(type='PREVIOUS_OR_SELECTION') for j in range(4)]
    [bpy.ops.font.text_insert(text=char) for char in title]
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

#Define data and generate slice labels
data = [0, 0.2, 0.45, 0.13, 0.17, 0.05] ### First value in slice needs to be 0
pieLabels = [str(data[i]*100)+'%' for i in range(len(data))]

#Calculate slice positions and rotations
slice = [data[i]*2*3.14159 for i in range(len(data))] #pi = 3.14159
rot = [-1*(sum(slice[0:i+1])) for i in range(len(slice))]

#Define some cosmetic variables
pieHeight, titleY = 0.5, 2.5
labelZ = pieHeight + 0.05
labelSize, titleSize = 0.25, 1
graphTitle = "Pie Graph"

#Create the overhead title of the pie chart
bpy.context.scene.cursor.location = (0, 0, 0)
txtCleanup(graphTitle)
bpy.data.objects['Text'].location = (0, titleY, 0.2)
bpy.ops.transform.resize(value=(titleSize, titleSize, titleSize))

#Generate slices for pie graph and their labels
for i in range(len(data)-1):
    ### Slices
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.mesh.primitive_plane_add(enter_editmode=False, location=(0, 0, 0)) #New plane
    bpy.ops.transform.resize(value=(pieHeight, 1, 1)) #Scale in x
    bpy.ops.transform.translate(value=(0, 1, 0)) #move up
    bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL')
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN') #set origin
    bpy.context.object.rotation_euler[2] = rot[i] #rotate by the previous calculated angle
    bpy.ops.object.editmode_toggle() #Extrude face
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0)})
    bpy.ops.mesh.spin(steps = 10, angle = slice[i+1], center=(0, 0, 0), axis=(0, 0, 1)) #Spin out

    ### Labels
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.context.scene.cursor.location = bpy.context.object.location
    txtCleanup(str(pieLabels[i+1]))
    bpy.context.object.location = bpy.context.scene.cursor.location
    bpy.context.object.location[2] = labelZ
    bpy.ops.transform.resize(value=(labelSize, labelSize, labelSize))

#Set cursor back to the origin
bpy.context.scene.cursor.location = (0, 0, 0)

#Add material to text
labelMat = bpy.data.materials.new(name='LabelMaterial')
labelMat.diffuse_color=(0, 0, 0, 1)
[bpy.data.objects[obj.name].data.materials.append(labelMat) for obj in bpy.data.objects if "Text" in obj.name]

#Add materials to bars
for obj in bpy.data.objects:
    if 'Plane' in obj.name:
        currentMat = bpy.data.materials.new(name='sliceMat' + obj.name)
        currentMat.diffuse_color=(random.random(), random.random(), random.random(), 1)
        bpy.data.objects[obj.name].data.materials.append(currentMat)
