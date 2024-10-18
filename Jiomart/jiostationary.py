import uuid
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to scrape data from Jiomart using Selenium
def scrape_jiomart_data():
    # Set up Selenium WebDriver with options
    options = Options()
    # Uncomment the following line to run in headless mode
    # options.add_argument("--headless")

    # Use webdriver_manager to manage the ChromeDriver installation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # URL to scrape (Jiomart Electronics section)
    url = 'https://www.jiomart.com/c/groceries/school-office-stationery/29985?prod_mart_groceries_products_popularity%5Bpage%5D=84'
    driver.get(url)

    # Wait for the page to load
    time.sleep(10)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all product cards
    product_cards = soup.find_all('div', class_='plp-card-details-name line-clamp jm-body-xs jm-fc-primary-grey-80')

    # Extract product details
    for i, card in enumerate(product_cards, start=1):
        title = card.text.strip()  # Get the product title
        price_tag = card.find_next('span', class_='jm-heading-xxs jm-mb-xxs')
        price = price_tag.text.strip() if price_tag else "Current Price not available"

        original_price_tag = card.find_next('span', class_='jm-body-xxs jm-fc-primary-grey-60 line-through jm-mb-xxs')
        original_price = original_price_tag.text.strip() if original_price_tag else "Original Price not available"
        
        discount_tag = card.find_next('div', class_='plp-card-details-discount jm-mb-xxs')
        discount = discount_tag.text.strip() if discount_tag else "Discount not available"
        
        link_tag = card.find_parent('a', href=True)
        product_link = f"https://www.jiomart.com{link_tag['href']}" if link_tag else "No link available"
        
        image_wrapper = card.find_previous('div', class_='plp-card-image')
        img_tag = image_wrapper.find('img') if image_wrapper else None
        
        # Try different attributes for the image source
        image_src = None
        if img_tag:
            image_src = img_tag.get('src') or img_tag.get('data-src') or img_tag.get('srcset')
        
        # Fallback if no image source found
        image_src = image_src if image_src else "Image not available"

        # Generate a unique ID for the product
        unique_id = str(uuid.uuid4())

        # Set the description equal to the title as no separate description is available
        description = title

        # Print the product details in the requested format
        print(f"{i}. UUID: {unique_id}\n"
              f"Name: {title}\n"
              f"Price: {price}\n"
              f"Original Price: {original_price}\n"
              f"Discount: {discount}\n"
              f"Product Link: {product_link}\n"
              f"Image: {image_src}\n"
              f"Description: {description}\n")

    # Close the WebDriver
    driver.quit()

# Call the scraping function
scrape_jiomart_data()
