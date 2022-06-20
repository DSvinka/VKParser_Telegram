import secrets
from aiogram import Bot

from app import config
from app.database.base import get_async_session
from app.database.models.access_token import AccessTokenUpdate, AccessTokenAdd, AccessToken
from app.database.models.chat import ChatAdd
from app.database.repositories.access_tokens import AccessTokensRepository
from app.database.repositories.chats import ChatsRepository


async def send_non_auth_message(bot: Bot, chat_id: str):
    await bot.send_message(
        chat_id,
        f'Здравствуйте! Это бот для отправки уведомлений о новых постах в VK сообществах. (VK группах) \n'
        f'Групп может быть не ограниченное количество. Как и людей которые подписались на уведомления. \n'
        f'\n'
        f'Но для использования бота, вам необходимо авторизоваться! \n'
        f'<u>Для этого отправьте боту ключ, без пробелов и дополнительных знаков.</u> \n'
        f'<b>Ключ можно получить только у администратора бота.</b> \n'
        f'\n'
        f'<u>Бот создан специально для страйкбольной команды "Гунгнир"</u> \n',
    )


async def check_auth(chat_id: str) -> bool:
    async with get_async_session() as session:
        access_token_repository = AccessTokensRepository(session)
        access_token = await access_token_repository.get_by_chat_id(chat_id)
        if access_token is not None:
            return True

    return False


async def auth(chat_id: str, token: str) -> bool:
    async with get_async_session() as session:
        access_token_repository = AccessTokensRepository(session)
        chats_repository = ChatsRepository(session)

        access_token_by_chat_id = await access_token_repository.get_by_chat_id(chat_id)
        if access_token_by_chat_id is not None:
            return True

        access_token = await access_token_repository.get_by_token(token)
        if access_token is None:
            return False

        if access_token.chat_id is not None:
            return False

        chat = await chats_repository.get_by_chat_id(chat_id)
        if chat is not None:
            await chats_repository.delete(chat)

        access_token_update = AccessTokenUpdate()
        access_token_update.chat_id = chat_id

        chat_add = ChatAdd()
        chat_add.chat_id = chat_id

        access_token_repository.update(access_token, access_token_update)
        chats_repository.add(chat_add)

        await access_token_repository.commit()
        await chats_repository.commit()

        return True


async def create_token() -> AccessToken:
    async with get_async_session() as session:
        random_token: str = ""
        access_token_repository = AccessTokensRepository(session)

        while True:
            random_token = secrets.token_hex(int(config['auth']['token_large']))
            access_token_search = await access_token_repository.get_by_token(random_token)
            if access_token_search is None:
                break

        access_token_add = AccessTokenAdd()
        access_token_add.token = random_token

        access_token = access_token_repository.add(access_token_add)
        await access_token_repository.commit()
        await access_token_repository.refresh(access_token)

        return access_token