import bpy
import blender.blenderpy
from blender.blenderpy import Graph

def create(cfg):
    """creates graph based on cfg"""
    graph = Graph(cfg)
    blender.blenderpy.util.delete_all()
    graph.camera()
    graph.light()
    graph.background_plane()

    graph.bars()
    graph.title()
    graph.title_axis()
    graph.materials()
    graph.hooks()
    graph.label_value()
    graph.label_axis(mode="max")
    graph.label_timeframe()
    graph.grid(mode="max")

    #group graph elements
    graph.group_graph()
    graph.group_bars()
    graph.group_value_labels()

    #fixed locations
    graph.loc_fix_labels()

    #add callbacks
    bpy.app.handlers.frame_change_post.extend([graph.handler_bar, graph.handler_timeframe, graph.handler_grid, graph.handler_value_label])
    # bpy.app.handlers.frame_change_post.extend([handler_pie])

    #keyframe inserts
    graph.animate_sorting()
    # graph.move_camera()

    #setup render
    blender.blenderpy.util.set_render_settings()
