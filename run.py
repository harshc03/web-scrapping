# from asyncio import wait
# import os
# from dotenv import load_dotenv
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from database import store_db

# load_dotenv()

# web = 'https://www.amazon.com'
# driver_path = r'C:\Users\Harsh Chandiramani\Downloads\geckodriver-v0.34.0-win32\geckodriver.exe'

# # Add the geckodriver path to the PATH environment variable
# os.environ["PATH"] += os.pathsep + os.path.dirname(driver_path)

# options = webdriver.FirefoxOptions()
# options.headless = True  # equivalent to '--headless' for Firefox

# keyword = 'laptop'
# next_page = ''

# def scrape_amazon(keyword, max_pages):
#     page_number = 1

#     driver = webdriver.Firefox(options=options)
#     wait = WebDriverWait(driver, 10)  # Use WebDriverWait for explicit waits

#     try:
#         driver.get(web)

#         # Wait for the search box to be present
#         search = wait.until(EC.presence_of_element_located((By.ID, 'twotabsearchtextbox')))
#         search.send_keys(keyword)

#         # Wait for the search button to be clickable
#         search_button = wait.until(EC.element_to_be_clickable((By.ID, 'nav-search-submit-button')))
#         search_button.click()

#         while page_number <= max_pages:
#             scrape_page(driver)
            
#             # Wait for the next page link to be clickable
#             next_page_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@class="a-selected"]/following-sibling::li/a')))
#             global next_page
#             next_page = next_page_element.get_attribute("href") if next_page_element else None

#             if next_page:
#                 driver.get(next_page)
#                 page_number += 1
#             else:
#                 break
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#     finally:
#         driver.quit()

# def scrape_page(driver):
#     product_asin = []
#     product_name = []
#     product_price = []
#     product_ratings = []
#     product_ratings_num = []
#     product_link = []

#     # Wait for the items to be present
#     items = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))

#     for item in items:
#         try:
#             # find name
#             name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
#             product_name.append(name.text)

#             # find ASIN number 
#             data_asin = item.get_attribute("data-asin")
#             product_asin.append(data_asin)
#             # if data_asin:
#             #     product_asin.append(data_asin)
#             # else:
#             #     product_asin.append("N/A")

#             # find price
#             whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
#             fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
            
#             if whole_price and fraction_price:
#                 price = '.'.join([whole_price[0].text, fraction_price[0].text])
#             else:
#                 price = '0'
#             product_price.append(price)

#             # find ratings box
#             ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

#             # find ratings and ratings_num
#             if ratings_box:
#                 ratings = ratings_box[0].get_attribute('aria-label')
#                 ratings_num = ratings_box[1].get_attribute('aria-label')
#             else:
#                 ratings, ratings_num = '0', '0'
            
#             product_ratings.append(str(ratings))
#             product_ratings_num.append(str(ratings_num))

#             # find link
#             link_element = item.find_element(By.XPATH, './/a[@class="a-link-normal a-text-normal"]')
#             link = link_element.get_attribute("href")
#             product_link.append(link)

#         except Exception as e:
#             print(f"An error occurred while processing an item: {str(e)}")

#     global next_page
#     next_page_element = driver.find_element(By.XPATH, '//div[@class="a-selected"]/following-sibling::div/a')
#     next_page = next_page_element.get_attribute("href") if next_page_element else None

#     store_db(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link)

# # Run the scraper
# scrape_amazon(keyword, 3)

from asyncio import wait
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# Assuming you have the geckodriver executable in your system PATH for Firefox
driver = webdriver.Firefox()

driver.get("https://www.flipkart.com")
driver.maximize_window()

parent_window_handler = driver.window_handles[0]  # Store your parent window
sub_window_handler = None

handles = driver.window_handles  # get all window handles
for handle in handles:
    sub_window_handler = handle

driver.switch_to.window(sub_window_handler)


load_dotenv()

web = 'https://www.flipkart.com'
driver_path = r'C:\Users\Harsh Chandiramani\Downloads\geckodriver-v0.34.0-win32\geckodriver.exe'

# Add the geckodriver path to the PATH environment variable
os.environ["PATH"] += os.pathsep + os.path.dirname(driver_path)

options = webdriver.FirefoxOptions()
options.headless = True  # equivalent to '--headless' for Firefox

keyword = 'headphones'
next_page = ''

def scrape_flipkart(keyword, max_pages):
    page_number = 1

    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 50)  # Use WebDriverWait for explicit waits

    try:
        # print("aaya flipkart-1")
        driver.get(web)
        driver.implicitly_wait(20) 
        # Wait for the search box to be present
        search = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Pke_EE')))
        search.send_keys(keyword)

        # Wait for the search button to be clickable
        search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_2iLD__')))
        search_button.click()
        while page_number <= max_pages:
            scrape_page(driver)
            # print("aaya amazon-2")
            
            # Wait for the next page link to be clickable
            
            next_page_element = wait.until(EC.element_to_be_clickable((By.XPATH,'//a[contains(@class,"ge-49M _2Kfbh8")]')))
            global next_page
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
    product_asin = []
    product_name = []
    product_price = []
    product_ratings = []
    # product_ratings_num = []
    product_link = []

    # Wait for the items to be present
    # print("fatagaya-3")
    items = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "_1AtVbE col-12-12")]')))
    print(items)        
 # usko item nahi mil raha hai sir!! USKA XPATH GALAT HAI
    for item in items:
        try:
            # find name using text-based XPath
            # print("aaya-4")
            # name = item.find_element((By.XPATH, '//span[contains(@class, "a-text-normal")]'))
            # name = item.find_element(By.CSS_SELECTOR, 'span.a-text-normal')
            name = item.find_element(By.CSS_SELECTOR, '[title].s1Q9rs')
            title = name.get_attribute('title')
            product_name.append(title)
            print(product_name)



            # product_name.append(name.text)
            # print(name.text)

            # find ASIN number 
            # data_asin = item.get_attribute("data-asin")
            # product_asin.append(data_asin)
            # print(product_asin)

            # # find price
            whole_price = item.find_element(By.CSS_SELECTOR, 'div._30jeq3')
            # fraction_price = item.find_elements(By.CSS_SELECTOR, 'span.a-price-fraction')
            
            # if whole_price and fraction_price:
            #     price = '.'.join([whole_price[0].text, fraction_price[0].text])
            # else:
            #     price = '0'
            product_price.append(whole_price.text)
            print(product_price)

            # # find ratings box
            ratings_box=item.find_element(By.CSS_SELECTOR, 'div._3LWZlK')
            print(ratings_box.text)
            product_ratings.append(ratings_box.text)

            # element = item.find_element(By.CSS_SELECTOR,'[aria-label]')

            # Get the value of the aria-label attribute
            # aria_label_value = element.get_attribute('aria-label')

            # Extract the desired value (assuming it's always a decimal number)
            # rating = aria_label_value.split()[0]
            # print(rating)
            # product_ratings.append(rating)
            # product_ratings.append(ratings_box.text.split()[0])
            # print(product_ratings)

            # Extract the numeric part (assuming it's always a decimal)
            # ratings = ratings.split()[0]
            # item.find_element(By.CSS_SELECTOR, 'span.a-icon-alt')
            # # print("hello-",ratings_box)

            # # # find ratings and ratings_num
            # if ratings_box:
            #     ratings = ratings_box[0].get_attribute('aria-label')
            #     ratings_num = ratings_box[1].get_attribute('aria-label')
            # else:
            #     ratings, ratings_num = '0', '0'
            
            # 
            # product_ratings.append(ratings)
            # product_ratings_num.append(str(ratings_num))
            # print(product_ratings)
            # Assuming you have a WebElement representing the HTML code
            

            # Extracting the text content from the WebElement

            # Converting the text to a float value
            # rating_value = float(rating_text)



            # # find link using text-based XPath
            # link_element = item.find_element(By.XPATH, '//a[contains(@class, "a-link-normal") and contains(@class, "a-text-normal")]')
            # link = link_element.get_attribute("href")
            # product_link.append(link)

        except Exception as e:
            print(f"An error occurred while processing an item: {str(e)}")

    # global next_page
    # next_page_element = driver.find_element(By.XPATH, '//span[contains(@class,"s-pagination-selected")]/following-sibling::a')
    # next_page = next_page_element.get_attribute("href") if next_page_element else None

    # store_db(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link)

# Run the scraper
scrape_flipkart(keyword, 2)
