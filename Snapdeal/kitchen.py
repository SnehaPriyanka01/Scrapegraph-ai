
# Snapdeal URL for kitchen product search results
url = "https://www.snapdeal.com/search?keyword=kitchen%20product&noOfResults=20&clickSrc=CatTrending&categoryId=0&searchCatRedirect=Home%20Audio%20Systems&searchState=&sort=rlvncy#bcrumbLabelId:46102431"

# Send a request to the Snapdeal page
r = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(r.content, "html.parser")

# Find all product containers
product_containers = soup.find_all('div', class_='product-tuple-description')

# Extract and print the product name, price, original price, discount percentage, rating count, image URL, and product link with numbering
for index, product in enumerate(product_containers, start=1):
    # Extract product name
    name = product.find('p', class_='product-title').get_text(strip=True)
    
    # Extract current price
    price = product.find('span', class_='lfloat product-price').get_text(strip=True)
    
    # Extract original price (from class 'lfloat product-desc-price strike')
    original_price = product.find('span', class_='lfloat product-desc-price strike')
    original_price = original_price.get_text(strip=True) if original_price else "N/A"
    
    # Extract discount percentage (if available)
    discount = product.find('div', class_='product-discount')
    discount = discount.get_text(strip=True) if discount else "N/A"
    
    # Extract rating count from p tag (class 'product-rating-count')
    rating_count = product.find('p', class_='product-rating-count')
    rating_count = rating_count.get_text(strip=True) if rating_count else "N/A"
    
    # Extract product image URL (checking both 'src' and 'data-src' attributes)
    image = product.find_previous_sibling('div').find('img', class_='product-image')
    image_url = image.get('src') if image and image.has_attr('src') else image.get('data-src', "N/A")
    
    # Extract product link
    link = product.find('a', class_='dp-widget-link')['href']
    product_link = f"{link}"
    
    # Print all the details
    print(f"{index}. {name} - Price: {price} - Original Price: {original_price} - Discount: {discount} - Rating Count: {rating_count} - Image URL: {image_url} - Product Link: {product_link}")
