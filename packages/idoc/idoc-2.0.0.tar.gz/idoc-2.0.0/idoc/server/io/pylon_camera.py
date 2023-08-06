import logging
import warnings
import time
import traceback

from pypylon import pylon
import cv2

from idoc.server.io.cameras import AdaptorCamera

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



class PylonCamera(AdaptorCamera):
    r"""
    Drive a Basler camera using pypylon.
    """

    def __init__(self, *args, timeout=5000, video_path=None, **kwargs):

        # TODO Put this stuff in the config
        self._max_failed_count = 10000
        self._timeout = timeout
        self._video_path = video_path
        super().__init__(*args, **kwargs)

    def is_last_frame(self):
        return False

    def _time_stamp(self):
        now = time.time()
        return now - self._start_time

    def is_opened(self):
        return self.camera.IsOpen()

    def _next_image(self):

        failed_count = 0
        # this while loop is designed to try several times,
        # not to be run continuosly
        # i.e. in normal conditions, it should be broken every time
        # the continously running loop is implemented BaseCamera.__iter__

        while self.camera.IsGrabbing():

            grab = self._grab()
            if grab.GrabSucceeded():
                # logger.debug("grab succeeded")
                img = grab.Array
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                self._validate(img)
                if failed_count != 0:
                    logger.warning(f"Pylon has recovered. Frame retrieval continues")
                    failed_count=0
                return img
            else:
                logger.warning(f"Pylon could not fetch next frame. Trial no {failed_count}/{self._max_failed_count}")
                failed_count += 1
                if failed_count == self._max_failed_count:
                    template = "Tried reading next frame %d times and none worked. Exiting."
                    message = template % self._max_failed_count
                    logger.warning(message)
                    self.close()
                    return None

    def open(self):

        try:
            super().open()
            logger.debug("Initializing camera")
            self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            logger.debug("Opening camera")
            self.camera.Open()
            # Print the model name of the camera.
            logger.info("Using device %s", self.camera.GetDeviceInfo().GetModelName())
            # self.camera.StartGrabbingMax(100) # if we want to limit the number of frames
            self.camera.MaxNumBuffer = 5
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            grab_result = self.camera.RetrieveResult(self._timeout, pylon.TimeoutHandling_ThrowException)
            image = grab_result.Array
            logger.info("Pylon camera loaded successfully")
            logger.info("Resolution of incoming frames: %dx%d", image.shape[1], image.shape[0])

        except Exception as error:
            logger.error(error)
            logger.error(traceback.print_exc())
            self.reset()


    # called by BaseCamera.__exit__()
    def close(self):
        super().close()
        logger.debug("Closing camera")
        self.camera.Close()


    def restart(self):
        r"""
        Attempt to restart a Basler camera
        """
        NotImplementedError


    def _grab(self):
        try:
            grab_result = self.camera.RetrieveResult(self._timeout, pylon.TimeoutHandling_ThrowException)
            return grab_result

        # TODO Use right exception
        except Exception as error:  # pylint: disable=broad-except
            logger.warning("Error in _grab method")
            logger.warning(traceback.print_exc())
            logger.warning(error)
            return


    @property
    def resolution(self):
        r"""
        Convenience function to return resolution of camera.
        Resolution = (number_horizontal_pixels, number_vertical_pixels)
        """
        self._settings["resolution"] = (self.camera.Width.GetValue(), self.camera.Height.GetValue())
        return self._settings["resolution"]



    @property
    def shape(self):
        r"""
        Convenience function to return shape of camera
        Shape = (number_vertical_pixels, number_horizontal_pixels, number_channels)
        """
        # TODO Return number of channels!
        return (self.camera.Height.GetValue(), self.camera.Width.GetValue(), 1)

    @property
    def framerate(self):
        try:
            return self.camera.AcquisitionFrameRateAbs.GetValue()
        except Exception:
            try:
                return self.camera.AcquisitionFrameRate.GetValue()
            except Exception:
                warnings.warn(
                    f"{self} camera doesn't have AcquisitionFrameRate or AcquisitionFrameRateAbs" \
                    "Please update the {self.__class__}.framerate property. I will assume 30"
                )
                return 30
        
