import requests
from bs4 import BeautifulSoup

url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=laptops&_sacat=0&_odkw=books&_osacat=0"
r = requests.get(url)

# Check if the request was successful
if r.status_code == 200:
    soup = BeautifulSoup(r.content, "html.parser")

    # Find all titles
    titles = soup.find_all('div', class_='s-item__title')

    # Extract and print the text for each title with serial number
    for idx, title in enumerate(titles, start=1):
        print(f"{idx}. {title.get_text(strip=True)}")
else:
    print(f"Failed to retrieve data. Status code: {r.status_code}")
