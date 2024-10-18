import requests
from bs4 import BeautifulSoup
import clickhouse_connect
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# ClickHouse connection details from .env file
CLICK_HOUSE_HOST = os.getenv('CLICK_HOUSE_HOST')
CLICK_HOUSE_PORT = os.getenv('CLICK_HOUSE_PORT')
CLICK_HOUSE_USER = os.getenv('CLICK_HOUSE_USER')
CLICK_HOUSE_PASSWORD = os.getenv('CLICK_HOUSE_PASSWORD')
CLICK_HOUSE_DATABASE = os.getenv('CLICK_HOUSE_DATABASE')
CLICK_HOUSE_TABLE = os.getenv('CLICK_HOUSE_TABLE')

# Establishing a connection to ClickHouse
client = clickhouse_connect.get_client(
    host=CLICK_HOUSE_HOST,
    port=int(CLICK_HOUSE_PORT),
    username=CLICK_HOUSE_USER,
    password=CLICK_HOUSE_PASSWORD,
    database=CLICK_HOUSE_DATABASE,
)

# Function to scrape data from Snapdeal
def scrape_snapdeal_data(max_pages=5):
    data_to_insert = []
    item_id = 1  # Initialize item ID

    for page in range(1, max_pages + 1):
        url = f"https://www.snapdeal.com/products/electronics-home-audio-systems?sort=plrty&page={page}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        # Find all products using the 'product-tuple-listing' class
        products = soup.find_all('div', class_='product-tuple-listing')

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
            ratings_text = ratings.get_text(strip=True) if ratings else 'N/A'

            image = product.find('img')
            image_data = image['src'] if image and 'src' in image.attrs else image['data-src'] if image and 'data-src' in image.attrs else 'N/A'

            product_link = product.find('a', class_='dp-widget-link')
            product_link_url = product_link['href'] if product_link else 'N/A'

            # Create a tuple for each item (id, name, price, original_price, discount, ratings, image, product_link)
            data_to_insert.append((item_id, title_text, price_text, original_price_text, discount_text, ratings_text, image_data, product_link_url))
            
            # Print the extracted data
            print(f"{item_id}. Title: {title_text}")
            print(f"   Price: {price_text}")
            print(f"   Original Price: {original_price_text}")
            print(f"   Discount: {discount_text}")
            print(f"   Ratings: {ratings_text}")  # Updated to reflect 'ratings'
            print(f"   Image: {image_data}")  # Updated to reflect 'image'
            print(f"   Product Link: {product_link_url}")
            
            item_id += 1

    return data_to_insert

# Scrape data from Snapdeal and collect data
data_to_insert = scrape_snapdeal_data(max_pages=5)

# Insert data into ClickHouse
if data_to_insert:
    client.insert(CLICK_HOUSE_TABLE, data_to_insert, column_names=['id', 'name', 'price', 'original_price', 'discount', 'ratings', 'image', 'product_link'])
    print("Data insertion completed.")
else:
    print("No data to insert.")
