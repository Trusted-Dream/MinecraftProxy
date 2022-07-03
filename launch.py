#!/bin/env python
from libs.setting import Setup
from libs.tasktray import Tray
import sys
import os

def resourcePath(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename.replace('icon_path/', '')

def main():
    # FILE INFO ENVIRONMENT
    os.environ['SETTING_FILE'] = "setting.txt"
    os.environ['IMAGE_FILE'] = resourcePath("icon_path/minecraft.ico")

    tray = Tray()
    Setup()
    tray.run()

if __name__ == "__main__":
    main()