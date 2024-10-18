import nest_asyncio
from playwright.sync_api import sync_playwright

# Allow nested event loops
nest_asyncio.apply()

# Define the URL for scraping
url = 'https://www.flipkart.com/home-furnishing/pr?sid=jra&marketplace=FLIPKART&otracker=nmenu_sub_Home%20%26%20Furniture_0_Furnishing'

# Use Playwright to open the browser and scrape the product links
with sync_playwright() as p:
    # Launch the browser
    browser = p.chromium.launch(headless=True)  # Set headless=True to run without opening a window
    page = browser.new_page()
    
    # Navigate to the URL
    page.goto(url)

    # Wait for the product elements to load
    page.wait_for_selector('a[href*="/p/"]')

    # Get all product links
    product_links = page.eval_on_selector_all('a[href*="/p/"]', 'elements => elements.map(el => el.href)')

    # Print the product links
    for product_link in product_links:
        print(product_link)

    # Close the browser
    browser.close()
