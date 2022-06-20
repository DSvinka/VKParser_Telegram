import asyncio
from typing import Dict

from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession

import app.utils.vk.group_get
from app import dp
from app.handlers.callbacks.settings import edit_settings_menu, send_settings_menu
from app.utils.vk.base import vk
from app.utils.vk.group_get import group_url_to_short_name, group_get_by_short_name
from app.consts.actions import VKGroupActionsNames, VKGroupsActionsNames
from app.consts.commands import AdminCommandsNames
from app.database.base import get_async_session
from app.database.models.vk_group import VKGroup, VKGroupAdd
from app.database.repositories.vk_groups import VKGroupsRepository

vk_groups_callback = CallbackData('vk_groups', 'action')
vk_group_callback = CallbackData('vk_group', 'id', 'action')


class AddVKGroupForm(StatesGroup):
    url = State()


@dp.callback_query_handler(vk_group_callback.filter(action=VKGroupActionsNames.group))
async def callback_settings_action_group(query: CallbackQuery, callback_data: Dict[str, str]):
    async with get_async_session() as session:
        settings_vk_groups_repository = VKGroupsRepository(session)
        model = await settings_vk_groups_repository.get_by_id(int(callback_data['id']))
        if model is None:
            await query.bot.edit_message_text(
                chat_id=query.message.chat.id, message_id=query.message.message_id,
                text=f"Нечего не найдено...",
                reply_markup=get_settings_back_keyboard()
            )

    await query.bot.edit_message_text(
        chat_id=query.message.chat.id, message_id=query.message.message_id,
        text=f"ID: {model.id} \n"
             f"Название: {model.name} \n"
             f"URL: {model.url}",
        reply_markup=get_group_keyboard(model)
    )

    return await query.answer()


@dp.callback_query_handler(vk_groups_callback.filter(action=VKGroupsActionsNames.group_list))
async def callback_settings_action_group_list(query: CallbackQuery, callback_data: Dict[str, str]):
    vk_groups_list_message = "<b>Список VK Групп на которые подписан бот:</b>\n"
    async with get_async_session() as session:
        settings_vk_groups_repository = VKGroupsRepository(session)
        models: list[VKGroup] = await settings_vk_groups_repository.get_all()

        if len(models) != 0:
            for model in models:
                vk_groups_list_message += f"<u>[ID:{model.id}]</u> {model.name}\n"

        else:
            vk_groups_list_message += f"<pre>\n         ... Пусто ...       \n</pre>"

    await query.bot.edit_message_text(
        chat_id=query.message.chat.id, message_id=query.message.message_id,
        text=vk_groups_list_message,
        reply_markup=get_groups_keyboard(models)
    )

    return await query.answer()


@dp.callback_query_handler(vk_group_callback.filter(action=VKGroupActionsNames.group_del))
async def callback_settings_action_group_del(query: CallbackQuery, callback_data: Dict[str, str]):
    async with get_async_session() as session:
        settings_vk_groups_repository = VKGroupsRepository(session)
        model: VKGroup = await settings_vk_groups_repository.get_by_id(int(callback_data['id']))

        await settings_vk_groups_repository.delete(model)
        await settings_vk_groups_repository.commit()

    await query.answer(
        f'Подписка на группу {model.name} успешно удалена!',
    )

    await edit_settings_menu(query.bot, query.message)

    return await query.answer()


@dp.callback_query_handler(vk_groups_callback.filter(action=VKGroupsActionsNames.group_add))
async def callback_settings_action_group_add(query: CallbackQuery, callback_data: Dict[str, str]):
    await AddVKGroupForm.url.set()
    await query.bot.send_message(
        chat_id=query.message.chat.id,
        text=f'Введите и отправьте ссылку на VK группу, на посты которой вы хотите подписаться.\n'
             f'Введите слово "отмена" для отмены добавления подписки на VK группу.',
    )

    return await query.answer()


@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def callback_settings_action_group_add_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer('Отмена...')

    await send_settings_menu(message.bot, message)


@dp.message_handler(state=AddVKGroupForm.url)
async def callback_settings_action_group_add_process(message: Message, state: FSMContext):
    url = message.text
    short_name = group_url_to_short_name(url)
    group_response = group_get_by_short_name(short_name)

    async with get_async_session() as session:
        vk_groups_repository = VKGroupsRepository(session)
        old_model = await vk_groups_repository.get_by_vk_id(group_response["id"])
        if old_model is not None:
            await state.finish()
            await message.answer(f'Подписка на группу {old_model.name} уже существует...')
            return await send_settings_menu(message.bot, message)

        model_create = VKGroupAdd()
        model_create.vk_id = group_response["id"]
        model_create.name = group_response["name"]
        model_create.url = url

        model = vk_groups_repository.add(model_create)
        await vk_groups_repository.commit()
        await vk_groups_repository.refresh(model)

    await state.finish()
    await message.answer(f'Подписка на группу {model.name} успешно создана!')

    await send_settings_menu(message.bot, message)


from app.utils.keyboards.settings import get_settings_keyboard, get_settings_back_keyboard
from app.utils.keyboards.vk_groups import get_groups_keyboard, get_group_keyboard
