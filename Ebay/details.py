import requests
from bs4 import BeautifulSoup

# eBay search URL for mobiles
url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=mobiles&_sacat=0"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# Find all titles, prices, ratings, links, image links, and discount prices
names = soup.find_all('div', class_='s-item__title')
prices = soup.find_all('span', class_='s-item__price')
ratings = soup.find_all('div', class_='x-star-rating')
links = soup.find_all('a', class_='s-item__link')
discounts = soup.find_all('span', class_='s-item__discount s-item__discount')  # Use this class for discount price
image_wrappers = soup.find_all('div', class_='s-item__image-wrapper image-treatment')

image_links = [img.find('img')['src'] for img in image_wrappers if img.find('img')]

# Ensure there's no mismatch in lengths
items_count = min(len(names), len(prices), len(ratings), len(links), len(discounts), len(image_links))

# Extract and print the text for each title, price, rating, discount, image link, and link with serial numbers
for idx in range(items_count):
    name = names[idx].get_text(strip=True)
    price = prices[idx].get_text(strip=True)
    rating = ratings[idx].get_text(strip=True) if idx < len(ratings) else "No rating available"
    link = links[idx]['href'] if idx < len(links) else "No link available"
    discount = discounts[idx].get_text(strip=True) if idx < len(discounts) else "No discount available"
    image_link = image_links[idx] if idx < len(image_links) else "No image available"

    print(f"{idx + 1}. Name: {name}")
    print(f"   Price: {price}")
    print(f"   Rating: {rating}")
    print(f"   Discount: {discount}")  # Use the s-item__discount s-item__discount class for discount
    print(f"   Image Link: {image_link}")
    print(f"   Link: {link}")
