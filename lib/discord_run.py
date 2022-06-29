from lib.command import Commnad
from dotenv import load_dotenv
import discord
import os

class Discord:

    def __init__(self) -> None:
        self.client = discord.Client()
        self.on_ready = self.client.event(self.on_ready)
        self.on_message = self.client.event(self.on_message)

    async def on_ready(self) -> None:
        await self.client.change_presence(
            activity=discord.Game(
                name='MinecraftProxy is Running')
            )
        print ("Connection OK")

    async def on_message(self, message) -> None:
        if message.author.name == os.environ.get("DISCORD_OWNER"):
            owner_id = os.environ.get("DISCORD_OWNER_ID")
            cmd = Commnad()
            if owner_id == None and message.content.startswith("OK"):
                result = cmd.discord_setup(message.author.id,message.author.name)
                await message.channel.send(result)
            elif owner_id == None:
                send_message: str = (
                    "BOTを使用するチャンネルで`OK`と入力し、セットアップを完了させてください！"
                )
                await message.channel.send(send_message)
            elif int(owner_id) == message.author.id:
                if message.content.startswith('!setup'):
                    argv = message.content.split()
                    msg: str = ":arrows_counterclockwise: **セットアップ開始します**"
                    await message.channel.send(msg)
                    result = cmd.minecraft_setup(argv)
                    await message.channel.send(result)

                if message.content.startswith('!start'):
                    argv = message.content.split()
                    msg: str = ":arrows_counterclockwise: **サーバーを起動しています**"
                    await message.channel.send(msg)
                    result = cmd.minecraft_start(argv)
                    await message.channel.send(result)

                elif message.content.startswith('!stop'):
                    msg: str = ":arrows_counterclockwise: **サーバーを停止しています**"
                    await message.channel.send(msg)
                    result = cmd.minecraft_stop()
                    await message.channel.send(result)

                elif message.content.startswith("!c"):
                    command = ' '.join(message.content.split()[1:])
                    try:
                        result = cmd.minecraft_command(command)
                        await message.channel.send(result)
                    except ConnectionRefusedError:
                        result = ":x: サーバが起動していません！"
                        await message.channel.send(result)

                elif message.content.startswith('!help'):
                    result = cmd.discord_help
                    await message.channel.send(result)

    def run(self) -> None:
        setting_file = os.environ.get("SETTING_FILE")
        load_dotenv(verbose=True,dotenv_path=setting_file)
        apikey=os.environ.get("DISCORD_API")
        self.client.run(apikey)