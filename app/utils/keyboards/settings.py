from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.consts.actions import SettingsActionsNames, VKGroupsActionsNames, SubscriptionsActionsNames


def get_settings_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "Управление Группами",
            callback_data=vk_groups_callback.new(action=VKGroupsActionsNames.group_list)
        )
    )
    markup.add(
        InlineKeyboardButton(
            "Управление Уведомлениями",
            callback_data=subscription_callback.new(action=SubscriptionsActionsNames.menu)
        )
    )
    return markup


def get_settings_back_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            '<< Назад',
            callback_data=settings_callback.new(action=SettingsActionsNames.menu)
        )
    )
    return markup


from app.handlers.callbacks.settings import settings_callback
from app.handlers.callbacks.vk_groups import vk_groups_callback
from app.handlers.callbacks.subscriptions import subscription_callback
