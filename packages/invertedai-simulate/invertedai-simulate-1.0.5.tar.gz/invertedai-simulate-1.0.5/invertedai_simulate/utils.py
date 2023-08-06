import collections
from typing import Tuple, Optional
from skimage.draw import line_aa
import logging
import pygame
import numpy as np
import cv2

logger = logging.getLogger(__name__)

Resolution = collections.namedtuple('Resolution', ['width', 'height'])

BB_COLOR_DICT = {
    'vehicles': (15, 3, 252),
    'pedestrians': (252, 186, 3),
    'traffic-lights': (252, 3, 3),
    'parked_vehicles': (15, 3, 252),
}
BB_COLOR = (248, 64, 24)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.3
FONT_COLOR = (255, 0, 0)
FONT_THICKNESS = 1


class ControllerNoiseType:
    UNIFORM = "uniform"
    TEMPORAL = "temporal"


class Res:
    """
    Some commonly used resolutions.
    """
    DEFAULT = Resolution(1280, 720)
    CIL = Resolution(200, 88)
    BIRDVIEW = Resolution(256, 256)
    SD = Resolution(640, 480)
    MD = Resolution(320, 240)


class SensorSettings:
    Available_Sensors = ['camera']
    Available_Camera_types = ['rgb-camera', 'segmentation', 'depth-camera']
    Location = collections.namedtuple('Location', ['x', 'y', 'z'])
    Rotation = collections.namedtuple('Rotation', ['yaw', 'pitch', 'roll'])
    Resolution = collections.namedtuple('Resolution', ['width', 'height'])
    Available_Tracked_Actors = ['vehicles', 'pedestrians', 'traffic-lights', 'parked_vehicles']
    Available_Reference_Frame = ['carla']  # 'opendrive', 'geolocation' will be added
    Default_Settings = {
        'camera': {
            'sensor_type': 'camera',
            'camera_type': 'rgb-camera',
            'bounding_box': True,
            'track_actor_types': Available_Tracked_Actors,  # or 'all'
            'show_bounding_boxes': True,
            'world_sensor': False,
            'location': Location(x=1.6, z=1.7, y=0),
            'rotation': Rotation(yaw=0, pitch=0, roll=0),
            'resolution': Resolution(200, 88),
            'fov': 90.0,
        },
        'boundingbox': {
            'sensor_type': 'boundingbox',
            'track_actor_types': Available_Tracked_Actors,  # or 'all'
            'world_sensor': False,
            'location': Location(x=0, z=0, y=0),
            'rotation': Rotation(yaw=0, pitch=0, roll=0),
            'frame_of_reference': 'carla',
            # if world_sensor=True returns coordinated based on either 'carla', 'opendrive', 'geolocation'
            'attach_to_actor': 'ego',
            'radius': 100000,  # If not specified all world is considered
            'occlusion': False,
        },
    }


# ==============================================================================
# -- ClientSideBoundingBoxes ---------------------------------------------------
# ==============================================================================


class ClientSideBoundingBoxes(object):
    """
    This is a module responsible for creating 3D bounding boxes and drawing them
    client-side on pygame surface.
    """

    @staticmethod
    def make_calibration(fov, size_x, size_y):
        f = size_x / (2 * np.tan(fov * np.pi / 360.))
        cx0 = size_x / 2
        cy0 = size_y / 2
        return np.array([[f, 0.0, cx0],
                         [0.0, f, cy0],
                         [0.0, 0.0, 1.0], ])

    @staticmethod
    def get_2d_bbox(actor_tracks, sensor_location, sensor_rotation, fov, res, car_location, car_rotation,
                    coordinate_system='carla', occlusion=False):
        # world location and rotaion of the sensor
        # position of the car must be taken into account
        bb2d = {}
        if coordinate_system == 'carla':
            sensor_matrix = ClientSideBoundingBoxes.get_transform_matrix(sensor_location, sensor_rotation)
            vehicle_world_matrix = ClientSideBoundingBoxes.get_transform_matrix(car_location, car_rotation)
            sensor_world_matrix = np.dot(vehicle_world_matrix, sensor_matrix)
            world_sensor_matrix = np.linalg.inv(sensor_world_matrix)
        elif coordinate_system == 'ego':
            sensor_matrix = ClientSideBoundingBoxes.get_transform_matrix(sensor_location, sensor_rotation)
            world_sensor_matrix = np.linalg.inv(sensor_matrix)
        else:
            world_sensor_matrix = np.eye(4)

        calibration = ClientSideBoundingBoxes.make_calibration(float(fov), float(res.width), float(res.height))
        for actor_type in actor_tracks:
            actor_type_tracks = actor_tracks[actor_type]
            bb2d[actor_type] = {}
            for actor_id in actor_type_tracks:
                track = actor_type_tracks[actor_id]['cords']
                cords_x_y_z = np.matrix(np.dot(world_sensor_matrix, track)[:3, :])
                cords_y_minus_z_x = np.concatenate([cords_x_y_z[1, :], -cords_x_y_z[2, :], cords_x_y_z[0, :]])
                bbox = np.transpose(np.dot(calibration, cords_y_minus_z_x))
                camera_bbox = np.concatenate([bbox[:, 0] / bbox[:, 2], bbox[:, 1] / bbox[:, 2], bbox[:, 2]], axis=1)
                if all(camera_bbox[:, 2] > 0):
                    bb2d[actor_type][actor_id] = {}
                    bb2d[actor_type][actor_id]['cords'] = camera_bbox
                    if occlusion:
                        bb2d[actor_type][actor_id]['occlusion'] = actor_type_tracks[actor_id]['occlusion']
        return bb2d

    @staticmethod
    def get_transform_matrix(location, rotation):
        """
        Creates matrix from carla transform.
        """
        c_y = np.cos(np.radians(rotation.yaw))
        s_y = np.sin(np.radians(rotation.yaw))
        c_r = np.cos(np.radians(rotation.roll))
        s_r = np.sin(np.radians(rotation.roll))
        c_p = np.cos(np.radians(rotation.pitch))
        s_p = np.sin(np.radians(rotation.pitch))
        matrix = np.matrix(np.identity(4))
        matrix[0, 3] = location.x
        matrix[1, 3] = location.y
        matrix[2, 3] = location.z
        matrix[0, 0] = c_p * c_y
        matrix[0, 1] = c_y * s_p * s_r - s_y * c_r
        matrix[0, 2] = -c_y * s_p * c_r - s_y * s_r
        matrix[1, 0] = s_y * c_p
        matrix[1, 1] = s_y * s_p * s_r + c_y * c_r
        matrix[1, 2] = -s_y * s_p * c_r + c_y * s_r
        matrix[2, 0] = s_p
        matrix[2, 1] = -c_p * s_r
        matrix[2, 2] = c_p * c_r
        return matrix

    @staticmethod
    def get_matrix(transform):
        """
        Creates matrix from carla transform.
        """

        rotation = transform.rotation
        location = transform.location
        c_y = np.cos(np.radians(rotation.yaw))
        s_y = np.sin(np.radians(rotation.yaw))
        c_r = np.cos(np.radians(rotation.roll))
        s_r = np.sin(np.radians(rotation.roll))
        c_p = np.cos(np.radians(rotation.pitch))
        s_p = np.sin(np.radians(rotation.pitch))
        matrix = np.matrix(np.identity(4))
        matrix[0, 3] = location.x
        matrix[1, 3] = location.y
        matrix[2, 3] = location.z
        matrix[0, 0] = c_p * c_y
        matrix[0, 1] = c_y * s_p * s_r - s_y * c_r
        matrix[0, 2] = -c_y * s_p * c_r - s_y * s_r
        matrix[1, 0] = s_y * c_p
        matrix[1, 1] = s_y * s_p * s_r + c_y * c_r
        matrix[1, 2] = -s_y * s_p * c_r + c_y * s_r
        matrix[2, 0] = s_p
        matrix[2, 1] = -c_p * s_r
        matrix[2, 2] = c_p * c_r
        return matrix

    @staticmethod
    def draw_bounding_boxes_on_array(img, actor_tracks, draw2d=False, occlusion=False):
        """
        Draws bounding boxes on the given image from the camera.
        """
        height, width, _ = img.shape
        for actor_type in actor_tracks:
            actor_type_tracks = actor_tracks[actor_type]
            BB_COLOR = BB_COLOR_DICT[actor_type]
            # for ind, track in enumerate(actor_type_tracks):
            for track_id in actor_type_tracks:
                # breakpoint()
                # if tracks:
                track = actor_type_tracks[track_id]['cords'].astype(int)
                track[:, 0] = np.clip(track[:, 0], 0, width - 1).astype(int)  # TODO: BUG: Squashes the bboxes to edges
                track[:, 1] = np.clip(track[:, 1], 0, height - 1).astype(int)
                rmin = np.min(track[:8, 1])
                rmax = np.max(track[:8, 1])
                cmin = np.min(track[:8, 0])
                cmax = np.max(track[:8, 0])
                if draw2d:
                    rr, cc, val = line_aa(rmin, cmin, rmin, cmax)
                    # img[rr, cc] = (255, 255, 255)
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(rmin, cmin, rmax, cmin)
                    # img[rr, cc] = (255, 255, 255)
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(rmax, cmin, rmax, cmax)
                    # img[rr, cc] = (255, 255, 255)
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(rmin, cmax, rmax, cmax)
                    # img[rr, cc] = (255, 255, 255)
                    img[rr, cc] = BB_COLOR

                    # Inner BOX
                    # rmax = np.min(track[:4, 1])
                    # rmin = np.max(track[4:8, 1])
                    # right = np.max(track[[0,3,4,7], 0])
                    # left = np.min(track[[1,2,5,6], 0])
                    # cmin = min(right, left)
                    # cmax = max(right, left)
                    # # cmin = np.min(track[:8, 0])
                    # # cmax = np.max(track[:8, 0])
                    # rr, cc, val = line_aa(rmin, cmin, rmin, cmax)
                    # img[rr, cc] = (0, 0, 0)
                    # rr, cc, val = line_aa(rmin, cmin, rmax, cmin)
                    # img[rr, cc] = (0, 0, 0)
                    # rr, cc, val = line_aa(rmax, cmin, rmax, cmax)
                    # img[rr, cc] = (0, 0, 0)
                    # rr, cc, val = line_aa(rmin, cmax, rmax, cmax)
                    # img[rr, cc] = (0, 0, 0)

                else:
                    # Base
                    rr, cc, val = line_aa(track[0, 1], track[0, 0], track[1, 1], track[1, 0])
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(track[1, 1], track[1, 0], track[2, 1], track[2, 0])
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(track[2, 1], track[2, 0], track[3, 1], track[3, 0])
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(track[3, 1], track[3, 0], track[0, 1], track[0, 0])
                    img[rr, cc] = BB_COLOR
                    # top
                    rr, cc, val = line_aa(track[4, 1], track[4, 0], track[5, 1], track[5, 0])
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(track[5, 1], track[5, 0], track[6, 1], track[6, 0])
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(track[6, 1], track[6, 0], track[7, 1], track[7, 0])
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(track[7, 1], track[7, 0], track[4, 1], track[4, 0])
                    img[rr, cc] = BB_COLOR
                    # base-top
                    rr, cc, val = line_aa(track[0, 1], track[0, 0], track[4, 1], track[4, 0])
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(track[1, 1], track[1, 0], track[5, 1], track[5, 0])
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(track[2, 1], track[2, 0], track[6, 1], track[6, 0])
                    img[rr, cc] = BB_COLOR
                    rr, cc, val = line_aa(track[3, 1], track[3, 0], track[7, 1], track[7, 0])
                    img[rr, cc] = BB_COLOR
                if occlusion:
                    occlusion_ratio = actor_type_tracks[track_id]['occlusion']
                    img = cv2.putText(img, f'{occlusion_ratio:.0f}', (cmin, rmin), FONT, FONT_SCALE, BB_COLOR,
                                      FONT_THICKNESS, cv2.LINE_AA)
        return img


class NotSpawnedError(RuntimeError):
    """
    Indicates an attempt to use a sensor that is not instantiated in any world.
    """
    pass


class Display:
    """
    Base class for displays that does nothing with received image.

    :param res: Resolution of this display.
    :type res: :class:`Res`
    """

    def __init__(self, res: Resolution = Res.DEFAULT):
        self.res = res
        self.feed = None
        self.stopped = False

    def render(self, array: np.ndarray, offset: Tuple[int, int] = (0, 0)) -> None:
        """
        Process the provided camera image.

        :param array: Height by width by 3 (RGB color channels) image array.
        :param offset: Position of the top left corner in screen coordinates to start rendering from.
            Subclasses may ignore it if not supported.
        :type array: np.array of np.uint8
        """
        pass

    def start(self) -> None:
        """
        Restart the display, reconnecting to last used camera.
        """
        if self.stopped:
            if self.feed is not None:
                self.feed.attach_display(self)
                self.stopped = False
            else:
                logger.debug("Display not connected to feed, can not start")
        else:
            logger.debug("Display already started")

    def stop(self) -> None:
        """
        Stop the display, remembering the camera connected to
        but disconnecting from it.
        """
        if not self.stopped:
            if self.feed is not None:
                self.feed.detach_display(self)
            self.stopped = True
        else:
            logger.debug("Display already stopped")

    def attach_to(self, feed) -> None:
        """
        Attach to a specific camera.

        :param feed: Camera to attach to.
        :type feed: :class:`sensors.Camera`
        """

        self.detach()
        feed.attach_display(self)
        self.feed = feed

    def detach(self) -> None:
        """
        Detach from the camera and stop displaying.
        """

        if self.feed is not None:
            try:
                self.feed.detach_display(self)
            except RuntimeError:
                # If the feed is already destroyed
                pass
            self.feed = None

    def resize(self, res: Resolution) -> None:
        """
        Change own resolution and reconnect to the camera,
        so it can adjust the images sent.

        :param res: New resolution.
        :type res: :class:`Res`
        """
        if self.feed is None:
            raise NotSpawnedError()
        else:
            feed = self.feed
            self.detach()
            self.res = res
            self.attach_to(feed)

    def destroy(self) -> None:
        """
        Disconnect from camera and close self.
        Can't be restarted after destroying.
        """
        self.detach()

    def close(self) -> None:
        self.destroy()

    def intercept_event(self, event: pygame.event) -> bool:
        return False


class SplitScreen(Display):
    """
    A split screen display uses a part of a larger display.
    Can only be used on displays that allow rendering with offset.

    :param res: Resolution of this display.
    :type res: :class:`Res`
    :param offset: Left right corner of this display in pixels of parent display.
    :type offset: (int, int)
    :param parent: Larger display to use a part of.
    :type parent: :class:`Display`
    """

    def __init__(self, res: Resolution, offset: Tuple[int, int], parent: Display):
        super().__init__(res)
        self.offset = offset
        self.parent = parent

    def render(self, array: np.ndarray, offset: Tuple[int, int] = (0, 0)) -> None:
        offset = (offset[0] + self.offset[0], offset[1] + self.offset[1])
        self.parent.render(array, offset)

    def intercept_event(self, event: pygame.event) -> bool:
        return self.parent.intercept_event(event)


class PyGameWindow(Display):
    """
    PyGame window displayed on the monitor. Using fake display with pygame
    will make it invisible. The window is necessary to capture key strokes.
    """

    def __init__(self, res: Resolution = Res.DEFAULT, fullscreen: bool = False):

        super(PyGameWindow, self).__init__(res)
        self.fullscreen = fullscreen
        self.display_flags = pygame.RESIZABLE
        self.fullscreen_flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN

        self.display: Optional[pygame.Surface] = None
        self.set_display()

    def set_display(self) -> None:
        self.display = pygame.display.set_mode(
            self.res, self.fullscreen_flags if self.fullscreen else self.display_flags
        )

    def render(self, array: np.ndarray, offset: Tuple[int, int] = (0, 0)) -> None:
        if self.display is not None:
            surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
            self.display.blit(surface, offset)

    def resize(self, res: Resolution) -> None:
        """
        Resize to new resolution. Underlying PyGame implementation is not
        very reliable.
        """
        super().resize(res)
        self.set_display()

    def intercept_event(self, event: pygame.event) -> bool:
        """
        Intercepts window resizing events.
        """
        if event.type == pygame.VIDEORESIZE:
            res = Resolution(event.w, event.h)
            self.resize(res)
            return True
        return False

    def split_screen(self, res: Resolution, offset: Tuple[int, int]) -> SplitScreen:
        """
        Create a smaller screen from a part of this one.
        """
        screen = SplitScreen(res, offset, self)
        return screen
