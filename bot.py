import sys
import os
from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import F


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
            await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n\n"
                               "🎾 Welcome to the Squash Court Booking Bot!\n"
                               "Use /help to see available commands.")
        
        @self.disp.message(Command("help"))
        async def command_help_handler(message: Message):
            help_text = (
                "🎾 <b>Squash Court Booking Bot - Commands</b>\n\n"
                "🏠 /start - Welcome message and bot introduction\n"
                "📅 /today - Book a squash court for today\n"
                "🌅 /tomorrow - Book a squash court for tomorrow\n"
                "📆 /book [day] - Book a squash court for a specific day (1-31)\n"
                "   Example: /book 15 (books for the 15th of current month)\n"
                "❓ /help - Show this help message\n\n"
                "📝 <b>How it works:</b>\n"
                "1. Choose a command (/today, /tomorrow, or /book [day])\n"
                "2. Select an available time slot\n"
                "3. Confirm your booking details\n"
                "4. Your court will be booked automatically!\n\n"
                "🏟️ <i>Booking for Caversham Park Squash Court</i>"
            )
            await message.answer(help_text)
        
        @self.disp.message(Command("today"))
        async def command_today_handler(message: Message):
            await message.answer("🎾 Booking squash court for today...\n"
                               "⚠️ This feature is coming soon!")
        
        @self.disp.message(Command("tomorrow"))
        async def command_tomorrow_handler(message: Message):
            await message.answer("🎾 Booking squash court for tomorrow...\n"
                               "⚠️ This feature is coming soon!")
        
        @self.disp.message(Command("book"))
        async def command_book_handler(message: Message):
            # Extract the day from the command arguments
            command_text = message.text or ""
            parts = command_text.split()
            
            if len(parts) < 2:
                await message.answer(
                    "📆 <b>Book Command Usage:</b>\n\n"
                    "Please specify a day of the month (1-31):\n"
                    "Example: <code>/book 15</code>\n\n"
                    "This will book a squash court for the 15th of the current month."
                )
                return
            
            try:
                day = int(parts[1])
                if 1 <= day <= 31:
                    await message.answer(
                        f"🎾 Booking squash court for day {day} of current month...\n"
                        "⚠️ This feature is coming soon!\n\n"
                        f"📅 Selected date: Day {day}\n"
                        "🏟️ Court: Squash Court"
                    )
                else:
                    await message.answer(
                        "❌ <b>Invalid day!</b>\n\n"
                        "Please enter a day between 1 and 31.\n"
                        "Example: <code>/book 15</code>"
                    )
            except ValueError:
                await message.answer(
                    "❌ <b>Invalid format!</b>\n\n"
                    "Please enter a valid number for the day.\n"
                    "Example: <code>/book 15</code>"
                )
    
    async def start_polling(self):
        """Start the Telegram bot polling"""
        bot = Bot(token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        print("Starting Telegram bot polling...")
        await self.disp.start_polling(bot)
