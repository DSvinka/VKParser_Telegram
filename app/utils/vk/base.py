from vk_api import VkApi

from app import config

vk_session = VkApi(
    token=config['tokens']['vk_token'],
    login=config['vk']['login'],
    password=config['vk']['password'],
)

vk = vk_session.get_api()
