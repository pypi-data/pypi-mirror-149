import numpy as np
import json
import os
from scale_lidar_io import LidarScene, Transform
from .view_utils import open_viewer, open_new_viewer
from .awsHandler import get_secret, get_db_connection, get_signed_url
from bson.objectid import ObjectId
from pyquaternion import Quaternion
import base64
import requests
from .lidarLiteHelper import get_points, get_cameras, combine_scenes

class DebugLidarScene(LidarScene):
    '''
        New Viewer method using open3d, this will work with python 3.8
    '''
    def preview(self, frame_id=None, file=None, aggregated_frames=10):
        if file:
            np.save(file, self.get_all_world_points())
        else:
            return open_new_viewer(self.get_all_world_points(), aggregated_frames)

    def get_all_world_points(self):
        all_points = []
        for idx, frame in enumerate(self.frames):
            points = frame.get_world_points()
            points[:, 3] = idx
            all_points.append(points)
        return all_points

    '''
        This method use PPTK, old Viewer implementation, leaving it here as a fallback
        I'm seing issue with the new viewer on pointclopuds with +150k points, need more testing but just in case I leave this as an alternative
        I've tested this method with 400k pointscloud and it worked fine
        this method will run only on python 3.6.0 (pptk requirement)
    '''
    def preview_motion(self, file=None):
        if file:
            np.save(file, self.get_all_world_points())
        else:
            return open_viewer(np.vstack(self.get_all_world_points()), point_size=0.005)

    '''
        Method to load the task attachments and add the data to the scene
    '''
    def load_task_attachments(self, task_id, attachments, load_images):
        cached = False   # Flag used to create the cache data if necessary.

        if os.path.exists(".cache"): # check for cache folder
            if os.path.exists(os.path.join(".cache", f"{task_id}")): # check for cache folder for this task
                cached = True
            else:
                os.makedirs(os.path.join(".cache", f"{task_id}")) # create a folder per each task
        else:
            os.makedirs(f".cache/{task_id}") # create a folder per each task

        for index, attachment in enumerate(attachments):
            # store in local cache folder if necessary
            if not cached:
                print(f"Loading attachment {index}")
                signed_url = get_signed_url(attachment)
                r = requests.get(signed_url)
                attachment_data = r.json()
                # Load point
                points = np.frombuffer(base64.b64decode(attachment_data['points']), 'float32').reshape([-1, 3])
                intensity = np.frombuffer(base64.b64decode(attachment_data['intensities']), 'float32').reshape([-1, 1])
                points = np.hstack((points,intensity))  # add intensity to the points
                np.save(os.path.join(".cache", f"{task_id}", f"frame-{index}.npy"), points) # save points into file
                del attachment_data['points']   # delete base64 points to store only the calibration data
                del attachment_data['intensities']

                with open(os.path.join(".cache", f"{task_id}", f"calibration-{index}.json"), 'w') as outfile:   # save calibration file
                    json.dump(attachment_data, outfile)

                if load_images: # maybe working on local we don't want to load the images to work faster
                    for camera_index, image in enumerate(attachment_data['images']):
                        print(f"Loading image {camera_index} of {len(attachment_data['images'])}")
                        signed_image = get_signed_url(image['image_url'])
                        r = requests.get(signed_image, stream=True)
                        if r.status_code == 200:
                            with open(os.path.join(".cache", f"{task_id}", f"camera-{camera_index}-{index}.jpg"), 'wb') as f:   # Save camera images
                                for chunk in r:
                                    f.write(chunk)

            # load points and device calibration values
            with open(os.path.join(".cache", f"{task_id}", f"calibration-{index}.json")) as json_file:
                calibration_data = json.load(json_file)
                device_position = list(calibration_data['device_position'].values()) if 'device_position' in calibration_data else list(calibration_data['devicePosition'].values())
                device_transformation = Transform.from_Rt(
                    Quaternion(np.array(list(calibration_data['device_heading'].values())) if 'device_heading' in calibration_data  else [1,0,0,0]),
                    np.array(device_position)
                )
                # load device data
                self.get_frame(index).apply_transform(device_transformation) # add frame transformation
                # load points
                self.get_frame(index).add_points(np.load(os.path.join(".cache", f"{task_id}", f"frame-{index}.npy")), transform=device_transformation.inverse) # need to remove the frame transformation
                if load_images: # maybe working on local we don't want to load the images to work faster
                    if index == 0:  # we calibate the cameras just one time (first frame)
                        with open(os.path.join(".cache", f"{task_id}", f"calibration-{index}.json")) as json_file:
                            calibration_data = json.load(json_file)
                            for camera_index, image in enumerate(calibration_data['images']):
                                distortion = [value for value in [image[key] if key in image.keys() else 0 for key in ['k1', 'k2', 'p1', 'p2', 'k3', 'k4']] ] # sometime we don't have all the cohefficients
                                position = list(image['position'].values())
                                self.get_camera(camera_index).calibrate(
                                        pose= Transform().from_Rt(
                                            Quaternion(image['heading']['w'], image['heading']['x'], image['heading']['y'], image['heading']['z']).rotation_matrix,
                                            np.array([position[0], position[1], position[2]])
                                            ),
                                        K=np.array([ [image['fx'],0,image['cx']],
                                            [0, image['fy'],image['cy']],
                                            [0,0,1]]),
                                        D=distortion,
                                        scale_factor=image['scale_factor'] if 'scale_factor' in image else 1,
                                        skew=image['skew'] if 'skew' in image else 0,
                                        model=image['camera_model'] if 'camera_model' in image else 'brown_conrady')
                                self.get_camera(camera_index).apply_transform(device_transformation.inverse) # need to remove the frame transformation
                    # load camera images
                    for camera_index, image in enumerate(calibration_data['images']):
                        self.get_frame(index).get_image(camera_index).load_file(os.path.join(".cache", f"{task_id}", f"camera-{camera_index}-{index}.jpg"))

    '''
        Method to load a task from a task ID
    '''
    def load_from_task(self, task_id=None, frames=0, load_images=True):
        if task_id:
            print("Connecting to DB")
            self.db = get_db_connection()
            subtasks = self.db['subtasks']
            results = subtasks.find({'task': ObjectId(task_id)})
            for r in results:
                if 'attachments' in r['params']:
                    attachments = r['params']['attachments'][:frames] if frames > 0 else r['params']['attachments'] # limit number of loaded frames
                elif 'full_attachments' in r['params']:
                    attachments = r['params']['full_attachments'][:frames] if frames > 0 else r['params']['full_attachments']
                else:
                    raise RuntimeError(f'Could not find attachments or full_attachments in task {task_id} params')
                print(f"Loading {len(attachments)} frames")
                self.load_task_attachments(task_id, attachments, load_images)
            return self


    def to_bs4(self, path, filename, camera="all"):
        get_points(self, path)
        get_cameras(self, path, camera)

        combine_scenes(camera, path, filename)
