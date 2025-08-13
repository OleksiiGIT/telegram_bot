import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

token = '8445356732:AAF-19VhpFcwT2rUW81HOgry1yZ9RxY1QTY'
disp = Dispatcher()

@disp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.reply("Hello! I'm your bot written with Python.")

async def main() -> None:
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await disp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())