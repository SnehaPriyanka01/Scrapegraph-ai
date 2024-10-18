from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = 'https://www.meesho.com/ethnicwear-women/pl/3tq'
driver.get(url)

# Wait for the page to load completely
time.sleep(5)  # Adjust as necessary for loading time

# Find all image elements with the specified class
images = driver.find_elements(By.CSS_SELECTOR, 'img.NewProductCardstyled__ProductImage-sc-6y2tys-19.czNIkn')

for img in images:
    # Get the source URL
    img_url = img.get_attribute('src')
    print(img_url)

# Close the browser
driver.quit()
