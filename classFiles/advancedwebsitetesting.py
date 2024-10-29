import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver before running tests
@pytest.fixture
def setup():
    driver = webdriver.Chrome()  # Ensure ChromeDriver is accessible
    yield driver  # Provide the driver instance to the tests
    driver.quit()  # Quit the driver after the test

# Test Case 1: Test homepage loads successfully
def test_google_homepage(setup):
    driver = setup
    driver.get("https://ictd.gov.bd/")
    
    # Give time for the page to load
    time.sleep(2)
    
    # Assert that the page title contains
    assert "ict" in driver.title, "homepage did not load correctly"

# Test Case 2: Test that the search bar is present and functional
def test_google_search(setup):
    driver = setup
    driver.get("https://ictd.gov.bd/")
    
    # Find the search bar element
    search_bar = driver.find_element(By.NAME, "nahid")
    
    # Assert that the search bar is displayed
    assert search_bar.is_displayed(), "Search bar is not visible"
    
    # Perform a search and submit the query
    search_bar.send_keys("Python website testing with PyTest")
    search_bar.submit()
    
    # Wait for results to load
    time.sleep(3)
    
    # Take a screenshot for visual verification
    driver.save_screenshot('google_search_results.png')
    print("Screenshot taken.")
    
    # Check if search results are displayed
    results = driver.find_element(By.ID, "search")
    assert results.is_displayed(), "Search results not displayed"

# Test Case 3: Test for page interactions (e.g., clicking buttons)
def test_button_click(setup):
    driver = setup
    driver.get("https://ictd.gov.bd/")  # Replace with a website with a button to test
    
    # Wait for the page to load
    time.sleep(2)
    
    # Example: Find a button by ID (replace 'button-id' with the actual button ID)
    button = driver.find_element(By.ID, 'button-id')
    
    # Click the button
    button.click()
    
    # Add an assertion to verify the action after clicking the button
    assert "Expected Result" in driver.page_source, "Button click did not lead to expected result"
