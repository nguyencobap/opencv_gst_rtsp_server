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

Run install

`python3 -m pip install .`

### Run

`python3 examples/main_frame.py` or  `python3 examples/main_stream.py`

Play using ffplay or vlc:

`ffplay -rtsp_transport tcp rtsp://localhost:8001/stream`

### Build

Install wheel:

`python3 -m pip install wheel`

Build:

`python3 setup.py bdist_wheel`

Install:

`python3 -m pip install build/opencv_gst_rtsp_server-0.1.3-py3-none-any.whl`
