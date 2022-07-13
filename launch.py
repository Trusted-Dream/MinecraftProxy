#!/bin/env python
from libs.setting import Setup
from libs.tasktray import Tray
import os

def main():

    dirname = os.path.dirname(__file__)
    image_file = os.path.join(dirname, "minecraft.ico")

    # FILE INFO ENVIRONMENT
    os.environ['SETTING_FILE'] = "setting.txt"
    os.environ['IMAGE_FILE'] = image_file

    tray = Tray()
    Setup()
    tray.run()

if __name__ == "__main__":
    main()