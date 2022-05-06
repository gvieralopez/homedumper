import cv2
import pathlib
import numpy.typing as npt

# Constant values
DEFAULT_OUT = "./output"


class FrameExtractor:
    """
    Class for extracting different frames from a video.
    """
    
    def __init__(self, video_path: str, out_path: str = DEFAULT_OUT):

        # Ensure video path and output path are valid and get Path objects
        self._digest_paths(video_path, out_path)
        self.frame_count = 1


    def _digest_paths(self, video_path: str, output_path: str = DEFAULT_OUT) -> tuple[pathlib.Path, pathlib.Path]:
        """
        Digests the video path and output path into a tuple of Path objects.
        Checks if the video path exists creates the output path if it doesn't exist.

        Parameters
        ----------
        video_path : str
                String describing the video path
        output_path : str, optional
                String describing the output path, by default DEFAULT_OUT

        Returns
        -------
        tuple[Path, Path]
            Tuple of Path objects describing the video and output paths

        Raises
        ------
        ValueError if the video path doesn't exist or is a folder
        """

        # Check if video path exists and is a file
        video_path = pathlib.Path(video_path)
        if not video_path.exists() or video_path.is_dir():
            raise ValueError(f"Invalid video path: {video_path.absolute()}")

        # Create a path object for the output
        output_path = pathlib.Path(output_path)

        # Append video name to output path
        output_path = output_path / video_path.stem / "frames"

        # Create output path if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)

        self.video_path = video_path
        self.output_path = output_path


    def extract_frames(self):
        # Create output path if it doesn't exist
        cap = cv2.VideoCapture(str(self.video_path))

        # Retreive each frame from the video and process it
        while True:
            # Retrieve frame
            ret, frame = cap.read()

            # If the frame is empty, break
            if not ret:
                return

            self.process_frame(frame, self.output_path)

    def process_frame(self, frame: npt.ArrayLike, output_path: pathlib.Path):
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

        # Check if the image is new
        # TODO: Implement

        # Save the frame to the output path
        cv2.imwrite(str(output_path / f"{self.frame_count}.png"), frame)
        self.frame_count += 1


def extract(video_path: str, output_path: str = DEFAULT_OUT):

    fe = FrameExtractor(video_path, output_path)
    fe.extract_frames()

        

if __name__ == "__main__":
    extract("./data/myhome.mp4")