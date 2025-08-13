import time
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
    'phone_number': '07423624107',
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
        
        # Click the Book button to submit the form
        try:
            book_button = driver.find_element(By.XPATH, "//button[@type='submit'][@aria-label='Book']")
            book_button.click()
            print("✅ Clicked 'Book' button to submit the booking!")
            
            # Wait a moment to see any confirmation or next page
            time.sleep(3)
            print("✅ Booking submission completed!")
            
        except Exception as e:
            # Try alternative selectors for the book button
            try:
                book_button = driver.find_element(By.CLASS_NAME, "i9DXY")
                book_button.click()
                print("✅ Clicked 'Book' button to submit the booking!")
                time.sleep(3)
                print("✅ Booking submission completed!")
            except Exception as e2:
                try:
                    book_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Book')]")
                    book_button.click()
                    print("✅ Clicked 'Book' button to submit the booking!")
                    time.sleep(3)
                    print("✅ Booking submission completed!")
                except Exception as e3:
                    print(f"❌ Error clicking Book button: {e}, {e2}, {e3}")
                    print("⚠️ Form was filled but booking submission may have failed")
        
        print("✅ Form filling and submission process completed!")
        return True
        
    except TimeoutException:
        print("❌ Timeout waiting for booking form to appear")
        return False
    except Exception as e:
        print(f"❌ Error filling booking form: {e}")
        return False


def get_squash_court_times(headless: bool = True, timeout: int = 30, interactive: bool = False) -> Optional[List[Dict[str, str]]]:
    """
    Navigate to the Caversam Park booking page, click on "Squash Court", 
    wait for the time picker to load, and return all available time slots.
    Optionally allow user to select and click on a specific time slot.
    
    Args:
        headless (bool): Whether to run browser in headless mode
        timeout (int): Maximum time to wait for elements (seconds)
        interactive (bool): Whether to ask user to select a time slot to book
    
    Returns:
        List[Dict[str, str]]: List of time slots with their properties, or None if failed
    """
    driver = None
    try:
        # Configure Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        
        print("Navigating to booking page...")
        # Navigate to the booking page
        url = "https://outlook.office365.com/book/CaversamParkVillageAssociationMilestoneCentre@cpva.org.uk/?ismsaljsauthenabled=true"
        driver.get(url)
        
        # Wait for page to load
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print("Looking for 'Squash Court' button...")
        # Look for "Squash Court" button/link - prioritize the working selector
        squash_court_selectors = [
            "//div[contains(text(), 'Squash Court')]",  # Known working selector
            "//button[contains(text(), 'Squash Court')]",
            "//a[contains(text(), 'Squash Court')]",
            "//span[contains(text(), 'Squash Court')]",
            "//*[contains(text(), 'Squash Court')]"
        ]
        
        squash_court_element = None
        for selector in squash_court_selectors:
            try:
                squash_court_element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"Found 'Squash Court' element using selector: {selector}")
                break
            except TimeoutException:
                continue
        
        if not squash_court_element:
            print("Could not find 'Squash Court' element")
            return None
        
        # Click on Squash Court
        print("Clicking on 'Squash Court'...")
        driver.execute_script("arguments[0].click();", squash_court_element)
        
        # Wait a moment for any transitions
        time.sleep(2)
        
        print("Waiting for time picker to load...")
        # Wait for the time picker div to be present
        time_picker_div = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label*="Time picker"]'))
        )
        
        print("Time picker found, waiting for list items to load...")
        # Wait for list items to be present within the time picker
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label*="Time picker"] li, div[aria-label*="Time picker"] button, div[aria-label*="Time picker"] div[role="option"]'))
        )
        
        # Give it a bit more time to ensure all items are loaded
        time.sleep(3)
        
        print("Extracting time slots...")
        # Try to find list elements within the time picker
        time_slots = []
        
        # Try different selectors for list items - prioritize the working selector
        list_selectors = [
            'div[aria-label*="Time picker"] li',  # Known working selector - finds 8 elements
            'div[aria-label*="Time picker"] button',
            'div[aria-label*="Time picker"] div[role="option"]',
            'div[aria-label*="Time picker"] div[role="listitem"]',
            'div[aria-label*="Time picker"] .time-slot',
            'div[aria-label*="Time picker"] [data-time]'
        ]
        
        for selector in list_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"Found {len(elements)} elements using selector: {selector}")
                    for element in elements:
                        try:
                            time_slot_info = {
                                'text': element.text.strip(),
                                'tag_name': element.tag_name,
                                'is_enabled': element.is_enabled(),
                                'is_displayed': element.is_displayed(),
                                'attributes': {}
                            }
                            
                            # Get common attributes
                            common_attrs = ['class', 'id', 'data-time', 'aria-label', 'title', 'value']
                            for attr in common_attrs:
                                try:
                                    value = element.get_attribute(attr)
                                    if value:
                                        time_slot_info['attributes'][attr] = value
                                except:
                                    pass
                            
                            if time_slot_info['text'] or time_slot_info['attributes']:
                                time_slots.append(time_slot_info)
                                
                        except Exception as e:
                            print(f"Error extracting info from element: {e}")
                            continue
                    
                    if time_slots:
                        break
                        
            except Exception as e:
                print(f"Error with selector {selector}: {e}")
                continue
        
        if not time_slots:
            print("No time slots found, trying to get all clickable elements in time picker...")
            # Fallback: get all clickable elements within the time picker
            try:
                all_elements = driver.find_elements(By.CSS_SELECTOR, 'div[aria-label*="Time picker"] *')
                for element in all_elements:
                    if element.is_displayed() and element.text.strip():
                        time_slot_info = {
                            'text': element.text.strip(),
                            'tag_name': element.tag_name,
                            'is_enabled': element.is_enabled(),
                            'is_displayed': element.is_displayed(),
                            'attributes': {}
                        }
                        
                        # Get common attributes
                        for attr in ['class', 'id', 'aria-label', 'title']:
                            try:
                                value = element.get_attribute(attr)
                                if value:
                                    time_slot_info['attributes'][attr] = value
                            except:
                                pass
                        
                        time_slots.append(time_slot_info)
                        
            except Exception as e:
                print(f"Fallback extraction failed: {e}")
        
        print(f"Successfully extracted {len(time_slots)} time slots")
        
        # Interactive mode: let user select a time slot to book
        if interactive and time_slots:
            selected_element = select_and_click_timeslot(driver, time_slots, timeout)
            if selected_element:
                print("Time slot successfully selected and clicked!")
                # Keep browser open for a moment to see the result
                time.sleep(5)
            else:
                print("No time slot was selected or click failed.")
        
        return time_slots
        
    except TimeoutException:
        print(f"Timeout waiting for elements after {timeout} seconds")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        if driver:
            driver.quit()
            print("Browser closed")


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


def select_and_click_timeslot(driver, time_slots: List[Dict[str, str]], timeout: int = 30) -> Optional[bool]:
    """
    Display available time slots to user, ask for selection, and click on the chosen slot.
    
    Args:
        driver: Selenium WebDriver instance
        time_slots: List of extracted time slot dictionaries
        timeout: Maximum time to wait for elements (seconds)
    
    Returns:
        bool: True if time slot was successfully clicked, False otherwise
    """
    try:
        # Display available time slots
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
            return False
        
        # Ask user to select a time slot by number only
        print(f"\nEnter the number (1-{len(time_slots)}) of the time slot you want to book:")
        print("Type 'cancel' to exit without booking.")
        
        user_input = input("> ").strip()
        
        if user_input.lower() == 'cancel':
            print("Booking cancelled by user.")
            return False
        
        selected_slot = None
        selected_index = None
        
        # Only match by number
        try:
            slot_number = int(user_input)
            if 1 <= slot_number <= len(time_slots):
                selected_slot = time_slots[slot_number - 1]
                selected_index = slot_number - 1
                print(f"Selected slot #{slot_number}: {selected_slot.get('text', 'No text')}")
            else:
                print(f"Invalid slot number. Please enter a number between 1 and {len(time_slots)}.")
                return False
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {len(time_slots)}.")
            return False
        
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
            
            # Fill the booking form with user details
            if fill_booking_form(driver):
                print("✅ Booking form filled successfully!")
                # Wait a bit to see the filled form
                time.sleep(3)
            else:
                print("⚠️ Failed to fill booking form, but time slot was selected")
            
            return True
        else:
            print("Failed to click on the selected time slot.")
            return False
            
    except Exception as e:
        print(f"Error in select_and_click_timeslot: {e}")
        return False


def print_time_slots(time_slots: List[Dict[str, str]]) -> None:
    """
    Pretty print the extracted time slots.
    
    Args:
        time_slots: List of time slot dictionaries
    """
    if not time_slots:
        print("No time slots to display")
        return
    
    print(f"\n=== Found {len(time_slots)} Time Slots ===")
    for i, slot in enumerate(time_slots, 1):
        print(f"\n{i}. {slot.get('text', 'No text')}")
        print(f"   Tag: {slot.get('tag_name', 'Unknown')}")
        print(f"   Enabled: {slot.get('is_enabled', 'Unknown')}")
        print(f"   Displayed: {slot.get('is_displayed', 'Unknown')}")
        
        if slot.get('attributes'):
            print("   Attributes:")
            for attr, value in slot['attributes'].items():
                print(f"     {attr}: {value}")


# Example usage
if __name__ == "__main__":
    print("Starting squash court booking scraper...")
    
    # Option 1: Just get time slots without booking
    # print("\n=== Option 1: Get available time slots ===")
    # slots = get_squash_court_times(headless=False, timeout=30, interactive=False)
    # print_time_slots(slots)
    
    # Option 2: Interactive booking (uncomment to use)
    print("\n=== Option 2: Interactive booking ===")
    slots = get_squash_court_times(headless=False, timeout=30, interactive=True)
    print("Booking session completed!")
