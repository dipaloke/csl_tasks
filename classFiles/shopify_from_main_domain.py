from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import openpyxl
import pandas as pd

driver = webdriver.Chrome()

search_term = 'site:myshopify.com'
target_links = 1000

driver.get('https://myip.ms/view/ip_addresses/400762368/23.227.38.0_23.227.38.255')
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'q'))
)
search_box.send_keys(search_term)
search_box.send_keys(Keys.RETURN)

time.sleep(2)

shopify_links = set()

def extract_links():
    results = driver.find_elements(By.XPATH, '//a')
    for result in results:
        link = result.get_attribute('href')
        if link and "myshopify.com" in link and "google.com" not in link:
            shopify_links.add(link)

while len(shopify_links) < target_links:
    extract_links()
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='pnnext']"))
        )
        next_button.click()
        time.sleep(random.uniform(2, 5))  # Random delay
    except Exception as e:
        print(f"No more pages available or blocked by Google. Error: {e}")
        break

driver.quit()

# Save initial data to Excel
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Shopify Links"
sheet['A1'] = 'Shopify Websites'

for i, link in enumerate(shopify_links, start=2):
    sheet[f'A{i}'] = link

filename = "shopify_websites.xlsx"
workbook.save(filename)
print(f"Initial collection saved to {filename}")

# Remove duplicates by reading and re-saving the file
df = pd.read_excel(filename)
df.drop_duplicates(subset=['Shopify Websites'], inplace=True)  # Remove duplicates
df.to_excel(filename, index=False)  # Overwrite the file without duplicates

print(f"Removed duplicates. Final data saved to {filename}")
