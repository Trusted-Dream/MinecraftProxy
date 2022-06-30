#!/bin/env python
from lib.setting import Setup
from lib.tasktray import Tray
from tkinter import messagebox
import ctypes
import sys
import os

def resourcePath(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename.replace('icon_path/', '')

def main():
    Kernel32 = ctypes.windll.Kernel32
    # Lock
    mutex = Kernel32.CreateMutexA(0, 1, "lock")
    result = Kernel32.WaitForSingleObject(mutex, 0)

    if result == 0x00000102:
        messagebox.showerror(
            "アプリケーションは既に起動しています！", 
            "アプリは既に起動しています\nタスクトレイを確認してください"
        )
    else:
        # FILE INFO ENVIRONMENT
        os.environ['SETTING_FILE'] = "setting.txt"
        os.environ['IMAGE_FILE'] = resourcePath("icon_path/minecraft.ico")

        tray = Tray()
        Setup()
        tray.run()

    Kernel32.ReleaseMutex(mutex)
    Kernel32.CloseHandle(mutex)

if __name__ == "__main__":
    main()