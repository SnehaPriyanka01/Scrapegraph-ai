import os
import uuid
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import clickhouse_connect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables from .env file
load_dotenv()

# ClickHouse connection details from .env file
CLICK_HOUSE_HOST = os.getenv('CLICK_HOUSE_HOST')
CLICK_HOUSE_PORT = os.getenv('CLICK_HOUSE_PORT')
CLICK_HOUSE_USER = os.getenv('CLICK_HOUSE_USER')
CLICK_HOUSE_PASSWORD = os.getenv('CLICK_HOUSE_PASSWORD')
CLICK_HOUSE_DATABASE = os.getenv('CLICK_HOUSE_DATABASE')
CLICK_HOUSE_TABLE = 'Dealwallet.Product'  # Updated to use the correct table name

# Establishing a connection to ClickHouse
client = clickhouse_connect.get_client(
    host=CLICK_HOUSE_HOST,
    port=int(CLICK_HOUSE_PORT),
    username=CLICK_HOUSE_USER,
    password=CLICK_HOUSE_PASSWORD,
    database=CLICK_HOUSE_DATABASE,
)

# Function to scrape data from Snapdeal using Selenium
def scrape_snapdeal_data(max_pages=1):
    data_to_insert = []
    
    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--headless")  # Run headless for faster scraping
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    page = 1  # Start from the first page

    while page <= max_pages:
        url = f"https://www.snapdeal.com/products/kids-toys?sort=plrty&page={page}"
        driver.get(url)

        # Allow some time for the page to load
        driver.implicitly_wait(10)  # Adjust the wait time as needed

        # Get page content and parse it
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.find_all('div', class_='product-tuple-listing')

        # Break the loop if no products are found
        if not products:
            break

        # Extract and prepare the data for ClickHouse
        for product in products:
            title = product.find('p', class_='product-title')
            title_text = title.get_text(strip=True) if title else 'N/A'

            price = product.find('span', class_='lfloat product-price')
            price_text = price.get_text(strip=True) if price else 'N/A'

            original_price = product.find('span', class_='lfloat product-desc-price strike')
            original_price_text = original_price.get_text(strip=True) if original_price else 'N/A'

            discount = product.find('div', class_='product-discount')
            discount_text = discount.get_text(strip=True) if discount else 'N/A'

            ratings = product.find('p', class_='product-rating-count')
            if ratings:
                ratings_text = ratings.get_text(strip=True) + " ratings"
            else:
                ratings_text = 'N/A'

            image = product.find('img')
            image_data = image['src'] if image and 'src' in image.attrs else image['data-src'] if image and 'data-src' in image.attrs else 'N/A'

            product_link = product.find('a', class_='dp-widget-link')
            product_link_url = product_link['href'] if product_link else 'N/A'

            # Use title_text as description
            description = title_text

            # Generate a UUID for each product
            product_id = str(uuid.uuid4())

            # Create a tuple for each item (id, name, price, original_price, ratings, discount, image, product_link, description)
            data_to_insert.append((product_id, title_text, price_text, original_price_text, ratings_text, discount_text, image_data, product_link_url, description))

            # Print the extracted data
            print(f"ID: {product_id}")
            print(f"Title: {title_text}")
            print(f"   Price: {price_text}")
            print(f"   Original Price: {original_price_text}")
            print(f"   Discount: {discount_text}")
            print(f"   Ratings: {ratings_text}")
            print(f"   Image: {image_data}")
            print(f"   Product Link: {product_link_url}")
            print(f"   Description: {description}")

        page += 1  # Move to the next page

    driver.quit()  # Close the browser after scraping
    return data_to_insert

# Scrape data from Snapdeal and collect data
data_to_insert = scrape_snapdeal_data(max_pages=5)  # Set the number of pages to scrape

# Insert data into ClickHouse
if data_to_insert:
    client.insert(CLICK_HOUSE_TABLE, data_to_insert, column_names=['id', 'name', 'price', 'original_price', 'ratings', 'discount', 'image', 'product_link', 'Description'])
    print("Data insertion completed.")
else:
    print("No data to insert.")
