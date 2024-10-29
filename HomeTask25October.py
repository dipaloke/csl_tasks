from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import openpyxl
import pandas as pd

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Search term and target number of links
search_term = 'site:myshopify.com'
target_links = 100

# Open Bing and search for Shopify websites
driver.get('https://www.google.com')
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys(search_term)
search_box.send_keys(Keys.RETURN)
time.sleep(2)  # Pause to let the page load

# Set to store unique Shopify links
shopify_links = set()

# Function to extract Shopify links from search results
def extract_links():
    results = driver.find_elements(By.XPATH, '//a')
    for result in results:
        link = result.get_attribute('href')
        # Only add valid Shopify links, avoiding bing-related links
        if link and "myshopify.com" in link and "google.com" not in link:
            # Get the base URL up to .com
            base_link = link.split('.com')[0] + '.com' if '.com' in link else link
            shopify_links.add(base_link)

# Loop to paginate and collect links until the target is met or pages run out
while len(shopify_links) < target_links:
    extract_links()  # Extract links on the current page

    # Attempt to go to the next page of search results
    try:
        next_button = driver.find_element(By.XPATH, "//a[@id='pnnext']")
        next_button.click()
        time.sleep(2)  # Pause between pages to prevent being blocked
    except Exception as e:
        print("No more pages available or blocked by Bing.")
        break

# Close the browser after completion
driver.quit()

# Save the collected links to an Excel file
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Shopify Links"
sheet['A1'] = 'Shopify Websites'  # Add header

# Write links to Excel starting from the second row
for i, link in enumerate(shopify_links, start=2):
    sheet[f'A{i}'] = link

filename = "shopify_websites1.xlsx"
workbook.save(filename)

print(f"Initial collection saved to {filename}")

# Load the Excel file to remove duplicates
df = pd.read_excel(filename)
df.drop_duplicates(subset=['Shopify Websites'], inplace=True)  # Remove duplicates
df.to_excel(filename, index=False)  # Overwrite the file without duplicates

print(f"Removed duplicates. Final data saved to {filename}")
