![alt tag](https://raw.githubusercontent.com/TheQYD/cobblr-music-player/master/music.png)

**Description:** This is the music application written for the RPI's cobblr software.

**Requirements**
 1. Raspberry Pi (https://www.adafruit.com/products/2358)
 2. Adafruit 2.8in PiTFT (https://www.adafruit.com/products/1601)
 3. Raspberry Pi Camera (https://www.adafruit.com/products/1367)
 4. USB Microphone Dongle (http://www.amazon.com/Super-Microphone-Adapter-Driver-Notebook/dp/B00M3UJ42A)
 5. The cobblr software (https://github.com/RoboQYD/cobblr)
 6. (Optional) Adafruit Powerboost 1000C (https://www.adafruit.com/products/2465)
 7. (Optional) Adafruit Lipo Battery 500mAh (https://www.adafruit.com/products/1578)

**Installation**
 1. Clone the repository.
 2. Enter the cobblr-music-player directory.
 3. Run "setup.py install (path)" where (path) is the location of the cobblr folder.
 4. Enter the "cobblr/config/" directory.
 5. Open "cobblr.yaml" and add "-music" to the list of applications.
 6. There are two ways to add an app's icon onto the screen.
    i. Set the application "music" to the startup application.
    ii. Change directory to the "applications/desktop/config/" folder and add it in the list of applications with a                 position.
 7. Run cobblr.

**Notes**
 
  I plan to write a script that automatically edits and adds new applications onto the screen. For now, the user is going to   have to edit and add the app icon onto the screen.
