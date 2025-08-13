import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Dict, Optional


# Default user data for form filling
default_user_data = {
    'first_and_surname': 'Oleksii Matiunin',
    'email': 'matalexnin@gmail.com',
    'address': '78 Curzon street, Reading, UK',
    'phone_number': '07423624106',
    'special_requests': 'Automated booking via Telegram bot',
    'membership_number': '8060',
    'opponent_name': '-'
}


def fill_booking_form(driver, user_data: Dict[str, str] = None) -> bool:
    """
    Fill out the booking form with user details after time slot selection.
    
    Args:
        driver: Selenium WebDriver instance
        user_data: Dictionary containing user details, defaults to default_user_data
    
    Returns:
        bool: True if form was successfully filled, False otherwise
    """
    if user_data is None:
        user_data = default_user_data
    
    try:
        print("Filling out booking form...")
        
        # Wait for the form to be visible
        form_heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Add your details')]"))
        )
        print("Form found, filling fields...")
        
        # Fill First and surname
        try:
            first_name_field = driver.find_element(By.XPATH, "//input[@placeholder='First and surname']")
            first_name_field.clear()
            first_name_field.send_keys(user_data.get('first_and_surname', ''))
            print(f"✅ Filled first and surname: {user_data.get('first_and_surname', '')}")
        except Exception as e:
            print(f"❌ Error filling first and surname: {e}")
        
        # Fill Email
        try:
            email_field = driver.find_element(By.XPATH, "//input[@type='email'][@placeholder='Email']")
            email_field.clear()
            email_field.send_keys(user_data.get('email', ''))
            print(f"✅ Filled email: {user_data.get('email', '')}")
        except Exception as e:
            print(f"❌ Error filling email: {e}")
        
        # Fill Address (optional)
        try:
            address_field = driver.find_element(By.XPATH, "//input[@placeholder='Address']")
            address_field.clear()
            address_field.send_keys(user_data.get('address', ''))
            print(f"✅ Filled address: {user_data.get('address', '')}")
        except Exception as e:
            print(f"❌ Error filling address: {e}")
        
        # Fill Phone number
        try:
            phone_field = driver.find_element(By.XPATH, "//input[@type='tel'][@placeholder='Add your phone number']")
            phone_field.clear()
            phone_field.send_keys(user_data.get('phone_number', ''))
            print(f"✅ Filled phone number: {user_data.get('phone_number', '')}")
        except Exception as e:
            print(f"❌ Error filling phone number: {e}")
        
        # Fill Special requests (optional)
        try:
            notes_field = driver.find_element(By.XPATH, "//textarea[@placeholder='Add any special requests']")
            notes_field.clear()
            notes_field.send_keys(user_data.get('special_requests', ''))
            print(f"✅ Filled special requests: {user_data.get('special_requests', '')}")
        except Exception as e:
            print(f"❌ Error filling special requests: {e}")
        
        # Fill Membership Number
        try:
            membership_field = driver.find_element(By.XPATH, "//input[@aria-labelledby='TextFieldLabel69']")
            membership_field.clear()
            membership_field.send_keys(user_data.get('membership_number', ''))
            print(f"✅ Filled membership number: {user_data.get('membership_number', '')}")
        except Exception as e:
            # Try alternative selector based on label text
            try:
                membership_field = driver.find_element(By.XPATH, "//label[contains(text(), 'Membership Number')]/following-sibling::div//input")
                membership_field.clear()
                membership_field.send_keys(user_data.get('membership_number', ''))
                print(f"✅ Filled membership number: {user_data.get('membership_number', '')}")
            except Exception as e2:
                print(f"❌ Error filling membership number: {e}, {e2}")
        
        # Fill Opponent's Name
        try:
            opponent_field = driver.find_element(By.XPATH, "//input[@aria-labelledby='TextFieldLabel74']")
            opponent_field.clear()
            opponent_field.send_keys(user_data.get('opponent_name', ''))
            print(f"✅ Filled opponent's name: {user_data.get('opponent_name', '')}")
        except Exception as e:
            # Try alternative selector based on label text
            try:
                opponent_field = driver.find_element(By.XPATH, "//label[contains(text(), 'Opponent')]/following-sibling::div//input")
                opponent_field.clear()
                opponent_field.send_keys(user_data.get('opponent_name', ''))
                print(f"✅ Filled opponent's name: {user_data.get('opponent_name', '')}")
            except Exception as e2:
                print(f"❌ Error filling opponent's name: {e}, {e2}")
        
        # Check the consent checkbox
        try:
            consent_checkbox = driver.find_element(By.ID, "consentCheckBox")
            if not consent_checkbox.is_selected():
                consent_checkbox.click()
                print("✅ Checked consent checkbox for data privacy policy")
            else:
                print("✅ Consent checkbox was already checked")
        except Exception as e:
            # Try alternative selector
            try:
                consent_checkbox = driver.find_element(By.XPATH, "//input[@type='checkBox'][@id='consentCheckBox']")
                if not consent_checkbox.is_selected():
                    consent_checkbox.click()
                    print("✅ Checked consent checkbox for data privacy policy")
                else:
                    print("✅ Consent checkbox was already checked")
            except Exception as e2:
                print(f"❌ Error checking consent checkbox: {e}, {e2}")
        
        print("✅ Form filling completed successfully!")
        return True
        
    except TimeoutException:
        print("❌ Timeout waiting for booking form to appear")
        return False
    except Exception as e:
        print(f"❌ Error filling booking form: {e}")
        return False


def confirm_booking(preferred_day: int, selected_time_slot: Dict[str, str], user_data: Dict[str, str] = None) -> bool:
    """
    Display booking details and ask user for confirmation before submission.
    
    Args:
        preferred_day (int): The selected day of the month
        selected_time_slot: Dictionary containing the selected time slot info
        user_data: Dictionary containing user details, defaults to default_user_data
    
    Returns:
        bool: True if user confirms booking, False if cancelled
    """
    if user_data is None:
        user_data = default_user_data
    
    print("\n" + "="*60)
    print("🎾 BOOKING CONFIRMATION")
    print("="*60)
    
    # Display booking details
    print(f"📅 Date: Day {preferred_day} of current month")
    print(f"⏰ Time Slot: {selected_time_slot.get('text', 'Unknown time')}")
    print(f"🏟️  Court: Squash Court")
    
    print("\n👤 PERSONAL DETAILS:")
    print("-" * 40)
    print(f"Name: {user_data.get('first_and_surname', 'Not specified')}")
    print(f"Email: {user_data.get('email', 'Not specified')}")
    print(f"Phone: {user_data.get('phone_number', 'Not specified')}")
    print(f"Address: {user_data.get('address', 'Not specified')}")
    print(f"Membership #: {user_data.get('membership_number', 'Not specified')}")
    print(f"Opponent: {user_data.get('opponent_name', 'Not specified')}")
    
    if user_data.get('special_requests'):
        print(f"Special Requests: {user_data.get('special_requests')}")
    
    print("\n" + "="*60)
    
    # Ask for confirmation
    while True:
        print("\n❓ Do you want to proceed with this booking?")
        print("Type 'yes' to confirm and submit, 'no' to cancel:")
        confirmation = input("> ").strip().lower()
        
        if confirmation in ['yes', 'y', 'confirm']:
            print("✅ Booking confirmed! Proceeding with submission...")
            return True
        elif confirmation in ['no', 'n', 'cancel']:
            print("❌ Booking cancelled by user.")
            return False
        else:
            print("Invalid input. Please type 'yes' to confirm or 'no' to cancel.")


def submit_booking_form(driver) -> bool:
    """
    Submit the booking form by clicking the Book button.
    
    Args:
        driver: Selenium WebDriver instance
    
    Returns:
        bool: True if form was successfully submitted, False otherwise
    """
    try:
        print("Submitting booking form...")
        
        # Click the Book button to submit the form
        try:
            book_button = driver.find_element(By.XPATH, "//button[@type='submit'][@aria-label='Book']")
            book_button.click()
            print("✅ Clicked 'Book' button to submit the booking!")
            
            # Wait a moment to see any confirmation or next page
            time.sleep(3)
            print("✅ Booking submission completed!")
            return True
            
        except Exception as e:
            # Try alternative selectors for the book button
            try:
                book_button = driver.find_element(By.CLASS_NAME, "i9DXY")
                book_button.click()
                print("✅ Clicked 'Book' button to submit the booking!")
                time.sleep(3)
                print("✅ Booking submission completed!")
                return True
            except Exception as e2:
                try:
                    book_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Book')]")
                    book_button.click()
                    print("✅ Clicked 'Book' button to submit the booking!")
                    time.sleep(3)
                    print("✅ Booking submission completed!")
                    return True
                except Exception as e3:
                    print(f"❌ Error clicking Book button: {e}, {e2}, {e3}")
                    print("⚠️ Form was filled but booking submission may have failed")
                    return False
                    
    except Exception as e:
        print(f"❌ Error submitting booking form: {e}")
        return False


def initialize_driver(headless: bool = True):
    """
    Initialize and configure Chromium WebDriver with optimal settings for web scraping.
    
    Args:
        headless (bool): Whether to run browser in headless mode
    
    Returns:
        webdriver.Chrome: Configured Chromium WebDriver instance
    """
    # Configure Chromium options for Docker/Linux environment
    chrome_options = Options()
    
    # Essential options for headless mode
    if headless:
        chrome_options.add_argument("--headless=new")  # Use new headless mode
    
    # Security and sandbox options (required for Docker)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    
    # Memory and performance options
    chrome_options.add_argument("--memory-pressure-off")
    chrome_options.add_argument("--max_old_space_size=4096")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    
    # Display options
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-web-security")
    
    # User agent
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Logging options
    chrome_options.add_argument("--log-level=3")  # Suppress INFO, WARNING, ERROR
    chrome_options.add_argument("--silent")
    chrome_options.add_argument("--disable-logging")
    
    # Additional stability options for containerized environments
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--metrics-recording-only")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--safebrowsing-disable-auto-update")
    chrome_options.add_argument("--disable-background-timer-throttling")
    
    # Set Chromium binary location for Docker environment
    chrome_options.binary_location = "/usr/bin/chromium"
    
    # Initialize and return the driver
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error initializing Chromium driver: {e}")
        print("Make sure Chromium and ChromeDriver are properly installed")
        raise


def get_squash_court_times(driver, preferred_day: int, timeout: int = 20):
    """
    Navigate to the Caversam Park booking page, click on "Squash Court", 
    select the preferred date, and return all available time slots.
    
    Args:
        driver: Pre-initialized Selenium WebDriver instance
        preferred_day (int): Day of the month (1-31) for booking
        timeout (int): Maximum time to wait for elements (seconds)
    
    Returns:
        List[Dict[str, str]]: List of time slots with their properties, or None if failed
    """
    try:
        print("Navigating to booking page...")
        # Navigate to the booking page
        url = "https://outlook.office365.com/book/CaversamParkVillageAssociationMilestoneCentre@cpva.org.uk/?ismsaljsauthenabled=true"
        driver.get(url)
        
        # Wait for page to load - reduced timeout for faster failure detection
        WebDriverWait(driver, min(timeout, 15)).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print("Looking for 'Squash Court' button...")
        # Use the known working selector first, with shorter timeout
        try:
            squash_court_element = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Squash Court')]"))
            )
            print("Found 'Squash Court' element")
        except TimeoutException:
            # Only try fallback selectors if the primary one fails
            fallback_selectors = [
                "//button[contains(text(), 'Squash Court')]",
                "//a[contains(text(), 'Squash Court')]",
                "//span[contains(text(), 'Squash Court')]",
                "//*[contains(text(), 'Squash Court')]"
            ]
            
            squash_court_element = None
            for selector in fallback_selectors:
                try:
                    squash_court_element = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"Found 'Squash Court' element using fallback selector")
                    break
                except TimeoutException:
                    continue
            
            if not squash_court_element:
                print("Could not find 'Squash Court' element")
                return None
        
        # Click on Squash Court
        print("Clicking on 'Squash Court'...")
        driver.execute_script("arguments[0].click();", squash_court_element)
        
        # Reduced wait time after click
        time.sleep(1)
        
        print(f"Looking for date picker and selecting day {preferred_day}...")
        try:
            # Wait for the date picker with shorter timeout
            date_picker = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Date picker."]'))
            )
            print("Date picker found")
            
            # Optimized date selection - use the most likely working pattern first
            date_element = None
            try:
                # Try the most common pattern first
                date_elements = driver.find_elements(
                    By.XPATH, 
                    f'//div[@aria-label="Date picker."]//div[@role="button" and text()="{preferred_day}"]'
                )
                
                # Look for available dates quickly
                for element in date_elements:
                    aria_label = element.get_attribute('aria-label') or ''
                    if 'Times available' in aria_label or element.is_enabled():
                        date_element = element
                        break
                        
            except Exception:
                pass
            
            # Only try fallback patterns if needed
            if not date_element:
                fallback_xpaths = [
                    f'//div[contains(@aria-label, "Date picker")]//div[@role="button" and text()="{preferred_day}"]',
                    f'//div[contains(@aria-label, "Date picker")]//div[text()="{preferred_day}"]'
                ]
                
                for xpath in fallback_xpaths:
                    try:
                        date_elements = driver.find_elements(By.XPATH, xpath)
                        for element in date_elements:
                            aria_label = element.get_attribute('aria-label') or ''
                            if 'Times available' in aria_label or element.is_enabled():
                                date_element = element
                                break
                        if date_element:
                            break
                    except Exception:
                        continue
            
            if date_element:
                print(f"Found date element for day {preferred_day}")
                # Click on the date
                driver.execute_script("arguments[0].click();", date_element)
                print(f"Clicked on date: day {preferred_day}")
                
                # Reduced wait time after date selection
                time.sleep(1.5)
            else:
                print(f"Could not find available date for day {preferred_day}")
                return None
                
        except TimeoutException:
            print("Date picker not found or not loaded in time")
            return None
        except Exception as e:
            print(f"Error selecting date: {e}")
            return None
        
        print("Waiting for time picker to load...")
        # Wait for the time picker with reduced timeout
        try:
            time_picker_div = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label*="Time picker"]'))
            )
            
            # Wait for list items with shorter timeout
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label*="Time picker"] li'))
            )
            
            # Minimal wait for content to stabilize
            time.sleep(1)
            
        except TimeoutException:
            print("Time picker not loaded in time")
            return None
        
        print("Extracting time slots...")
        # Use the known working selector first
        time_slots = []
        
        try:
            # Primary selector (known to work)
            elements = driver.find_elements(By.CSS_SELECTOR, 'div[aria-label*="Time picker"] li')
            
            if elements:
                print(f"Found {len(elements)} time slot elements")
                for element in elements:
                    try:
                        text = element.text.strip()
                        if text:  # Only process elements with text
                            time_slot_info = {
                                'text': text,
                                'tag_name': element.tag_name,
                                'is_enabled': element.is_enabled(),
                                'is_displayed': element.is_displayed(),
                                'attributes': {}
                            }
                            
                            # Get only essential attributes
                            for attr in ['class', 'aria-label']:
                                try:
                                    value = element.get_attribute(attr)
                                    if value:
                                        time_slot_info['attributes'][attr] = value
                                except:
                                    pass
                            
                            time_slots.append(time_slot_info)
                    except Exception:
                        continue
            
            # Only try fallback selectors if primary failed
            if not time_slots:
                fallback_selectors = [
                    'div[aria-label*="Time picker"] button',
                    'div[aria-label*="Time picker"] div[role="option"]'
                ]
                
                for selector in fallback_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            for element in elements:
                                text = element.text.strip()
                                if text:
                                    time_slots.append({
                                        'text': text,
                                        'tag_name': element.tag_name,
                                        'is_enabled': element.is_enabled(),
                                        'is_displayed': element.is_displayed(),
                                        'attributes': {}
                                    })
                            break
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"Error extracting time slots: {e}")
            return None
        
        print(f"Successfully extracted {len(time_slots)} time slots")
        return time_slots if time_slots else None
        
    except TimeoutException:
        print(f"Timeout waiting for elements after {timeout} seconds")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def validate_slot_selection(driver, element) -> bool:
    """
    Validate that a time slot was successfully selected by checking for the selection style.
    
    Args:
        driver: Selenium WebDriver instance
        element: The clicked element to validate
    
    Returns:
        bool: True if element shows selection styling, False otherwise
    """
    try:
        # Wait a bit more for selection styles to apply
        time.sleep(0.5)
        
        # The selection color is #008273 which in RGB is rgb(0, 130, 115)
        selection_colors = [
            'rgb(0, 130, 115)',
            'rgba(0, 130, 115, 1)',
            '#008273',
            'rgb(0,130,115)',
            'rgba(0,130,115,1)'
        ]
        
        # Check the clicked element itself
        background_color = element.value_of_css_property('background-color')
        print(f"Element background color: {background_color}")
        
        if background_color and any(color.lower() in background_color.lower() for color in selection_colors):
            print("✅ Time slot selection confirmed by element background color")
            return True
        
        # Check parent elements (sometimes selection style is applied to parent)
        try:
            parent = element.find_element(By.XPATH, "..")
            parent_bg = parent.value_of_css_property('background-color')
            print(f"Parent element background color: {parent_bg}")
            
            if parent_bg and any(color.lower() in parent_bg.lower() for color in selection_colors):
                print("✅ Time slot selection confirmed by parent background color")
                return True
        except:
            pass
        
        # Check child elements (sometimes selection style is applied to child)
        try:
            children = element.find_elements(By.XPATH, ".//*")
            for child in children:
                child_bg = child.value_of_css_property('background-color')
                if child_bg and any(color.lower() in child_bg.lower() for color in selection_colors):
                    print(f"✅ Time slot selection confirmed by child element background color: {child_bg}")
                    return True
        except:
            pass
        
        # Check for border changes (sometimes selection is indicated by border)
        border_color = element.value_of_css_property('border-color')
        border_style = element.value_of_css_property('border-style')
        print(f"Element border: {border_style} {border_color}")
        
        if border_color and any(color.lower() in border_color.lower() for color in selection_colors):
            print("✅ Time slot selection confirmed by border color")
            return True
        
        # Check for outline changes
        outline_color = element.value_of_css_property('outline-color')
        outline_style = element.value_of_css_property('outline-style')
        if outline_color and outline_style != 'none':
            print(f"Element outline: {outline_style} {outline_color}")
            if any(color.lower() in outline_color.lower() for color in selection_colors):
                print("✅ Time slot selection confirmed by outline color")
                return True
        
        # Check for CSS classes indicating selection
        element_class = element.get_attribute('class') or ''
        parent_class = ''
        try:
            parent = element.find_element(By.XPATH, "..")
            parent_class = parent.get_attribute('class') or ''
        except:
            pass
        
        print(f"Element classes: '{element_class}'")
        if parent_class:
            print(f"Parent classes: '{parent_class}'")
        
        selection_keywords = ['selected', 'active', 'current', 'chosen', 'picked']
        all_classes = f"{element_class} {parent_class}".lower()
        
        for keyword in selection_keywords:
            if keyword in all_classes:
                print(f"✅ Time slot selection confirmed by CSS class containing '{keyword}'")
                return True
        
        # Check for aria attributes indicating selection
        aria_selected = element.get_attribute('aria-selected')
        aria_pressed = element.get_attribute('aria-pressed')
        aria_current = element.get_attribute('aria-current')
        
        if aria_selected and aria_selected.lower() == 'true':
            print("✅ Time slot selection confirmed by aria-selected='true'")
            return True
        if aria_pressed and aria_pressed.lower() == 'true':
            print("✅ Time slot selection confirmed by aria-pressed='true'")
            return True
        if aria_current:
            print(f"✅ Time slot selection confirmed by aria-current='{aria_current}'")
            return True
        
        # Check if the element now has focus
        active_element = driver.switch_to.active_element
        if active_element == element:
            print("✅ Time slot selection confirmed by element having focus")
            return True
        
        # Final check: look for any visual change by comparing before/after screenshots (conceptual)
        print("⚠️ No clear selection indicator found in standard properties")
        
        # Let's also check if there are any data attributes that changed
        data_attrs = {}
        for attr_name in element.get_property('attributes'):
            if hasattr(attr_name, 'name') and attr_name.name.startswith('data-'):
                data_attrs[attr_name.name] = element.get_attribute(attr_name.name)
        
        if data_attrs:
            print(f"Data attributes: {data_attrs}")
            # Look for common selection indicators in data attributes
            selection_indicators = ['selected', 'active', 'current', 'true', '1']
            for attr_name, attr_value in data_attrs.items():
                if attr_value and any(indicator in str(attr_value).lower() for indicator in selection_indicators):
                    print(f"✅ Time slot selection potentially confirmed by {attr_name}='{attr_value}'")
                    return True
        
        return False
        
    except Exception as e:
        print(f"Error validating selection: {e}")
        return False


def display_available_time_slots(time_slots: List[Dict[str, str]]) -> None:
    """
    Display available time slots to user.
    
    Args:
        time_slots: List of extracted time slot dictionaries
    """
    print(f"\n=== Available Time Slots ({len(time_slots)}) ===")
    available_slots = []
    
    for i, slot in enumerate(time_slots, 1):
        text = slot.get('text', '').strip()
        enabled = slot.get('is_enabled', False)
        displayed = slot.get('is_displayed', False)
        
        if text and enabled and displayed:
            available_slots.append((i, text, slot))
            status = "✅ Available"
        else:
            status = "❌ Not available"
        
        print(f"{i}. {text or 'No text'} - {status}")
    
    if not available_slots:
        print("No available time slots found for booking.")


def validate_time_slot_choice(user_input: str, time_slots: List[Dict[str, str]]) -> Optional[int]:
    """
    Validate user input for time slot selection.
    
    Args:
        user_input: User's input string
        time_slots: List of extracted time slot dictionaries
    
    Returns:
        int: Valid slot number (1-based), or None if invalid/cancelled
    """
    if user_input.lower() == 'cancel':
        print("Booking cancelled by user.")
        return None
    
    try:
        slot_number = int(user_input)
        if 1 <= slot_number <= len(time_slots):
            # Check if the selected slot is available for booking
            selected_slot = time_slots[slot_number - 1]
            if selected_slot.get('is_enabled', False) and selected_slot.get('is_displayed', False):
                return slot_number
            else:
                print(f"Selected time slot #{slot_number} is not available for booking.")
                return None
        else:
            print(f"Invalid slot number. Please enter a number between 1 and {len(time_slots)}.")
            return None
    except ValueError:
        print(f"Invalid input. Please enter a number between 1 and {len(time_slots)}.")
        return None


def select_and_click_timeslot(driver, time_slots: List[Dict[str, str]], slot_number: int, timeout: int = 30) -> Optional[bool]:
    """
    Click on the specified time slot.
    
    Args:
        driver: Selenium WebDriver instance
        time_slots: List of extracted time slot dictionaries
        slot_number: The slot number (1-based) to select and click
        timeout: Maximum time to wait for elements (seconds)
    
    Returns:
        bool: True if time slot was successfully clicked, False otherwise
    """
    try:
        # Validate slot number
        if not (1 <= slot_number <= len(time_slots)):
            print(f"Invalid slot number {slot_number}. Must be between 1 and {len(time_slots)}.")
            return False
        
        selected_slot = time_slots[slot_number - 1]
        print(f"Attempting to click on slot #{slot_number}: {selected_slot.get('text', 'No text')}")
        
        # Check if the selected slot is available for booking
        if not (selected_slot.get('is_enabled', False) and selected_slot.get('is_displayed', False)):
            print(f"Selected time slot is not available for booking.")
            return False
        
        # Find the actual element in the browser and click it
        print(f"Attempting to click on time slot: {selected_slot.get('text', 'Unknown')}")
        
        # Strategy 1: Find by exact text match
        element_found = False
        try:
            slot_text = selected_slot.get('text', '').strip()
            if slot_text:
                # XPath to look for exact match: div[aria-label*="Time picker"] > ul > li > label > span[text()=slot_text]
                xpath_patterns = [
                    f"//div[contains(@aria-label, 'Time picker')]//ul//li//label//span[text()='{slot_text}']",
                    f"//div[contains(@aria-label, 'Time picker')]//ul//li[.//label//span[text()='{slot_text}']]",
                    f"//div[contains(@aria-label, 'Time picker')]//ul//li//label//span[contains(text(), '{slot_text}')]",
                    f"//div[contains(@aria-label, 'Time picker')]//ul//li[.//span[text()='{slot_text}']]",
                    f"//div[contains(@aria-label, 'Time picker')]//ul//li[.//label[text()='{slot_text}']]",
                    f"//div[contains(@aria-label, 'Time picker')]//ul//li[.//*[text()='{slot_text}']]"
                ]
                
                element = None
                successful_xpath = None
                
                for xpath in xpath_patterns:
                    try:
                        element = driver.find_element(By.XPATH, xpath)
                        if element.is_displayed() and element.is_enabled():
                            successful_xpath = xpath
                            break
                    except:
                        continue
                
                if element and successful_xpath:
                    # The XPath finds a span element, but we need to click on its parent label element
                    if element.tag_name.lower() == 'span':
                        # Find the parent label element and click it instead
                        label_element = element.find_element(By.XPATH, "./ancestor::label[1]")
                        driver.execute_script("arguments[0].click();", label_element)
                        element = label_element  # Update element reference for validation
                        print(f"Found span element, clicked on parent label instead")
                    
                    print(f"Successfully clicked on time slot: {slot_text} using XPath: {successful_xpath}")
                    
                    # Validate selection by checking background color
                    time.sleep(1)  # Wait for style to apply
                    if validate_slot_selection(driver, element):
                        element_found = True
                    else:
                        print("Click registered but slot selection not confirmed")
                        element_found = True  # Still consider it successful
                else:
                    print("Element not found or not clickable")
        except Exception as e:
            print(f"Strategy 1 (text match) failed: {e}")
        
        if element_found:
            # Wait a moment to see if any changes occur
            time.sleep(2)
            print("Time slot selection completed!")
            return True
        else:
            print("Failed to click on the selected time slot.")
            return False
            
    except Exception as e:
        print(f"Error in select_and_click_timeslot: {e}")
        return False


def get_user_preferred_day() -> Optional[int]:
    """
    Get user input for preferred booking day.
    
    Returns:
        int: Valid day (1-31), or None if cancelled
    """
    while True:
        print("\nEnter the day of the month you want to book (1-31):")
        print("Type 'cancel' to exit without booking.")
        user_input = input("> ").strip()
        
        if user_input.lower() == 'cancel':
            print("Booking cancelled by user.")
            return None
        
        try:
            day = int(user_input)
            if 1 <= day <= 31:
                return day
            else:
                print("Invalid day. Please enter a number between 1 and 31.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 31.")
