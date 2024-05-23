"""
main.py - основний файл звідки запускається бот
"""

import asyncio
import logging
import sys

from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher, types

from settings import bot_token
from app.handlers import router
from aiogram.client.session.aiohttp import AiohttpSession

#  proxy Потрібен для деплою на pythonAnywhere
# session = AiohttpSession(proxy="http://proxy.server:3128")


bot = Bot(bot_token,
          # session=session
          )

dp = Dispatcher()
dp.include_routers(router)


# Головна функція пакету
async def main() -> None:
    # Додаемо "меню" з власнимим командами
    await bot.set_my_commands(commands=[
        types.BotCommand(command="/start", description="Старт бот"),
        types.BotCommand(command="/menu", description="Main menu"),
        types.BotCommand(command="/films", description="Фільми"),
        types.BotCommand(command="/create_film", description="Додати новий фільм"),
        types.BotCommand(command="/cancel", description="Відміна додавання фільму"),
    ]
    )
    # Почнемо обробляти події для бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
