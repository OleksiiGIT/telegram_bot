import asyncio
import logging
import sys
import ssl
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession

token = '8445356732:AAF-19VhpFcwT2rUW81HOgry1yZ9RxY1QTY'
disp = Dispatcher()

@disp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.reply("Hello! I'm your bot.")

async def main() -> None:
    # Create SSL context that doesn't verify certificates (for development only)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Create aiohttp connector with disabled SSL verification
    # connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    # Create custom session with the connector
    session = aiohttp.ClientSession(verify_ssl=False)
    
    # Create bot with custom session that bypasses SSL verification
    bot = Bot(
        token=token, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session
    )

    try:
        await disp.start_polling(bot)
    finally:
        await session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())