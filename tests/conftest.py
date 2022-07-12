import tkinter as tk
import pytest
import string
import secrets
import os
import asyncio

@pytest.fixture(autouse=True)
def init():
    os.environ['SETTING_FILE'] = "setting.txt"
    os.environ['IMAGE_FILE'] = "minecraft.ico"

@pytest.fixture(autouse=True)
def Tk():
    root = tk.Tk()
    root.title(u"Test_MinecraftProxy")
    root.resizable(False,False)
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    scw = root.winfo_screenwidth()
    sch = root.winfo_screenheight()
    geometry = "+{:d}+{:d}".format(
        int((scw - w) / 2),
        int((sch - h) / 2)
    )
    root.geometry("450x150"+geometry)
    root.attributes("-alpha",0.8)
    root.iconbitmap(default="")
    root.after(50, root.destroy)
    return root

@pytest.fixture
def TestAPI(size=61):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    password = ''.join(secrets.choice(chars) for x in range(size))
    return password