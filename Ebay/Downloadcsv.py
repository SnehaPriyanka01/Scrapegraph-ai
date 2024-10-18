import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=mobiles&_sacat=0"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# Find all titles, prices, and ratings
names = soup.find_all('div', class_='s-item__title')
prices = soup.find_all('span', class_='s-item__price')
ratings = soup.find_all('div', class_='x-star-rating')

# Ensure there's no mismatch in lengths
items_count = min(len(names), len(prices), len(ratings))

# Create a CSV file to store the data
with open('ebay_mobiles.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Serial No', 'Name', 'Price', 'Rating'])

    # Extract and write the text for each title, price, and rating with serial numbers to the CSV file
    for idx in range(items_count):
        name = names[idx].get_text(strip=True)
        price = prices[idx].get_text(strip=True)
        rating = ratings[idx].get_text(strip=True) if idx < len(ratings) else "No rating available"
        
        # Write the row data to the CSV file
        writer.writerow([idx + 1, name, price, rating])

    print("Data has been successfully written to 'ebay_mobiles.csv'")
