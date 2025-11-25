#!/bin/sh
#Sesion minima para el Centro Multimedia

xset s off
xset -dpms
xset s noblank
xrandr --output HDMI-1 --mode 1920x1080 --rate 60
#xkbcomp /home/pi/keymap.xkb $DISPLAY &
xmodmap /home/pi/.Xmodmap-kiosk &
xbindkeys &

#exec sudo -E /usr/bin/python3 /home/pi/kiosk/kiosk_gui.py
exec /usr/bin/python3 /home/pi/kiosk/kiosk_gui.py
#xterm
