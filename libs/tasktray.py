import asyncio
import os
import ctypes

from libs.discord_run import Discord
from pystray import Icon, Menu, MenuItem
from tkinter import messagebox
from PIL import Image
from threading import Thread

class Tray:

    def __init__(self):
        # IMAGE FILE ENVIRONMENT
        image:str = os.environ.get("IMAGE_FILE","")
        menu = Menu(
            MenuItem('Exit',self.exit_app)
        )

        self.icon = Icon(
            name='Connector',
            title='MinecraftProxy',
            icon=Image.open(image),
            menu=menu
        )

    def exit_app(self) -> None:
        self.icon.stop()

    def discord_run(self,loop) -> None:
        asyncio.set_event_loop(loop)
        objDiscord = Discord()
        try:
            objDiscord.run()
        except Exception as e:
            messagebox.showerror(
                "エラーが発生しました！", 
                f"DiscordBotへの接続に失敗しました\n"
                "API KEYを確認してください\n{e.args[0]}"
            )
            self.icon.stop()

    def run(self) -> None:
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
            loop = asyncio.new_event_loop()
            thread = Thread(target=self.discord_run,args=(loop,),daemon=True)
            thread.start()
            self.icon.run()
        Kernel32.ReleaseMutex(mutex)
        Kernel32.CloseHandle(mutex)

# Fix Runtime Error
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport

def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper

_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)