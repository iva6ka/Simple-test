import time
import random
import os
import logging
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Default values for arguments ===
DEFAULT_HEADLESS = False
DEFAULT_USE_PROXY = False
DEFAULT_PROXY_URL = "http://8.210.117.141:8888"

# === Command line arguments ===
parser = argparse.ArgumentParser(description="demoqa.com test")
parser.add_argument("--headless", action="store_true", default=DEFAULT_HEADLESS, help="Run browser in headless mode")
parser.add_argument("--proxy", action="store_true", default=DEFAULT_USE_PROXY, help="Use proxy with DEFAULT_PROXY_URL")
parser.add_argument("--proxy-url", type=str, help="Proxy server URL (e.g. http://ip:port or socks5://ip:port)")
args = parser.parse_args()

# === Logging configuration ===
log_filename = "demoqa_test.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Print to both terminal and log file
def log(msg):
    print(f"[LOG] {msg}")
    logging.info(msg)

# === Browser setup with options ===
options = Options()
if args.proxy and args.proxy_url:
    options.add_argument(f"--proxy-server={args.proxy_url}")
    log(f"Proxy set to: {args.proxy_url}")
elif args.proxy:
    options.add_argument(f"--proxy-server={DEFAULT_PROXY_URL}")
    log(f"Proxy set to default: {DEFAULT_PROXY_URL}")

log(f"Headless mode: {'ON' if args.headless else 'OFF'}")
log(f"Proxy enabled: {'ON' if args.proxy else 'OFF'}")

# === Start Chrome ===
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)  # Wait max 10 seconds for elements
actions = ActionChains(driver)

# === Delay to simulate human thinking ===
def human_pause(min_sec=1, max_sec=3, allow_skip=True):
    chance = random.random()
    if allow_skip and chance < 0.1:
        log("Skipping pause")
        return
    if chance > 0.9:
        pause_time = random.uniform(max_sec, max_sec + 3)
        log(f"Long pause: {pause_time:.2f}s")
    else:
        pause_time = random.uniform(min_sec, max_sec)
    time.sleep(pause_time)

# === Quick random delay ===
def random_behavior_pause():
    time.sleep(random.uniform(0.2, 1.2))

# === Simulate moving the mouse to the element ===
def move_mouse_to(elem):
    offset_x = random.randint(-5, 5)
    offset_y = random.randint(-5, 5)
    actions.move_to_element_with_offset(elem, offset_x, offset_y).perform()
    human_pause(0.3, 0.9)

# === Random click or press ENTER on the element ===
def click_or_enter_element(elem):
    move_mouse_to(elem)
    if random.choice([True, False]):
        actions.click().perform()
        log("Mouse click")
    else:
        elem.send_keys(Keys.ENTER)
        log("Click by ENTER key")
    human_pause()

# === Smooth scroll to center the target element ===
def scroll_to_element(elem):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elem)
    human_pause(1, 2)
    log("Scrolled to element")

# === Fill input field with text ===
def fill_field(by, field_id, text):
    field = wait.until(EC.visibility_of_element_located((by, field_id)))
    move_mouse_to(field)
    actions.click(field).perform()
    random_behavior_pause()
    field.send_keys(text)
    log(f"Filled field: {field_id}")

# === Fill all form fields in random order ===
def random_field_order():
    fields = [
        (By.ID, "userName", "Username"),
        (By.ID, "userEmail", "test@google.com"),
        (By.ID, "currentAddress", "Street 1"),
        (By.ID, "permanentAddress", "Street 2"),
    ]
    random.shuffle(fields)
    for by, field_id, value in fields:
        fill_field(by, field_id, value)
        human_pause(0.7, 1.7)

# === Main script logic ===
try:
    log("Opening site...")
    driver.get("https://demoqa.com/text-box")
    wait.until(EC.presence_of_element_located((By.ID, "userName")))
    human_pause()

    log("Filling fields in random order...")
    random_field_order()

    # Submit the form
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
    scroll_to_element(submit_btn)
    log("Clicking Submit button...")
    click_or_enter_element(submit_btn)

    # Wait for the output
    wait.until(lambda d: "name" in d.page_source)
    log("✅ Success: output detected!")

    # Save screenshot
    screenshot_name = "final_screen.png"
    screenshot_path = os.path.abspath(screenshot_name)
    driver.save_screenshot(screenshot_path)
    log(f"Screenshot saved at: {screenshot_path}")

# === Handle error and take error screenshot ===
except Exception as e:
    log(f"❗Error occurred: {e}")
    driver.save_screenshot("error_screen.png")
    log("🛑 Error screenshot saved: error_screen.png")

# === Cleanup and close browser ===
finally:
    driver.quit()
    log("Browser closed.")
    log(f"Logs saved at: {os.path.abspath(log_filename)}")
