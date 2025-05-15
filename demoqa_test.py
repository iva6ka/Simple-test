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

# === Default arguments ===
DEFAULT_HEADLESS = False
DEFAULT_USE_PROXY = False
DEFAULT_PROXY_URL = "http://127.0.0.1:8080"

# === CLI Arguments ===
parser = argparse.ArgumentParser(description="demoqa.com test")
parser.add_argument("--headless", action="store_true", default=DEFAULT_HEADLESS, help="Run browser in headless mode")
parser.add_argument("--proxy", action="store_true", default=DEFAULT_USE_PROXY, help="Use proxy if enabled in code")
args = parser.parse_args()

# === Logging Setup ===
log_filename = "demoqa_test.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log(msg):
    print(f"[LOG] {msg}")
    logging.info(msg)

# === Chrome Options ===
options = Options()
if args.headless:
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
if args.proxy:
    options.add_argument(f"--proxy-server={DEFAULT_PROXY_URL}")

# Log startup config
log(f"Headless mode: {'ON' if args.headless else 'OFF'}")
log(f"Proxy enabled: {'ON' if args.proxy else 'OFF'}")


driver = webdriver.Chrome(options=options)
# Max timeout for the element visibility
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

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

def random_behavior_pause():
    time.sleep(random.uniform(0.2, 1.2))

def move_mouse_to(elem):
    offset_x = random.randint(-5, 5)
    offset_y = random.randint(-5, 5)
    actions.move_to_element_with_offset(elem, offset_x, offset_y).perform()
    human_pause(0.3, 0.9)

def click_or_enter_element(elem):
    move_mouse_to(elem)
    if random.choice([True, False]):
        actions.click().perform()
        log("Mouse click")
    else:
        elem.send_keys(Keys.ENTER)
        log("Click by ENTER key")
    human_pause()

def scroll_to_element(elem):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elem)
    human_pause(1, 2)
    log("Scrolled to element")

def fill_field(by, field_id, text):
    field = wait.until(EC.visibility_of_element_located((by, field_id)))
    move_mouse_to(field)
    actions.click(field).perform()
    random_behavior_pause()
    field.send_keys(text)
    log(f"Filled field: {field_id}")

# Fill the fields in random order
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

# Act
try:
    log("Opening site...")
    driver.get("https://demoqa.com/text-box")
    wait.until(EC.presence_of_element_located((By.ID, "userName")))
    human_pause()

    log("Filling fields in random order...")
    random_field_order()

    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
    scroll_to_element(submit_btn)
    log("Clicking Submit button...")
    click_or_enter_element(submit_btn)

    wait.until(lambda d: "name" in d.page_source)
    log("✅ Success: output detected!")

    screenshot_name = "final_screen.png"
    screenshot_path = os.path.abspath(screenshot_name)
    driver.save_screenshot(screenshot_path)
    log(f"Screenshot saved at: {screenshot_path}")

except Exception as e:
    log(f"❗Error occurred: {e}")
    driver.save_screenshot("error_screen.png")
    log("🛑 Error screenshot saved: error_screen.png")

finally:
    driver.quit()
    log("Browser closed.")
    log(f"Logs saved at: {os.path.abspath(log_filename)}")