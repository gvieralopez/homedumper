# This scripts evaluates the extraction of the Pokémon from the video by
# comparing the extracted ids with the ground truth manually labeled for
# the sample video.

import json



def compare_boxes(box1: dict, box2: dict) -> tuple[int, int, int, int, list]:
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
    tuple[int, int, int, int, list]
        Number of correct, species-incorrect, form-incorrect and fake-deteted 
        pokemon followed by a list of incorrect matches.
    """

    errors = []
    correct = 0
    species_incorrect = 0
    form_incorrect = 0
    fake_detected = 0

    for i in range(30):
        pkm1 = box1["pokemon"][i] if i < len(box1["pokemon"]) else None
        pkm2 = box2["pokemon"][i] if i < len(box2["pokemon"]) else None

        if pkm1 is None and pkm2 is None:
            continue
        if pkm1 is None and pkm2 is not None:
            fake_detected += 1
            errors.append((pkm1, pkm2, "fake detect"))
            continue
        if pkm1 == pkm2:
            correct += 1
            continue
        if pkm1 is not None and pkm2 is not None:
            print(pkm1, pkm2)
            if pkm1.split("-")[0] == pkm2.split("-")[0]:
                form_incorrect += 1
                errors.append((pkm1, pkm2, "form"))
            continue
        errors.append((pkm1, pkm2, "species"))
        species_incorrect += 1

    return correct, species_incorrect, form_incorrect, fake_detected, errors



if __name__ == "__main__":

    with open('data/perfect.json') as f:
        ground_truth = json.load(f)

    with open('../homedumper/output/myhome/match.json') as f:
        predicted = json.load(f)

    
    correct = 0
    species_incorrect = 0
    form_incorrect = 0
    fake_detected = 0
    errors = []

    for gt_box, dp_box in zip(ground_truth["boxes"], predicted["boxes"]):
        c, si, fi, vi, err = compare_boxes(gt_box, dp_box)
        correct += c
        species_incorrect += si
        form_incorrect += fi
        fake_detected += vi
        errors += err

    print('Bad matches: \n')
    for er in errors:
        print(f'[{er[2]}] {er[0]} -> {er[1]}')

    print(f'\nCorrect: {correct}')
    print(f'Incorrect: {species_incorrect + form_incorrect + fake_detected}')
    print(f'     Species: {species_incorrect}')
    print(f'     Form: {form_incorrect}')
    print(f'     Empty slots: {fake_detected}')
 
