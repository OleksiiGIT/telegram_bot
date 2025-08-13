import sys
import os
from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


class TelegramBot:
    def __init__(self):
        # Get token from environment variable
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            print("Error: TELEGRAM_BOT_TOKEN environment variable is not set")
            sys.exit(1)
        
        self.disp = Dispatcher()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup message handlers"""
        @self.disp.message(CommandStart())
        async def command_start_handler(message: Message):
            await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    
    async def start_polling(self):
        """Start the Telegram bot polling"""
        bot = Bot(token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        print("Starting Telegram bot polling...")
        await self.disp.start_polling(bot)
