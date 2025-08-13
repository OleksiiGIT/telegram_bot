import asyncio
import logging
import sys
import os
from fastapi import FastAPI
import uvicorn
import threading
from bot import TelegramBot

# FastAPI app for Render.com health checks
app = FastAPI(title="Telegram Bot", description="Squash Court Booking Bot")

@app.get("/")
async def root():
    return {"message": "Telegram bot is running!", "status": "healthy"}

def run_fastapi():
    """Run FastAPI server in a separate thread"""
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

async def main() -> None:
    # Start FastAPI server in a separate thread for Render.com
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    print(f"FastAPI server starting on port {os.getenv('PORT', 8000)}")
    
    # Initialize and start Telegram bot
    telegram_bot = TelegramBot()
    await telegram_bot.start_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())