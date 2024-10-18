import time
import uuid
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import clickhouse_connect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ClickHouse connection parameters
CLICK_HOUSE_HOST = os.getenv("CLICK_HOUSE_HOST")
CLICK_HOUSE_PORT = int(os.getenv("CLICK_HOUSE_PORT", 8443))  # Default to 8443
CLICK_HOUSE_USER = os.getenv("CLICK_HOUSE_USER")
CLICK_HOUSE_PASSWORD = os.getenv("CLICK_HOUSE_PASSWORD")
CLICK_HOUSE_DATABASE = os.getenv("CLICK_HOUSE_DATABASE")
CLICK_HOUSE_TABLE = os.getenv("CLICK_HOUSE_TABLE")

# Initialize the ClickHouse client
client = clickhouse_connect.get_client(
    host=CLICK_HOUSE_HOST,
    port=CLICK_HOUSE_PORT,
    username=CLICK_HOUSE_USER,
    password=CLICK_HOUSE_PASSWORD,
    database=CLICK_HOUSE_DATABASE,
)

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL of the Meesho ethnic wear page
url = "https://www.meesho.com/ethnicwear-women/pl/3tq"
driver.get(url)

# Wait for the page to load
time.sleep(10)  # Adjust the sleep time as needed

# Function to scrape product details
def scrape_products():
    data_to_insert = []  # List to hold the data for ClickHouse
    product_cards = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"]')

    # Extract product details
    for card in product_cards:
        product_url = card.get_attribute('href')
        full_title = card.text.strip()

        # Extract only the title from the full title
        title = full_title.split('₹')[0].strip()  # Get the text before the price
        description = title

        # Extract price and rating from the full title
        price_info = full_title.split('₹')
        price = price_info[1].split('Free Delivery')[0].strip() if len(price_info) > 1 else "N/A"
        rating_info = full_title.split('Free Delivery')[-1].strip()
        
        # Extracting only the numeric rating
        rating = ''.join(filter(str.isdigit, rating_info.split('.')[0]))  # Get only the first part of rating if it's numeric
        if rating:
            rating = rating_info.split()[0]  # Get the first part that is a rating, e.g. '3.9'
        else:
            rating = "N/A"

        # Get image URL
        image_tag = card.find_element(By.TAG_NAME, 'img')
        image_url = image_tag.get_attribute('src') if image_tag else "N/A"

        # Generate a UUID
        product_uuid = str(uuid.uuid4())

        # Collect product details in a tuple for insertion
        data_to_insert.append((
            product_uuid,
            title,
            f"Rs.{price}",  # Prepend Rs. to price
            f"Rs.{price}",  # Prepend Rs. to original price
            rating,  # Only the numeric rating value
            "N/A",  # Assuming discount is not available
            image_url,
            product_url,
            description
        ))

    # Print product details in a structured format before insertion
    for index, (product_id, title_text, price_text, original_price_text, ratings_text, discount_text, image_data, product_link_url, description) in enumerate(data_to_insert, start=1):
        print(f"{index:3}. UUID: {product_id}")
        print(f"   Title: {title_text}")
        print(f"   Price: {price_text}")
        print(f"   Original Price: {original_price_text}")
        print(f"   Discount: {discount_text}")
        print(f"   Ratings: {ratings_text}")
        print(f"   Image: {image_data}")
        print(f"   Product Link: {product_link_url}")
        print(f"   Description: {description}\n")

    # Insert data into ClickHouse
    if data_to_insert:
        client.insert(
            CLICK_HOUSE_TABLE,
            data_to_insert,
            column_names=['id', 'name', 'price', 'original_price', 'ratings', 'discount', 'image', 'product_link', 'Description']
        )
        print("Data insertion completed.")
    else:
        print("No data to insert.")

# Call the scrape function
scrape_products()

# Close the driver
driver.quit()
