import requests
from bs4 import BeautifulSoup
import clickhouse_connect
from dotenv import load_dotenv
import os
import uuid  # Import the uuid module

# Load environment variables from .env file
load_dotenv()

# ClickHouse connection details from .env file
CLICK_HOUSE_HOST = os.getenv('CLICK_HOUSE_HOST')
CLICK_HOUSE_PORT = os.getenv('CLICK_HOUSE_PORT')
CLICK_HOUSE_USER = os.getenv('CLICK_HOUSE_USER')
CLICK_HOUSE_PASSWORD = os.getenv('CLICK_HOUSE_PASSWORD')
CLICK_HOUSE_DATABASE = os.getenv('CLICK_HOUSE_DATABASE')
CLICK_HOUSE_TABLE = os.getenv('CLICK_HOUSE_TABLE')  # Load table name from environment variable

# Establishing a connection to ClickHouse
client = clickhouse_connect.get_client(
    host=CLICK_HOUSE_HOST,
    port=int(CLICK_HOUSE_PORT),
    username=CLICK_HOUSE_USER,
    password=CLICK_HOUSE_PASSWORD,
    database=CLICK_HOUSE_DATABASE,
)

# URL to scrape
url = 'https://www.jiomart.com/c/electronics/4'

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all product cards based on the specific class for titles
    product_cards = soup.find_all('div', class_='plp-card-details-name line-clamp jm-body-xs jm-fc-primary-grey-80')

    # Initialize a list to hold the data for insertion
    data_to_insert = []

    # Extract product details
    for index, card in enumerate(product_cards, start=1):
        title = card.text.strip()  # Get the text content for the title
        description = title  # Set the description equal to the title
        ratings = "NA"  # Set ratings to NA
        link_tag = card.find_parent('a', href=True)  # Navigate up to the parent anchor tag

        # Attempt to find the current price using span
        price_tag = card.find_next('span', class_='jm-heading-xxs jm-mb-xxs')  # Current price span class
        price = price_tag.text.strip() if price_tag else "Current Price not available"  # Get current price text if available
        
        # Attempt to find the original price using span
        original_price_tag = card.find_next('span', class_='jm-body-xxs jm-fc-primary-grey-60 line-through jm-mb-xxs')  # Original price span class
        original_price = original_price_tag.text.strip() if original_price_tag else "Original Price not available"  # Get original price text if available
        
        # Attempt to find the discount
        discount_tag = card.find_next('div', class_='plp-card-details-discount jm-mb-xxs')  # Discount class
        discount = discount_tag.text.strip() if discount_tag else "Discount not available"  # Get discount text if available
        
        # Attempt to find the product image source
        image_wrapper = card.find_previous('div', class_='plp-card-image')  # Navigate to the previous div with 'plp-card-image'
        if image_wrapper and image_wrapper.find('img'):
            image_src = image_wrapper.find('img')['src']  # Get the image src attribute directly from <img>
        else:
            image_src = "Image not available"  # Handle if image is not found

        # Generate a unique ID for the product
        unique_id = str(uuid.uuid4())

        # Append the product data to the list as a tuple
        data_to_insert.append((
            unique_id,
            title,
            price,
            original_price,
            ratings,
            discount,
            image_src,
            f"https://www.jiomart.com{link_tag['href']}" if link_tag else "No link available",
            description
        ))

    # Check if there's data to insert
    if data_to_insert:
        # Print the product details
        for index, (product_id, title_text, price_text, original_price_text, ratings_text, discount_text, image_data, product_link_url, description) in enumerate(data_to_insert, start=1):
            print(f"{index}. UUID: {product_id}")
            print(f"   Title: {title_text}")
            print(f"   Price: {price_text}")
            print(f"   Original Price: {original_price_text}")
            print(f"   Discount: {discount_text}")
            print(f"   Ratings: {ratings_text}")
            print(f"   Image: {image_data}")
            print(f"   Product Link: {product_link_url}")
            print(f"   Description: {description}")
            print()  # Blank line for readability

        # Insert data into ClickHouse
        client.insert(CLICK_HOUSE_TABLE, data_to_insert, column_names=['id', 'name', 'price', 'original_price', 'ratings', 'discount', 'image', 'product_link', 'Description'])
        print("Data insertion completed.")
    else:
        print("No data to insert.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
