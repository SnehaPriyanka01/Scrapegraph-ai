import nest_asyncio
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

nest_asyncio.apply()

# Function to scrape product titles, ratings, prices, actual prices, discounts, links, and images from Flipkart
def scrape_flip():
    with sync_playwright() as p:
        # Launch Chromium in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to Flipkart's home furnishing page
        url = "https://www.flipkart.com/home-furnishing/pr?sid=jra&marketplace=FLIPKART&otracker=nmenu_sub_Home%20%26%20Furniture_0_Furnishing"
        page.goto(url)
        
        # Get the page content
        content = page.content()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all product titles
        titles = soup.find_all('a', {'class': 'wjcEIp'})  # Verify if this class is up-to-date
        
        # Find all product ratings
        ratings = soup.find_all('div', {'class': 'XQDdHH'})  # Verify this class name
        
        # Find all discounted prices
        prices = soup.find_all('div', {'class': 'Nx9bqj'})  # Verify this class name
        
        # Find all actual prices (original prices)
        actual_prices = soup.find_all('div', {'class': 'yRaY8j'})  # Verify this class name
        
        # Find all discounts
        discount_elements = soup.find_all('div', {'class': 'UkUFwK'})  # Verify this class name
        
        # Find all product images using the correct class for images
        images = soup.find_all('img', {'class': 'DByuf4'})  # Correct class for product images

        # Extract and combine the product titles, links, ratings, prices, actual prices, discounts, and images
        products = []
        for i in range(min(len(titles), len(ratings), len(prices), len(actual_prices), len(discount_elements), len(images))):
            product_title = titles[i].get_text()
            product_link = "https://www.flipkart.com" + titles[i]['href']  # Construct the full product link
            product_image = images[i]['src']  # Extract the image URL from the src attribute
            product_rating = ratings[i].get_text() if i < len(ratings) else "N/A"  # Handle potential missing ratings
            product_price = prices[i].get_text()
            actual_price = actual_prices[i].get_text()
            product_discount = discount_elements[i].get_text()  # Renamed to avoid the overwrite

            products.append({
                'Title': product_title, 
                'Link': product_link,  # Adding the product link
                'Image': product_image,  # Adding the product image URL
                'Rating': product_rating, 
                'Price': product_price,
                'Actual Price': actual_price,
                'Discount': product_discount,  # Using the renamed variable
            })
        
        browser.close()  # Close the browser after scraping
        return products

# Scrape and print the product information in the specified order
products = scrape_flip()
for i, product in enumerate(products, 1):
    print(f"{i}. Title: {product['Title']}")
    print(f"   Link: {product['Link']}")
    print(f"   Image: {product['Image']}")  # Displaying the product image link
    print(f"   Price: {product['Price']}")
    print(f"   Actual Price: {product['Actual Price']}")
    print(f"   Discount: {product['Discount']}")
    print(f"   Rating: {product['Rating']}")
