
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import openpyxl

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Search term and target number of links
search_term = 'site:myshopify.com'
target_links = 100

# Open Google and search for Shopify websites
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
        # Only add valid Shopify links, avoiding Google-related links
        if link and "myshopify.com" in link and "google.com" not in link:
            shopify_links.add(link)

# Loop to paginate and collect links until the target is met or pages run out
while len(shopify_links) < target_links:
    extract_links()  # Extract links on the current page

    # Attempt to go to the next page of search results
    try:
        next_button = driver.find_element(By.XPATH, "//a[@id='pnnext']")
        next_button.click()
        time.sleep(2)  # Pause between pages to prevent being blocked
    except Exception as e:
        print("No more pages available or blocked by Google.")
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

workbook.save("shopify_websites.xlsx")

print(f"Collected by Dipaloke Biswas {len(shopify_links)} Shopify links and saved to shopify_websites.xlsx")
