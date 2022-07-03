import os
import string
import secrets

from libs.minecraft_launcher import MinecraftLauncher
from libs.minecraft_setup import Minecraft_SetUp
from dotenv import load_dotenv

class Commnad:

    def __init__(self):
        self.file = os.environ.get("SETTING_FILE","")

    # Discord Bot Setup
    def discord_setup(self,id,name) -> str:
        with open(self.file, mode="a",encoding='utf-8') as f:
            f.write(
                f"DISCORD_OWNER_ID={id}\n"
                f"RCON_PASSWORD={self.pass_gen()}\n"
                f"SERVER_PORT=25565\n"
                f"RCON_PORT=25575\n"
            )
            send_message: str = (
                f"セットアップ完了！\n"
                f"これで`{name}`さんだけが使えるボットになったよ！\n"
                "使えるコマンドを確認する場合は「!help」と入力してください！"
            )

        load_dotenv(verbose=True,dotenv_path=self.file)
        return send_message

    # Discord Command Help
    def discord_help(self) -> str:
        send_message: str = (
        "```"
        "[使用できるコマンド]\n"
        "!setup -- Minecraftサーバを構築します。\n \
         引数なしは最新。引数にバージョン指定ができます。使用例：!setup 1.18.2\n"
        "!start -- Minecraftサーバを起動します。\n \
         引数なしはsetting.txtのバージョンで立ち上げます。使用例：!start 1.18.2\n"
        "!stop  -- Minecraftサーバを停止します\n"
        "!c     -- Minecraftにコマンドを送信します。使用例：!c weather clear"
        "```"
        )
        return send_message

    # Minecraft Setup
    def minecraft_setup(self,argv) -> str:
        version_check_url = "https://mcversions.net"
        if len(argv) == 2:
            try:
                send_message = Minecraft_SetUp(argv[1]).setup()
            except FileExistsError as e:
                return e.args[0]
            return send_message
            
        else:
            file:str = os.environ.get("SETTING_FILE","")
            version:str =os.environ.get("VERSION","")
            if not version:
                version = Minecraft_SetUp().get_server_url(version_check_url)  # type: ignore
                with open(file, mode="a",encoding='utf-8') as f:
                    f.write(f"VERSION={version}\n")
            send_message = Minecraft_SetUp(version).setup()
            return send_message

    # RCON Password Generator
    def pass_gen(self,size=18) -> str:
        chars = '?%&$#()' + string.ascii_uppercase + string.ascii_lowercase + string.digits
        password = ''.join(secrets.choice(chars) for x in range(size))
        return password

    # Minecraft Start
    def minecraft_start(self,argv) -> str:
        try:
            if len(argv) == 2:
                send_message = MinecraftLauncher(f"minecraft_{argv[1]}/start.bat").start()
                return send_message
            else:
                version = os.environ.get("VERSION")
                send_message = MinecraftLauncher(f"minecraft_{version}/start.bat").start()
                return send_message
        except NotADirectoryError:
            send_message = ":x: **セットアップされていないため、起動できません！**"
            return send_message

    # Minecraft Stop
    def minecraft_stop(self) -> str:
        send_message = MinecraftLauncher().stop()
        return send_message

    # Minecraft Command
    def minecraft_command(self,command) -> str:
        send_message = MinecraftLauncher().cmd(command)
        return send_message