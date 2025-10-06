# main.py

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# --- Constants and Configuration ---
# It's a best practice to load sensitive data from environment variables
# for security reasons, rather than hardcoding them in the script.
ACCOUNT_EMAIL = os.getenv("LINKEDIN_EMAIL")
ACCOUNT_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# Check if environment variables are set
if not all([ACCOUNT_EMAIL, ACCOUNT_PASSWORD, PHONE_NUMBER]):
    print("Error: Please set the LINKEDIN_EMAIL, LINKEDIN_PASSWORD, and PHONE_NUMBER environment variables.")
    exit()

# URL for the job search query on LinkedIn
LINKEDIN_JOBS_URL = "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=python%20developer&location=London%2C%20England"

def abort_application(driver):
    """Closes the job application modal and discards the application."""
    try:
        # Click the 'X' button to close the modal
        close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
        close_button.click()
        time.sleep(1) # Allow time for the next dialog to appear

        # Click the 'Discard' button in the confirmation dialog
        discard_buttons = driver.find_elements(by=By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")
        if len(discard_buttons) > 1:
            discard_buttons[1].click()
            print("Application aborted.")
    except NoSuchElementException:
        print("Could not find close or discard buttons to abort the application.")


# --- Selenium WebDriver Setup ---
# Keep the browser open after the script finishes (optional, for debugging)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Use webdriver-manager to automatically handle the chromedriver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set a timeout for the entire driver session
# This is an implicit wait, but we will prefer explicit waits.
# driver.implicitly_wait(5)

# Use a try...finally block to ensure the browser is closed even if an error occurs
try:
    # --- 1. Navigate to LinkedIn and Sign In ---
    driver.get(LINKEDIN_JOBS_URL)
    wait = WebDriverWait(driver, 10) # Initialize WebDriverWait with a 10-second timeout

    # Reject cookies
    try:
        reject_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[action-type="DENY"]')))
        reject_button.click()
    except TimeoutException:
        print("Cookie rejection button not found. Continuing...")

    # Click Sign in Button
    try:
        sign_in_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
        sign_in_button.click()
    except TimeoutException:
        print("Sign in button not found. Maybe you are already logged in.")
        # Handle cases where user might already be logged in
        if "feed" not in driver.current_url:
            driver.get("https://www.linkedin.com/login")


    # Perform sign-in if we are on the login page
    if "login" in driver.current_url:
        try:
            email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
            email_field.send_keys(ACCOUNT_EMAIL)

            password_field = driver.find_element(by=By.ID, value="password")
            password_field.send_keys(ACCOUNT_PASSWORD)
            password_field.send_keys(Keys.ENTER)
        except TimeoutException:
            print("Login fields not found on the page.")
            raise  # Stop the script if login fails

    # Handle manual CAPTCHA solving
    input("Press Enter when you have solved the Captcha (if any) and the job page has loaded.")

    # --- 2. Find Job Listings and Apply ---
    # Wait for the job listings to be present on the page
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".job-card-container--clickable")))
        all_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container--clickable")
    except TimeoutException:
        print("Could not find job listings. Exiting.")
        all_listings = []

    print(f"Found {len(all_listings)} job listings.")

    for listing in all_listings:
        print("\n--- Opening new listing ---")
        try:
            listing.click()
            # Use an explicit wait for the apply button to appear after clicking a listing
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-s-apply button")))
        except (TimeoutException, NoSuchElementException):
            print("Could not click on listing or apply button did not appear. Skipping.")
            continue

        try:
            # Click the 'Easy Apply' button
            apply_button = driver.find_element(by=By.CSS_SELECTOR, value=".jobs-s-apply button")
            apply_button.click()

            # --- 3. Fill Out Application Modal ---
            # Wait for the phone number input to be visible
            phone_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[id*=phoneNumber]")))

            # **BUG FIX**: Use get_attribute('value') to check if an input is empty
            if phone_input.get_attribute("value") == "":
                print("Entering phone number.")
                phone_input.send_keys(PHONE_NUMBER)

            # Check if this is a multi-step application
            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "footer button")))
            if submit_button.get_attribute("data-control-name") == "continue_unify":
                print("Complex application with multiple steps, skipping.")
                abort_application(driver)
                continue
            else:
                # This is a single-step 'Submit' button
                print("Submitting job application...")
                # submit_button.click() # Uncomment this line to actually submit the application
                print("--- SIMULATED SUBMISSION ---") # For safety during testing

            # Wait for the submission to process and then close the confirmation modal
            time.sleep(2) # Give a moment for the 'Done' screen to appear
            
            # This part can sometimes fail if the submission confirmation modal is different.
            # It's better to find a more reliable way to close it or just continue.
            try:
                done_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
                done_button.click()
            except NoSuchElementException:
                print("Could not find the 'Done' button after submission. Moving to next listing.")

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Skipping job. Reason: Could not find an element during application. Error: {e}")
            abort_application(driver) # Try to close any open modals before continuing
            continue

finally:
    # --- 4. Quit the Browser ---
    print("\nScript finished. Closing browser in 10 seconds.")
    time.sleep(10)
    driver.quit()