import sys
import os
from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from service import (
    initialize_driver,
    get_squash_court_times,
    select_and_click_timeslot,
    fill_booking_form,
    submit_booking_form
)


class BookingStates(StatesGroup):
    waiting_for_slot_selection = State()
    waiting_for_confirmation = State()


class TelegramBot:
    def __init__(self):
        # Get token from environment variable
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            print("Error: TELEGRAM_BOT_TOKEN environment variable is not set")
            sys.exit(1)
        
        # Use memory storage for FSM (Finite State Machine)
        storage = MemoryStorage()
        self.disp = Dispatcher(storage=storage)
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
        async def command_book_handler(message: Message, state: FSMContext):
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
                    time_slots = get_squash_court_times(driver, preferred_day, timeout=25)
                    
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
                            slots_text += f"\n📝 Please reply with the number (1-{len(available_slots)}) of your preferred time slot or 'cancel' to exit."
                            await message.answer(slots_text)
                            
                            # Store booking data in FSM context and wait for user input
                            await state.update_data(
                                driver=driver,
                                time_slots=time_slots,
                                preferred_day=preferred_day,
                                available_slots=available_slots
                            )
                            await state.set_state(BookingStates.waiting_for_slot_selection)
                            
                        else:
                            await message.answer("❌ No available time slots found for booking.")
                            driver.quit()
                    else:
                        await message.answer("❌ Failed to retrieve time slots. Please try again later.")
                        driver.quit()
                        
                except Exception as inner_e:
                    await message.answer(f"❌ Error during time slot retrieval: {inner_e}")
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
        
        # Handler for slot selection
        @self.disp.message(BookingStates.waiting_for_slot_selection)
        async def handle_slot_selection(message: Message, state: FSMContext):
            user_input = message.text.strip().lower()
            
            # Handle cancel
            if user_input == 'cancel':
                data = await state.get_data()
                if 'driver' in data:
                    data['driver'].quit()
                await state.clear()
                await message.answer("❌ Booking cancelled.")
                return
            
            # Get stored data
            data = await state.get_data()
            driver = data.get('driver')
            time_slots = data.get('time_slots', [])
            preferred_day = data.get('preferred_day')
            available_slots = data.get('available_slots', [])
            
            try:
                selected_slot_number = int(user_input)
                
                # Validate slot number
                if not (1 <= selected_slot_number <= len(available_slots)):
                    await message.answer(f"❌ Invalid slot number. Please enter a number between 1 and {len(available_slots)} or 'cancel' to exit.")
                    return
                
                # Find the selected slot from available slots
                selected_available_slot = None
                for slot_num, slot_text, slot_data in available_slots:
                    if slot_num == selected_slot_number:
                        selected_available_slot = (slot_num, slot_text, slot_data)
                        break
                
                if not selected_available_slot:
                    await message.answer("❌ Selected slot is not available. Please choose from the available slots.")
                    return
                
                await message.answer(f"🎯 Selected slot #{selected_slot_number}: {selected_available_slot[1]}\n"
                                   f"⏳ Processing your selection...")
                
                # Step 4: Click on the selected time slot
                if select_and_click_timeslot(driver, time_slots, selected_slot_number, timeout=30):
                    await message.answer("✅ Time slot successfully selected!")
                    
                    # Step 5: Fill the booking form
                    if fill_booking_form(driver):
                        await message.answer("✅ Booking form filled successfully!")
                        
                        # Step 6: Show confirmation and ask user
                        selected_time_slot = time_slots[selected_slot_number - 1]
                        
                        confirmation_text = (
                            f"🎾 <b>BOOKING CONFIRMATION</b>\n\n"
                            f"📅 Date: Day {preferred_day} of current month\n"
                            f"⏰ Time Slot: {selected_time_slot.get('text', 'Unknown time')}\n"
                            f"🏟️ Court: Squash Court\n\n"
                            f"✅ Please type 'confirm' to proceed with booking or 'cancel' to cancel."
                        )
                        await message.answer(confirmation_text)
                        
                        # Update state data and move to confirmation state
                        await state.update_data(selected_time_slot=selected_time_slot)
                        await state.set_state(BookingStates.waiting_for_confirmation)
                        
                    else:
                        await message.answer("⚠️ Failed to fill booking form.")
                        driver.quit()
                        await state.clear()
                else:
                    await message.answer("❌ Failed to select the time slot.")
                    driver.quit()
                    await state.clear()
                    
            except ValueError:
                await message.answer(f"❌ Invalid input. Please enter a number between 1 and {len(available_slots)} or 'cancel' to exit.")
        
        # Handler for booking confirmation
        @self.disp.message(BookingStates.waiting_for_confirmation)
        async def handle_booking_confirmation(message: Message, state: FSMContext):
            user_input = message.text.strip().lower()
            
            data = await state.get_data()
            driver = data.get('driver')
            preferred_day = data.get('preferred_day')
            
            if user_input == 'confirm':
                await message.answer("🎾 Confirming your booking...")
                
                # Step 7: Submit the booking form
                if submit_booking_form(driver):
                    await message.answer("🎉 <b>Booking completed successfully!</b>\n\n"
                                       f"Your squash court is booked for day {preferred_day}!")
                else:
                    await message.answer("⚠️ Form was filled but submission may have failed.")
                
                driver.quit()
                await state.clear()
                
            elif user_input == 'cancel':
                await message.answer("❌ Booking cancelled.")
                driver.quit()
                await state.clear()
            else:
                await message.answer("❌ Invalid input. Please type 'confirm' to proceed or 'cancel' to cancel.")
    
    async def start_polling(self):
        """Start the Telegram bot polling"""
        bot = Bot(token=self.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        print("Starting Telegram bot polling...")
        await self.disp.start_polling(bot)
