from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

from google import genai

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q" : q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/generate-text/")
def generate_text():
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Write a poem about FastAPI in Python."
    )
    return {response.text}








# import os
# from typing import Union
# from fastapi import FastAPI
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()  # loads .env file

# app = FastAPI()


# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


# @app.get("/")
# def read_root():
#     return {"message": "FastAPI is running successfully 🚀"}


# @app.get("/generate-text")
# def generate_text():
#     api_key = os.getenv("GEMINI_API_KEY")

#     if not api_key:
#         return {"error": "GEMINI_API_KEY not found in environment"}

#     client = genai.Client(api_key=api_key)

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents="Write a poem about FastAPI in Python."
#     )

#     return {
#         "generated_text": response.text
#     }



