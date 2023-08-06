import logging
import time
from enum import Enum
from threading import Thread

import cv2
import numpy as np
from botcity.base import BaseBot

logger = logging.getLogger(__name__)


class RecorderState(str, Enum):
    """
    Enum for recorder state
    """
    STOPPED = "stopped"
    RECORDING = "recording"
    PAUSED = "paused"


class RecorderCodec(str, Enum):
    """
    Enum for recorder codec
    """
    XVID = "XVID"
    MJPG = "MJPG"


class BotRecorderPlugin(Thread):
    """A video recorder for your BotCity bot.

    Args:
        bot (BaseBot): The bot to record.
        output_file (str): The file to save the video to.
    """

    def __init__(self, bot: BaseBot, output_file: str = "output.avi", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._bot = bot
        self._interrupted = False
        self._state = RecorderState.STOPPED
        self._codec = RecorderCodec.MJPG
        self._video_writer = None
        self._last_frame_time = 0
        self._output_file = output_file

        self._frame_rate = 5
        self._scale = 100

    @property
    def frame_rate(self) -> int:
        """Frame rate of the recorder.

        Returns:
            int: Frame rate of the recorder in frames per second.
        """
        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self, value: int):
        """Set the frame rate of the recorder.

        Args:
            value (int): Frame rate of the recorder in frames per second.
        """
        self._frame_rate = value

    @property
    def scale(self) -> int:
        """Scale of the recorder.

        Returns:
            int: Scale of the recorder in percent.
        """
        return self._scale

    @scale.setter
    def scale(self, value: int):
        """Set the scale of the recorder.

        Args:
            value (int): Scale of the recorder in percent.
        """
        self._scale = value

    @property
    def state(self) -> RecorderState:
        """Get the recorder state.

        Returns:
            RecorderState: Recorder state.
        """
        return self._state

    def pause(self):
        """Pause the recorder."""
        if self._state == RecorderState.RECORDING:
            self._state = RecorderState.PAUSED

    def resume(self):
        """Resume the recorder."""
        if self._state == RecorderState.PAUSED:
            self._state = RecorderState.RECORDING

    def stop(self):
        """Stop the recorder."""
        if self._state != RecorderState.STOPPED:
            self._state = RecorderState.STOPPED
            self._interrupted = True

    def start(self):
        """Start the recorder."""
        if self._state == RecorderState.STOPPED:
            self._state = RecorderState.RECORDING
            super().start()

    def _get_frame(self):
        try:
            frame = self._bot.get_screenshot()
            # frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
            frame = np.array(frame)
            if self.scale != 100:
                # calculate the scale percent of original dimensions
                width = int(frame.shape[1] * self.scale/100)
                height = int(frame.shape[0] * self.scale/100)
                # dsize
                dsize = (width, height)
                # resize image
                frame = cv2.resize(frame, dsize)
        except Exception:
            frame = None
        return frame

    def _try_setup_writer(self):
        frame = self._get_frame()
        if frame is None:
            return False
        w = frame.shape[1]
        h = frame.shape[0]
        self._video_writer = cv2.VideoWriter(
            self._output_file,  # filename
            cv2.VideoWriter_fourcc(*self._codec.value),  # fourcc
            self.frame_rate,  # fps
            (w, h)  # frame size
        )

        self._video_writer.write(frame)
        return True

    def run(self) -> None:
        while not self._interrupted:
            if self._state == RecorderState.RECORDING:
                if not self._video_writer:
                    self._try_setup_writer()
                else:
                    frame = self._get_frame()
                    cv_img = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
                    self._video_writer.write(cv_img)

            sleep_time = 1 / self._frame_rate
            sleep_time = sleep_time - (time.time() - self._last_frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                logger.warn("Recorder: Frame rate is too high!")
            self._last_frame_time = time.time()

        self._state = RecorderState.STOPPED
        if self._video_writer:
            self._video_writer.release()
            self._video_writer = None
