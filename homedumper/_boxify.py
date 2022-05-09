import logging
import pytesseract
import cv2
from pathlib import Path
import numpy.typing as npt
from typing import Tuple, List


current_tittle = 1


def box_title(frame: npt.NDArray) -> str:
    """
    Extract the title of the box from the frame.

    Parameters
    ----------
    frame : npt.ArrayLike
        Screen capture of a Pokemon HOME screen with a box on it.

    Returns
    -------
    str
        Text of the box title.
    """

    # Extract the region of interest and convert it to grayscale
    title_region = frame[70:102, 166:487, :]
    gray = cv2.cvtColor(title_region, cv2.COLOR_BGR2GRAY)

    # Return the text of the box title extracted with tesseract
    try:
        return pytesseract.image_to_string(gray)
    # If tesseract is not installed, return default sequenced string
    except pytesseract.pytesseract.TesseractNotFoundError:
        logging.error("Tesseract not found. Please install it.")
        logging.info("Using default names for the boxes.")

        # Get the last tittle id and format the new name
        global current_tittle
        name = f"HOME {str(current_tittle).rjust(3,'0')}"

        # Increment the current tittle id and return the name
        current_tittle += 1
        return name


def pokemon_thumbnails(frame: npt.NDArray) -> List[npt.NDArray]:
    """
    Extract the pokemon thumbnails from a frame.

    Parameters
    ----------
    frame : npt.NDArray
        Screen capture of Pokemon HOME with a box on it.

    Returns
    -------
    List[npt.NDArray]
        List of the pokemon thumbnails.
    """

    # Parametrize the layout of the thumbnails
    dy = 76
    dx = 92
    y0 = 128
    x0 = 50

    # Get the coordinates of each possible pokemon thumbnail
    regions = (
        (y0 + i * dy, y0 + (i + 1) * dy, x0 + j * dx, x0 + (j + 1) * dx)
        for i in range(5)
        for j in range(6)
    )

    # Extract the pokemon thumbnails
    return [frame[y1:y2, x1:x2, :] for y1, y2, x1, x2 in regions]


def _export_thumbnails(pokemons: List[npt.NDArray], output_path: Path):
    """
    Export the pokemon thumbnails to a folder.

    Parameters
    ----------
    pokemons : List[npt.NDArray]
        List of the pokemon thumbnails.
    output_path : Path
        Path to the destination image file
    """
    # Save all thumbnails to the output folder
    for i, pokemon in enumerate(pokemons):
        file_name = f"{str(i+1).rjust(2,'0')}.png"
        file_path = output_path / file_name
        cv2.imwrite(str(file_path), pokemon)


def _export_box_title(box_title: str, output_path: Path):
    """
    Export the box title to a file.

    Parameters
    ----------
    box_title : str
        Box title found from the images.
    output_path : Path
        Destination folder of the box.
    """
    file_name = "title.txt"
    file_path = output_path / file_name
    with open(str(file_path), "w") as f:
        f.write(box_title)


def export_box(pokemons: List[npt.NDArray], box_title: str, output_path: Path):
    """
    Export the box data to a folder.

    Parameters
    ----------
    pokemons : List[npt.NDArray]
        List of the pokemon thumbnails.
    box_title : str
        Title of the box.
    output_path : Path
        Path to the output folder.
    """

    # Save all thumbnails to the output folder
    _export_thumbnails(pokemons, output_path)

    # Save the box title to the output folder
    _export_box_title(box_title, output_path)


def frame2box(frame: npt.NDArray) -> Tuple[str, List[npt.NDArray]]:
    """
    Extract the box data from a frame.

    Parameters
    ----------
    frame : npt.NDArray
        Screen capture of a Pokemon HOME screen with a box on it.

    Returns
    -------
    Tuple[str, List[npt.NDArray]]
        Tuple with the box title and a list of the pokemon rois.
    """
    # Extract the box title
    title = box_title(frame)

    # Extract the box pokemon rois
    pokemons = pokemon_thumbnails(frame)

    print(title)
    return title, pokemons


def _diggest_project_path(folder_path: str) -> Tuple[Path, Path]:
    """
    Get the input and output path objects from a folder path string.

    Parameters
    ----------
    folder_path : str
        Path to the folder that contains the 'frames' subfolder with the images.

    Returns
    -------
    Tuple[Path, Path]
        Input and output path object.

    Raises
    ------
    ValueError
        When the folder_path doesn't not contains the 'frames' subfolder.
    """

    # Convert the path to a pathlib object
    folder_path_obj = Path(folder_path)

    # Create a path to the output folder
    output_path_obj = folder_path_obj / "boxes"
    output_path_obj.mkdir(parents=True, exist_ok=True)

    # Create a path to the input folder
    input_path_obj = folder_path_obj / "frames"
    if not input_path_obj.exists() or input_path_obj.is_file():
        err_msg = (
            f"No subfolder 'frames' with png files inside was found in {folder_path}"
        )
        raise ValueError(err_msg)

    return input_path_obj, output_path_obj


def boxify_image(image_path: Path, output_path: Path):
    """
    Transform an image into a box folder structure.

    Parameters
    ----------
    image_path : Path
        Path to the image to be converted.
    output_path : Path
        Path to the output folder.
    """

    # Load the image
    image = cv2.imread(str(image_path))

    # Extract the box data
    title, pokemons = frame2box(image)

    # Create the output folder for the image
    name = image_path.stem
    out_folder = output_path / name
    out_folder.mkdir(parents=True, exist_ok=True)

    # Export the box data
    export_box(pokemons, title, out_folder)


def boxify(folder_path: str) -> int:
    """
    Transform all the images in a folder into a folder structure with isolated
    images of each pokemon found.

    Parameters
    ----------
    folder_path : str
        Path to the folder that contains the 'frames' subfolder with the images.

    Returns
    -------
    int
        Number of frames converted to box.
    """

    # Get the input and output path objects
    input_path_obj, output_path_obj = _diggest_project_path(folder_path)

    # Set a counter for processed images
    image_count = 0

    # Read all png images
    for image_path in input_path_obj.glob("*.png"):

        # Convert the image to a box
        boxify_image(image_path, output_path_obj)

        # Increment the counter
        image_count += 1

    return image_count
