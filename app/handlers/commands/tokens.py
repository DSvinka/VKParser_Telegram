from aiogram.types import Message

from app import dp
from app.consts.commands import AdminCommandsNames
from app.database.base import get_async_session
from app.database.repositories.access_tokens import AccessTokensRepository
from app.utils.auth import create_token


@dp.message_handler(commands=AdminCommandsNames.access_token_add)
async def command_token_add(message: Message):
    async with get_async_session() as session:
        access_token = await create_token()

    await message.bot.send_message(
        message.chat.id,
        f'Ключ успешно создан! Не давайте ключ тем, кому вы не доверяете! \n'
        f'<code>{access_token.token}</code>'
    )


@dp.message_handler(commands=AdminCommandsNames.access_token_del)
async def command_token_del(message: Message):
    async with get_async_session() as session:
        if len(message.text.split(" ")) == 1 or not message.text.split(" ")[1].isdigit():
            return await message.bot.send_message(
                message.chat.id,
                f'Введите ID ключа вместе с командой! \n'
                f'ID ключа можно посмотреть командой /{AdminCommandsNames.access_token_list}'
            )

        access_tokens_repository = AccessTokensRepository(session)
        access_token = await access_tokens_repository.get_by_id(int(message.text.split(" ")[1]))
        if access_token is None:
            return await message.bot.send_message(
                message.chat.id,
                f'Ключ не найден! Введите ID ключа вместе с командой. \n'
                f'ID ключа можно посмотреть командой /{AdminCommandsNames.access_token_list}'
            )

        await access_tokens_repository.delete(access_token)
        await access_tokens_repository.commit()

    await message.bot.send_message(
        message.chat.id,
        f'Ключ <b>{access_token.token}</b> успешно удален!'
    )


@dp.message_handler(commands=AdminCommandsNames.access_token_list)
async def command_token_list(message: Message):
    tokens_list_message = f'<b>Список всех ключей:</b>. \n'
    async with get_async_session() as session:
        access_tokens_repository = AccessTokensRepository(session)
        access_tokens = await access_tokens_repository.get_all()

        if len(access_tokens) != 0:
            for access_token in access_tokens:
                token_used = "Используется" if access_token.chat_id is not None else "Не Используется"
                tokens_list_message += f'<u>[ID:{access_token.id}]</u> {access_token.token} - {token_used} \n'
        else:
            tokens_list_message += f'<pre>\n         ... Пусто ...       \n</pre>'

    await message.bot.send_message(
        message.chat.id,
        tokens_list_message
    )