This is an example of creating an
animated surface rotation GIF file
using pyeq3 and matplotlib.
see http://commonproblems.readthedocs.io/en/latest/


Step 1: Install imagemagick and gifsicle

Assuming you already have pyeq3 installed with the appropriate dependencies
(see documentation), you need only install imagemagick and gifsicle:

Linux: sudo apt-get install imagemagick gifsicle

Mac: brew install imagemagick gifsicle



Step 2: Run the AnimatedGIF example

From a command prompt run this command:

python3 AnimatedGIF.py

The example will display its progress
as it runs, and will create a file named
rotation.gif.



Step 3: View the animation

You can open the rotation.gif file in a
browser to see the animation.  The animation
may appear to stutter or jerk until fully loaded
from the computer's hard disk drive into the browser.
