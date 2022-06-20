from aiogram.types import Message
from aiogram.dispatcher.webhook import SendMessage

from app import dp, bot
from app.consts.commands import AdminCommandsNames
from app.utils.auth import check_auth, auth, send_non_auth_message


@dp.message_handler()
async def message_auth(message: Message):
    if await check_auth(message.chat.id):
        return await message.bot.send_message(
            message.chat.id,
            f"Используйте команду /{AdminCommandsNames.settings_menu} для справки о функциях бота."
        )

    if await auth(message.chat.id, message.text):
        return await message.bot.send_message(
            message.chat.id,
            f"<b>Вы успешно авторизовались!</b> \n"
            f"Используйте команду /{AdminCommandsNames.settings_menu} для справки о функциях бота."
        )

    return await send_non_auth_message(message.bot, message.chat.id)


