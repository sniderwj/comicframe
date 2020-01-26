# comicframe
Raspberry Pi powered Display Frame with a filter site

# Description
This script was inspired from https://github.com/Geektoolkit/Dynaframe

I liked the idea of a RPi powered frame where I could upload the scans of my comic books and display them with the rest of my Comic Book Room. My requirements were to have a frame that could be updated automatically and then be able to apply somw filtering based off of my collection. I have used the  Comic Collectorz https://www.collectorz.com/comic app for a number of years. Prior to them syncing with the could I had my collection in Dropbox so I knew I had a way to get my images to the frame.

## Requirements
1. Automatically start  
2. Parse an export from Comics Collectorz for filter information
3. Launch a site that can set filters, changing the images shown
4. Use Dropbox to copy images and Comic Collectorz export automatically

## Needed applications
1. Python 3
2. feh
3. Comic Collectorz
4. Dropbox (optional)
5. Dropbox Uploader (optional)
  * https://github.com/andreafabrizi/Dropbox-Uploader

# Setup
1. In Comic Collectorz run *File --> Export To --> XML* and place in a path in your Dropbox folder.
2. On the frame create a folder */Frame* and put AdminFrame.py, config.py, syncdropbox.sh and cronrun.sh there
  ~~~
  pi@comicframe: mkdir /Frame
  ~~~
3. Configure config.py, syncdropbox.sh, and cronrun.sh for all the proper paths.
4. Assuming the frame will run under the *pi* user copy the autostart_feh.desktop to */home/pi/.config/autostart*.
## Using Dropbox?
5. Set up the dropbox_uploader.sh following the instructions on their site.
6. Configure crontab to run the syncdropbox.sh to run. I would suggest once a day:
  * Run the command 
      ~~~
      pi@comicframe: crontab -u pi -e
      ~~~
      It will ask what editor to use if this is the first time.
      ~~~
        0 0 * * * cd /Frame && bash /Frame/syncdropbox.sh
      ~~~
7. Run the syncdropbox.sh to get your initial set of images and export file
## Not Using Dropbox?
5. Copy your images to the frame in the proper paths. You can use SCP or Samba depending on your Raspbian setup. Basically get your images and your export to the proper paths. based on your *config.py* file.
6. Comment out the *dropbox_uploader.sh* line in the *cronrun.sh*. No reason to call it if you arent using it.

