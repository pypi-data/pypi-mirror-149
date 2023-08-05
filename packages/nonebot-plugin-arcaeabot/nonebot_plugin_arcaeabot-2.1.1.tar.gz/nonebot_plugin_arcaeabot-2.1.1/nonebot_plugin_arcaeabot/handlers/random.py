import random
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..main import arc
from ..draw_text import draw_song
from .._RHelper import RHelper
from ..utils import is_float_num, json

root = RHelper()


async def random_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "random":
        with open(root.assets / "slst.json", "r", encoding="UTF-8") as f:
            slst = json.loads(f.read())
        min: int = 0
        max: int = 1150

        if len(args) == 2:
            if is_float_num(args[1]):
                min = float(args[1].strip()) * 10
                max = float(args[1].strip()) * 10
            else:
                min, max = int(args[1]), int(args[1])

        if len(args) >= 3:

            if is_float_num(args[1]):
                min = float(args[1].strip()) * 10
            if is_float_num(args[2]):
                max = float(args[2].strip()) * 10

        if min > max:
            await arc.finish(MessageSegment.reply(event.message_id) + "最小难度大于最大难度")

        n = 0
        for s in slst["songs"]:
            for l in s["difficulties"]:
                if min <= l["rating"] <= max:
                    n = n + 1
                    break

        n = random.randint(0, n - 1)
        song = "no_song"

        for s in slst["songs"]:
            for l in s["difficulties"]:
                if min <= l["rating"] <= max:
                    if n == 0:
                        song = s
                    n = n - 1
                    break

        if song == "no_song":
            await arc.finish(MessageSegment.reply(event.message_id) + "此难度下不存在歌曲")

        await arc.finish(
            MessageSegment.reply(event.message_id) + draw_song(song_info=song)
        )
