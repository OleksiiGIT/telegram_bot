import sys
import os
from aiogram import Bot, Dispatcher
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
            await message.reply("Hello! I'm your bot written with Python.")
    
    async def start_polling(self):
        """Start the Telegram bot polling"""
        bot = Bot(token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        
        # Clear any existing webhooks and pending updates to avoid conflicts
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            print("Cleared webhooks and pending updates")
        except Exception as e:
            print(f"Warning: Could not clear webhooks: {e}")
        
        print("Starting Telegram bot polling...")
        await self.disp.start_polling(bot, skip_updates=True)
