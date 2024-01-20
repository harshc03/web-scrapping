from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:4200",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
options = webdriver.FirefoxOptions()
options.headless = True

def scrape_page(driver):
    product_data = []

    try:
        # Wait for the items to be present
        items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]'))
        )

        for item in items:
            try:
                # find name using text-based XPath
                print("moye moye-1")
                name = WebDriverWait(item, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.a-text-normal'))
                ).text
                print("moye moye-2 with name")

                # find ASIN number 
                data_asin = item.get_attribute("data-asin")
                print("moye moye-2 with data-asin")

                # find image url  
                image_url = item.find_element(By.CSS_SELECTOR, 'img.s-image').get_attribute('src')
                print("moye moye-2 with image url")
                # find price
                whole_price = item.find_elements(By.CSS_SELECTOR, 'span.a-price-whole')
                fraction_price = item.find_elements(By.CSS_SELECTOR, 'span.a-price-fraction')
                price = '.'.join([whole_price[0].text, fraction_price[0].text]) if whole_price and fraction_price else '0'
                print("moye moye-2 with price")

                # find ratings box
                 # Find ratings box
                ratings_box = item.find_element(By.CSS_SELECTOR, 'span.a-icon-alt')
                ratings = ratings_box.get_attribute('innerHTML') if ratings_box else '0'


                product_data.append({ 
                    "name": name,
                    "image_url" : image_url,
                    "data_asin": data_asin,
                    "price": price,
                    "rating": ratings,
                })
                print(product_data)
            except TimeoutException:
                print("Timed out waiting for an element to be present.")
            except Exception as e:
                print(f"An error occurred while processing an item: {str(e)}")

    except TimeoutException:
        print("Timed out waiting for items to be present.")

    return product_data

def scrape_amazon_data(keyword, max_pages):
    page_number = 1
    data = []

    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get('https://www.amazon.com')

        search = wait.until(EC.presence_of_element_located((By.ID, 'twotabsearchtextbox')))
        search.send_keys(keyword)

        search_button = wait.until(EC.element_to_be_clickable((By.ID, 'nav-search-submit-button')))
        search_button.click()

        while page_number <= max_pages:
            data.extend(scrape_page(driver))

            next_page_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@class="a-selected"]/following-sibling::li/a')))
            next_page = next_page_element.get_attribute("href") if next_page_element else None

            if next_page:
                driver.get(next_page)
                page_number += 1
            else:
                break
    except Exception as e:
        pass
    finally:
        driver.quit()

    return data

@app.get("/scrape-amazon/{keyword}/{max_pages}")
async def scrape_amazon(keyword: str, max_pages: int):
    data = scrape_amazon_data(keyword, max_pages)
    return JSONResponse(content={"message": "Scraping complete", "data": data}, status_code=200)
