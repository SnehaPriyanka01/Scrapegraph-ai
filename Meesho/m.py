import time
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL of the Meesho ethnic wear page
url = "https://www.meesho.com/ethnicwear-women/pl/3tq"
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time as needed

# Function to scrape product details
def scrape_products():
    product_cards = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"]')

    # Extract and print product details
    for index, card in enumerate(product_cards, start=1):
        product_url = card.get_attribute('href')
        full_title = card.text.strip()

        # Extract only the title from the full title
        title = full_title.split('₹')[0].strip()  # Get the text before the price
        description = title

        # Extract price and rating from the full title
        price_info = full_title.split('₹')
        price = price_info[1].split('Free Delivery')[0].strip() if len(price_info) > 1 else "N/A"
        rating_info = full_title.split('Free Delivery')[-1].strip()
        rating = rating_info.split('Reviews')[0].strip() if 'Reviews' in rating_info else "N/A"

        # Get image URL
        image_tag = card.find_element(By.TAG_NAME, 'img')
        image_url = image_tag.get_attribute('src') if image_tag else "N/A"

        # Generate a UUID
        product_uuid = str(uuid.uuid4())

        # Print product details in a structured format
        print(f"{index:3}. UUID: {product_uuid}")
        print(f"   Title: {title}")
        print(f"   Description: {description}")
        print(f"   Price: Rs.{price}")
        print(f"   Rating: {rating}")
        print(f"   Image URL: {image_url}")
        print(f"   Product URL: {product_url}\n")

# Call the scrape function
scrape_products()

# Close the driver
driver.quit()
