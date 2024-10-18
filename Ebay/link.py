import requests
from bs4 import BeautifulSoup

url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=laptops&_sacat=0&_odkw=books&_osacat=0"
r = requests.get(url)

# Check if the request was successful
if r.status_code == 200:
    soup = BeautifulSoup(r.content, "html.parser")

    # Find all items
    items = soup.find_all('div', class_='s-item__info')

    # Print the source and prompt
    print("Source: https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=laptops&_sacat=0&_odkw=books&_osacat=0")
    print("Prompt: List of laptops available on eBay\n")

    # Extract and print the title and link for each item with serial number
    for idx, item in enumerate(items, start=1):
        title_tag = item.find('div', class_='s-item__title')
        link_tag = item.find('a', class_='s-item__link')

        # Get the title and link if available
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "No link found"

        print(f"{idx}. {title}")
        print(f"   Link: {link}\n")
else:
    print(f"Failed to retrieve data. Status code: {r.status_code}")
