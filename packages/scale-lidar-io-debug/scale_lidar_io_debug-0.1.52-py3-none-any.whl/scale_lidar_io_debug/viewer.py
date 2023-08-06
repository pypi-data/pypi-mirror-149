import numpy as np
import open3d as o3d
import matplotlib.cm as cm
from pyquaternion import Quaternion

class Viewer():
    def __init__(self, points, aggregated_frames):
        self.current_frame = 0
        self.aggregated_frames = int(aggregated_frames/2)
        self.aggregated_mode = False
        self.pcs = [] # list point clouds (one pc per frame)
        colors = cm.rainbow(np.linspace(0, 1, len(points))) # define a rainbow secuence of colors for each frame

        # create pointcloud per frame
        for index in range(0, len(points)):
            #  print(len(points[index]))
            pc = o3d.geometry.PointCloud()
            pc.points = o3d.utility.Vector3dVector(np.array(points[index][:,:3], dtype=np.float32))
            color = np.tile(np.array(colors[index][:3], dtype=np.float32),(len(points[index]),1))
            pc.colors = o3d.utility.Vector3dVector(color)
            self.pcs.append(pc)


        # Define new keybinding here (remember to add them to the help screen)
        self.print_help()
        vis = o3d.visualization.VisualizerWithKeyCallback()
        vis.register_key_callback(ord("P"), self.previous_frame)
        vis.register_key_callback(ord("N"), self.next_frame)
        vis.register_key_callback(ord("A"), self.aggregated_view)
        vis.register_key_callback(ord("T"), self.top_view)
        vis.register_key_callback(ord("S"), self.side_view)
        self.vis = vis
        self.vis.create_window()
        self.set_camera()
        self.vis.run()


    def set_camera(self):
        self.vis.add_geometry(self.pcs[self.current_frame])
        self.vis.add_geometry(o3d.geometry.TriangleMesh.create_sphere().paint_uniform_color(np.array([0,1,0]))) # add car as a green sphere at point [0,0,0]

        opt = self.vis.get_render_option()
        opt.background_color = np.asarray([0, 0, 0]) # background color = black
        opt.show_coordinate_frame = True # show cross with the axis
        opt.point_size = 3.0 # define point size (bigger than this make the scene looks weird)

    def top_view(self, vis):
        cam = self.vis.get_view_control().convert_to_pinhole_camera_parameters()
        pose = np.eye(4)
        pose[:3, :3] = Quaternion(array=np.array([0.0, -1.0, 0.0, 0.0])).rotation_matrix
        pose[:3, 3] = [0, 0, 10]
        cam.extrinsic = pose
        self.vis.get_view_control().convert_from_pinhole_camera_parameters(cam)

    def side_view(self, vis):
        cam = self.vis.get_view_control().convert_to_pinhole_camera_parameters()
        pose = np.eye(4)
        pose[:3, :3] = Quaternion(array=np.array([1.0, 1.0, 0.0, 0.0])).rotation_matrix
        pose[:3, 3] = [0, 0, 10]
        cam.extrinsic = pose
        self.vis.get_view_control().convert_from_pinhole_camera_parameters(cam)


    def next_frame(self, vis):
        if len(self.pcs) > self.current_frame + 1 and not self.aggregated_mode:
            self.current_frame+=1
            self.vis.clear_geometries()
            self.vis.add_geometry(self.pcs[self.current_frame])
            self.set_camera()
            print(f"You are now at frame {self.current_frame}")

    def previous_frame(self, vis):
        if (self.current_frame > 0) and not self.aggregated_mode:
            self.current_frame-=1
            self.vis.clear_geometries()
            self.vis.add_geometry(self.pcs[self.current_frame])
            self.set_camera()
            print(f"You are now at frame {self.current_frame}")

    def aggregated_view(self, vis):
        if self.aggregated_mode: # go out of aggregated mode
            print("aggregated mode - OFF")
            self.vis.clear_geometries()
            self.vis.add_geometry(self.pcs[self.current_frame], True)
            self.aggregated_mode = False
        else: #set aggregated mode on
            print("aggregated mode - ON")
            # display current_frame +/- self.aggregated_frames (default 5) frames if possible
            min_frame = self.current_frame - self.aggregated_frames if self.current_frame - self.aggregated_frames > 0 else 0
            max_frame = self.current_frame + self.aggregated_frames if self.current_frame + self.aggregated_frames < len(self.pcs) else len(self.pcs)
            print(f"Frames {min_frame} to {max_frame}")
            for index in range(min_frame, max_frame):
                self.vis.add_geometry(self.pcs[index], True)
                self.aggregated_mode = True
        self.set_camera()

    def print_help(self):
        print("""
                -- Frame control --
      N : Next frame
      P : Previous frame
      A : Aggregated view (default 10 frames, -/+5 frames from the current frame)
      T : Top view
      S : Side View
      H : Help (more options)

                -- Mouse view control --
      Left button + drag         : Rotate.
      Ctrl + left button + drag  : Translate.
      Wheel button + drag        : Translate.
      Shift + left button + drag : Roll.
      Wheel                      : Zoom in/out.

    -- Keyboard view control --
      [/]          : Increase/decrease field of view.
      R            : Reset view point.
      Ctrl/Cmd + C : Copy current view status into the clipboard.
      Ctrl/Cmd + V : Paste view status from clipboard.

    -- General control --
      Q, Esc       : Exit window.
      H            : Print help message.
      PrtScn       : Take a screen capture.
      D            : Take a depth capture.
      O            : Take a capture of current rendering settings.
                """)
