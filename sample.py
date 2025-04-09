from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib.request
import os

# Set up Chrome options for headless browsing
options = Options()
options.add_argument("--headless")

# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(), options=options)

# URL of the page to scrape
url = "https://riyasewana.com/buy/bajaj-pulsar-135-sale-negombo-9622007"
driver.get(url)

# Create an 'images' directory if it doesn't exist
if not os.path.exists('./images'):
    os.makedirs('./images')

# Extract the high-quality main image
main_image_url = driver.find_element(By.CSS_SELECTOR, "#sliderFrame #slider #main-image-url img").get_attribute("src")
print(f"Main Image URL: {main_image_url}")

# Download the main image
urllib.request.urlretrieve(main_image_url, './images/main_image.jpg')
print("Main Image downloaded successfully!")

# Extract all thumbnail image elements
thumb_elements = driver.find_elements(By.CSS_SELECTOR, "#sliderFrame #thumbs .thumb img")

# List to store the high-res image URLs for thumbnails
thumb_urls = []

# For each thumbnail, get the high-res image URL from the 'alt' attribute
for thumb in thumb_elements:
    high_res_url = thumb.get_attribute("alt")
    thumb_urls.append(high_res_url)
    print(f"Found Thumbnail URL: {high_res_url}")

# Download the thumbnail images
image_name_counter = 1
for thumb_url in thumb_urls:
    print(f"Downloading Thumbnail {image_name_counter}...")
    file_name = f"./images/thumbnail_{image_name_counter}.jpg"
    urllib.request.urlretrieve(thumb_url, file_name)
    print(f"Thumbnail {image_name_counter} downloaded successfully to {file_name}")
    image_name_counter += 1

# Close the browser
driver.quit()
