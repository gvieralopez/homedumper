# Work To do in homedumper

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