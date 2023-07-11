## What is this?

Restream rtsp with opencv frame using **gst-rtsp-server**.

## Usecases?

Modified opencv frame and restream.

## Fundamental?

There are 2 component: media_factory and server:
*  **media_factory** (rtsp_media_factory): convert opencv frame to gst buffer.
*  **server** (rtsp_server): publish buffer to rtsp stream.

## Test with example:
### Setup environment:
Create virtual environment (Optional):

`python3 -m venv .venv`

Run setup_env.sh

`source setup_env.sh`

### Run

`python3 main_frame.py` or  `python3 main_stream.py`

Play using ffplay or vlc:

`ffplay -rtsp_transport tcp rtsp://localhost:8001/stream`