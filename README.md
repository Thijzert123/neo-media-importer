# DJI Neo Media Importer
An easy-to-use media importer written in Python. It imports media from the sd-card inside of the DJI Neo. It might also work with other (DJI) drones, but only the DJI Neo has been tested.

It works as follows:
 - You specify a source directory (the DJI sd-card inside of the drone) and a target directory (where the files will be copied to).
 - The video files will be merged with the associated audio files, if they exist.
 - Optionally, you can choose to encode every video to h264, a more supported video codec.
 - After that, the output files will be copied to the target directory. The filenames will look like this: `YYYY-mm-dd-HH:MM:SS.mp4`.
 - Flight data files (.SRT files) and photos will also be imported with the same filename format.

## Usage
```
python3 neo-media-importer.py <SOURCE-DIRECTORY> <TARGET-DIRECTORY>
```
If more (random) arguments are passed, every video will be encoded to h264.
