import numpy as np
from .viewer import Viewer

def open_new_viewer(points, aggregated_frames):
    viewer = Viewer(points, aggregated_frames)
    return viewer

def open_viewer(points, point_size=0.005):
    import pptk
    v = pptk.viewer(points[:, :3], points[:, 3])
    v.set(
        point_size=point_size,
        floor_level=0.0,
        phi=np.pi,
        theta=np.pi / 2,
        lookat=[0, 0, 0],
        r=50
    )
    # v.wait()
    return v


def load_points(viewer, points, point_size=0.005):
    viewer.load(points[:, :3], points[:, 3])
    viewer.set(
        point_size=point_size,
        floor_level=0.0,
        phi=np.pi,
        theta=np.pi / 2,
        lookat=[0, 0, 0],
        r=50
    )
    return viewer
