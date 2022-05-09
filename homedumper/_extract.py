from typing import List
import cv2
import pathlib
import logging
import numpy.typing as npt
from homedumper.const import DEFAULT_OUT


class FrameExtractor:
    """
    Class for extracting different frames from a video.
    """

    def __init__(self, video_path: str, out_path: str = DEFAULT_OUT):

        # Ensure video path and output path are valid and get Path objects
        if not self._digest_paths(video_path, out_path):
            raise ValueError("Invalid video path")
        self.frame_count = 1
        self.processed_frames: List[npt.ArrayLike] = []

    def _digest_paths(self, video_path: str, output_path: str = DEFAULT_OUT) -> bool:
        """
        Digests the video path and output path into a tuple of Path objects.
        Creates the output path if it doesn't exist and returns False if the 
        video path doesn't exist or is a folder.

        Parameters
        ----------
        video_path : str
                String describing the video path
        output_path : str, optional
                String describing the output path, by default DEFAULT_OUT
        """

        # Check if video path exists and is a file
        video_path_obj = pathlib.Path(video_path)
        if not video_path_obj.exists() or video_path_obj.is_dir():
            logging.error(f"Invalid video path: {video_path_obj.absolute()}")
            return False

        # Create a path object for the output
        output_path_obj = pathlib.Path(output_path)

        # Append video name to output path
        output_path_obj = output_path_obj / video_path_obj.stem / "frames"

        # Create output path if it doesn't exist
        output_path_obj.mkdir(parents=True, exist_ok=True)

        self.video_path = video_path_obj
        self.output_path = output_path_obj
        return True

    def extract_frames(self) -> int:
        """
        Extracts frames from the video and saves them to the output path only
        if they are unique.

        Returns
        -------
        int
            Number of frames extracted
        """

        # Create output path if it doesn't exist
        cap = cv2.VideoCapture(str(self.video_path))

        # Retreive each frame from the video and process it
        while True:
            # Retrieve frame
            ret, frame = cap.read()

            # If the frame is empty, break
            if not ret:
                return self.frame_count - 1

            self.process_frame(frame, self.output_path)

    def _is_stable(self, frame: npt.NDArray, threshold: int = 10) -> bool:
        """
        Checks if the frame is stable by inspecting if the
        animation caused by pressing either L or R buttons is not present
        in the frame. This can be done by checking the color of the regions of
        the frame that indicate when one of those buttons are pressed.

        Parameters
        ----------
        frame : npt.ArrayLike
            Image frame to analyze
        threshold : int, optional
            Threshold for the color difference of the regions to be considered
            stable, by default 10

        Returns
        -------
        bool
            True if the frame is stable (Not a transient of movement)
        """

        # Defines the regions of the frame to be checked
        regions = {
            "R": frame[74:103, 513:533],
            "L": frame[74:103, 121:141],
        }

        # Define the color of the stable condition
        target_color = [167, 180, 31]

        # Check if the regions are stable
        for region in regions.values():

            # Retrieve the average value of the region's red channel
            red_channel = region[:, :, 2]
            avg = red_channel.mean()

            # Check if the region is not stable
            if abs(avg - target_color[2]) > threshold:
                return False

        # If all regions are stable, return True
        return True

    def _is_not_duplicate(self, frame: npt.NDArray, threshold: int = 10) -> bool:
        """
        Checks if the frame is not duplicate by comparing it with the previous
        frames.

        Parameters
        ----------
        frame : npt.ArrayLike
            Image frame to analyze
        threshold : int, optional
            Threshold for the color difference of the images to be considered
            different, by default 10

        Returns
        -------
        bool
            True if the frame is a new one (Not a duplicate)
        """

        # Retreive the region of interest from the frame
        region = frame[59:505, 30:623, :]

        # Check if the frame is the first one
        if len(self.processed_frames) == 0:
            self.processed_frames.append(region)
            return True

        # Check if the frame is a duplicate
        for previous_frame_region in self.processed_frames:

            diff = cv2.absdiff(previous_frame_region, region)

            # Convert image to grayscale image
            gray_image = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

            # Convert the grayscale image to binary image
            mask = cv2.inRange(gray_image, threshold, 255)

            # Count the number of pixels that execeeding the threshold difference
            diff_pix = cv2.countNonZero(mask)

            # If there are more than 2000 pixelels that exceed the threshold,
            # the frame is not a duplicate, 2000 is a number chosen analyzing
            # the average frame difference between two consecutive slots with
            # different pokemon
            if diff_pix < 2000:
                return False

        # If the frame is not a duplicate, add it to the list
        self.processed_frames.append(region)
        return True

    def process_frame(self, frame: npt.NDArray, output_path: pathlib.Path):
        """
        Processes a frame and saves it to the output path if it is a new
        one.

        Parameters
        ----------
        frame : npt.ArrayLike
            Image containing the frame to be processed
        output_path : pathlib.Path
            Destination where the frame will be saved if it is new
        """

        # Check if the image is not a transient
        if self._is_stable(frame):

            # Check if the image is not a duplicate
            if self._is_not_duplicate(frame):

                # Save the frame to the output path
                img_name = f"{self.frame_count}.png".rjust(7,"0")
                cv2.imwrite(str(output_path / img_name), frame)
                self.frame_count += 1


def extract(video_path: str, output_path: str = DEFAULT_OUT) -> int:
    """
    Extracts frames from the video and saves them to the output path only
    if they are unique.

    Parameters
    ----------
    video_path : str
        Path to the video file
    output_path : str, optional
        Path to the folder where the output will be generated, by default
        './output/'
    """

    try:
        fe = FrameExtractor(video_path, output_path)
    except ValueError:
        return 0
    return fe.extract_frames()
