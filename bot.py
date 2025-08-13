import sys
import os
from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import F
from service import (
    initialize_driver,
    get_squash_court_times,
    select_and_click_timeslot,
    fill_booking_form,
    submit_booking_form
)


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
                preferred_day = int(parts[1])
                if not (1 <= preferred_day <= 31):
                    await message.answer(
                        "❌ <b>Invalid day!</b>\n\n"
                        "Please enter a day between 1 and 31.\n"
                        "Example: <code>/book 15</code>"
                    )
                    return
            except ValueError:
                await message.answer(
                    "❌ <b>Invalid format!</b>\n\n"
                    "Please enter a valid number for the day.\n"
                    "Example: <code>/book 15</code>"
                )
                return
            
            await message.answer(f"🎾 Starting squash court booking for day {preferred_day}...\n"
                               f"📅 Selected date: Day {preferred_day}\n"
                               f"🏟️ Court: Squash Court\n\n"
                               f"⏳ Please wait while I check available time slots...")
            
            # Run the booking process in an executor to avoid blocking
            try:
                # Step 1: Initialize the driver
                driver = initialize_driver(headless=True)
                
                try:
                    # Step 2: Get time slots for the selected day
                    time_slots = get_squash_court_times(driver, preferred_day, timeout=30)
                    
                    if time_slots:
                        # Step 3: Display available time slots
                        slots_text = f"\n🕐 <b>Available Time Slots for Day {preferred_day}:</b>\n"
                        available_slots = []
                        
                        for i, slot in enumerate(time_slots, 1):
                            text = slot.get('text', '').strip()
                            enabled = slot.get('is_enabled', False)
                            displayed = slot.get('is_displayed', False)
                            
                            if text and enabled and displayed:
                                available_slots.append((i, text, slot))
                                slots_text += f"{i}. {text} ✅\n"
                            else:
                                slots_text += f"{i}. {text or 'No text'} ❌\n"
                        
                        if available_slots:
                            slots_text += f"\n📝 Reply with the number (1-{len(time_slots)}) of your preferred time slot."
                            await message.answer(slots_text)
                            
                            # For now, automatically select the first available slot as a demo
                            # In a full implementation, you'd wait for user input
                            selected_slot_number = available_slots[0][0]  # First available slot
                            await message.answer(f"🎯 Auto-selecting slot #{selected_slot_number}: {available_slots[0][1]}")
                            
                            # Step 4: Click on the selected time slot
                            if select_and_click_timeslot(driver, time_slots, selected_slot_number, timeout=30):
                                await message.answer("✅ Time slot successfully selected!")
                                
                                # Step 5: Fill the booking form
                                if fill_booking_form(driver):
                                    await message.answer("✅ Booking form filled successfully!")
                                    
                                    # Step 6: For demo, auto-confirm booking
                                    # In full implementation, you'd ask user for confirmation
                                    selected_time_slot = time_slots[selected_slot_number - 1]
                                    
                                    confirmation_text = (
                                        f"🎾 <b>BOOKING CONFIRMATION</b>\n\n"
                                        f"📅 Date: Day {preferred_day} of current month\n"
                                        f"⏰ Time Slot: {selected_time_slot.get('text', 'Unknown time')}\n"
                                        f"🏟️ Court: Squash Court\n\n"
                                        f"✅ Auto-confirming booking for demo..."
                                    )
                                    await message.answer(confirmation_text)
                                    
                                    # Step 7: Submit the booking form
                                    if submit_booking_form(driver):
                                        await message.answer("🎉 <b>Booking completed successfully!</b>\n\n"
                                                           f"Your squash court is booked for day {preferred_day}!")
                                    else:
                                        await message.answer("⚠️ Form was filled but submission may have failed.")
                                else:
                                    await message.answer("⚠️ Failed to fill booking form.")
                            else:
                                await message.answer("❌ Failed to select the time slot.")
                        else:
                            await message.answer("❌ No available time slots found for booking.")
                    else:
                        await message.answer("❌ Failed to retrieve time slots. Please try again later.")
                        
                finally:
                    # Always close the browser
                    if driver:
                        driver.quit()
                        
            except Exception as e:
                error_message = str(e)
                if "chromedriver" in error_message.lower():
                    await message.answer("❌ <b>Browser Error:</b>\n\n"
                                       "Chrome browser is not properly configured on this server.\n"
                                       "Please contact the administrator to install Chrome dependencies.")
                elif "permission denied" in error_message.lower():
                    await message.answer("❌ <b>Permission Error:</b>\n\n"
                                       "Server doesn't have proper permissions to run Chrome browser.\n"
                                       "Please contact the administrator.")
                else:
                    await message.answer(f"❌ <b>Booking Error:</b>\n\n"
                                       f"An error occurred during booking: {error_message}\n\n"
                                       f"Please try again later.")
    
    async def start_polling(self):
        """Start the Telegram bot polling"""
        bot = Bot(token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        print("Starting Telegram bot polling...")
        await self.disp.start_polling(bot)
