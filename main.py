from playwright.sync_api import sync_playwright, Playwright
from playwright_stealth import Stealth
from playwright_recaptcha import recaptchav2
import time
import sys
import os
import platform
from playsound3 import playsound
from dotenv import load_dotenv

# Load local credentials if .env exists
load_dotenv()

USERNAME = os.getenv("ROLL_NUMBER", "YOUR_ROLL_NUMBER")
PASSWORD = os.getenv("PASSWORD", "YOUR_PASSWORD")
REFRESH_FREQUENCY_SECONDS = 300


def sound_alert():
    print("\n" + "="*50)
    print("🚨 REGISTRATION EVENT DETECTED! 🚨")
    print("="*50 + "\n")

    try:
        # Plays your custom audio file smoothly and cleanly across Windows, Mac, and Linux
        # (Make sure 'alert.mp3' or 'chime.wav' is in your script folder)
        playsound("alert.mp3", block=False)
        
    except Exception as e:
        # Fallback if the audio file isn't found or speakers encounter issues
        system_name = platform.system()
        if system_name == "Windows":
            import winsound
            winsound.Beep(1000, 800)
        else:
            print("\a", end="")
            
    sys.stdout.flush()
def is_error(page):
    #checks for ASP.NET Runtime Error headings or crash elements
    try:
        # Check if the red ASP.NET "Server Error" title exists on screen
        server_error_heading = page.locator("h1:has-text('Server Error in'), h1:has-text('Runtime Error')")
        if server_error_heading.is_visible():
            return True

        # Check page title specifically for 500 status
        if "500" in page.title():
            return True

        return False
    except Exception:
        return False

def is_captcha_expired(page):
    try:
        captcha_frame = page.frame_locator("iframe[title='reCAPTCHA']")
        checkbox = captcha_frame.locator(".recaptcha-checkbox")

        if checkbox.is_visible() and checkbox.get_attribute("aria-checked") == "false":
            return True

        if captcha_frame.locator(".recaptcha-checkbox-expired").is_visible():
            return True

        token_val = page.locator("textarea[name='g-recaptcha-response'], input[name='g-recaptcha-response']").input_value()
        if not token_val:
            return True

        return False
    except Exception:
        return False

# Specify a local directory to store browser profile, cookies, and cache
USER_DATA_DIR = os.path.join(os.getcwd(), "flex_session_data")


with sync_playwright() as playwright:
# Launch Browser
# Launch persistent context (Saves cookies and profile across restarts)
    context = playwright.chromium.launch_persistent_context(
    user_data_dir=USER_DATA_DIR,
    headless=False,
    args=["--disable-blink-features=AutomationControlled"]
    )
    #args makes it harer for websites to detect automation


    # Grab the default page created by persistent context
    page = context.pages[0] if context.pages else context.new_page()

    # Apply stealth anti-bot evasion
    Stealth().apply_stealth_sync(page) #modifies the browser’s internal JavaScript properties in real time to hide the fact that Playwright is controlling the browser.

    while True:
        registration_opened = False
        try:
            page.set_default_navigation_timeout(0)
            page.set_default_timeout(0)

            #Navigate to flex
            page.goto("https://flexstudent.nu.edu.pk/Login")

            #Login

            roll_input = page.get_by_placeholder("Roll N", exact=False)
            if roll_input.is_visible(timeout=3000):
                # Roll Number input field
                roll_input.click()
                roll_input.press("Control+A")
                roll_input.press("Backspace")
                roll_input.type(USERNAME, delay=100)

                page.wait_for_timeout(300)

                # Password input field
                pass_input = page.get_by_placeholder("Password")
                pass_input.click()
                pass_input.press("Control+A")
                pass_input.press("Backspace")
                pass_input.type(PASSWORD, delay=100)


                # Check i am not a robot
                # Use playwright-recaptcha solver context manager
                with recaptchav2.SyncSolver(page) as solver:
                    solver.solve_recaptcha()
                    
                    # --- AUTOMATE THE AUDIO CHALLENGE PLAY BUTTON ---
                    try:
                        # Give the audio frame a second to load
                        page.wait_for_timeout(1000)
                        
                        # Locate the reCAPTCHA audio challenge iframe
                        audio_frame = page.frame_locator("iframe[title*='audio challenge']")
                        
                        # Find and click the play button inside the audio challenge
                        play_button = audio_frame.locator("button:has-text('Play'), .rc-button-default, #recaptcha-audio-button")
                        if play_button.is_visible(timeout=2000):
                            play_button.click()
                            print("Audio challenge play button clicked automatically!")
                    except Exception as e:
                        print("Audio challenge wasn't triggered or play button was already handled.")
               
                page.wait_for_timeout(500)

                #click sign in
                page.get_by_role("button").click()
                print("Logging in...")

                page.wait_for_load_state("domcontentloaded", timeout=0)
                
                if is_captcha_expired(page):
                    print("⚠️ reCAPTCHA expired during sign in. Restarting whole process...")
                    time.sleep(2)
                    continue

                if is_error(page):
                    print("Runtime error on login post. Restarting whole process...")
                    time.sleep(2)
                    continue

            if is_error(page):
                print("Runtime error on login. Restarting whole process...")
                time.sleep(2)
                continue


            #click course registration
            page.get_by_text("Course Registration").click(no_wait_after=True)
            page.wait_for_load_state("domcontentloaded", timeout=0) 
            print("Navigating to Course Registration page...")

            if is_error(page):
                print("⚠️ Runtime error on course registration. Restarting whole process...")
                time.sleep(2)
                continue


            while True:
            
                # If server responded with Runtime Error screen, break to re-login immediately
                if is_error(page):
                    print("Runtime error page detected! Restarting whole process from Login...")
                    break

                # wait for full page content to render
                page.wait_for_load_state("domcontentloaded", timeout=0)
                
                # If logged out and redirected to Login screen, break to re-login immediately
                if "Login" in page.url:
                    print("Session expired / logged out. Restarting whole process from Login...")
                    break
                # wait 3 secs before checking for registration not active yet banner
                registration_banner = page.get_by_text("Registration not active yet.")
                if registration_banner.is_visible(timeout=3000):
                    print("Registration not active banner detected!")
                else:
                    print("Registration might be active! Banner not found.")
                    registration_opened = True
                    break

                # Check for Register button (case-insensitive or partial)
                register_button = page.locator("button:has-text('Register Courses'), input[value*='Register']")

                #register_button = page.get_by_role("button", name="Register", exact=False)
                if not register_button.is_visible():
                    print("Register button not found, refreshing the page...")
                else: #Registration button is visible
                    registration_opened = True
                    break

                print(f"Waiting {REFRESH_FREQUENCY_SECONDS} seconds before refreshing...")
                page.wait_for_timeout(REFRESH_FREQUENCY_SECONDS * 1000)

                #  Refresh the page to get the latest state
                print("Refreshing Course Registration page...")
                page.goto("https://flexstudent.nu.edu.pk/CourseRegistration", wait_until="commit", timeout=0)
                


            if registration_opened:
                break
        except Exception as e:
            time.sleep(2)

    while(True):
        sound_alert()
        time.sleep(1)
