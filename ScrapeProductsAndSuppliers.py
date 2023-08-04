import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize webdriver 
driver = webdriver.Chrome()

# Search Google for top selling products/niches
driver.get("https://www.google.com/search?q=top+selling+products")

# Scrape results
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

# Extract product ideas
products = []
for result in soup.find_all('div', class_='g'):
    title = result.find('h3').text
    products.append(title)

print(products)

# Search for suppliers
driver.get("https://www.alibaba.com") 
search_input = driver.find_element(By.ID, 'search-key')
search_input.send_keys('iphone charger')
search_input.submit()

# Extract supplier data
suppliers = []

# Do something with the supplier data
