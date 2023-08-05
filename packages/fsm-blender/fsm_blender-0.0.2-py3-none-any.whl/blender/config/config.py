# import blender.blenderpy
import pandas as pd
import pickle

import blender
from blender.default_cfg import *

class Config:
    def __init__(self):
        self._data = DATA
        self._MODE_ANIMATION = "max"
        self._barLabels = barLabels
        self._tickLabels = tickLabels
        self._barHeight = barHeight
        self._graphTitle = graphTitle
        self._xAxisTitle = xAxisTitle
        self._yAxisTitle = yAxisTitle
        ###
        self._Gridx = Gridx
        self._Gridy = Gridy
        self._labelSize = labelSize
        self._tickSize = tickSize
        self._titleSize = titleSize
        self._axisTitleSize = axisTitleSize
        self._barThick = barThick
        self._nsubs = nsubs
        self._nxlabels = len(tickLabels)
        self._nylabels = len(barLabels)
        self._t = t

        self._step = Gridy/(nylabels +1)
        self._tickStep = Gridx/(nxlabels-1)
        self._barLocation = [-1*(Gridy/2)+(k*step) for k in range(1, nylabels+1)] #Actual y coords of bars
        self._xLabelHeight = -1*(Gridy/2)-1.4
        self._labelLocx = labelLocx

        self._LABEL_TIME_LOC = LABEL_TIME_LOC
        self._CAM_LOC = CAM_LOC
        self._GRID_LINE_HEIGHT = GRID_LINE_HEIGHT

        self._SPEED_SORT = SPEED_SORT
        self._FONT = FONT
        self._COLOR_PALETTE = COLOR_PALETTE
        self._FPS = FPS

    @property
    def MODE_ANIMATION(self):
        return self._MODE_ANIMATION

    @property
    def barLabels(self):
        return self._barLabels

    @property
    def graphTitle(self):
        return self._graphTitle

    @property
    def FPS(self):
        return self._FPS

    @property
    def COLOR_PALETTE(self):
        return self._COLOR_PALETTE

    @property
    def FONT(self):
        return self._FONT

    @property
    def SPEED_SORT(self):
        return self._SPEED_SORT

    @property
    def GRID_LINE_HEIGHT(self):
        return self._GRID_LINE_HEIGHT

    @property
    def CAM_LOC(self):
        return self._CAM_LOC

    @property
    def LABEL_TIME_LOC(self):
        return self._LABEL_TIME_LOC

    @property
    def labelLocx(self):
        return self._labelLocx

    @property
    def xLabelHeight(self):
        return self._xLabelHeight

    @property
    def barLocation(self):
        return self._barLocation

    @property
    def tickStep(self):
        return self._tickStep

    @property
    def step(self):
        return self._step

    @property
    def t(self):
        return self._t

    @property
    def nylabels(self):
        return self._nylabels

    @property
    def nxlabels(self):
        return self._nxlabels

    @property
    def nsubs(self):
        return self._nsubs

    @property
    def barThick(self):
        return self._barThick

    @property
    def axisTitleSize(self):
        return self._axisTitleSize

    @property
    def titleSize(self):
        return self._titleSize

    @property
    def tickSize(self):
        return self._tickSize

    @property
    def labelSize(self):
        return self._labelSize

    @property
    def data(self):
        return self._data

    @property
    def Gridx(self):
        return self._Gridx

    @property
    def Gridy(self):
        return self._Gridy

    @property
    def barHeight(self):
        return self._barHeight

    @property
    def xAxisTitle(self):
        return self._xAxisTitle

    @property
    def yAxisTitle(self):
        return self._yAxisTitle

    @data.setter
    def data(self, value):
        self._data = value

    @MODE_ANIMATION.setter
    def MODE_ANIMATION(self, value):
        self._MODE_ANIMATION = value

    @graphTitle.setter
    def graphTitle(self, value):
        self._graphTitle = value

    @barHeight.setter
    def barHeight(self, value):
        self._barHeight = value

    @xAxisTitle.setter
    def xAxisTitle(self, value):
        self._xAxisTitle = value

    @yAxisTitle.setter
    def yAxisTitle(self, value):
        self._yAxisTitle = value

    @FPS.setter
    def FPS(self, value):
        self._FPS = value

    @COLOR_PALETTE.setter
    def COLOR_PALETTE(self, value):
        self._COLOR_PALETTE = value

    @FONT.setter
    def FONT(self, value):
        self._FONT = value

    @SPEED_SORT.setter
    def SPEED_SORT(self, value):
        self._SPEED_SORT = value

    @GRID_LINE_HEIGHT.setter
    def GRID_LINE_HEIGHT(self, value):
        self._GRID_LINE_HEIGHT = value

    @CAM_LOC.setter
    def CAM_LOC(self, value):
        self._CAM_LOC = value

    @LABEL_TIME_LOC.setter
    def LABEL_TIME_LOC(self, value):
        self._LABEL_TIME_LOC = value

    @labelLocx.setter
    def labelLocx(self, value):
        self._labelLocx = value

    @xLabelHeight.setter
    def xLabelHeight(self, value):
        self._xLabelHeight = value

    @barLocation.setter
    def barLocation(self, value):
        self._barLocation = value

    @tickStep.setter
    def tickStep(self, value):
        self._tickStep = value

    @step.setter
    def step(self, value):
        self._step = value

    @t.setter
    def t(self, value):
        self._t = value

    @barLabels.setter
    def barLabels(self, value):
        self._barLabels = value

    @nylabels.setter
    def nylabels(self, value):
        self._nylabels = value

    @nxlabels.setter
    def nxlabels(self, value):
        self._nxlabels = value

    @nsubs.setter
    def nsubs(self, value):
        self._nsubs = value

    @barThick.setter
    def barThick(self, value):
        self._barThick = value

    @axisTitleSize.setter
    def axisTitleSize(self, value):
        self._axisTitleSize = value

    @titleSize.setter
    def titleSize(self, value):
        self._titleSize = value

    @tickSize.setter
    def tickSize(self, value):
        self._tickSize = value

    @labelSize.setter
    def labelSize(self, value):
        self._labelSize = value

    @Gridy.setter
    def Gridy(self, value):
        self._Gridy = value

    @Gridx.setter
    def Gridx(self, value):
        self._Gridx = value

    def read_csv(self, csv_file):
        df = pd.read_csv(csv_file, index_col=0)
        self.barLabels = [col for col in df]
        data = []
        for i in range(df.shape[1]-1):
            data.append([value for value in df.iloc[:,i]])
        self.data = data

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def from_pickle(cls, filename):
        with open(filename, "rb") as f:
            new_cfg = pickle.load(f)
        return new_cfg


# import blender
# import bpy

# from mathutils import Vector, Matrix
# from math import floor

# from blender import cfg
# from blender.data import *
# from blender.handler import *

# MODE_ANIMATION = cfg.MODE_ANIMATION

# def main():
#     #setup graph elements
#     blender.util.delete_all()
#     blender.graph.camera()
#     blender.graph.light()
#     blender.graph.background_plane()
#     blender.graph.bars()
#     blender.graph.title()
#     blender.graph.title_axis()
#     blender.graph.materials()
#     blender.graph.hooks()
#     blender.graph.label_value()
#     blender.graph.label_axis(mode=MODE_ANIMATION)
#     blender.graph.label_timeframe()
#     blender.graph.grid(mode=MODE_ANIMATION)

#     #group graph elements
#     blender.graph.group_graph()
#     blender.graph.group_bars()
#     blender.graph.group_value_labels()

#     #fixed locations
#     blender.graph.loc_fix_labels()

#     #add callbacks
#     bpy.app.handlers.frame_change_post.extend([handler_bar, handler_timeframe, handler_grid, handler_value_label])

#     #keyframe inserts
#     blender.graph.animate_sorting()
#     blender.graph.move_camera()

#     #setup render
#     blender.util.set_render_settings()
