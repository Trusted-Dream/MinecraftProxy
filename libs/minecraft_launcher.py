import subprocess as prc
import time
import os
import pathlib
import re

from mcrcon import MCRcon
from typing import Union

class MinecraftLauncher:
    def __init__(self,batchfile=""):
        self.batchfile = batchfile
        self.rcon_password=os.environ.get("RCON_PASSWORD")
        self.server_port=os.environ.get("SERVER_PORT")
        self.rcon_port = os.environ.get("RCON_PORT")
        self.cwd = pathlib.Path(batchfile).resolve().parent

    def port_check(self) -> bytes:
        cmd = f'netstat -nao |findstr "0.0.0.0:{self.rcon_port}"'
        port = prc.Popen(cmd, shell=True,stdout=prc.PIPE)
        stdout,_ = port.communicate()
        return stdout

    def server_properties(self) -> None:
        file = f"{self.cwd}//server.properties"

        with open(file, mode="r",encoding='utf-8') as f:
            data_lines = f.read()
            data_lines = data_lines.replace("enable-rcon=false", "enable-rcon=true")
            data_lines = data_lines.replace("server-port=25565", f"server-port={self.server_port}")
            data_lines = data_lines.replace("query.port=25565", f"query.port={self.server_port}")
            data_lines = data_lines.replace("rcon.port=25575", f"rcon.port={self.rcon_port}")
            if not "rcon.password=" in data_lines:
                data_lines += f"rcon.password={self.rcon_password}\n"
            elif not f"rcon.password={self.rcon_password}" in data_lines:
                data_lines = data_lines.replace("rcon.password=",f"rcon.password={self.rcon_password}")

        with open(file, mode="w", encoding='utf-8') as f:
            f.write(data_lines)

    def latest_log_check(self) -> list:
        log_file = f"{self.cwd}//logs/latest.log"
        p=r"Done.*!\s.*"
        with open(log_file, mode="r") as f:
            result = [x for x in f.readlines() if re.search(p,x) is not None]
            return result

    def start(self,switch=None) -> str:
        cwd = pathlib.Path(self.batchfile).resolve().parent
        prc.Popen("start.bat", cwd=cwd,shell=True)

        # 3分間チェックする
        for x in range(60):
            time.sleep(2)
            if switch == "setup":
                try:
                    check = self.latest_log_check()
                except FileNotFoundError as e:
                    return e.args[1]
            else:
                check = self.port_check()
            if check:
                break
        else:
            msg = f":x: サーバーが正常に起動しませんでした"
            return msg
        
        msg = f":white_check_mark: サーバーを起動しました"
        return msg

    def stop(self) -> str:
        with MCRcon("localhost", self.rcon_password, int(self.rcon_port)) as mcr:
            mcr.command("/stop")
            # 3分間チェックする
            for x in range(60):
                time.sleep(2)
                check = self.port_check()
                if not check:
                    break
            else:
                msg = f":x: サーバーが正常に停止しませんでした"
                return msg

            msg = ":white_check_mark: サーバーを停止しました"
            prc.run("taskkill /F /IM cmd.exe /T", shell=True)
            return msg

    def cmd(self,cmd) -> str:
        with MCRcon("localhost", self.rcon_password, int(self.rcon_port)) as mcr:
            mcr.command(cmd)
            msg = f":white_check_mark: 以下コマンドを実行しました\n`{cmd}`"
            return msg