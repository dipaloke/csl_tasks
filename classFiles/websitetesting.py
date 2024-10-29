from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open a website
driver.get("https://ictd.gov.bd/")
time.sleep(2)  # Wait for the page to load

# Check if the title contains 'ICT'
assert "ict" in driver.title, "homepage title is incorrect."

# Find the search bar and perform a search
search_bar = driver.find_element(By.NAME, "ict")
search_bar.send_keys("Selenium Python testing")
search_bar.submit()

# Wait for search results to load
time.sleep(3)

# Take a screenshot
driver.save_screenshot('search_results.png')
print("Screenshot taken.")

# Find and click a specific result link
result_link = driver.find_element(By.CSS_SELECTOR, 'h3')
result_link.click()

# Optional: Handle a dropdown if applicable
dropdown = Select(driver.find_element(By.ID, 'dropdown-id'))
dropdown.select_by_visible_text('Option 1')

# Close the browser
driver.quit()

print("Test completed successfully!")
