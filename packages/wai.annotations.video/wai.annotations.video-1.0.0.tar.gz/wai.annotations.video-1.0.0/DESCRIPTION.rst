wai.annotations plugin for video support.

The following sources are available:

* `from-video-file-od`: reads video files and forwards the frames in the object detection domain (with empty annotations)
* `from-webcam-od`: reads frames from a webcam and forwards the frames in the object detection domain (with empty annotations)

The following inline stream processors (ISPs) are available:

* `drop-frames`: drops every nth frame from the stream
* `skip-similar-frames`: drops frames that are too similar to each other

The following sinks are avilable:

* `to-video-file-od`: writes frames to an MJPG video file
* `calc-frame-changes`: generates a histogram of the changes between frames, can be used for calculating a threshold for `skip-similar-frames`
