import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ----------------------------
# Configuration
# ----------------------------
URL = "https://ikman.lk/en/ad/mercedes-benz-e200-avantgarde-dimo-2010-for-sale-colombo"
OUTPUT_DIR = "./images"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}
# ----------------------------

# 1. Prepare output folder
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 2. Set up Selenium in headless mode
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=ChromeService(), options=options)

try:
    # 3. Load the page
    driver.get(URL)
    time.sleep(3)  # wait for thumbnails & main image to load

    # 4. Find all thumbnail elements
    thumbnails = driver.find_elements(By.CSS_SELECTOR, ".thumbnail-list--WjLo0 img")

    def download_main_image(index: int):
        """Download the currently displayed main image."""
        time.sleep(0.5)  # allow the main image to update
        main_img_el = driver.find_element(By.CSS_SELECTOR, ".main-image-container--JbCG0 img")
        img_url = main_img_el.get_attribute("src")
        file_path = os.path.join(OUTPUT_DIR, f"image_{index+1}.jpg")

        resp = requests.get(img_url, headers=HEADERS)
        resp.raise_for_status()  # will raise if download failed

        with open(file_path, "wb") as f:
            f.write(resp.content)

        print(f"[{index+1}/{len(thumbnails)}] Downloaded: {img_url}")

    # 5. Download the first (default) main image
    download_main_image(0)

    # 6. Click each thumbnail in turn, then download the updated main image
    for i, thumb in enumerate(thumbnails[1:], start=1):
        thumb.click()
        download_main_image(i)

finally:
    driver.quit()
    print("All done — browser closed.")
