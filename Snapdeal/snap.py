import requests
from bs4 import BeautifulSoup

url = "https://www.snapdeal.com/products/lifestyle-sunglasses?sort=plrty"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# Find all product names
product_names = soup.find_all('p', class_='product-title')

# Extract and print the text for each product name with an index
for index, product in enumerate(product_names, start=1):
    print(f"{index}. {product.get_text(strip=True)}")