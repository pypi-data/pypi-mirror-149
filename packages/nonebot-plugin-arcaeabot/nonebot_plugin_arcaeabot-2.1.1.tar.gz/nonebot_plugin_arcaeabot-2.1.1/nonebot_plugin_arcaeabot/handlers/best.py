from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from ..data import UserInfo
from ..main import arc
from ..draw_image import UserArcaeaInfo
from .._RHelper import RHelper
from ..utils import json

root = RHelper()


async def best_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "best":
        user_info = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)

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

        # Exception
        if not user_info:
            await arc.finish(MessageSegment.reply(event.message_id) + "你还没绑定呢！")

        if UserArcaeaInfo.is_querying(user_info.arcaea_id):
            await arc.finish(
                MessageSegment.reply(event.message_id) + "您已在查询队列, 请勿重复发起查询。"
            )

        # Query
        result = await UserArcaeaInfo.draw_user_best(
            arcaea_id=user_info.arcaea_id,
            song_id=song["song_id"],
            difficulty=str(difficulty),
        )
        await arc.finish(MessageSegment.reply(event.message_id) + result)
