import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Get token from environment variable
token = os.getenv('TELEGRAM_BOT_TOKEN')
if not token:
    print("Error: TELEGRAM_BOT_TOKEN environment variable is not set")
    sys.exit(1)

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