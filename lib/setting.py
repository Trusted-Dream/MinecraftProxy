from tkinter import messagebox
import tkinter as tk
import os
import sys

class Setting(tk.Frame):

    def __init__(self, root=None,file=None):
        super().__init__(root)
        self.file= file
        self.root = root
        self.pack()
        self.pack_propagate(False)
        self.tk_frame()

    def tk_frame(self):
        msg1 = (
            u'Discordで使用するBOTのAPIKEYを入力してください'
        )
        msg2 = (
            u'Discordで実行するユーザー名(管理者)を入力してください'
        )
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        Label = tk.Label(text=msg1,fg='black')
        Label.pack()

        self.EditBox1 = tk.Entry(width=200)
        self.EditBox1.pack()

        Label = tk.Label(text=msg2,fg='black')
        Label.pack()

        self.EditBox2 = tk.Entry(width=200)
        self.EditBox2.pack()

        OK_Button = tk.Button(text="OK",command=self.button_action,width=16)
        OK_Button.pack(fill = "x", padx=50, side = "left")

        Quit_Button = tk.Button(text=("閉じる"), command=self.exit,width=16)
        Quit_Button.pack(fill = "x", padx=50, side = "left")
        

    def button_action(self):
        self.input_msg1 = self.EditBox1.get()
        self.input_msg2 = self.EditBox2.get()
        if len(self.input_msg1)<=60:
            messagebox.showwarning(
                title="APIKEYの文字数が少ないです",
                message="API KEYが間違っている可能性があります！\n確認してください"
            )
        elif len(self.input_msg2)<=0:
            messagebox.showwarning(
                title="名前を入力してください",
                message="使用するにはDiscordの管理者名を入力する必要があります"
            )
        else:
            messagebox.showinfo(
                title="初回セットアップを完了させてください", 
                message="「OK」ボタンを押した後、\nDiscordを開き、BOTを使用するチャンネルで「OK」と入力してください"
            )
            self.root.destroy()

    def exit(self):
        self.root.destroy()
        sys.exit()

    def CreateSettingFile(self,value):
        try:
            with open(self.file, mode="a",encoding='utf-8') as f:
                f.write(value)
        except Exception as e:
            messagebox.showerror("エラーが発生しました！", e.args[0])
            os.remove(self.file)

def Setup():

    # IMAGE FILE ENVIRONMENT
    image:str = os.environ.get("IMAGE_FILE","")
    # SETTING FILE ENVIRONMENT
    file:str = os.environ.get("SETTING_FILE","")

    if not os.path.isfile(file):
        root = tk.Tk()
        root.title(u"MinecraftProxy")
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
        root.iconbitmap(default=image)
        setting = Setting(root=root,file=file)
        setting.mainloop()

        value = (
            f"DISCORD_API={setting.input_msg1}\n"
            f"DISCORD_OWNER={setting.input_msg2}\n"
        )

        setting.CreateSettingFile(value)