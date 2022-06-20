from typing import Dict

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from app import dp
from app.consts.actions import SubscriptionsActionsNames
from app.database.base import get_async_session
from app.database.models.chat import ChatAdd
from app.database.repositories.chats import ChatsRepository

subscription_callback = CallbackData('subscription', 'action')


async def send_subscriptions_menu(bot: Bot, message: Message):
    new_message = await bot.send_message(message.chat.id, "Загрузка...")
    await edit_subscriptions_menu(message.bot, new_message)


async def edit_subscriptions_menu(bot: Bot, message: Message):
    user_subscribed_message = "Отключено"
    async with get_async_session() as session:
        chat_repository = ChatsRepository(session)
        current_chat = await chat_repository.get_by_chat_id(message.chat.id)
        if current_chat is not None:
            user_subscribed_message = "Включено"

    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=message.message_id,
        text=f'Эта настройка меняется только у вас. На других пользователей он не влияет. \n'
             f'Настройка уведомлений позволяет отключить отправку постов в этот чат \n'
             '\n'
             f'Отправка новых постов из VK групп в этот канал: <b>{user_subscribed_message}</b>\n',
        reply_markup=get_subscriptions_keyboard()
    )


@dp.callback_query_handler(subscription_callback.filter(action=SubscriptionsActionsNames.menu))
async def callback_subscriptions_menu(query: CallbackQuery, callback_data: Dict[str, str]):
    await send_subscriptions_menu(query.bot, query.message)
    return await query.answer()


@dp.callback_query_handler(subscription_callback.filter(action=SubscriptionsActionsNames.subscribe))
async def callback_subscription_subscribe(query: CallbackQuery, callback_data: Dict[str, str]):
    async with get_async_session() as session:
        chat_repository = ChatsRepository(session)
        current_chat = await chat_repository.get_by_chat_id(query.message.chat.id)
        if current_chat is not None:
            return await query.answer(
                f'Вы уже включили отправку постов из VK групп в этот чат!'
            )

        chat_add = ChatAdd()
        chat_add.chat_id = query.message.chat.id

        chat_repository.add(chat_add)
        await chat_repository.commit()

    await edit_subscriptions_menu(query.bot, query.message)
    return await query.answer(
        f'Вы успешно включили отправку постов из VK групп в этот чат.'
    )


@dp.callback_query_handler(subscription_callback.filter(action=SubscriptionsActionsNames.unsubscribe))
async def callback_subscription_unsubscribe(query: CallbackQuery, callback_data: Dict[str, str]):
    async with get_async_session() as session:
        chat_repository = ChatsRepository(session)
        current_chat = await chat_repository.get_by_chat_id(query.message.chat.id)
        if current_chat is None:
            return await query.message.bot.send_message(
                query.message.chat.id,
                f'У вас уже отключена отправка постов из VK групп в этот чат!'
            )

        await chat_repository.delete(current_chat)
        await chat_repository.commit()

    await edit_subscriptions_menu(query.bot, query.message)
    return await query.answer(
        f'Вы успешно отключили отправку постов из VK групп в этот чат.'
    )

from app.utils.keyboards.subscriptions import get_subscriptions_keyboard
