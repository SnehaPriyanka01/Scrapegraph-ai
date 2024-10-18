import requests
from bs4 import BeautifulSoup

url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=mobiles&_sacat=0"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# Find all titles
titles = soup.find_all('div', class_='s-item__title')

# Extract and print the text for each title
for title in titles:
    print(title.get_text(strip=True))
