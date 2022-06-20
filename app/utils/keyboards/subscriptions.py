from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.consts.actions import SubscriptionsActionsNames, SettingsActionsNames


def get_subscriptions_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "Включить отправку постов из VK групп в этот чат",
            callback_data=subscription_callback.new(action=SubscriptionsActionsNames.subscribe)
        )
    )

    markup.add(
        InlineKeyboardButton(
            "Отключить отправку постов из VK групп в этот чат",
            callback_data=subscription_callback.new(action=SubscriptionsActionsNames.unsubscribe)
        )
    )

    markup.add(
        InlineKeyboardButton(
            '<< Назад',
            callback_data=settings_callback.new(action=SettingsActionsNames.menu)
        )
    )
    return markup


from app.handlers.callbacks.subscriptions import subscription_callback
from app.handlers.callbacks.settings import settings_callback
