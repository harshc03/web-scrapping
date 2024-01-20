from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

app = FastAPI()

options = webdriver.FirefoxOptions()
options.headless = True

def scrape_flipkart_page(driver):
    product_data = []

    try:
        # Wait for the items to be present
        items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "_1AtVbE col-12-12")]'))
        )

        for item in items:
            try:
                # find name using text-based XPath
                name = WebDriverWait(item, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[title].s1Q9rs'))
                ).get_attribute('title')

                # find price
                whole_price = item.find_element(By.CSS_SELECTOR, 'div._30jeq3')
                price = whole_price.text

                # find ratings box
                ratings_box = item.find_element(By.CSS_SELECTOR, 'div._3LWZlK')
                ratings = ratings_box.text

                product_data.append({
                    "name": name,
                    "price": price,
                    "rating": ratings,
                })
            except TimeoutException:
                print("Timed out waiting for an element to be present.")
            except Exception as e:
                print(f"An error occurred while processing an item: {str(e)}")

    except TimeoutException:
        print("Timed out waiting for items to be present.")

    return product_data

def scrape_flipkart_data(keyword, max_pages):
    page_number = 1
    data = []

    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get('https://www.flipkart.com')

        search = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Pke_EE')))
        search.send_keys(keyword)

        search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_2iLD__')))
        search_button.click()

        while page_number <= max_pages:
            data.extend(scrape_flipkart_page(driver))

            next_page_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class,"ge-49M _2Kfbh8")]')))
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

@app.get("/scrape-flipkart/{keyword}/{max_pages}")
async def scrape_flipkart(keyword: str, max_pages: int):
    data = scrape_flipkart_data(keyword, max_pages)
    return JSONResponse(content={"message": "Scraping complete", "data": data}, status_code=200)
