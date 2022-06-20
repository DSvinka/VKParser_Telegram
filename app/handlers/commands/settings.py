from aiogram.types import Message

from app import dp
from app.consts.commands import AdminCommandsNames
from app.handlers.callbacks.settings import edit_settings_menu


@dp.message_handler(commands=AdminCommandsNames.settings_menu)
async def command_settings_menu(message: Message):
    new_message = await message.bot.send_message(message.chat.id, "Загрузка...")
    await edit_settings_menu(message.bot, new_message)
