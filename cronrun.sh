#!/bin/sh

bash /Frame/dropbox_uploader.sh -f /home/pi/.dropbox_uploader -s download /Comic\ Collector/Wes\ Collection.cmcp/Images /Frame &
xte 'mousermove 100 100'

cd /Frame
python3 AdminFrame.py
sleep 5
feh -z -x -F -D 5 -R 10 -f /Frame/displayFileNames.txt &
