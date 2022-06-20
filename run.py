from aiogram.utils.executor import start_webhook

from app import dp, config, on_startup, on_shutdown

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=config['webhook']['path'],
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host=config['webserver']['host'],
        port=config['webserver']['port'],
    )