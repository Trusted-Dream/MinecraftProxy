# Minecraft_Proxy
![Python Version](https://img.shields.io/badge/Python-3.8%2B-orange)

## 概要
Minecraft ServerをDiscordから構築/開始/停止が行えます

## 環境
Windows 10,11

## 実行ファイル
[MinecraftProxy_v1.2](https://github.com/Trusted-Dream/MinecraftProxy/releases/tag/v1.2)

## 動作に必要な項目
- [Discord API](https://discord.com/developers/applications)

## ウィルスと誤検知してしまった場合の対処方法
- [Wiki](https://github.com/Trusted-Dream/MinecraftProxy/wiki/%E7%A2%BA%E8%AA%8D%E3%81%97%E3%81%A6%E3%81%84%E3%82%8B%E4%B8%8D%E5%85%B7%E5%90%88)
## Discord コマンド
 - `!help`
 - `!setup {Ver}`
 - `!stat {Ver}`
 - `!stop`


## プログラム実行方法
```
$ pip install .
$ python launch.py
```
※ Tkinter は必須です。

- [Tkinter Dev](https://www.tcl.tk/software/tcltk/download.html)

## バイナリ化方法
- nuitka を使いました。ビルドに結構時間かかりますが、ファイルが小さく速度も速いです。
```
$ pip install nuitka zstandard
$ pip install .
$ python -m nuitka --windows-disable-console --onefile --mingw64 --windows-icon-from-ico=minecraft.ico --enable-plugin=tk-inter --include-data-file="D:/Path/MinecraftProxy/minecraft.ico=./" --follow-imports --show-progress --output-dir=output -o minecraft_proxy.exe launch.py
```
※1 `--include-data-file` は`minecraft.ico`の階層までの絶対パスを記述します。`=./`はそのままでOK

※2 `mingw64`を使用しています。

- 実行したディレクトリに`minecraft_proxy.exe`があればOK

## その他
 - バグ等の報告は大歓迎です
 - Issue上げてください