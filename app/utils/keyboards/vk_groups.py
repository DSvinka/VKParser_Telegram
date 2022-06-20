from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.consts.actions import VKGroupsActionsNames, VKGroupActionsNames, SettingsActionsNames
from app.database.models.vk_group import VKGroup
from app.handlers.callbacks.settings import settings_callback
from app.handlers.callbacks.vk_groups import vk_group_callback, vk_groups_callback


def get_groups_keyboard(models: list[VKGroup]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "Добавить Группу",
            callback_data=vk_groups_callback.new(action=VKGroupsActionsNames.group_add)
        ),
    )

    for model in models:
        markup.add(
            InlineKeyboardButton(
                model.name,
                callback_data=vk_group_callback.new(id=model.id, action=VKGroupActionsNames.group)
            )
        )

    markup.add(
        InlineKeyboardButton(
            '<< Назад',
            callback_data=settings_callback.new(action=SettingsActionsNames.menu)
        )
    )
    return markup


def get_group_keyboard(model: VKGroup) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "Удалить Группу из подписок",
            callback_data=vk_group_callback.new(id=model.id, action=VKGroupActionsNames.group_del)
        )
    )
    markup.add(
        InlineKeyboardButton(
            '<< Назад',
            callback_data=settings_callback.new(action=SettingsActionsNames.menu)
        )
    )
    return markup