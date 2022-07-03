import requests
import lxml.html
import os
import re
import subprocess as prc
from typing import Union
from libs.minecraft_launcher import MinecraftLauncher
from bs4 import BeautifulSoup

class Minecraft_SetUp:

    def __init__(self,argv=None):
        self.session = requests.session()
        # Switch User Agent
        self.user_agent = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                AppleWebKit/537.36 (KHTML, like Gecko)\
                Chrome/103.0.0.0 Safari/537.36"
                }
        self.dirname = f"minecraft_{argv}"
        self.jarname = f"server_{argv}.jar"
        self.download_url = f"https://mcversions.net/download/{argv}"

    def get_server_url(self,url) -> Union[str,None]:
        request = self.session.get(
                url,
                timeout=5,
                headers = self.user_agent
        )
        if request.status_code == requests.codes.ok:
            soup = BeautifulSoup(request.text, "html.parser")
            lxml_data = lxml.html.fromstring(str(soup))
            if "download" in url:
                lxml_data.xpath('/html/body/main/div/div[1]/div[2]/div[1]/a')
                for _, _, link, _ in lxml_data[1].iterlinks():
                    if "server.jar" in link:
                        return link
            else:
                p=r"\d{4}-\d{1,2}-\d{1,2}"
                s = lxml_data.xpath('string(///div[1]/p)')[1:]
                version=re.sub(p,'',s)
                return version

    def create_setup_file(self):
        os.makedirs(self.dirname)
        eulafile = f"{self.dirname}/eula.txt"
        url = self.get_server_url(self.download_url)
        urlData = requests.get(url).content
        with open(f"{self.dirname}/{self.jarname}" ,mode='wb') as f:
            f.write(urlData)
        with open(eulafile, mode='w') as f:
            f.write("eula=true")

    def create_batch_file(self):
        batch_filename = f"{self.dirname}/start.bat"
        # Initial Value -Xmx1024M -Xms1024M
        batch_contents = (
            f"java -Xmx1024M -Xms1024M -jar {self.jarname} nogui"
        )
        with open(batch_filename, mode='w') as f:
            f.write(batch_contents)

    def setup(self):
        self.create_setup_file()
        self.create_batch_file()
        launcher = MinecraftLauncher(f"{self.dirname}/start.bat")
        result = launcher.start("setup")
        if "起動しました" in result:
            prc.run("taskkill /F /IM cmd.exe /T", shell=True)
            launcher.server_properties()
            msg = ":white_check_mark: セットアップ完了しました。"
            return msg
        else:
            msg = ":x: セットアップに失敗しました。"
            return msg