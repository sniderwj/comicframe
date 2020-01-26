#! /bin/bash

bash /Frame/dropbox_uploader.sh -f /home/pi/.dropbox_uploader -s download \
/Comic\ Collector/Wes\ Collection.cmcp/Images /Frame/

bash /Frame/dropbox_uploader.sh -f /home/pi/.dropbox_uploader -s download \
/ComicFrame/Comic_data.xml /Frame/Comic_data.xml

logger "[syncdropbox.sh] - Finished Sync Dropbox Script"
