import requests
from bs4 import BeautifulSoup
import clickhouse_connect

# ClickHouse connection details
CLICK_HOUSE_HOST = 'vizuaevya7.ap-south-1.aws.clickhouse.cloud'
CLICK_HOUSE_PORT = 8443
CLICK_HOUSE_USER = 'default'
CLICK_HOUSE_PASSWORD = '6gp~9sKvs1WKb'
CLICK_HOUSE_DATABASE = 'Dealwallet'  
CLICK_HOUSE_TABLE = 'mobiles'  

# Establishing a connection to ClickHouse
client = clickhouse_connect.get_client(
    host=CLICK_HOUSE_HOST,
    port=CLICK_HOUSE_PORT,
    username=CLICK_HOUSE_USER,
    password=CLICK_HOUSE_PASSWORD,
    database=CLICK_HOUSE_DATABASE,
)

# Function to scrape data from eBay
def scrape_ebay_data(search_query, max_pages=5):
    data_to_insert = []
    
    for page in range(1, max_pages + 1):
        url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw={search_query}&_sacat=0&_ipg=240&_pgn={page}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        
        # Find all titles, prices, ratings, links, image links, and discount prices
        names = soup.find_all('div', class_='s-item__title')
        prices = soup.find_all('span', class_='s-item__price')
        ratings = soup.find_all('div', class_='x-star-rating')
        links = soup.find_all('a', class_='s-item__link')
        discounts = soup.find_all('span', class_='s-item__discount s-item__discount')
        image_wrappers = soup.find_all('div', class_='s-item__image-wrapper image-treatment')

        # Extract image links
        image_links = [img.find('img')['src'] for img in image_wrappers if img.find('img')]

        # Ensure there's no mismatch in lengths
        items_count = min(len(names), len(prices), len(ratings), len(links), len(discounts), len(image_links))

        # Extract and prepare the data for ClickHouse
        for idx in range(items_count):
            name = names[idx].get_text(strip=True)
            price = prices[idx].get_text(strip=True)
            rating = ratings[idx].get_text(strip=True) if idx < len(ratings) else "No rating available"
            link = links[idx]['href'] if idx < len(links) else "No link available"
            discount = discounts[idx].get_text(strip=True) if idx < len(discounts) else "No discount available"
            image_link = image_links[idx] if idx < len(image_links) else "No image available"

            # Create a tuple for each item
            data_to_insert.append((name, price, rating, discount, image_link, link))

            # Print data to be inserted
            print(f"{len(data_to_insert)}. Name: {name}")
            print(f"   Price: {price}")
            print(f"   Rating: {rating}")
            print(f"   Discount: {discount}")  
            print(f"   Image Link: {image_link}")
            print(f"   Link: {link}")

    return data_to_insert

# Search for mobiles and collect data
search_query = "mobiles"
data_to_insert = scrape_ebay_data(search_query, max_pages=5)

# Insert data into ClickHouse
if data_to_insert:
    client.insert(CLICK_HOUSE_TABLE, data_to_insert, column_names=['name', 'price', 'rating', 'discount', 'image_link', 'link'])
    print("Data insertion completed.")
else:
    print("No data to insert.")
