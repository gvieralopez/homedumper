# Work To do in homedumper

The current version of the project is able to identify the 1120 Pokémon present
in the sample video with the following performance:

Correct: 847
Incorrect: 259

Current mistakes are distributed according its nature as:

Incorrect species: 133
Incorrect forms: 126
Empty slots missed: 2

Current results are far from perfect and still take some time to be computed. 
Next, we will list some further task that we believe will improve the overall
accuracy or the computing time. Feel free to contribute on any of them. 

## Related to the identification of key frames from videos (_extract.py)

* Improve the algorithm to compare if an image is a duplicate frame
* Add some extra logging
* Write unit tests

## Related to the extraction of thumbnails from screenshots (_boxify.py)

* Add some extra logging
* Remove background before store the thumbnails
* Manually deal with Go logo if required
* Write unit tests

## Related to matching extracted thumbnails with actual data (_match.py)

* Search also for shiny pokemon
* Export also a json file
* Improve matching algorithm with something smarter
* Add multiprocessing for faster matching
* Write unit tests

# Integration

* Rework dump command to avoid writting unnecesary files to disk