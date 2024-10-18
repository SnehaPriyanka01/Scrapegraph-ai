import time
import uuid
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import clickhouse_connect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ClickHouse connection parameters
CLICK_HOUSE_HOST = os.getenv("CLICK_HOUSE_HOST")
CLICK_HOUSE_PORT = int(os.getenv("CLICK_HOUSE_PORT"))  # Set your desired default port
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

# Function to scrape data from Jiomart using Selenium
def scrape_jiomart_data():
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # URL to scrape (Jiomart Electronics section)
    url = 'https://www.jiomart.com/c/electronics/4'
    driver.get(url)

    # Wait for the page to load
    time.sleep(25)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all product cards
    product_cards = soup.find_all('div', class_='plp-card-details-name line-clamp jm-body-xs jm-fc-primary-grey-80')

    # List to hold data for insertion
    data_to_insert = []

    # Extract product details
    for card in product_cards:
        title = card.text.strip()  # Get the product title
        price_tag = card.find_next('span', class_='jm-heading-xxs jm-mb-xxs')
        price = price_tag.text.strip() if price_tag else "Current Price not available"

        original_price_tag = card.find_next('span', class_='jm-body-xxs jm-fc-primary-grey-60 line-through jm-mb-xxs')
        original_price = original_price_tag.text.strip() if original_price_tag else "Original Price not available"
        
        discount_tag = card.find_next('div', class_='plp-card-details-discount jm-mb-xxs')
        discount = discount_tag.text.strip() if discount_tag else "Discount not available"
        
        link_tag = card.find_parent('a', href=True)
        product_link = f"https://www.jiomart.com{link_tag['href']}" if link_tag else "No link available"
        
        image_wrapper = card.find_previous('div', class_='plp-card-image')
        image_src = image_wrapper.find('img')['src'] if image_wrapper and image_wrapper.find('img') else "Image not available"

        # Generate a unique ID for the product
        unique_id = str(uuid.uuid4())

        # Prepare data for insertion as a tuple
        data_to_insert.append((
            unique_id,
            title,
            price,
            original_price,
            "Ratings not available",  # Placeholder if ratings are not found
            discount,
            image_src,
            product_link,
            title  # Description as title
        ))

        # Print the product details in the requested format
        print(f"{len(data_to_insert)}. UUID: {unique_id}")
        print(f"   Title: {title}")
        print(f"   Price: {price}")
        print(f"   Original Price: {original_price}")
        print(f"   Discount: {discount}")
        print(f"   Ratings: Ratings not available")  # Assuming you don't scrape ratings yet
        print(f"   Image: {image_src}")
        print(f"   Product Link: {product_link}")
        print(f"   Description: {title}\n")

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

    # Close the driver
    driver.quit()

# Call the scraping function
scrape_jiomart_data()
