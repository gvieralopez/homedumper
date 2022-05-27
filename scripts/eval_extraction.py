# This scripts evaluates the extraction of the Pokémon from the video by
# comparing the extracted ids with the ground truth manually labeled for
# the sample video.

import json
import csv


def emptybox(name: str) -> dict:
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

def csv2json(csvreader: csv.reader) -> dict:
    """
    Converts a csv reader to a json list.

    Parameters
    ----------
    csvreader : csv.reader
        csv reader object to convert

    Returns
    -------
    dict
        Dictionary with the extracted data in json format.
    """

    extracted = list(csvreader)
    data = {
        "name": "Dumped",
        "slug": "dumped",
        "description": "Pokémon Boxes dumped from the video",
        "boxes": []
    }

    current_box_name = None
    current_box = None

    for box_name, slot_id, pokemon_id in extracted[1:]:

        if current_box is None:
            current_box_name = box_name
            current_box = emptybox(box_name)

        if box_name != current_box_name:
            current_box_name = box_name

            data["boxes"].append(current_box)
            current_box = emptybox(box_name)
        
        current_box["pokemon"][int(slot_id)-1] = pokemon_id

    return data



def compare_boxes(box1: dict, box2: dict) -> tuple[int, int, int]:
    """
    Compares two boxes.

    Parameters
    ----------
    box1 : dict
        First box to compare.
    box2 : dict
        Second box to compare.

    Returns
    -------
    tuple[int, int, int]
        Number of correct, incorrect and form-incorrect pokemon.
    """

    correct = 0
    incorrect = 0
    form_incorrect = 0

    for i in range(30):
        pkm1 = box1["pokemon"][i] if i < len(box1["pokemon"]) else None
        pkm2 = box2["pokemon"][i] if i < len(box2["pokemon"]) else None

        if pkm1 is None and pkm2 is None:
            continue
        if pkm1 == pkm2:
            correct += 1
        elif pkm1 and pkm2 and (pkm1.startswith(pkm2) or pkm2.startswith(pkm1)):
            form_incorrect += 1
        else:
            incorrect += 1

    return correct, incorrect, form_incorrect



if __name__ == "__main__":

    with open('data/perfect.json') as f:
        ground_truth = json.load(f)

    try:
        with open('../homedumper/output/myhome/match.csv', 'r') as f:
            extracted = csv.reader(f)
            extracted = csv2json(extracted)
    except FileNotFoundError:
        print('No match.csv found. Please run the matching script first.')
        exit()

    
    correct = 0
    incorrect = 0
    form_incorrect = 0

    for gt_box, dp_box in zip(ground_truth["boxes"], extracted["boxes"]):
        c, i, f = compare_boxes(gt_box, dp_box)
        correct += c
        incorrect += i
        form_incorrect += f

    
    print(f'Correct: {correct}')
    print(f'Incorrect: {incorrect}')
    print(f'Form-incorrect: {form_incorrect}')

