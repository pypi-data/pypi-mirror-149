import numpy as np

from blender.default_cfg import DATA, FPS

def get_all_frames(data):
    all_frames = []
    for j, bar in enumerate(data):
        all_frames.append([])
        for i, value in enumerate(bar[:-1]):
            next = bar[i+1]
            if value >= next:
                per_frame = np.arange(next, value, (value-next)/FPS)[::-1]
            else:
                per_frame = np.arange(value, next, (next-value)/FPS)
            if not per_frame.any():
                per_frame = [value] * FPS
            all_frames[j].extend(per_frame)
        all_frames[j].extend([bar[-1]] * FPS)
    return all_frames

def get_all_frames_max(data):
    all_frames_max = []
    all_frames = get_all_frames(data)
    for frame, value in enumerate(all_frames[0]):
        all_frames_max.append(max([bar[frame] for bar in all_frames]))
    return all_frames_max

def get_all_frames_sum(data):
    all_frames = get_all_frames(data)
    res = []
    for frame in range(0, get_LAST_FR(DATA)):
        total = sum([all_frames[i][frame] for i, _ in enumerate(data)])
        res.append(total)
    return res

def get_LAST_FR(data):
    LAST_FR = FPS*len(data[0]) #2 secs(48 frames) worth of animation for each datapoint
    return LAST_FR

def get_FR(data):
    FR = tuple(range(0, get_LAST_FR(DATA)+1, FPS))
    return FR

def get_data(data=None):
    if data:
        return data
    return DATA

def get_DATA_MAX(data):
    DATA_MAX = max([point for bar in DATA for point in bar])
    return DATA_MAX

def get_DATA_MIN(data):
    DATA_MIN = min([point for bar in DATA for point in bar])
    return DATA_MIN

def get_constants(data):
    FR = get_FR(data)
    LAST_FR = get_LAST_FR(data)
    all_frames = get_all_frames(data)
    all_frames_max = get_all_frames_max(data)
    SUM_FR = get_all_frames_sum(data)
    MAX_FR = get_DATA_MAX(data)
    MIN_FR = get_DATA_MIN(data)
    return FR, LAST_FR, all_frames, all_frames_max, SUM_FR, MAX_FR, MIN_FR
