#!/bin/sh
sudo apt install libcairo2-dev libxt-dev libgirepository1.0-dev gir1.2-gst-rtsp-server-1.0 gstreamer1.0-plugins-ugly -y
python3 -m pip install -r requirements.txt