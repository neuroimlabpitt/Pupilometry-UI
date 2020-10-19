# Pupil Measurement in Rodents

This repository contains code which captures videos to measure pupil diameter change in rodents for research purposes. Code was acquired from a publication by Bohacek Et al, and modified for use by our lab (PI: Dr. Alberto Vazquez, PhD). This program is made to run on Raspberry Pi (generation 3 and 4), and requires a PiCamera.

## Installation

To install this GUI (on a Raspberry Pi device), open terminal and run these commands
  
  1.) mkdir Code
  2.) cd Code
  3.) git clone https://github.com/aet37/pupilUX.git
  4.) cd pupilUX
  5.) chmod +x install.sh
  6.) ./install
  
Your RaspberryPi will reboot after this, and you should be able to start using the GUI:

  1.) Open terminal
  2.) cd Code/pupilUX
  3.) python camGUI.py
  
## Uninstall

To uninstall this GUI program, simply delete the pupilUX directory, and optionally the "Code" directory as well.

## Update

To update this GUI, simply:

  1.) Open terminal
  2.) cd Code/pupilUX
  3.) git pull origin

## Resources

Please refer to [this link](https://ein-lab.github.io/pupillometry-raspi) for an explanation of this software from the creators (EIN Lab).
