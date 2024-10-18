import requests
from bs4 import BeautifulSoup

# The URL of the page to scrape
url = 'https://www.meesho.com/ethnicwear-women/pl/3tq'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all img tags
    images = soup.find_all('img')

    # Extract and print the src attribute (image links)
    for img in images:
        img_link = img.get('src')
        if img_link:
            print(img_link)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
