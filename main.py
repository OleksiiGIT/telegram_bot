import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI
import uvicorn
import threading

# Get token from environment variable
token = os.getenv('TELEGRAM_BOT_TOKEN')
if not token:
    print("Error: TELEGRAM_BOT_TOKEN environment variable is not set")
    sys.exit(1)

# FastAPI app for Render.com health checks
app = FastAPI(title="Telegram Bot", description="Squash Court Booking Bot")

@app.get("/")
async def root():
    return {"message": "Telegram bot is running!", "status": "healthy"}

def run_fastapi():
    """Run FastAPI server in a separate thread"""
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

disp = Dispatcher()

@disp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.reply("Hello! I'm your bot written with Python.")

async def main() -> None:
    # Start FastAPI server in a separate thread for Render.com
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    print(f"FastAPI server starting on port {os.getenv('PORT', 8000)}")
    
    # Start Telegram bot
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    print("Starting Telegram bot polling...")
    
    await disp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())