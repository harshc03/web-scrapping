from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Assuming you have the geckodriver executable in your system PATH for Firefox
# Removed redundant import statements
driver = webdriver.Firefox()

driver.get("https://www.flipkart.com")
driver.maximize_window()

parent_window_handler = driver.window_handles[0]  # Store your parent window
sub_window_handler = None

handles = driver.window_handles  # get all window handles
for handle in handles:
    sub_window_handler = handle

driver.switch_to.window(sub_window_handler)

# Load environment variables using dotenv
# Note: Make sure to install the 'python-dotenv' package if not already installed (pip install python-dotenv)
from dotenv import load_dotenv
load_dotenv()

web = 'https://www.myntra.com'
driver_path = r'C:\Users\Harsh Chandiramani\Downloads\geckodriver-v0.34.0-win32\geckodriver.exe'

# Add the geckodriver path to the PATH environment variable
import os
os.environ["PATH"] += os.pathsep + os.path.dirname(driver_path)

options = webdriver.FirefoxOptions()
options.headless = True  # equivalent to '--headless' for Firefox

keyword = 'milk'
next_page = ''

def scrape_myntra(keyword, max_pages):
    page_number = 1

    # Use the existing driver, no need to create a new one here
    # driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)  # Use WebDriverWait for explicit waits

    try:
        print("aaya myntra-1")
        # The following line is redundant, as the driver is already on the desired page
        # driver.get(web)

        # Wait for the search box to be present
        search = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_3704LK')))
        search.send_keys(keyword)

        # Wait for the search button to be clickable
        search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'L0Z3Pu')))
        search_button.click()

        while page_number <= max_pages:
            scrape_page(driver)
            print("aaya amazon-2")

            # Wait for the next page link to be clickable
            next_page_element = wait.until(EC.element_to_be_clickable((By.XPATH,'//a[contains(@class,"ge-49M _2Kfbh8")]')))
            next_page = next_page_element.get_attribute("href") if next_page_element else None

            if next_page:
                driver.get(next_page)
                page_number += 1
            else:
                break
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

def scrape_page(driver):
    # Rest of your code for scraping a page
    pass

# Run the scraper
scrape_myntra(keyword, 2)
