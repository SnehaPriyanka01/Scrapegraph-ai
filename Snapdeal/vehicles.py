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

def scrape_snapdeal_data(max_pages=1):
    data_to_insert = []
    page = 1  # Start from the first page

    while page <= max_pages:
        # URL of the Snapdeal page you want to scrape
        url = f"https://www.snapdeal.com/products/car-vehicle-electronics?sort=plrty&page={page}"

        # Send a GET request to fetch the HTML content
        response = requests.get(url)
        html_content = response.content

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all product containers (div with class 'product-tuple-listing')
        product_divs = soup.find_all("div", class_="product-tuple-listing")

        # Loop through each product container and extract the required data
        for product in product_divs:
            # 1. Extract the product ID from 'id' attribute
            product_id = product.get('id')  # Use the actual product ID from the 'id' attribute

            # 2. Extract the product name from 'p' tag with class 'product-title'
            product_name = product.find('p', class_='product-title').text.strip() if product.find('p', class_='product-title') else "No name available"

            # 3. Extract the discounted price
            price = product.find('span', class_='product-price').text.strip() if product.find('span', class_='product-price') else "No price available"

            # 4. Extract the original price (strike-through price)
            original_price = product.find('span', class_='product-desc-price').text.strip() if product.find('span', class_='product-desc-price') else "No original price available"

            # 5. Extract the discount percentage
            discount = product.find('div', class_='product-discount').text.strip() if product.find('div', class_='product-discount') else "No discount available"

            # 6. Extract the ratings (if available, else return 'No rating available')
            ratings = product.find('p', class_='product-rating-count')
            ratings_text = f"{ratings.get_text(strip=True)} ratings" if ratings else "N/A"

            # 7. Extract the image URL from the 'img' tag
            image = product.find('img')
            image_url = image['src'] if image and 'src' in image.attrs else image['data-src'] if image and 'data-src' in image.attrs else 'N/A'

            # 8. Extract the product link from the 'a' tag
            product_link = product.find('a', class_='dp-widget-link')
            product_link_url = product_link['href'] if product_link else 'N/A'

            # 9. Extract product description (sometimes available in the title or a related tag)
            description = product_name  # If no detailed description, use product name as a fallback

            # Prepare data for insertion into ClickHouse (as a tuple)
            data_to_insert.append((
                product_id,
                product_name,
                price,
                original_price,
                discount,
                ratings_text,
                image_url,
                product_link_url,
                description
            ))

            # Print all the extracted information in the specified format
            print(f"Product ID: {product_id}")  # Format as specified
            print(f"Product Name: {product_name}")
            print(f"Price: {price}")
            print(f"Original Price: {original_price}")
            print(f"Discount: {discount}")
            print(f"Ratings: {ratings_text}")
            print(f"Image URL: {image_url}")
            print(f"Product Link: {product_link_url}")
            print(f"Description: {description}")
            print()  # Add a blank line for better readability

        page += 1  # Move to the next page

    return data_to_insert

# Scrape data from Snapdeal and collect data
data_to_insert = scrape_snapdeal_data(max_pages=2)  # Set the number of pages to scrape

# Insert data into ClickHouse, including the description
if data_to_insert:
    client.insert(CLICK_HOUSE_TABLE, data_to_insert, column_names=['id', 'name', 'price', 'original_price', 'discount', 'ratings', 'image', 'product_link', 'Description'])
    print("Data insertion completed.")
else:
    print("No data to insert.")
