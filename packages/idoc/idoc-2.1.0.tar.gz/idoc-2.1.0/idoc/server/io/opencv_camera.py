import logging
import os
import os.path
import time
import traceback
import numpy as np
import cv2

from idoc.server.io.cameras import AdaptorCamera

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



class OpenCVCamera(AdaptorCamera):
    r"""
    Drive a Basler camera using pypylon.
    """

    def __init__(self, *args, timeout=5000, video_path=None, **kwargs):

        # TODO Put this stuff in the config
        self._max_failed_count = 10
        self._timeout = timeout
        self._video_path = video_path
        self._is_opened = False
        super().__init__(*args, **kwargs)

    def is_last_frame(self):
        return False

    def _time_stamp(self):
        now = time.time()
        return now - self._start_time

    def is_opened(self):
        return self._is_opened

    def _next_image(self):

        failed_count = 0
        # this while loop is designed to try several times,
        # not to be run continuosly
        # i.e. in normal conditions, it should be broken every time
        # the continously running loop is implemented BaseCamera.__iter__

        while failed_count < self._max_failed_count:

            ret, img = self.camera.read()
            if ret and isinstance(img, np.ndarray):
                break
            else:
                failed_count += 1
        
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        self._validate(img)
        return img

    def open(self):

        try:
            super().open()
            self.camera = cv2.VideoCapture(self._video_path)
            self._is_opened = True
            ret, image = self.camera.read()
            logger.info("OpenCV camera loaded successfully")
            logger.info("Resolution of incoming frames: %dx%d", image.shape[1], image.shape[0])

        except Exception as error:
            logger.error(error)
            logger.error(traceback.print_exc())


    # called by BaseCamera.__exit__()
    def close(self):
        super().close()
        self.camera.release()
        self._is_opened = False


    def restart(self):
        r"""
        Attempt to restart a Basler camera
        """
        NotImplementedError

    @property
    def resolution(self):
        r"""
        Convenience function to return resolution of camera.
        Resolution = (number_horizontal_pixels, number_vertical_pixels)
        """
        width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        self._settings["resolution"] = (width, height)
        return self._settings["resolution"]

    @resolution.setter
    def resolution(self, resolution):
        pass

    @property
    def shape(self):
        r"""
        Convenience function to return shape of camera
        Shape = (number_vertical_pixels, number_horizontal_pixels, number_channels)
        """
        width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

        return (width, height, 1)

    @property
    def framerate(self):
        return self.camera.get(cv2.CAP_PROP_FPS)
