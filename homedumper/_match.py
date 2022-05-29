import csv
import json
import logging
from pathlib import Path
from typing import List, Tuple
from skimage.metrics import structural_similarity
import cv2
import numpy.typing as npt

from homedumper.const import CACHE_DIR
from homedumper._download import name_dict

def ssim_likelihood(img1: npt.NDArray, img2: npt.NDArray) -> float:
    """
    Compute the likelihood of two images being the same using the Structural
    Similarity Index

    Parameters
    ----------
    img1 : npt.NDarray
        The first image.
    img2 : npt.NDarray
        The second image.

    Returns
    -------
    float
        The likelihood of the two images being the same using the SSIM method.
    """

    # Convert the second image to the first image's size
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, img1.shape)

    # Compute SSIM between two images
    return structural_similarity(img1, img2, channel_axis=2)

def id2name(id: str) -> str:
    """
    Translate the id of a pokemon into its name.

    Parameters
    ----------
    id : str
        Name of the template file

    Returns
    -------
    str
        Name of the pokemon
    """    

    translator = name_dict()
    if id in translator.keys():
        return translator[id]
    logging.error(f"No pokemon name found for template with {id}.png")
    return id

def _best_match(thumbnail: npt.NDArray, templates: dict) -> str:
    """
    Estimate the id of the most likely Pokemon corresponding to a thumbnail.

    Parameters
    ----------
    thumbnail : npt.NDArray
        Image of the target Pokemon.
    templates : dict
        Dictionary with the templates. Keys are the ids and values are
        the template images.
    """
    best = None
    like = 0.0

    # Iterate over the templates
    for name, template in templates.items():

        # Compute the likelihood of the template being the thumbnail
        lk = ssim_likelihood(thumbnail, template)

        # If he likelihood is better than the current best, update the best
        if lk > like:
            best = name
            like = lk

    # If the match is with the empty image, return None
    if best == "0000":
        return None

    # Translate best match into pokemon name
    return id2name(best)


def parse_slot_path(path: Path) -> Tuple[str, str]:
    """
    Parse the path to a slot thumbnail and return the box name and the slot number.

    Parameters
    ----------
    path : Path
        Path to the slot thumbnail.

    Returns
    -------
    Tuple[str, str]
        Box name and slot number.
    """   

    slot_id = path.stem
    title_path = path.parent / 'title.txt' 

    # Read the title file
    with open(title_path, "r", encoding="utf-8") as f:
        title = f.read().strip()
    
    return title, slot_id


def _match(boxes_path: Path) -> List[Tuple[str, str, str]]:
    """
    Iterate over all boxes and estimates the id of the more likely Pokemon
    corresponding to each slot.

    Parameters
    ----------
    path : str
        Path to the folder that contains the 'boxes' subfolder with the images.

    Returns
    -------
    List[Tuple[Path, str]]
        List of tuples with the path to the image and the pokemon id.
    """

    # Path to the resized template dir
    assets_path = Path(CACHE_DIR) / "resized" / "regular"

    # Load the templates
    templates = {}
    for template in assets_path.glob("*.png"):
        templates[template.stem] = cv2.imread(str(template))
    # TODO: See what to do with the shiny

    # Initialize empty list
    matches = []

    # Iterate over the boxes
    for box_path in sorted(boxes_path.iterdir()):

        # Iterate over the slots
        for thumbnail in sorted(box_path.glob("*.png")):

            # Read the target image
            logging.info(f"Matching {thumbnail.name} from {box_path.name}")
            thu = cv2.imread(str(thumbnail))
            name = _best_match(thu, templates)
            box_name, slot_id = parse_slot_path(thumbnail)

            matches.append((box_name, slot_id, name))

    return matches


def export_csv(path: Path, header: Tuple[str, str, str], data: List[Tuple[str, str, str]]):
    """
    Export the data to a csv file.

    Parameters
    ----------
    path : Path
        Path to the csv file.
    header : Tuple[str, str, str]
        Title of the columns in the csv file.
    data : List[Tuple[str, str, str]
        List of all rows (Box name, Slot Number, Pokemon ID).
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerows(data)

def _emptybox(name: str) -> dict:
    """
    Creates an empty box.

    Parameters
    ----------
    name : str
        Name of the box.

    Returns
    -------
    dict
        Dictionary with the empty box.
    """

    return {
      "title": name,
      "pokemon": [None for i in range(30)]
    }

def export_json(path: Path, data: List[Tuple[str, str, str]]):
    """
    Export the data to a csv file.

    Parameters
    ----------
    path : Path
        Path to the json file.
    data : List[Tuple[str, str, str]
        List of all rows (Box name, Slot Number, Pokemon ID).
    """

    json_data = {
        "name": "Dumped",
        "slug": "dumped",
        "description": "Pokémon Boxes dumped from the video",
        "boxes": []
    }

    current_box_name = None
    current_box = None

    for box_name, slot_id, pokemon_id in data:

        if current_box is None:
            current_box_name = box_name
            current_box = _emptybox(box_name)

        if box_name != current_box_name:
            current_box_name = box_name

            json_data["boxes"].append(current_box)
            current_box = _emptybox(box_name)
        
        current_box["pokemon"][int(slot_id)-1] = pokemon_id
    
    json_data["boxes"].append(current_box)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)


def match(path: str) -> int:
    """
    Iterate over all boxes and estimates the id of the more likely Pokemon

    Parameters
    ----------
    path : str
        Path to the folder that contains the 'boxes' subfolder with the images.

    Returns
    -------
    int
       Total number of pokemon found.
    """

    # Create a path to the input folder
    project_path = Path(path)

    if project_path.exists() and project_path.is_dir():
        boxes_path = project_path / "boxes"

        # Check if the input folder exists and is a valid project folder
        if boxes_path.exists() and boxes_path.is_dir():       

            # match the data
            data = _match(boxes_path)

            # Write the data to a csv file
            header = ("Box name", "Slot Number", "Pokemon ID")
            csv_file = project_path / "match.csv"
            export_csv(csv_file, header, data)

            # Write the data to a json file
            json_file = project_path / "match.json"
            export_json(json_file, data)

            return len(data)
        else:
            logging.error(f"{boxes_path} doesn't exist. Remember to boxify before match.")
    
    else:
        logging.error(f"{path} doesn't exist.")

    # Return 0 if the input folder doesn't exist or is not a valid project folder
    return 0
