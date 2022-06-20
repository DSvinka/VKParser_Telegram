import asyncio
import logging
import re

import aiojobs
from aiogram import Bot
from app.config import config

from app.database.base import get_async_session
from app.database.models.vk_group import VKGroupUpdate, VKGroup
from app.database.repositories.chats import ChatsRepository
from app.database.repositories.vk_groups import VKGroupsRepository
from app.utils.vk.base import vk


class GroupsCheckNewPostsScheduler:
    def __init__(self, bot: Bot):
        self._scheduler = None
        self._bot = bot

    async def create(self):
        self._scheduler = await aiojobs.create_scheduler()

    async def launch(self):
        await self._scheduler.spawn(self.groups_check_new_posts())

    async def close(self):
        await self._scheduler.close()

    async def groups_check_new_posts(self) -> None:
        while True:
            async with get_async_session() as session:
                vk_groups_repository = VKGroupsRepository(session)
                groups = await vk_groups_repository.get_all()

                await asyncio.sleep(len(groups) + int(config['ratelimit']['additional_pause_between_new_posts_check']))

                for group in groups:
                    await asyncio.sleep(int(config['ratelimit']['pause_between_group_request']))

                    response = vk.wall.get(
                        owner_id="-" + group.vk_id,
                        count="1",
                        filter="owner",
                        extended="1",
                        offset=0
                    )

                    logging.debug(response)

                    try:
                        if (
                                str(response["items"][0]["is_pinned"]) == "1"
                                and
                                (group.last_post_id is None or int(response["items"][0]["id"]) <= group.last_post_id)
                        ):

                            response = vk.wall.get(
                                owner_id="-" + group.vk_id,
                                count="1",
                                filter="owner",
                                extended="1",
                                offset=1,
                            )
                            logging.debug(response)

                    except KeyError:
                        pass

                    for item in response["items"]:
                        if (
                                (group.last_post_id is None or group.last_post_id < int(item["id"]))
                                and item["marked_as_ads"] != 1
                                and not item["text"].find("#партнёр") != -1
                                and not item["text"].find("#ad") != -1
                                and len(re.findall(r"\w+\|\w+", item["text"])) == 0
                        ):
                            try:
                                await self.send_post_to_telegram(item, group)
                            except Exception as error:
                                logging.error(error)
                                logging.info(item)

                            vk_groups_repository = VKGroupsRepository(session)
                            vk_group_update = VKGroupUpdate()
                            vk_group_update.last_post_id = int(item["id"])

                            vk_groups_repository.update(group, vk_group_update)
                            await vk_groups_repository.commit()

    async def send_post_to_telegram(self, response, group: "VKGroup"):
        async with get_async_session() as session:
            chats_repository = ChatsRepository(session)
            chats = await chats_repository.get_all()

            post_url = f'{group.url}?w=wall-{group.vk_id}_{response["id"]}'
            group_href = f'{group.name}'
            post_href = f'<a href="{post_url}">Ссылка на пост</a>'

            for chat in chats:
                await self._bot.send_message(
                    chat.chat_id,
                    f'В VK Группе "{group_href}" появился новый пост! \n'
                    f'\n'
                    f'{response["text"]}\n'
                    f'{post_href}'
                )
