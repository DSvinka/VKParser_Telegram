import asyncio
import configparser
import logging

import aiojobs
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher

from app.config import config
from app.utils.vk.group_sender import GroupsCheckNewPostsScheduler

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config['tokens']['telegram_token'], parse_mode="html")
groups_check_new_posts_scheduler = GroupsCheckNewPostsScheduler(bot)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dispatcher):
    logging.info('app >> Launching Bot...')

    logging.info('app >> Setup Webhook...')
    await bot.set_webhook(config['webhook']['host'] + config['webhook']['path'])

    logging.info('app >> Creating Schedulers...')
    await groups_check_new_posts_scheduler.create()

    logging.info('app >> Launching Schedulers...')
    await groups_check_new_posts_scheduler.launch()

    logging.info('app >> Bot Successfully Launched!')


async def on_shutdown(dispatcher):
    logging.info('app >> Disabling Bot...')

    logging.info('app >> Disabling Schedulers...')
    await groups_check_new_posts_scheduler.close()

    logging.info('app >> Removing Webhook...')
    await bot.delete_webhook()

    # logging.info('app >> Закрываю подключение к Redis...')
    # await dispatcher.storage.close()
    # await dispatcher.storage.wait_closed()

    logging.info('app >> Bot Successfully Disabled!')


from app import handlers
from app.utils.auth import create_token
