#! env python
# -*- coding: utf-8 -*-
"""
  main.py
    ドラクエを小一時間で作ってみた
    https://www.youtube.com/watch?v=TfSLsT4fkCE&t=4205s

  Created by Seiji Ota on 2021/01/2.

"""


import os
from PIL import Image
from enum import IntEnum, auto
import sys
import tty
import termios

# Unicode制御文字のエイリアス
EOT = 3
TAB = 9
ESC = 27

# マップチップ
class MapChip(IntEnum):
    SEA = 0
    SEA2 = auto()
    PLANE = auto()
    FOREST = auto()
    MOUNTAIN = auto()
    ROCK = auto()
    WALL = auto()
    DESERT = auto()
    POISON = auto()
    BRIDGE = auto()
    CASTLE = auto()
    TOWN = auto()
    DUNGEON = auto()
    SHRINE = auto()
    STAIRS = auto()
    MAX = auto()


# フラグ定義
class Flag(IntEnum):
    MAGIC_KEY = 0
    RORA_RESCUED = auto()
    RORA_LOVE = auto()
    SUN_STONE = auto()
    SILVER_HERP = auto()
    RAIN_CLOUD_STAFF = auto()
    FAIRY_FLUTE = auto()
    ROTO_ARMOR = auto()
    GOLEM_KILLED = auto()
    ROTO_EMBLEM = auto()
    RAINBOW_DROP = auto()
    RAINBOW_BRIDGE = auto()
    LIGHT_BALL = auto()
    MAX = auto()


# フラグ
flags = [0 for i in range(Flag.MAX)]

FIELD_WIDTH = 136
FIELD_HEIGHT = 136

map = [[0 for i in range(FIELD_WIDTH)] for j in range(FIELD_HEIGHT)]

# フィールド詳細
cell_descs = [
    ((91, 119, 234), "〜", True),  # SEA
    ((90, 119, 234), "~~", True),  # SEA2
    ((121, 195, 0), "．", False),  # PLANE
    ((50, 132, 5), "木", False),  # FOREST
    ((123, 158, 23), "山", False),  # MOUNTAIN
    ((109, 128, 70), "岩", True),  # ROCK
    ((154, 154, 154), "壁", True),  # WALL
    ((231, 209, 119), "砂", False),  # DESERT
    ((16, 45, 0), "毒", False),  # POISON
    ((111, 117, 142), "橋", False),  # BRIDGE
    ((117, 118, 122), "城", False),  # CASTLE
    ((126, 127, 130), "町", False),  # TOWN
    ((62, 75, 37), "穴", False),  # DUNGEON
    ((167, 87, 167), "祠", False),  # SHRINE
    ((100, 109, 81), "階", False),  # STAIRS
]

# プレイヤーの位置
playerX = 51
playerY = 52

# キーボード入力
def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


# BMP画像からマップデータを作成
def create_map():
    # 自前で読むのもいいかも。原始的な方が楽しいよ。
    # https://www.tutimogura.com/python-bitmap-read/
    map_bmp_path = os.path.join(os.getcwd(), "assets", "map.bmp")
    map_bmp = Image.open(map_bmp_path)
    map_rgb = map_bmp.convert("RGB")
    size = map_rgb.size
    im2 = Image.new("RGBA", size)

    for y in range(size[1]):
        for x in range(size[0]):
            # ピクセルを取得
            rgb = map_rgb.getpixel((x, y))

            # マップチップに変換
            for cellDesc in cell_descs:
                if cellDesc[0] == rgb:
                    map[x][y] = cellDesc


# マップの表示
def draw_map():
    os.system("clear")
    for y in range(-8, 8):
        for x in range(-8, 8):
            x2 = playerX + x
            y2 = playerY + y
            if x2 == playerX and y2 == playerY:
                print("勇", end="")
            else:
                print(map[x2][y2][1], end="")
        print("")
    print("x: " + str(playerX) + ", y: " + str(playerY))


def event_radatom(event):
    if flags[Flag.MAGIC_KEY]:
        flags[Flag.SUN_STONE] = True
        print("城の裏の地下で太陽の石を手に入れた！")
    else:
        print("城の裏に何かありそうだが、鍵がかかっていて入れない。")


def event_dungeon_north(event):
    if flags[Flag.RORA_RESCUED] == False:
        if flags[Flag.MAGIC_KEY]:
            print("ドラゴンを倒してローラ姫を救出した！")
            flags[Flag.RORA_RESCUED] = True
        else:
            print("ダンジョンに扉があるが、鍵がかかっていて入れない。")

    global playerX, playerY
    playerX = event_locations[2][0][0]
    playerY = event_locations[2][0][1]


def event_dungeon_south(event):
    print("event_dungeon_south")


def event_rimurudaru(event):
    print("event_rimurudaru")


def event_garai(event):
    print("event_garai")


def event_rain_cloud(event):
    print("event_rain_cloud")


def event_maira(event):
    print("event_maira")


def event_domudora(event):
    print("event_domudora")


def event_golem(event):
    print("event_golem")


def event_merukido(event):
    print("event_merukido")


def event_roto_emblem(event):
    print("event_roto_emblem")


def event_holly(event):
    print("event_holly")


def event_rainbow_bridge(event):
    print("event_rainbow_bridge")


def event_dragon_king(event):
    print("event_dragon_king")


# イベントロケーション
event_locations = [
    ((51, 51), event_radatom),
    ((112, 52), event_dungeon_north),
    ((112, 57), event_dungeon_south),
    ((110, 80), event_rimurudaru),
    ((10, 10), event_garai),
    ((89, 9), event_rain_cloud),
    ((112, 18), event_maira),
    ((33, 97), event_domudora),
    ((81, 108), event_golem),
    ((136, 136), event_merukido),
    ((91, 121), event_roto_emblem),
    ((116, 117), event_holly),
    ((73, 57), event_rainbow_bridge),
    ((56, 56), event_dragon_king),
]


def event_control():
    for event_location in event_locations:
        if playerX == event_location[0][0] and playerY == event_location[0][1]:
            # イベント発生
            event_location[1](event_location)
            break


def main():
    create_map()

    # メインループ
    while True:
        draw_map()
        event_control()

        # キー入力
        global playerX, playerY
        x = playerX
        y = playerY
        key = ord(getch())
        if key == ESC:
            break
        elif key == ord("w"):
            y = y - 1
        elif key == ord("s"):
            y = y + 1
        elif key == ord("a"):
            x = x - 1
        elif key == ord("d"):
            x = x + 1
        else:
            continue

        if map[x][y][2] == False:
            playerY = y
            playerX = x


if __name__ == "__main__":
    main()
