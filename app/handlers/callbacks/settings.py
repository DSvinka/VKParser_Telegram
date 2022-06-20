import asyncio
from typing import Dict

from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession

from app import dp
from app.consts.actions import SettingsActionsNames
from app.consts.commands import AdminCommandsNames

settings_callback = CallbackData('settings', 'action')


class AddVKGroupForm(StatesGroup):
    url = State()


async def send_settings_menu(bot: Bot, message: Message):
    new_message = await bot.send_message(message.chat.id, "Загрузка...")
    await edit_settings_menu(message.bot, new_message)


async def edit_settings_menu(bot: Bot, message: Message):
    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=message.message_id,
        text="Меню настроек. \nДля редактирования настроек используйте кнопки.\n"
             "\n"
             "Для управлением ключами доступа используйте следующие команды: \n"
             f"/{AdminCommandsNames.access_token_add} - Создать ключ доступа \n"
             f"/{AdminCommandsNames.access_token_del} (ID) - Удалить ключ доступа \n"
             f"/{AdminCommandsNames.access_token_list} - Получить список ключей доступа и их ID \n"
             f"\n"
             f"<b>Справка:</b> Ключи доступа требуются для выдачи доступа к боту другим людям. "
             f"Они смогут получать уведомления о новых постах, добавлять/удалять группы из подписок и генерировать ключи доступа. \n",
        reply_markup=get_settings_keyboard()
    )


@dp.callback_query_handler(settings_callback.filter(action=SettingsActionsNames.menu))
async def callback_settings_action_menu(query: CallbackQuery, callback_data: Dict[str, str]):
    await edit_settings_menu(query.bot, query.message)

    return await query.answer()

from app.utils.keyboards.settings import get_settings_keyboard
