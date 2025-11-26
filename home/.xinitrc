#!/bin/sh
xset s off
xset -dpms
xset s noblank
xrandr --output HDMI-1 --mode 1920x1080 --rate 60
xmodmap /home/pi/.Xmodmap-kiosk &
xbindkeys &

exec /usr/bin/python3 /home/pi/kiosk/kiosk_gui.py

