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
4. Bootstrap CSS
5. JQuery
4. Dropbox (optional)
5. Dropbox Uploader (optional)
  * https://github.com/andreafabrizi/Dropbox-Uploader

## Workflow
1. The cronrun.sh file will:
    1. Pull the latest image files from dropbox
    2. Start feh in slideshow mode using a text file (by default: displayFileNames.txt)
    3. Launch the AdminFrame.py
2. The AdminFrame.py will
    1. Read the Comic Collectorz export and build a list of comics, image names, and filter information
       * Filters are: Series, Comic Age, Publisher, and Creators
    2. Initially the text file will have all image file names
    3. Launches a web site @ http://<ipaddress>:5000
3. The website will:
    1. Select filters
    2. When the filter is changed the corresponding file names are written into the text file.

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
6. Comment out the *dropbox_uploader.sh* line in the *cronrun.sh*. No reason to call it if you aren't using it.  

# What next?
7. Rotate your screen 90 Degrees to support portrait mode:
    * Edit /boot/config.txt and add the following:
    ~~~
    display_rotate=3
    ~~~
8. Change the Pi's background to black.
9. In the cronrun.sh set the desired slideshow rotation in the feh command
    * **-D #** sets the slideshow delay. How long do you want an image displayed?
    * **-R #** sets the file list reload delay. How soon do you want filter applied?
10. Start AdminFrame.py to create your initial displayFileNames.txt and make sure that your paths are correct
11. Reboot and test it all again.



