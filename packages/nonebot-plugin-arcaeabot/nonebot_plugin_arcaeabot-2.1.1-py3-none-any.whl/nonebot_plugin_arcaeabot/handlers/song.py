from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..main import arc
from ..draw_text import draw_song
from .._RHelper import RHelper
from ..utils import json

root = RHelper()


async def song_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "song" or args[0] == "songs":

        slst_json = root.assets / ("slst.json")
        with open(slst_json, "r") as file:
            data = json.load(file)

        difficulty = 233
        if args[-1].strip().lower() == "byd":
            difficulty = 3
        elif args[-1].strip().lower() == "ftr":
            difficulty = 2
        elif args[-1].strip().lower() == "prs":
            difficulty = 1
        elif args[-1].strip().lower() == "pst":
            difficulty = 0

        if 0 <= difficulty <= 3:
            song_id = " ".join(args[1:-1])
        else:
            song_id = " ".join(args[1:])

        song = "no_song"
        for s in data["songs"]:
            if s["song_id"] == song_id:
                song = s
            if (
                s["difficulties"][0]["name_en"] == song_id
                or s["difficulties"][0]["name_jp"] == song_id
            ):
                song = s
            if len(s["difficulties"]) == 4:
                if (
                    s["difficulties"][3]["name_en"] == song_id
                    or s["difficulties"][3]["name_jp"] == song_id
                ):
                    song = s
            for alias in s["alias"]:
                if alias == song_id:
                    song = s

        # check
        if song == "no_song":
            await arc.finish(MessageSegment.reply(event.message_id) + "曲目不存在！")

        if len(song["difficulties"]) == 3 and difficulty == 3:
            await arc.finish(MessageSegment.reply(event.message_id) + "难度不存在！")

        if difficulty == 233:
            difficulty = "all"

        await arc.finish(
            MessageSegment.reply(event.message_id)
            + draw_song(song_info=song, difficulty=difficulty)
        )
