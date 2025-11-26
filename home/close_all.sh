#!/bin/bash
# Cierra Chromium, VLC .
killall chromium chromium-browser vlc
pkill -9 chromium
pkill -9 chromium-browser
pkill -9 vlc
