# wai-annotations-video
wai.annotations plugin for video support.

## Plugins
### FROM-VIDEO-FILE-OD
Reads frames from a video file.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: from-video-file-od [-f FROM_FRAME] [-i INPUT_FILE] [-m MAX_FRAMES] [-n NTH_FRAME] [-p PREFIX] [-t TO_FRAME]

optional arguments:
  -f FROM_FRAME, --from-frame FROM_FRAME
                        determines with which frame to start the stream (1-based index)
  -i INPUT_FILE, --input INPUT_FILE
                        the video file to read
  -m MAX_FRAMES, --max-frames MAX_FRAMES
                        determines the maximum number of frames to read; ignored if <=0
  -n NTH_FRAME, --nth-frame NTH_FRAME
                        determines whether frames get skipped and only evert nth frame gets forwarded
  -p PREFIX, --prefix PREFIX
                        the prefix to use for the frames
  -t TO_FRAME, --to-frame TO_FRAME
                        determines after which frame to stop (1-based index); ignored if <=0
```

### FROM-WEBCAM-OD
Reads frames from a webcam.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: from-webcam-od [-f FROM_FRAME] [-m MAX_FRAMES] [-n NTH_FRAME] [-p PREFIX] [-t TO_FRAME] [-i WEBCAM_ID]

optional arguments:
  -f FROM_FRAME, --from-frame FROM_FRAME
                        determines with which frame to start the stream (1-based index)
  -m MAX_FRAMES, --max-frames MAX_FRAMES
                        determines the maximum number of frames to read; ignored if <=0
  -n NTH_FRAME, --nth-frame NTH_FRAME
                        determines whether frames get skipped and only evert nth frame gets forwarded
  -p PREFIX, --prefix PREFIX
                        the prefix to use for the frames
  -t TO_FRAME, --to-frame TO_FRAME
                        determines after which frame to stop (1-based index); ignored if <=0
  -i WEBCAM_ID, --webcam-id WEBCAM_ID
                        the webcam ID to read from
```

### DROP-FRAMES
Drops frames from the stream.

#### Domain(s):
- **Image Classification Domain**
- **Image Object-Detection Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: drop-frames [-n NTH_FRAME]

optional arguments:
  -n NTH_FRAME, --nth-frame NTH_FRAME
                        which nth frame to drop, e..g, '2' means to drop every 2nd frame; passes frames through if <=1
```

### SKIP-SIMILAR-FRAMES
Skips frames in the stream that are deemed too similar.

#### Domain(s):
- **Image Classification Domain**
- **Image Object-Detection Domain**
- **Image Segmentation Domain**

#### Options:
```
usage: skip-similar-frames [-b BW_THRESHOLD] [-t CHANGE_THRESHOLD] [-c CONVERSION] [-v]

optional arguments:
  -b BW_THRESHOLD, --bw-threshold BW_THRESHOLD
                        the threshold to use for converting a gray-scale like image to black and white (0-255)
  -t CHANGE_THRESHOLD, --change-threshold CHANGE_THRESHOLD
                        the percentage of pixels that changed relative to size of image (0-1)
  -c CONVERSION, --conversion CONVERSION
                        how to convert the BGR image to a single channel image (gray/r/g/b)
  -v, --verbose         whether to output some debugging output.
```


### TO-VIDEO-FILE-OD
Writes frames to a MJPG video file.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-video-file-od [-f FPS] [-o OUTPUT_FILE]

optional arguments:
  -f FPS, --fps FPS     the frames per second to use
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        the MJPG video file to write to
```

### CALC-FRAME-CHANGES
Calculates the changes between frames, which can be used with the skip-similar-frames ISP.

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: calc-frame-changes [-b BW_THRESHOLD] [-t CHANGE_THRESHOLD] [-c CONVERSION] [-B NUM_BINS] [-o OUTPUT_FILE] [-f OUTPUT_FORMAT] [-v]

optional arguments:
  -b BW_THRESHOLD, --bw-threshold BW_THRESHOLD
                        the threshold to use for converting a gray-scale like image to black and white (0-255)
  -t CHANGE_THRESHOLD, --change-threshold CHANGE_THRESHOLD
                        the percentage of pixels that changed relative to size of image (0-1)
  -c CONVERSION, --conversion CONVERSION
                        how to convert the BGR image to a single channel image (gray/r/g/b)
  -B NUM_BINS, --num-bins NUM_BINS
                        the number of bins to use for the histogram
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        the file to write to statistics to, stdout if not provided
  -f OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
                        how to output the statistics (text/csv/json)
  -v, --verbose         whether to output some debugging output.
```
