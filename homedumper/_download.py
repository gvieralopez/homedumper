import json
import logging
import zipfile
import urllib.request
import os
import cv2
import shutil
from pathlib import Path

import requests
from homedumper.const import (
    CACHE_DIR,
    URL_TEMPLATES,
    THUMBANIL_SIZE,
    URL_RAW_POKEMON_METADATA,
)


def download_templates(URL: str, path: Path):
    """
    Download the templates from the given URL.

    Parameters
    ----------
    URL : str
        The URL to download the templates from.
    path : Path
        The path to download the templates to.
    """

    zip_path = path / "master.zip"

    # Download the templates
    logging.info("Downloading templates...")
    urllib.request.urlretrieve(URL, zip_path)

    # Extract project
    logging.info("Uncompressing templates...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(path)
    os.remove(zip_path)

    # Move content to the raw folder
    raw_path = path / "raw"
    raw_path.mkdir(parents=True, exist_ok=True)

    regular_path = path / "livingdex-renders" / "images" / "pokemon" / "regular"
    shutil.move(regular_path, raw_path)

    shiny_path = path / "livingdex-renders" / "images" / "pokemon" / "shiny"
    shutil.move(shiny_path, raw_path)

    # Delete useless folders
    shutil.rmtree(path / "livingdex-renders")
    shutil.rmtree(path / "__MACOSX")


def check_cached_templates(
    cache_path: Path, folder: str = "raw", count: int = 1385
) -> bool:
    """
    Check if the templates are cached.

    Parameters
    ----------
    path : Path
        Path to the folder where the templates are stored.

    Returns
    -------
    bool
        Returns True if the templates are cached, False otherwise.
    """

    # Check if the templates are cached

    shiny_path = cache_path / folder / "shiny"
    regular_path = cache_path / folder / "regular"

    if shiny_path.exists() and regular_path.exists():
        if len(list(shiny_path.glob("*.png"))) > count:
            if len(list(regular_path.glob("*.png"))) > count:
                return True
    return False


def is_valid_thumbnail(name: str) -> bool:
    """
    Filters out the invalid templates.

    Parameters
    ----------
    name : str
        Name of the template image file

    Returns
    -------
    bool
        True if the template is valid (It can be found in a typical HOME box),
        False otherwise.
    """

    # List of banned keywords in the template name
    banned = [
        "-gmax",
        "-mega",
        "-back",
        "-complete",
        "-busted",
        "-ultra",
        "-primal",
        "0000",
    ]

    # Filter templates by name
    for word in banned:
        if word in name:
            return False
    return True


def resize_templates(cache_path: Path, subfolder: str):
    """
    Resize the templates according homedumper.consts.THUMBANIL_SIZE x 2.

    Parameters
    ----------
    cache_path : Path
        Path to the folder where the raw subfolder is stored.
    """

    # Create the destination folder
    resized_path = cache_path / subfolder

    # Iterate over regular and shiny versions
    for type in ["regular", "shiny"]:

        # Path to the folder with the input templates
        in_path = cache_path / "raw" / type

        # Create the destination folders
        out_path = cache_path / subfolder / type
        out_path.mkdir(parents=True, exist_ok=True)

        # Pick each file
        for in_file in in_path.glob("*.png"):

            # Check if it is a possible template
            if is_valid_thumbnail(in_file.stem):

                # Resize the image
                out_file = resized_path / type / in_file.name
                new_size = (THUMBANIL_SIZE * 2, THUMBANIL_SIZE * 2)
                img = cv2.imread(str(in_file))
                resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
                cv2.imwrite(str(out_file), resized_img)


def convert_name_dict(data: dict) -> dict:
    """
    Convert the name dictionary to the expected format.

    Parameters
    ----------
    data : dict
        Raw Pokemon metadata dictionary

    Returns
    -------
    dict
        Dictionary to map template ids with pokemon names.
    """

    # Create the output dictionary
    names = {}

    # Fill the output dictionary
    for name, metadata in data.items():
        id = metadata["images"]["home_render"]
        names[id] = name

    return names

def _path_to_id2name_file() -> Path:
    """
    Returns the path to the id2name file.

    Returns
    -------
    Path
        Path to the id2name file.
    """    
    cache_path = Path(CACHE_DIR)
    filename = 'id2name.json'
    filepath = cache_path / filename

    return filepath

def download_name_dict():
    """
    Download the name dictionary to map template ids with pokemon names.
    """

    # Fetch data in json format
    resp = requests.get(URL_RAW_POKEMON_METADATA)
    data = json.loads(resp.text)

    # Convert it to the expected format
    data = convert_name_dict(data)
    
    # Save it in cache
    path = _path_to_id2name_file()
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


def download(force_redownload: bool = False, force_resize: bool = False):
    """
    Download the templates.
    """

    cache_path = Path(CACHE_DIR)

    # Check if the cache folder exists
    if not cache_path.exists():
        cache_path.mkdir(parents=True, exist_ok=True)

    # Check if the templates are already cached
    if check_cached_templates(cache_path) and not force_redownload:
        logging.info("Templates are already cached.")
    # Download only if there are no cached templates
    else:
        logging.info("Templates are being dowloaded.")
        download_templates(URL_TEMPLATES, cache_path)

    # Check if the preprocessed templates are ready
    resize = True
    resized_folder = "resized"
    if not force_redownload and check_cached_templates(
        cache_path, resized_folder, 1000
    ):
        logging.info("Resized templates are already cached.")
        resize = False

    # Resize only if there are no cached resized templates
    if resize:
        logging.info("Resizing templates.")
        resize_templates(cache_path, resized_folder)
    
    logging.info("Templates are ready.")

    # Ensure the existence of the name dictionary
    if not _path_to_id2name_file().exists() or force_redownload:
        logging.info("Downloading name dictionary.")
        download_name_dict()

    logging.info("Name dictionary is ready.")


if __name__ == "__main__":
    download()
