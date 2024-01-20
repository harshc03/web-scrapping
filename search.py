from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fuzzywuzzy import fuzz
from nltk.stem import WordNetLemmatizer

app = FastAPI()

class SearchInput(BaseModel):
    search_string: str
    flipkart_products: list[str]
    amazon_products: list[str]

class SearchOutput(BaseModel):
    similar_flipkart_products: list[str]
    similar_amazon_products: list[str]

def lemmatize(text):
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

def find_similar_products(string, products, threshold=80):
    string_lemmatized = lemmatize(string)

    similar_products = []
    for product in products:
        product_lemmatized = lemmatize(product)
        similarity_ratio = fuzz.token_set_ratio(string_lemmatized, product_lemmatized)

        if similarity_ratio > threshold:
            similar_products.append(product)

    return similar_products

@app.post("/search")
async def search_products(input_data: SearchInput):
    try:
        print("Reached /search endpoint")
        similar_flipkart_products = find_similar_products(
            input_data.search_string, input_data.flipkart_products
        )
        similar_amazon_products = find_similar_products(
            input_data.search_string, input_data.amazon_products
        )

        return SearchOutput(
            similar_flipkart_products=similar_flipkart_products,
            similar_amazon_products=similar_amazon_products
        )
    except Exception as e:
        print(f"Error in /search endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
