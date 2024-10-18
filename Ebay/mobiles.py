import requests
from bs4 import BeautifulSoup

# eBay search URL for mobiles
url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=mobiles&_sacat=0"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# Find all titles, prices, ratings, and descriptions
names = soup.find_all('div', class_='s-item__title')
prices = soup.find_all('span', class_='s-item__price')
ratings = soup.find_all('div', class_='x-star-rating')

# Ensure there's no mismatch in lengths
items_count = min(len(names), len(prices), len(ratings), len(descriptions))

# Extract and print the text for each title, price, rating, and description with serial numbers
for idx in range(items_count):
    name = names[idx].get_text(strip=True)
    price = prices[idx].get_text(strip=True)
    rating = ratings[idx].get_text(strip=True) if idx < len(ratings) else "No rating available"
    description = descriptions[idx].get_text(strip=True) if idx < len(descriptions) else "No description available"

    print(f"{idx + 1}. Name: {name}")
    print(f"   Price: {price}")
    print(f"   Rating: {rating}")
    print(f"   Description: {description}")
